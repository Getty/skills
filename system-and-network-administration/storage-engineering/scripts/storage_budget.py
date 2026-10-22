#!/usr/bin/env python3
"""Calculate idealized storage capacity and transfer budgets; perform no I/O except JSON output."""

from __future__ import annotations

import argparse
import json
import math
import sys


TIB = 2**40
MIB = 2**20


class InputError(ValueError):
    """Invalid model input or an unrepresentable numerical result."""


class JsonArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        raise InputError(message)


def finite_number(value: str) -> float:
    try:
        number = float(value)
    except (ValueError, OverflowError) as exc:
        raise argparse.ArgumentTypeError("must be a finite number") from exc
    if not math.isfinite(number):
        raise argparse.ArgumentTypeError("must be a finite number")
    return number


def positive_count(value: str) -> int:
    try:
        count = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("must be a positive integer") from exc
    if count <= 0:
        raise argparse.ArgumentTypeError("must be a positive integer")
    # Preserve exact integer representation in ordinary JSON number consumers.
    if count > 2**53 - 1:
        raise argparse.ArgumentTypeError("must be at most 9007199254740991")
    return count


def checked(value: float, name: str, *, positive: bool = False) -> float:
    if not math.isfinite(value):
        raise InputError(f"{name} exceeds the finite numerical range")
    if positive and value <= 0:
        raise InputError(f"{name} underflows the positive numerical range")
    return value


def parser() -> JsonArgumentParser:
    result = JsonArgumentParser(
        description="Idealized capacity and transfer arithmetic; no device, file, or network access.",
        add_help=False,
        allow_abbrev=False,
    )
    result.add_argument("-h", "--help", action="store_true", help="print help as JSON")
    result.add_argument("--raw-tib", type=finite_number, required=True, help="positive raw capacity in TiB")
    protection = result.add_mutually_exclusive_group(required=True)
    protection.add_argument("--replicas", type=positive_count, metavar="N", help="positive number of full copies")
    protection.add_argument("--ec", type=positive_count, nargs=2, metavar=("K", "M"), help="positive data and parity fragment counts")
    result.add_argument("--reserve-percent", type=finite_number, default=20.0, help="reserved fraction of protected capacity, 0 <= value < 100; default 20")
    result.add_argument("--occupied-tib", type=finite_number, help="nonnegative logical payload to compare with budgets")
    result.add_argument("--lost-raw-tib", type=finite_number, default=0.0, help="raw capacity removed from service, 0 <= loss < raw; default 0")
    result.add_argument("--transfer-tib", type=finite_number, help="nonnegative transfer/backlog bytes expressed in TiB")
    result.add_argument("--bandwidth-mbps", type=finite_number, help="positive transfer-path bandwidth in decimal Mbit/s")
    result.add_argument("--efficiency", type=finite_number, help="transfer efficiency, 0 < value <= 1; default 0.7 when transfer is modeled")
    result.add_argument("--ongoing-mib-s", type=finite_number, help="nonnegative transfer-equivalent continuing demand in MiB/s; default 0")
    return result


