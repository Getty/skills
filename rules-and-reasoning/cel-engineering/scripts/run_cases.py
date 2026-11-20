#!/usr/bin/env python3
"""Run trusted bounded CEL fixtures through official cel-expr-python."""
import argparse
import importlib.metadata
import json
from pathlib import Path
import sys


def reject_constant(value):
    raise ValueError("nonstandard JSON constant: " + value)


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key: " + key)
        result[key] = value
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cases", type=Path)
    args = parser.parse_args()
    try:
        from cel_expr_python import cel
        version = importlib.metadata.version("cel-expr-python")
        if args.cases.stat().st_size > 1_048_576:
            raise ValueError("fixture exceeds 1 MiB")
        document = json.loads(args.cases.read_text(encoding="utf-8"),
                              parse_constant=reject_constant,
                              object_pairs_hook=unique_object)
        cases = document["cases"]
        if not isinstance(cases, list) or not 1 <= len(cases) <= 200:
            raise ValueError("expected 1 to 200 cases")
        types = {name.lower(): getattr(cel.Type, name)
                 for name in ["INT", "UINT", "DOUBLE", "BOOL", "STRING", "DYN"]}
        ids = set()
        for case in cases:
            if not isinstance(case["id"], str) or case["id"] in ids:
                raise ValueError("case IDs must be unique strings")
            ids.add(case["id"])
            if not isinstance(case["expression"], str) or len(case["expression"]) > 10000:
                raise ValueError("invalid/oversized expression")
            if not isinstance(case["bindings"], dict):
                raise ValueError("bindings must be an object")
            if not isinstance(case["declarations"], dict):
                raise ValueError("declarations must be an object")
            for typ in case["declarations"].values():
                if typ not in types:
                    raise ValueError("unsupported fixture declaration: " + str(typ))
            if case["expect"]["kind"] not in {"value", "runtime_error", "compile_error"}:
                raise ValueError("unsupported expected category")
    except (ImportError, OSError, UnicodeError, ValueError, KeyError, TypeError, RecursionError) as exc:
        print(json.dumps({"setup_error": str(exc)}))
        return 2

    results = []
    for case in cases:
        try:
            env = cel.NewEnv(variables={k: types[v] for k, v in case["declarations"].items()})
            program = env.compile(case["expression"])
        except Exception as exc:
            actual = {"kind": "compile_error", "detail": str(exc)}
        else:
            try:
                value = program.eval(data=case["bindings"])
                value_type = str(value.type())
                if value_type == "ERROR":
                    actual = {"kind": "runtime_error", "detail": str(value.value())}
                else:
                    actual = {"kind": "value", "type": value_type, "value": value.value()}
            except Exception as exc:
                actual = {"kind": "runtime_error", "detail": str(exc)}
        expected = case["expect"]
        passed = actual["kind"] == expected["kind"]
        if passed and expected["kind"] == "value":
            passed = (actual.get("type") == expected.get("type") and
                      type(actual.get("value")) is type(expected.get("value")) and
                      actual.get("value") == expected.get("value"))
        results.append({"id": case["id"], "passed": passed, "actual": actual})
    failed = sum(not result["passed"] for result in results)
    print(json.dumps({"runtime": "cel-expr-python", "version": version,
                      "total": len(results), "failed": failed, "results": results},
                     indent=2, default=str))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
