#!/usr/bin/env python3
"""Run original Cedar examples through the real Cedar CLI (tested with 4.15.0)."""
import argparse
import json
import subprocess
import tempfile
from collections import defaultdict
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cedar", default="cedar", help="path to the Cedar CLI executable")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1] / "assets" / "examples"
    entities = json.loads((root / "entities.json").read_text())
    cases = json.loads((root / "cases.json").read_text())
    groups = defaultdict(list)
    for case in cases:
        policy = case.get("policies", "policies.cedar")
        use_schema = not case["errors"]
        test = {
            "name": case["name"],
            "request": {
                "principal": f'Workshop::User::"{case["principal"]}"',
                "action": f'Workshop::Action::"{case["action"]}"',
                "resource": f'Workshop::Document::"{case["resource"]}"',
                "context": case["context"],
            },
            "entities": entities,
            "decision": case["expected"].lower(),
            "reason": case["reasons"],
            "num_errors": 1 if case["errors"] else 0,
        }
        groups[(policy, use_schema)].append(test)
    def invoke(arguments):
        result = subprocess.run([args.cedar] + arguments, text=True, capture_output=True, timeout=30)
        if result.stdout:
            print(result.stdout.strip())
        if result.stderr:
            print(result.stderr.strip())
        if result.returncode:
            raise RuntimeError(f"Cedar command failed with exit {result.returncode}: {arguments[0]}")
    invoke(["--version"])
    invoke(["validate", "--policies", str(root / "policies.cedar"),
            "--schema", str(root / "schema.cedarschema")])
    with tempfile.TemporaryDirectory(prefix="cedar-example-cases-") as work:
        for index, ((policy, use_schema), tests) in enumerate(groups.items()):
            file = Path(work) / f"cases-{index}.json"
            file.write_text(json.dumps(tests))
            command = ["run-tests", "--policies", str(root / policy), "--tests", str(file)]
            if use_schema:
                command += ["--schema", str(root / "schema.cedarschema")]
            invoke(command)
    print(f"PASS: {len(cases)} original cases evaluated by Cedar; no application effects executed")


if __name__ == "__main__":
    main()
