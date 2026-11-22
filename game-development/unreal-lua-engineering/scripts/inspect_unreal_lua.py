#!/usr/bin/env python3
"""Read-only Unreal/Lua metadata inspection; never compiles or certifies compatibility."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

MAX_SOURCE_BYTES = 1024 * 1024
MAX_SOURCE_FILES = 2500
TARGET_IDENTITY_FIELDS = (
    "name", "type", "platform", "architecture", "configuration", "compiler",
    "compiler_version", "toolset_version", "windows_sdk_version", "crt",
)
MARKERS = {
    "raw_field_link_review": re.compile(r"UField\s*\*\s*\*"),
    "class_default_object_review": re.compile(r"\bClassDefaultObject\b"),
    "all_libraries_exposed_review": re.compile(r"\bluaL_openlibs\s*\("),
    "lua_internal_header_review": re.compile(r'#\s*include\s*[<"](?:lstate|lobject|lapi|lfunc|lstring)\.h'),
    "deprecated_toolchain_review": re.compile(r"\bVisualStudio2019\b"),
}


def read_json(path: Path) -> dict:
    if path.stat().st_size > MAX_SOURCE_BYTES:
        raise ValueError(f"JSON metadata exceeds {MAX_SOURCE_BYTES} bytes: {path}")
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict):
        raise ValueError(f"Expected a JSON object: {path}")
    return data


def inspect_plugin(selected: Path) -> dict:
    if selected.is_file():
        descriptor = selected
        root = selected.parent
    else:
        root = selected
        candidates = sorted(root.glob("*.uplugin"))
        if len(candidates) != 1:
            raise ValueError("Plugin directory must contain exactly one .uplugin; pass its file path if ambiguous")
        descriptor = candidates[0]
    if descriptor.suffix != ".uplugin":
        raise ValueError("Plugin metadata must be a .uplugin file")
    data = read_json(descriptor)
    headers, markers, build_files = [], [], []
    inspected = 0
    scan_truncated = False
    for path in sorted(root.rglob("*")):
        if path.is_symlink() or not path.is_file() or path.suffix not in (".h", ".cpp", ".cs"):
            continue
        # Do not traverse a directory symlink outside the explicitly selected plugin.
        if not path.resolve().is_relative_to(root.resolve()):
            continue
        if path.stat().st_size > MAX_SOURCE_BYTES:
            continue
        inspected += 1
        if inspected > MAX_SOURCE_FILES:
            scan_truncated = True
            break
        content = path.read_text(encoding="utf-8-sig", errors="replace")
        relative = str(path.relative_to(root))
        if path.name == "lua.h":
            macros = {}
            for name in ("LUA_VERSION_MAJOR", "LUA_VERSION_MINOR", "LUA_VERSION_RELEASE", "LUA_VERSION_NUM"):
                match = re.search(r"^\s*#\s*define\s+" + name + r"\s+([^\r\n]+)", content, re.M)
                if match:
                    macros[name] = match.group(1).strip()
            headers.append({"path": relative, "macros": macros,
                            "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
        if path.name.endswith(".Build.cs"):
            build_files.append(relative)
        for line_number, line in enumerate(content.splitlines(), 1):
            for label, pattern in MARKERS.items():
                if pattern.search(line) and len(markers) < 80:
                    markers.append({"kind": label, "path": relative, "line": line_number})
    return {"descriptor": str(descriptor),
            "metadata": {k: data.get(k) for k in ("FriendlyName", "VersionName", "EngineVersion", "SupportedTargetPlatforms", "Modules")},
            "lua_headers": headers, "build_files": build_files, "source_review_markers": markers,
            "source_scan_truncated": scan_truncated,
            "limits": "Markers can match comments and are review locations, not confirmed defects; at most 80 are shown."}


def inspect_evidence(path: Path) -> dict:
    record = read_json(path)
    errors, warnings = [], []
    if record.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    for section in ("engine", "target", "integration"):
        if not isinstance(record.get(section), dict):
            errors.append(f"{section} must be an object")
        elif any(value is None for value in record[section].values()):
            warnings.append(f"{section} contains unspecified values")
    target = record.get("target")
    if isinstance(target, dict):
        missing = [field for field in TARGET_IDENTITY_FIELDS if field not in target]
        if missing:
            warnings.append("target is missing identity fields: " + ", ".join(missing))
        for field in TARGET_IDENTITY_FIELDS:
            value = target.get(field)
            if value is not None and not isinstance(value, str):
                errors.append(f"target.{field} must be a string or null")
        if isinstance(target.get("type"), str) and target["type"] not in (
                "Game", "Client", "Server", "Editor", "Program"):
            errors.append("target.type must name Game, Client, Server, Editor or Program")
    gates = record.get("gates")
    if not isinstance(gates, list) or not gates:
        errors.append("gates must be a nonempty array")
        gates = []
    seen = set()
    outstanding = []
    for index, gate in enumerate(gates):
        if not isinstance(gate, dict):
            errors.append(f"gate {index} must be an object")
            continue
        identity = gate.get("id")
        if not isinstance(identity, str) or not identity or identity in seen:
            errors.append(f"gate {index} needs a unique nonempty string id")
        else:
            seen.add(identity)
        if not isinstance(gate.get("required"), bool):
            errors.append(f"gate {index} required must be boolean")
        status = gate.get("status")
        if status not in ("passed", "failed", "not_run", "not_applicable"):
            errors.append(f"gate {index} has invalid status")
        if status in ("passed", "failed"):
            evidence = gate.get("evidence")
            if not isinstance(evidence, dict) or not all(evidence.get(k) for k in ("action", "observed_at", "result", "location")):
                errors.append(f"gate {index} completed status requires evidence action, observed_at, result and location")
        if status == "not_applicable" and not gate.get("reason"):
            errors.append(f"gate {index} not_applicable requires reason")
        if gate.get("required") is True and status not in ("passed", "not_applicable"):
            outstanding.append(identity)
    return {"path": str(path), "errors": errors, "warnings": warnings,
            "outstanding_required_gates": outstanding,
            "limits": "This checks record structure only; referenced evidence is not read or authenticated."}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, help="Exact .uproject path")
    parser.add_argument("--engine", type=Path, help="Engine installation root, containing Engine/Build/Build.version")
    parser.add_argument("--plugin", type=Path, help="Plugin directory or exact .uplugin path")
    parser.add_argument("--evidence", type=Path, help="Optional build evidence JSON")
    args = parser.parse_args()
    if not any((args.project, args.engine, args.plugin, args.evidence)):
        parser.error("provide at least one explicit input path")
    output = {"scope": "read-only observations; build/runtime compatibility is not assessed", "errors": []}
    for kind, path in (("project", args.project), ("engine", args.engine), ("plugin", args.plugin), ("evidence", args.evidence)):
        if path is None:
            continue
        try:
            path = path.expanduser().resolve()
            if kind == "project":
                data = read_json(path)
                output[kind] = {"path": str(path), "EngineAssociation": data.get("EngineAssociation"),
                                "Modules": data.get("Modules"), "Plugins": data.get("Plugins")}
            elif kind == "engine":
                version = path / "Engine" / "Build" / "Build.version"
                output[kind] = {"path": str(version), "version": read_json(version)}
            elif kind == "plugin":
                output[kind] = inspect_plugin(path)
            else:
                output[kind] = inspect_evidence(path)
                output["errors"].extend(output[kind]["errors"])
        except (OSError, ValueError) as exc:
            output["errors"].append(f"{kind}: {exc}")
    print(json.dumps(output, indent=2))
    return 1 if output["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
