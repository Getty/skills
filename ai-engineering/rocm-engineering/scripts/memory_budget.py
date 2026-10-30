#!/usr/bin/env python3
"""Estimate dense/GQA decoder inference storage; never certify a model fits.

Decimal parameter billions, binary GiB. Weight and KV sharding are separate
explicit assumptions. No training, MLA, hybrid/state-space, or automatic TP model.
"""
from __future__ import annotations

import argparse
import json
import math

GIB = 1024 ** 3


def estimate(*, parameters_b: float, weight_bits: float, weight_overhead: float,
             layers: int, kv_heads: int, head_dim: int, tokens: int,
             sequences: int, kv_bytes: float, weight_shards: int = 1,
             kv_shards: int = 1, runtime_gib: float = 2,
             safety_fraction: float = 0.15, device_gib: float | None = None) -> dict:
    positive = {"parameters_b": parameters_b, "weight_bits": weight_bits,
                "layers": layers, "kv_heads": kv_heads, "head_dim": head_dim,
                "tokens": tokens, "sequences": sequences, "kv_bytes": kv_bytes,
                "weight_shards": weight_shards, "kv_shards": kv_shards}
    for name, value in positive.items():
        if not math.isfinite(value) or value <= 0:
            raise ValueError(f"{name} must be finite and greater than zero")
    for name, value in {"weight_overhead": weight_overhead, "runtime_gib": runtime_gib}.items():
        if not math.isfinite(value) or value < 0:
            raise ValueError(f"{name} must be finite and nonnegative")
    if not math.isfinite(safety_fraction) or not 0 <= safety_fraction < 1:
        raise ValueError("safety_fraction must be in [0, 1)")
    if device_gib is not None and (not math.isfinite(device_gib) or device_gib <= 0):
        raise ValueError("device_gib must be finite and greater than zero")
    if kv_heads % kv_shards:
        raise ValueError("kv_heads must divide evenly across kv_shards in this simplified model; use kv_shards=1 for replicated KV")
    total_weight = parameters_b * 1e9 * weight_bits / 8 * (1 + weight_overhead)
    total_kv = 2 * layers * kv_heads * head_dim * tokens * sequences * kv_bytes
    subtotal = total_weight / weight_shards / GIB + total_kv / kv_shards / GIB + runtime_gib
    inputs = dict(parameters_b=parameters_b, weight_bits=weight_bits,
        weight_overhead=weight_overhead, layers=layers, kv_heads=kv_heads,
        head_dim=head_dim, tokens=tokens, sequences=sequences, kv_bytes=kv_bytes,
        weight_shards=weight_shards, kv_shards=kv_shards, runtime_gib=runtime_gib,
        safety_fraction=safety_fraction, device_gib=device_gib)
    result = {"schema_version": 1, "kind": "planning_estimate_not_a_fit_verdict", "inputs": inputs,
        "total_weight_gib": total_weight / GIB, "total_kv_gib": total_kv / GIB,
        "per_device_weight_gib_if_evenly_sharded": total_weight / weight_shards / GIB,
        "per_device_kv_gib_if_evenly_sharded": total_kv / kv_shards / GIB,
        "per_device_subtotal_gib": subtotal,
        "required_capacity_gib_with_reserve": subtotal / (1 - safety_fraction),
        "assumptions": ["Every layer stores conventional full-context K and V; grouped-query heads are explicit.",
            "All sequences have the same allocated token count; use prompt plus generation reserve.",
            "Weights and KV shard evenly only if the chosen runtime implements that layout.",
            "Runtime GiB is a user allowance, not a measurement of activations, workspace or graphs.",
            "Quantization scales, padding and higher-precision tensors need a measured overhead allowance.",
            "MLA, sliding/hybrid attention, encoder-decoder, speculative decoding, MoE placement and training require separate models.",
            "This estimate does not prove backend, dtype, GPU or operating-system compatibility."]}
    if device_gib is not None:
        result["device_usable_budget_gib_after_reserve"] = device_gib * (1 - safety_fraction)
        result["remaining_budget_gib"] = device_gib * (1 - safety_fraction) - subtotal
        result["budget_comparison"] = "within_assumed_budget_verify_on_hardware" if result["remaining_budget_gib"] >= 0 else "exceeds_assumed_budget"
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--parameters-b", type=float, required=True)
    parser.add_argument("--weight-bits", type=float, required=True)
    parser.add_argument("--weight-overhead", type=float, default=0.15, help="Fraction beyond nominal weight bits; an estimate")
    for arg in ("layers", "kv-heads", "head-dim", "tokens"):
        parser.add_argument("--" + arg, type=int, required=True)
    parser.add_argument("--sequences", type=int, default=1)
    parser.add_argument("--kv-bytes", type=float, default=2)
    parser.add_argument("--weight-shards", type=int, default=1)
    parser.add_argument("--kv-shards", type=int, default=1)
    parser.add_argument("--runtime-gib", type=float, default=2)
    parser.add_argument("--safety-fraction", type=float, default=0.15)
    parser.add_argument("--device-gib", type=float)
    args = parser.parse_args()
    try:
        result = estimate(**vars(args))
    except ValueError as error:
        parser.error(str(error))
    print(json.dumps(result, indent=2, sort_keys=True, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
