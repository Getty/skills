#!/usr/bin/env python3
"""Check ROCm torch.distributed NCCL/RCCL all-reduce correctness under torchrun.

Example: torchrun --standalone --nproc-per-node=2 scripts/distributed_smoke.py
Use only allocated, matching GPUs. No speed claims. Process-group timeouts do
not guarantee recovery from a driver hang; enforce a job-level time limit too.
"""
from __future__ import annotations

import argparse
from datetime import timedelta
import json
import os
import sys


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--elements", type=int, default=4096)
    parser.add_argument("--iterations", type=int, default=3)
    parser.add_argument("--timeout", type=int, default=30)
    parser.add_argument("--one-device-per-process", action="store_true",
        help="Use visible index 0 when the scheduler already exposes one GPU to each process")
    args = parser.parse_args()
    if not 1 <= args.elements <= 1048576 or not 1 <= args.iterations <= 20 or not 1 <= args.timeout <= 60:
        parser.error("Require elements 1..1048576, iterations 1..20, timeout 1..60")
    required = ("LOCAL_RANK", "RANK", "WORLD_SIZE")
    if any(key not in os.environ for key in required):
        print(json.dumps({"status": "prerequisite_missing", "reason": "Launch with torchrun; rank environment is missing."}))
        return 2
    try:
        rank, local_rank, world = (int(os.environ[k]) for k in ("RANK", "LOCAL_RANK", "WORLD_SIZE"))
    except ValueError:
        print(json.dumps({"status": "invalid_rank_environment"}))
        return 2
    if not 2 <= world <= 1024 or not 0 <= rank < world or local_rank < 0:
        print(json.dumps({"status": "invalid_rank_environment", "reason": "Need 2..1024 ranks and valid rank indices."}))
        return 2
    try:
        import torch
        import torch.distributed as dist
    except ImportError:
        print(json.dumps({"status": "prerequisite_missing", "reason": "PyTorch is not installed."}))
        return 2
    if not getattr(torch.version, "hip", None) or not torch.cuda.is_available() or not dist.is_nccl_available():
        print(json.dumps({"status": "prerequisite_missing", "reason": "Need HIP PyTorch, visible GPU and the NCCL API backend using RCCL."}))
        return 2
    count = torch.cuda.device_count()
    if args.one_device_per_process and count != 1:
        print(json.dumps({"status": "invalid_device_mapping", "reason": "Expected exactly one visible device for this process."}))
        return 2
    index = 0 if args.one_device_per_process else local_rank
    if index >= count:
        print(json.dumps({"status": "invalid_device_mapping", "local_rank": local_rank, "visible_count": count}))
        return 2
    torch.cuda.set_device(index)
    try:
        dist.init_process_group(backend="nccl", timeout=timedelta(seconds=args.timeout))
        pattern = torch.arange(args.elements, device=f"cuda:{index}", dtype=torch.float32).remainder_(17)
        expected = world * pattern + world * (world + 1) // 2
        for _ in range(args.iterations):
            value = pattern + rank + 1
            dist.all_reduce(value, op=dist.ReduceOp.SUM)
            torch.cuda.synchronize(index)
            # These bounded integer-valued sums are exactly representable in FP32.
            torch.testing.assert_close(value, expected, rtol=0, atol=0)
        # Success includes clean communication teardown; do not emit a passed
        # record followed by failure if the backend raises during cleanup.
        dist.destroy_process_group()
        print(json.dumps({"schema_version": 1, "status": "passed", "rank": rank,
            "world_size": world, "visible_device_index": index,
            "device_name": torch.cuda.get_device_name(index), "hip_version": torch.version.hip,
            "elements": args.elements, "iterations": args.iterations,
            "scope": "all-reduce correctness at selected size; not bandwidth, all protocols or all model collectives"}), flush=True)
        return 0
    except Exception as error:
        print(json.dumps({"status": "failed", "rank": rank, "error_type": type(error).__name__,
                          "error": str(error)[:2000]}), file=sys.stderr, flush=True)
        # Let torchrun terminate sibling ranks; avoid another potentially blocking
        # collective or destroy call during a failed communication operation.
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
