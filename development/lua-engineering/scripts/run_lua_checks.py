#!/usr/bin/env python3
"""Run only bundled trusted diagnostics using explicitly selected Lua executables."""
from __future__ import annotations
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lua", action="append", required=True, help="Executable path/name; repeat for a matrix")
    parser.add_argument("--timeout", type=float, default=15.0, help="Per-script seconds, maximum 60")
    args = parser.parse_args()
    if not 0 < args.timeout <= 60:
        parser.error("timeout must be greater than zero and at most 60 seconds")
    root = Path(__file__).resolve().parents[1]
    environment = {key: value for key, value in os.environ.items()
                   if not (key == "LUA_INIT" or key.startswith("LUA_INIT_"))}
    reports = []
    failed = False
    for selected in args.lua:
        resolved = shutil.which(selected)
        if resolved is None:
            reports.append({"executable": selected, "status": "missing"})
            failed = True
            continue
        runs = []
        for script in ("runtime_probe.lua", "semantic_checks.lua"):
            try:
                run = subprocess.run([resolved, str(root / "scripts" / script)], cwd=root,
                                     capture_output=True, text=True, encoding="utf-8", errors="replace",
                                     timeout=args.timeout, check=False, env=environment)
                runs.append({"script": script, "returncode": run.returncode,
                             "stdout": run.stdout, "stderr": run.stderr})
                failed = failed or run.returncode != 0
            except (OSError, subprocess.TimeoutExpired) as exc:
                runs.append({"script": script, "error": str(exc)})
                failed = True
        reports.append({"executable": resolved, "runs": runs})
    print(json.dumps({"scope": "bundled diagnostics only", "results": reports}, indent=2))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
