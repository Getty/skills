#!/usr/bin/env python3
"""Offline package checks only: structure, local links, JSON, and Python syntax."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
from urllib.parse import unquote


def validate(root: Path) -> dict:
    root = root.resolve()
    errors: list[str] = []
    counts = {"markdown_files": 0, "local_links": 0, "json_files": 0, "python_files": 0}
    required = ("SKILL.md", "README.md", "VALIDATION.md", "sources.json", "references", "scripts", "configs", "templates", "tests")
    for name in required:
        if not (root / name).exists():
            errors.append("Missing: " + name)
    skill = root / "SKILL.md"
    if skill.exists():
        text = skill.read_text(encoding="utf-8")
        if not text.startswith("---\n") or "\n---\n" not in text[4:]:
            errors.append("SKILL.md lacks bounded YAML front matter")
        else:
            front = text[4:].split("\n---\n", 1)[0]
            name = re.search(r"^name:\s*([a-z0-9-]+)\s*$", front, re.M)
            if not name or name.group(1) != root.name:
                errors.append("Skill name must match folder name and use lowercase hyphens")
            if not re.search(r"^description:\s*\S", front, re.M):
                errors.append("Skill description is missing")
        if len(text.splitlines()) > 500:
            errors.append("Central SKILL.md exceeds progressive-disclosure budget of 500 lines")
    for path in root.rglob("*.md"):
        counts["markdown_files"] += 1
        content = path.read_text(encoding="utf-8")
        for match in re.finditer(r"(?<!!)\[[^\]\n]+\]\(([^)\n]+)\)", content):
            target = match.group(1).strip()
            if re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", target) or target.startswith("#"):
                continue
            local = unquote(target.split("#", 1)[0])
            if not local:
                continue
            counts["local_links"] += 1
            candidate = (path.parent / local).resolve()
            if not candidate.is_relative_to(root):
                errors.append(f"Link escapes package: {path.relative_to(root)} -> {target}")
            elif not candidate.exists():
                errors.append(f"Broken local link: {path.relative_to(root)} -> {target}")
    for path in root.rglob("*.json"):
        counts["json_files"] += 1
        try:
            def reject_nonfinite(value):
                raise ValueError("non-finite JSON number")
            json.loads(path.read_text(encoding="utf-8"), parse_constant=reject_nonfinite)
        except (OSError, ValueError) as exc:
            errors.append(f"Invalid JSON: {path.relative_to(root)} ({type(exc).__name__})")
    for path in root.rglob("*.py"):
        counts["python_files"] += 1
        try:
            compile(path.read_text(encoding="utf-8"), str(path), "exec")
        except (OSError, SyntaxError) as exc:
            errors.append(f"Invalid Python: {path.relative_to(root)} ({type(exc).__name__})")
    if (root / "sources.json").exists():
        try:
            entries = json.loads((root / "sources.json").read_text(encoding="utf-8"))["sources"]
            ids = [item["id"] for item in entries]
            if len(ids) != len(set(ids)):
                errors.append("Duplicate source IDs")
            if any(not item["url"].startswith("https://") for item in entries):
                errors.append("Source URL is not HTTPS")
        except (ValueError, KeyError, TypeError):
            errors.append("Source registry schema invalid")
    return {"ok": not errors, "counts": counts, "errors": errors,
            "not_checked": ["GPU/model runtime compatibility and speed", "external link availability",
                            "Prometheus/Collector/NGINX runtime syntax", "formal complete YAML schema", "quality and SLO compliance"]}


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    a = p.parse_args()
    result = validate(a.root)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