def calculate(args: argparse.Namespace) -> dict:
    if args.raw_tib <= 0:
        raise InputError("--raw-tib must be greater than zero")
    if not 0 <= args.reserve_percent < 100:
        raise InputError("--reserve-percent must satisfy 0 <= value < 100")
    if not 0 <= args.lost_raw_tib < args.raw_tib:
        raise InputError("--lost-raw-tib must satisfy 0 <= loss < raw capacity")
    if args.occupied_tib is not None and args.occupied_tib < 0:
        raise InputError("--occupied-tib must be nonnegative")

    has_transfer = args.transfer_tib is not None
    if has_transfer != (args.bandwidth_mbps is not None):
        raise InputError("--transfer-tib and --bandwidth-mbps must be supplied together")
    if not has_transfer and (args.efficiency is not None or args.ongoing_mib_s is not None):
        raise InputError("--efficiency and --ongoing-mib-s require the paired transfer inputs")

    if args.replicas is not None:
        protection_efficiency = 1.0 / args.replicas
        protection = {"method": "replication", "replicas": args.replicas}
    else:
        data_fragments, parity_fragments = args.ec
        if data_fragments + parity_fragments > 2**53 - 1:
            raise InputError("--ec fragment-count sum must be at most 9007199254740991")
        protection_efficiency = data_fragments / (data_fragments + parity_fragments)
        protection = {
            "method": "erasure_coding",
            "data_fragments": data_fragments,
            "parity_fragments": parity_fragments,
        }
    protection["ideal_raw_to_logical_ratio"] = protection_efficiency

    available_fraction = 1.0 - args.reserve_percent / 100.0
    ideal_logical = checked(args.raw_tib * protection_efficiency, "ideal logical capacity", positive=True)
    planned_logical = checked(ideal_logical * available_fraction, "planned logical capacity", positive=True)
    surviving_raw = checked(args.raw_tib - args.lost_raw_tib, "surviving raw capacity", positive=True)
    survivor_budget = checked(
        surviving_raw * protection_efficiency * available_fraction,
        "survivor budget at original protection",
        positive=True,
    )
    occupied = args.occupied_tib
    capacity = {
        "raw_tib": args.raw_tib,
        "ideal_logical_tib": ideal_logical,
        "reserve_percent": args.reserve_percent,
        "planned_logical_tib": planned_logical,
        "occupied_logical_tib": occupied,
        "lost_raw_tib": args.lost_raw_tib,
        "surviving_raw_tib": surviving_raw,
        "survivor_budget_at_original_protection_tib": survivor_budget,
        "capacity_only_fit_healthy": None if occupied is None else occupied <= planned_logical,
        "capacity_only_fit_after_loss": None if occupied is None else occupied <= survivor_budget,
        "healthy_budget_margin_tib": None if occupied is None else checked(planned_logical - occupied, "healthy margin"),
        "survivor_budget_margin_tib": None if occupied is None else checked(survivor_budget - occupied, "survivor margin"),
        "scope": "Raw-capacity arithmetic only. Survivor budget is capacity for the original protection scheme after repair, not currently readable data or a placement/availability guarantee.",
    }

    transfer = None
    if has_transfer:
        if args.transfer_tib < 0:
            raise InputError("--transfer-tib must be nonnegative")
        if args.bandwidth_mbps <= 0:
            raise InputError("--bandwidth-mbps must be greater than zero")
        efficiency = 0.7 if args.efficiency is None else args.efficiency
        ongoing_mib_s = 0.0 if args.ongoing_mib_s is None else args.ongoing_mib_s
        if not 0 < efficiency <= 1:
            raise InputError("--efficiency must satisfy 0 < value <= 1")
        if ongoing_mib_s < 0:
            raise InputError("--ongoing-mib-s must be nonnegative")

        transfer_bytes = checked(args.transfer_tib * TIB, "transfer bytes")
        line_rate = checked(args.bandwidth_mbps * (1_000_000 / 8), "line rate", positive=True)
        effective_rate = checked(line_rate * efficiency, "effective transfer rate", positive=True)
        ongoing_rate = checked(ongoing_mib_s * MIB, "ongoing transfer demand")
        net_rate = checked(effective_rate - ongoing_rate, "net backlog drain rate")
        ideal_seconds = checked(transfer_bytes / line_rate, "ideal transfer time")
        effective_seconds = checked(transfer_bytes / effective_rate, "effective transfer time")
        can_catch_up = net_rate > 0
        drain_seconds = checked(transfer_bytes / net_rate, "backlog drain time") if can_catch_up else None
        transfer = {
            "transfer_tib": args.transfer_tib,
            "transfer_bytes": transfer_bytes,
            "bandwidth_mbps_decimal": args.bandwidth_mbps,
            "efficiency": efficiency,
            "line_rate_bytes_per_second": line_rate,
            "effective_rate_bytes_per_second": effective_rate,
            "ongoing_mib_per_second_binary": ongoing_mib_s,
            "ongoing_bytes_per_second": ongoing_rate,
            "net_backlog_drain_bytes_per_second": net_rate,
            "ideal_no_overhead_transfer_seconds": ideal_seconds,
            "assumed_effective_transfer_seconds_without_ongoing": effective_seconds,
            "can_catch_up_under_assumptions": can_catch_up,
            "estimated_current_backlog_drain_seconds": drain_seconds,
            "status": "positive_net_drain_rate" if can_catch_up else "cannot_catch_up",
            "scope": "Arithmetic with constant bandwidth, efficiency, and transfer-equivalent ongoing demand. This is not an RTO or a guaranteed completion time.",
        }

    return {
        "schema_version": 1,
        "units": {"TiB": "2^40 bytes", "MiB": "2^20 bytes", "Mbps": "10^6 bits per second"},
        "protection": protection,
        "capacity": capacity,
        "transfer": transfer,
        "limitations": [
            "Metadata, snapshots, journals, padding, imbalance, and implementation overhead are not automatically modeled; reserve is a planning input, not a measured overhead ratio.",
            "Sufficient independent failure domains, correct placement, quorum, fencing, and surviving valid fragments/copies must be verified separately.",
            "Raw capacity loss does not determine lost data, currently readable data, repair traffic, or erasure-code decode availability.",
            "Transfer size and ongoing demand must already include the work of the chosen transfer/repair method; no amplification factor is inferred.",
        ],
    }


def emit(payload: dict, *, stream=sys.stdout) -> None:
    print(json.dumps(payload, indent=2, sort_keys=True, allow_nan=False), file=stream)


def main(argv: list[str] | None = None) -> int:
    arguments = sys.argv[1:] if argv is None else argv
    argument_parser = parser()
    if "--help" in arguments or "-h" in arguments:
        emit({"schema_version": 1, "help": argument_parser.format_help()})
        return 0
    try:
        result = calculate(argument_parser.parse_args(arguments))
    except (InputError, OverflowError, ZeroDivisionError) as exc:
        emit({"schema_version": 1, "error": str(exc)}, stream=sys.stderr)
        return 2
    emit(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
