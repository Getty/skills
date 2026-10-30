#!/usr/bin/env python3
"""Compute effective cost from USER-SUPPLIED billing and accepted output counts."""
from __future__ import annotations

import argparse
import json
import math
from _common import nonnegative_float, nonnegative_int


def calculate(hourly: float, hours: float, other_cost: float,
              useful_tokens: int, successful_requests: int, currency: str) -> dict:
    if any(isinstance(v, bool) or not math.isfinite(v) or v < 0 for v in (hourly, hours, other_cost)):
        raise ValueError("cost inputs must be finite and nonnegative")
    if any(isinstance(v, bool) or not isinstance(v, int) or v < 0 for v in (useful_tokens, successful_requests)):
        raise ValueError("accepted output counts must be nonnegative integers")
    if not currency.isalpha() or not 3 <= len(currency) <= 8:
        raise ValueError("currency must be a short alphabetic unit, e.g. EUR")
    total = hourly * hours + other_cost
    if not math.isfinite(total):
        raise ValueError("total cost overflows the supported numerical range")
    return {
        "currency": currency.upper(), "compute_cost": hourly * hours,
        "other_cost": other_cost, "total_cost": total,
        "accepted_useful_tokens": useful_tokens,
        "accepted_successful_requests": successful_requests,
        "cost_per_million_useful_tokens": total / useful_tokens * 1e6 if useful_tokens else None,
        "cost_per_accepted_request": total / successful_requests if successful_requests else None,
        "note": "User-supplied inputs, NOT live provider prices. Counts must satisfy your quality and SLO gates. Null means no valid denominator."
    }


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--hourly", type=nonnegative_float, required=True)
    p.add_argument("--hours", type=nonnegative_float, required=True)
    p.add_argument("--other-cost", type=nonnegative_float, default=0)
    p.add_argument("--useful-tokens", type=nonnegative_int, required=True)
    p.add_argument("--successful-requests", type=nonnegative_int, required=True)
    p.add_argument("--currency", default="EUR")
    try:
        result = calculate(**vars(p.parse_args()))
    except ValueError as exc:
        p.error(str(exc))
    print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
