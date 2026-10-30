#!/usr/bin/env python3
"""Read-only local hardware/package/CLI audit. Does not import torch or start vLLM."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from importlib import metadata
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
from _common import positive_float, private_text_file, write_json

PACKAGES = ("vllm", "torch", "transformers", "tokenizers", "triton", "flashinfer-python",
            "flash-attn", "lmcache", "openai", "opentelemetry-api", "opentelemetry-sdk")
MAX_CAPTURE_CHARS = 1_000_000


def run_readonly(argv: list[str], timeout: float) -> dict:
    if shutil.which(argv[0]) is None:
        return {"argv": argv, "status": "not_installed", "returncode": None, "output": ""}
    try:
        cp = subprocess.run(argv, capture_output=True, text=True, encoding="utf-8",
                            errors="replace", timeout=timeout, check=False)
        output = cp.stdout + "\n" + cp.stderr
        return {"argv": argv, "status": "ok" if cp.returncode == 0 else "command_failed",
                "returncode": cp.returncode, "output": output[:MAX_CAPTURE_CHARS],
                "output_truncated": len(output) > MAX_CAPTURE_CHARS}
    except subprocess.TimeoutExpired:
        return {"argv": argv, "status": "timeout", "returncode": None, "output": ""}
    except OSError as exc:
        return {"argv": argv, "status": type(exc).__name__, "returncode": None, "output": ""}


def package_versions() -> dict:
    result = {}
    for name in PACKAGES:
        try:
            result[name] = metadata.version(name)
        except metadata.PackageNotFoundError:
            result[name] = None
    return result


def small_system_file(path: str) -> str | None:
    try:
        return Path(path).read_text(encoding="utf-8")[:8192].strip()
    except (OSError, UnicodeError):
        return None


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out", type=Path, required=True, help="new audit directory, never overwritten")
    p.add_argument("--command-timeout", type=positive_float, default=30)
    p.add_argument("--skip-cli-help", action="store_true", help="collect versions but no vLLM help commands")
    a = p.parse_args()
    try:
        a.out.mkdir(parents=True, mode=0o700, exist_ok=False)
    except OSError:
        p.exit(1, "Audit directory exists or cannot be created; choose a fresh path.\n")
    meminfo = small_system_file("/proc/meminfo")
    mem = {}
    if meminfo:
        for line in meminfo.splitlines():
            key, _, value = line.partition(":")
            if key in {"MemTotal", "MemAvailable", "SwapTotal", "SwapFree"}:
                mem[key] = value.strip()
    report = {
        "utc": datetime.now(timezone.utc).isoformat(),
        "platform": {"system": platform.system(), "release": platform.release(),
                     "machine": platform.machine(), "python": sys.version.split()[0],
                     "cpu_count_visible": os.cpu_count()},
        "packages": package_versions(), "linux_memory": mem,
        "cgroup_v2_memory_max": small_system_file("/sys/fs/cgroup/memory.max"),
        "cgroup_v2_cpu_max": small_system_file("/sys/fs/cgroup/cpu.max"),
        "commands": [],
        "limitations": ["Read-only local commands; no GPU inference or performance benchmark.",
                        "No environment dump or GPU UUID/serial requested.",
                        "Containers/WSL may expose incomplete host topology/sensor information.",
                        "Review CLI logs/model paths before sharing."]
    }
    commands = [
        ["nvidia-smi", "--query-gpu=name,memory.total,driver_version,pstate,power.draw,power.limit,temperature.gpu,utilization.gpu", "--format=csv"],
        ["nvidia-smi", "topo", "-m"],
        ["vllm", "--version"]
    ]
    if not a.skip_cli_help:
        commands.extend([["vllm", "serve", "--help=all"], ["vllm", "bench", "serve", "--help"]])
    for i, argv in enumerate(commands, 1):
        entry = run_readonly(argv, a.command_timeout)
        if argv == ["vllm", "serve", "--help=all"] and entry["status"] == "command_failed":
            entry = run_readonly(["vllm", "serve", "--help"], a.command_timeout)
        filename = f"command-{i:02d}.txt"
        with private_text_file(a.out / filename) as f:
            f.write(entry.pop("output"))
        entry["output_file"] = filename
        report["commands"].append(entry)
    write_json(a.out / "environment.json", report)
    print(f"Audit written to {a.out}; unavailable commands are recorded, not treated as GPU test results.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
