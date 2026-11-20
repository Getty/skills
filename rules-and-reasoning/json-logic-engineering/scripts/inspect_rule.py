#!/usr/bin/env python3
"""Static inspector for the skill's restricted JSON Logic authoring profile."""
import argparse
from collections import Counter
import json
import math
from pathlib import Path
import sys

ARITY = {
    "var": (0, 2), "missing": (1, None), "missing_some": (2, 2),
    "if": (3, None), "==": (2, 2), "===": (2, 2), "!=": (2, 2),
    "!==": (2, 2), "!": (1, 1), "!!": (1, 1), "and": (1, None),
    "or": (1, None), ">": (2, 2), ">=": (2, 2), "<": (2, 3),
    "<=": (2, 3), "min": (1, None), "max": (1, None),
    "+": (1, None), "-": (1, 2), "*": (1, None), "/": (2, 2),
    "%": (2, 2), "map": (2, 2), "filter": (2, 2), "reduce": (3, 3),
    "all": (2, 2), "none": (2, 2), "some": (2, 2), "merge": (1, None),
    "in": (2, 2), "cat": (1, None), "substr": (2, 3)
}
BLOCKED_SEGMENTS = {"__proto__", "prototype", "constructor"}

def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key: " + key)
        result[key] = value
    return result

def reject_constant(value):
    raise ValueError("non-JSON numeric constant: " + value)

def inspect(value, max_depth, max_nodes):
    ops, paths = Counter(), set()
    counts = {"nodes": 0, "max_depth": 0, "dynamic_paths": 0}
    stack = [(value, 0, "$")]
    while stack:
        node, depth, loc = stack.pop()
        counts["nodes"] += 1
        counts["max_depth"] = max(counts["max_depth"], depth)
        if counts["nodes"] > max_nodes:
            raise ValueError("node limit exceeded")
        if depth > max_depth:
            raise ValueError("depth limit exceeded")
        if isinstance(node, float) and not math.isfinite(node):
            raise ValueError(loc + ": non-finite number")
        if isinstance(node, list):
            stack.extend((item, depth + 1, loc + "[" + str(i) + "]")
                         for i, item in enumerate(node))
        elif isinstance(node, dict):
            if len(node) != 1:
                raise ValueError(loc + ": literal records are outside this profile")
            op, operands = next(iter(node.items()))
            if op not in ARITY:
                raise ValueError(loc + ": unsupported operator: " + op)
            args = operands if isinstance(operands, list) else [operands]
            low, high = ARITY[op]
            if len(args) < low or (high is not None and len(args) > high):
                raise ValueError(loc + ": unsuitable operand count for " + op)
            if op == "if" and len(args) % 2 == 0:
                raise ValueError(loc + ": this profile requires a final if fallback")
            ops[op] += 1
            if op == "var":
                path = args[0] if args else ""
                if path is None:
                    paths.add("")
                elif isinstance(path, str) or type(path) is int:
                    text = str(path)
                    if any(segment in BLOCKED_SEGMENTS for segment in text.split(".")):
                        raise ValueError(loc + ": prohibited static path segment")
                    paths.add(text)
                else:
                    counts["dynamic_paths"] += 1
            stack.extend((arg, depth + 1, loc + "." + op + "[" + str(i) + "]")
                         for i, arg in enumerate(args))
    return {"profile": "restricted-authoring-v1", "accepted": True, **counts,
            "operators": dict(sorted(ops.items())), "static_paths": sorted(paths),
            "limitations": ["not an evaluator", "paths are scope-relative",
                            "not a runtime cost or security proof"]}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("rule", type=Path)
    parser.add_argument("--max-bytes", type=int, default=1024 * 1024)
    parser.add_argument("--max-depth", type=int, default=64)
    parser.add_argument("--max-nodes", type=int, default=10000)
    args = parser.parse_args()
    if min(args.max_bytes, args.max_depth, args.max_nodes) < 1:
        parser.error("limits must be positive")
    try:
        with args.rule.open("rb") as stream:
            raw = stream.read(args.max_bytes + 1)
        if len(raw) > args.max_bytes:
            raise ValueError("byte limit exceeded")
        value = json.loads(raw.decode("utf-8"), object_pairs_hook=unique_object,
                           parse_constant=reject_constant)
        result = inspect(value, args.max_depth, args.max_nodes)
    except (OSError, ValueError, UnicodeError, RecursionError) as exc:
        print(json.dumps({"profile": "restricted-authoring-v1", "accepted": False,
                          "error": str(exc)}))
        return 2
    print(json.dumps(result, indent=2))
    return 0

if __name__ == "__main__":
    sys.exit(main())
