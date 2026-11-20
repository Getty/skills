#!/usr/bin/env python3
"""Classify saved Boolean OPA Data API responses; never evaluate policy."""
import argparse
import json
import sys
from pathlib import Path


def strict_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key: " + key)
        result[key] = value
    return result


def bad_constant(value):
    raise ValueError("nonstandard JSON constant: " + value)


def classify(document):
    if not isinstance(document, dict):
        return 2, "invalid_envelope"
    if "error" in document or "errors" in document or "code" in document:
        return 2, "error_envelope"
    if "result" not in document:
        return 2, "undefined"
    if type(document["result"]) is not bool:
        return 2, "non_boolean_result"
    return (0, "allow") if document["result"] else (1, "deny")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("response", type=Path)
    args = parser.parse_args()
    try:
        if args.response.stat().st_size > 1_048_576:
            raise ValueError("response exceeds 1 MiB")
        document = json.loads(args.response.read_text(encoding="utf-8"),
                              object_pairs_hook=strict_object,
                              parse_constant=bad_constant)
        status, reason = classify(document)
        result = {"status": reason, "permit": status == 0}
    except (OSError, UnicodeError, ValueError, RecursionError) as exc:
        status = 2
        result = {"status": "invalid_json", "permit": False, "detail": str(exc)}
    print(json.dumps(result, ensure_ascii=True))
    return status


if __name__ == "__main__":
    sys.exit(main())
