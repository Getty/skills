#!/usr/bin/env python3
"""Collect a small ROCm inventory; no installs, sudo, network, or raw log export.

Default collection reads metadata only. --probe-runtime invokes installed HIP
utilities with a timeout, which may initialize the GPU runtime. Missing tools
are evidence gaps, never a verdict that hardware is unsupported.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
from typing import Any


PACKAGES = (
    "torch", "torchvision", "torchaudio", "triton", "pytorch-triton-rocm",
    "jax", "jaxlib", "onnxruntime", "onnxruntime-migraphx", "vllm", "sglang",
    "rocm", "rocm-sdk",
)
ENV_NAMES = (
    "ROCR_VISIBLE_DEVICES", "HIP_VISIBLE_DEVICES", "CUDA_VISIBLE_DEVICES",
    "GPU_DEVICE_ORDINAL", "HSA_OVERRIDE_GFX_VERSION", "HSA_XNACK",
    "AMD_SERIALIZE_KERNEL", "AMD_SERIALIZE_COPY", "HIP_LAUNCH_BLOCKING",
    "CUDA_LAUNCH_BLOCKING", "AMD_LOG_LEVEL", "NCCL_DEBUG", "NCCL_ALGO",
    "NCCL_PROTO", "NCCL_P2P_DISABLE", "NCCL_IB_DISABLE", "ROCM_PATH",
    "HIP_PATH", "LD_LIBRARY_PATH", "PYTORCH_ROCM_ARCH",
)


def read_text(path: Path) -> str | None:
    try:
        return path.read_text(errors="replace").strip()
    except (OSError, UnicodeError):
        return None


def linux_os_release() -> dict[str, str]:
    result: dict[str, str] = {}
    content = read_text(Path("/etc/os-release"))
    if content:
        for line in content.splitlines():
            key, sep, value = line.partition("=")
            if sep and key in {"ID", "VERSION_ID", "PRETTY_NAME"}:
                result[key.lower()] = value.strip('"')
    return result


def device_node(path: Path) -> dict[str, Any]:
    return {"path": str(path), "exists": path.exists(),
            "readable": os.access(path, os.R_OK),
            "writable": os.access(path, os.W_OK)}


def drm_inventory() -> list[dict[str, Any]]:
    devices: dict[str, dict[str, Any]] = {}
    for node in sorted(Path("/sys/class/drm").glob("*")):
        if not re.fullmatch(r"(?:card\d+|renderD\d+)", node.name):
            continue
        device = node / "device"
        if read_text(device / "vendor") != "0x1002":
            continue
        try:
            key = device.resolve(strict=True).name
        except OSError:
            continue
        record = devices.setdefault(key, {"pci_address": key, "vendor": "0x1002",
            "device_id": read_text(device / "device"),
            "revision": read_text(device / "revision"), "drm_nodes": []})
        record["drm_nodes"].append(node.name)
        try:
            record["driver"] = (device / "driver").resolve(strict=True).name
        except OSError:
            record["driver"] = None
        for sysname, outname in (("mem_info_vram_total", "vram_bytes_reported"),
                                 ("mem_info_gtt_total", "gtt_bytes_reported")):
            value = read_text(device / sysname)
            if value and value.isdigit():
                record[outname] = int(value)
    return list(devices.values())


def probe(name: str, args: list[str], timeout: float) -> dict[str, Any]:
    executable = shutil.which(name)
    if not executable:
        return {"status": "not_found_on_PATH"}
    try:
        process = subprocess.run([executable, *args], capture_output=True,
            text=True, errors="replace", timeout=timeout, check=False)
    except subprocess.TimeoutExpired:
        return {"status": "timeout", "timeout_seconds": timeout}
    except OSError as error:
        return {"status": "launch_failed", "error_type": type(error).__name__}
    report: dict[str, Any] = {"status": "ok" if process.returncode == 0 else "failed",
                             "returncode": process.returncode}
    if name == "rocminfo":
        report["gfx_targets"] = sorted(set(re.findall(r"\bgfx[0-9a-f]+\b", process.stdout)) - {"gfx000"})
        report["note"] = "Targets indicate enumeration only; no kernel or support test."
    else:
        match = re.search(r"\b\d+\.\d+(?:\.\d+)?(?:[-+][0-9A-Za-z.]+)?", process.stdout)
        report["version_token"] = match.group(0) if match else None
    if process.returncode:
        report["next_step"] = "Run this utility locally and inspect stderr; raw logs are intentionally omitted."
    return report


def collect(probe_runtime: bool = False, timeout: float = 15) -> dict[str, Any]:
    system = platform.system()
    release = platform.release()
    report: dict[str, Any] = {
        "schema_version": 1,
        "collected_at_utc": datetime.now(timezone.utc).isoformat(),
        "support_assessment": "unverified; compare exact SKU, OS, driver and workload with official matrices",
        "platform": {"system": system, "release": release,
                     "machine": platform.machine(), "python": platform.python_version()},
        "environment_variables_set": [key for key in ENV_NAMES if key in os.environ],
        "tools_on_PATH": {name: shutil.which(name) is not None for name in
            ("hipcc", "hipconfig", "rocminfo", "amd-smi", "rocprofv3", "torchrun")},
        "python_distributions": {},
        "notes": ["No hostnames, usernames, process lists, network configuration, UUIDs, or raw logs collected.",
                  "Package metadata does not prove that the imported package or GPU backend works."],
    }
    if system == "Linux":
        report["platform"]["os_release"] = linux_os_release()
        report["platform"]["wsl_detected"] = "microsoft" in release.lower() or "WSL_INTEROP" in os.environ
        report["amdgpu_module_version"] = read_text(Path("/sys/module/amdgpu/version"))
        report["amd_drm_devices"] = drm_inventory()
        nodes = [Path("/dev/kfd"), Path("/dev/dxg"), *sorted(Path("/dev/dri").glob("renderD*"))]
        report["device_nodes"] = [device_node(node) for node in nodes]
    else:
        report["notes"].append("Linux sysfs/device-node collection is inapplicable; obtain native device and driver details separately.")
    for package in PACKAGES:
        try:
            report["python_distributions"][package] = importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:
            pass
    if probe_runtime:
        report["runtime_probes"] = {"hipconfig": probe("hipconfig", ["--version"], timeout),
                                    "rocminfo": probe("rocminfo", [], timeout)}
    else:
        report["runtime_probes"] = {"status": "not_requested"}
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--probe-runtime", action="store_true", help="Run installed hipconfig and rocminfo; may initialize runtime")
    parser.add_argument("--timeout", type=float, default=15, help="Seconds per runtime probe (0 < value <= 60)")
    args = parser.parse_args()
    if not 0 < args.timeout <= 60:
        parser.error("--timeout must be greater than zero and at most 60")
    print(json.dumps(collect(args.probe_runtime, args.timeout), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
