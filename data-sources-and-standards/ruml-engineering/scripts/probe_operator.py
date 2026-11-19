#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Trace the six RUML 1.0 built-in operators over supplied direct-child statuses; not a runtime."""
from __future__ import annotations

import argparse
import json

OPERATORS = ("AND", "NOT_AND", "OR", "NOT_OR", "XOR", "NOT_XOR")
STATUSES = ("true", "false", "undefined")


def evaluate(operator, statuses, mode="optimized"):
    """Apply RUML 1.0.0 §3.6 only; no empty nodes, capabilities, recursion, or actions."""
    statuses = list(statuses)
    if operator not in OPERATORS or mode not in ("optimized", "complete"):
        raise ValueError("unsupported operator or mode")
    if not statuses or any(s not in STATUSES for s in statuses):
        raise ValueError("supply one or more true/false/undefined child statuses")
    base = operator.removeprefix("NOT_")
    child_results = list(statuses)
    result = None
    decisive = None
    if mode == "optimized" and base in ("AND", "XOR"):
        stop_status = "false" if base == "AND" else "true"
        for index, value in enumerate(statuses):
            if value in (stop_status, "undefined"):
                result, decisive = value, index
                child_results[index + 1:] = ["ignored"] * (len(statuses) - index - 1)
                break
    if result is None:
        priority = ("false", "undefined", "true") if base == "AND" else ("true", "undefined", "false")
        result = next(value for value in priority if value in statuses)
    if operator.startswith("NOT_") and result != "undefined":
        result = "false" if result == "true" else "true"
    return {"operator": operator, "mode": mode, "status": result,
            "children": child_results, "stop_child_index": decisive}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operator", choices=OPERATORS)
    parser.add_argument("statuses", nargs="+", choices=STATUSES)
    parser.add_argument("--mode", choices=("optimized", "complete", "both"), default="both")
    args = parser.parse_args()
    modes = ("optimized", "complete") if args.mode == "both" else (args.mode,)
    print(json.dumps({"specification": "RUML 1.0.0 §3.6",
                      "scope": "operator probe only; JSON output is NOT a .ruml-result document",
                      "traces": [evaluate(args.operator, args.statuses, mode) for mode in modes]}, indent=2))


if __name__ == "__main__":
    main()
