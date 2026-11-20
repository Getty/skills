#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Offline RUML JSON Schema preflight; deliberately NOT a conformance validator."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from pathlib import Path

FORMATS = {
    "RUML": "ruml.schema.json",
    "RUML-Result": "ruml-result.schema.json",
    "RUML-EXT": "ruml-ext.schema.json",
}
DEFAULT_LIMIT = 100 * 1024 * 1024


class InputError(ValueError):
    """The input cannot be processed under this tool's documented profile."""


def unique_object(pairs):
    obj = {}
    for key, value in pairs:
        if key in obj:
            raise InputError(f"duplicate object key {key!r}; local preflight rejects ambiguous JSON")
        obj[key] = value
    return obj


def finite_float(value):
    number = float(value)
    if not math.isfinite(number):
        raise InputError("number exceeds this tool's finite floating-point range")
    return number


def reject_constant(value):
    raise InputError(f"{value} is not an RFC 8259 JSON number")


def load_json(path, max_bytes=DEFAULT_LIMIT):
    """Read bounded UTF-8 JSON; allow an initial UTF-8 BOM per RFC 8259 parser policy."""
    with Path(path).open("rb") as stream:
        raw = stream.read(max_bytes + 1)
    if len(raw) > max_bytes:
        raise InputError(f"file exceeds local byte limit {max_bytes}")
    try:
        return json.loads(
            raw.decode("utf-8-sig"), object_pairs_hook=unique_object,
            parse_float=finite_float, parse_constant=reject_constant,
        )
    except (UnicodeError, json.JSONDecodeError, RecursionError) as exc:
        raise InputError(f"UTF-8/JSON parsing failed: {exc}") from exc


def walk(value):
    pending = [value]
    while pending:
        item = pending.pop()
        if isinstance(item, dict):
            yield item
            pending.extend(item.values())
        elif isinstance(item, list):
            pending.extend(item)


def pointer(path):
    return "".join("/" + str(p).replace("~", "~0").replace("/", "~1") for p in path) or "/"


def validate(path, schemas_dir, max_bytes, max_errors):
    try:
        from jsonschema import Draft202012Validator, FormatChecker
        from referencing import Registry
        from referencing.exceptions import NoSuchResource
    except ImportError as exc:
        raise InputError("install jsonschema[format] in the active environment") from exc
    document = load_json(path, max_bytes)
    if not isinstance(document, dict) or document.get("$format") not in FORMATS:
        raise InputError("expected RUML, RUML-Result, or RUML-EXT JSON object; containers need a separate processor")
    schema_path = Path(schemas_dir) / FORMATS[document["$format"]]
    schema = load_json(schema_path, max_bytes)
    if not isinstance(schema, dict) or schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        raise InputError("expected an explicit JSON Schema draft 2020-12 schema")
    for item in walk(schema):
        for key in ("$ref", "$dynamicRef"):
            if key in item and not str(item[key]).startswith("#"):
                raise InputError("this offline helper accepts self-contained schemas only")
    checker = FormatChecker()
    required_formats = {item["format"] for item in walk(schema) if isinstance(item.get("format"), str)}
    missing = required_formats - set(checker.checkers)
    if missing:
        raise InputError("missing format checkers: " + ", ".join(sorted(missing)) + "; install jsonschema[format]")
    Draft202012Validator.check_schema(schema)

    def no_network(uri):
        raise NoSuchResource(ref=uri)

    validator = Draft202012Validator(schema, format_checker=checker, registry=Registry(retrieve=no_network))
    errors = []
    truncated = False
    for error in validator.iter_errors(document):
        if len(errors) >= max_errors:
            truncated = True
            break
        errors.append({"path": pointer(error.absolute_path), "validator": error.validator, "message": error.message})
    return {
        "file": str(Path(path)), "format": document["$format"],
        "specVersion": document.get("$specVersion"), "schema": str(schema_path),
        "schema_file_sha256": hashlib.sha256(schema_path.read_bytes()).hexdigest(),
        "schema_id": schema.get("$id"), "schema_valid": not errors,
        "scope": "strict JSON preflight and JSON Schema only; NOT semantic, runtime, signature, or legal conformance",
        "errors": errors, "errors_truncated": truncated,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="+", type=Path)
    parser.add_argument("--schemas-dir", required=True, type=Path, help="local schemas directory from a pinned official release")
    parser.add_argument("--max-bytes", type=int, default=DEFAULT_LIMIT)
    parser.add_argument("--max-errors", type=int, default=30)
    args = parser.parse_args()
    if args.max_bytes < 1 or args.max_errors < 1:
        parser.error("limits must be positive")
    status = 0
    for path in args.files:
        try:
            report = validate(path, args.schemas_dir, args.max_bytes, args.max_errors)
            if not report["schema_valid"]:
                status = max(status, 1)
        except Exception as exc:
            report = {"file": str(path), "schema_valid": None, "error": f"{type(exc).__name__}: {exc}",
                      "scope": "preflight/tool failure; not a completed conformance judgment"}
            status = 2
        print(json.dumps(report, ensure_ascii=False, indent=2))
    return status


if __name__ == "__main__":
    sys.exit(main())
