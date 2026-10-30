#!/usr/bin/env python3
"""Approximate single-GPU homogeneous full-attention MHA/GQA memory capacity."""
from __future__ import annotations

import argparse
import json
import math
from _common import positive_float, nonnegative_float, positive_int

GIB = 1024 ** 3


def estimate(*, gpu_gib: float, utilization: float, parameters_b: float,
             weight_bits: float, weight_overhead: float, runtime_gib: float,
             reserve_gib: float, layers: int, kv_heads: int, head_dim: int,
             kv_bits: float, context_tokens: int, block_size: int,
             kv_overhead: float = 1.0) -> dict:
    positive = dict(gpu_gib=gpu_gib, utilization=utilization,
                    parameters_b=parameters_b, weight_bits=weight_bits,
                    weight_overhead=weight_overhead, layers=layers,
                    kv_heads=kv_heads, head_dim=head_dim, kv_bits=kv_bits,
                    context_tokens=context_tokens, block_size=block_size,
                    kv_overhead=kv_overhead)
    if any(isinstance(v, bool) or not math.isfinite(v) or v <= 0 for v in positive.values()):
        raise ValueError("all capacity dimensions must be finite and positive")
    if any(isinstance(v, bool) or not math.isfinite(v) or v < 0 for v in (runtime_gib, reserve_gib)):
        raise ValueError("runtime/reserve must be finite and nonnegative")
    if utilization > 1 or weight_overhead < 1 or kv_overhead < 1:
        raise ValueError("utilization must be <= 1; overhead multipliers must be >= 1")
    if any(not isinstance(v, int) for v in (layers, kv_heads, head_dim, context_tokens, block_size)):
        raise ValueError("architecture dimensions and token counts must be integers")
    raw_weights = parameters_b * 1e9 * weight_bits / 8
    weights = raw_weights * weight_overhead
    budget = gpu_gib * GIB * utilization
    remaining = budget - weights - (runtime_gib + reserve_gib) * GIB
    kv_per_token = 2 * layers * kv_heads * head_dim * kv_bits / 8 * kv_overhead
    rounded = ((context_tokens + block_size - 1) // block_size) * block_size
    per_sequence = rounded * kv_per_token
    intermediate = (raw_weights, weights, budget, remaining, kv_per_token, per_sequence)
    if not all(math.isfinite(n) for n in intermediate):
        raise ValueError("inputs overflow the supported numerical range")
    return {
        "model": "single GPU; homogeneous full-attention MHA/GQA; no prefix sharing",
        "raw_weights_gib": raw_weights / GIB,
        "weights_with_assumed_overhead_gib": weights / GIB,
        "executor_budget_gib": budget / GIB,
        "runtime_gib": runtime_gib,
        "additional_reserve_inside_executor_budget_gib": reserve_gib,
        "remaining_kv_gib": remaining / GIB,
        "kv_bytes_per_token_with_assumed_overhead": kv_per_token,
        "context_tokens_rounded_to_blocks": rounded,
        "kv_gib_per_full_length_sequence": per_sequence / GIB,
        "estimated_full_length_sequence_capacity": max(0, math.floor(remaining / per_sequence)),
        "estimated_memory_fit_for_one_sequence": remaining >= per_sequence,
        "limitations": [
            "Not measured. No kernel, model, driver, or quantization compatibility check.",
            "Not valid for MLA, SSM, hybrid/sliding-window models, or naive TP/PP division.",
            "Context must include prompt AND allowed generated tokens.",
            "Overheads are explicit assumptions; actual load/capture/activation peaks may be larger.",
            "No tokens/s, latency, scheduler limit, or SLO guarantee; confirm actual startup KV budget.",
            "Spark/unified memory needs a separately justified system-wide usable-memory budget."
        ]
    }


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__)
    for name in ("gpu-gib", "parameters-b", "weight-bits", "kv-bits"):
        p.add_argument("--" + name, type=positive_float, required=True)
    p.add_argument("--utilization", type=positive_float, default=.85)
    p.add_argument("--weight-overhead", type=positive_float, default=1.15)
    p.add_argument("--kv-overhead", type=positive_float, default=1.0)
    p.add_argument("--runtime-gib", type=nonnegative_float, default=3.0)
    p.add_argument("--reserve-gib", type=nonnegative_float, default=1.0)
    for name in ("layers", "kv-heads", "head-dim", "context-tokens"):
        p.add_argument("--" + name, type=positive_int, required=True)
    p.add_argument("--block-size", type=positive_int, default=16)
    return p


def main() -> int:
    p = parser()
    try:
        result = estimate(**vars(p.parse_args()))
    except ValueError as exc:
        p.error(str(exc))
    print(json.dumps(result, indent=2, ensure_ascii=False, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
