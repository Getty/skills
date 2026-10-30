#!/usr/bin/env python3
"""Measure records against an explicit gold fixture, without reading evidence.

Python 3.10+, standard library only. Run:
    python scripts/evaluate_records.py RECORDS.jsonl --gold GOLD.json

Matching uses exact record IDs, field names, statuses, and scalar types/values.
Unknown entity/field pairs count against observed-value precision. Missing gold
entities count against entity recall, observed-value recall, and state accuracy.
An imperfect measurement is a successful execution; malformed input exits 2.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from validate_evidence import (
    load_records,
    strict_loads,
    validate_record_structure,
)


STATUSES = frozenset({"observed", "absent", "explicit_null", "unparseable", "conflict"})
MAX_GOLD_BYTES = 16 * 1024 * 1024


def _exact_object(value: Any, keys: set[str], where: str) -> dict[str, Any]:
    if type(value) is not dict:
        raise ValueError(f"{where}: expected an object")
    if any(type(key) is not str for key in value):
        raise ValueError(f"{where}: object keys must be strings")
    actual = set(value)
    if actual != keys:
        missing = sorted(keys - actual)
        extra = sorted(actual - keys)
        raise ValueError(f"{where}: invalid keys (missing={missing}, extra={extra})")
    return value


def _nonempty_string(value: Any, where: str) -> str:
    if type(value) is not str or not value.strip():
        raise ValueError(f"{where}: expected a nonempty string")
    return value


def validate_gold(value: Any) -> dict[str, dict[str, Any]]:
    """Validate the small gold format and index its records without coercion."""
    gold = _exact_object(value, {"schema_version", "records"}, "gold")
    if gold["schema_version"] != "1.0":
        raise ValueError("gold.schema_version: expected '1.0'")
    if type(gold["records"]) is not list or not gold["records"]:
        raise ValueError("gold.records: expected a nonempty array")

    indexed: dict[str, dict[str, Any]] = {}
    for index, raw_record in enumerate(gold["records"]):
        where = f"gold.records[{index}]"
        record = _exact_object(raw_record, {"record_id", "fields"}, where)
        record_id = _nonempty_string(record["record_id"], f"{where}.record_id")
        if record_id in indexed:
            raise ValueError(f"{where}: duplicate record_id {record_id!r}")
        fields = record["fields"]
        if type(fields) is not dict:
            raise ValueError(f"{where}.fields: expected an object")
        for name, raw_field in fields.items():
            _nonempty_string(name, f"{where}.fields key")
            field_where = f"{where}.fields[{name!r}]"
            field = _exact_object(raw_field, {"status", "value"}, field_where)
            status = field["status"]
            if type(status) is not str or status not in STATUSES:
                raise ValueError(f"{field_where}.status: unsupported field state")
            field_value = field["value"]
            if status == "observed":
                if type(field_value) not in (str, int, bool):
                    raise ValueError(
                        f"{field_where}.value: observed values must be string, integer, or boolean"
                    )
            elif field_value is not None:
                raise ValueError(f"{field_where}.value: non-observed states require null")
        indexed[record_id] = record
    return indexed


def _index_candidates(records: Any) -> dict[str, dict[str, Any]]:
    if type(records) is not list:
        raise ValueError("records: expected a list of parsed candidate records")
    indexed: dict[str, dict[str, Any]] = {}
    for index, record in enumerate(records):
        errors = validate_record_structure(record)
        if errors:
            raise ValueError(f"records[{index}]: " + "; ".join(errors))
        record_id = record["record_id"]
        if record_id in indexed:
            raise ValueError(f"records[{index}]: duplicate record_id {record_id!r}")
        indexed[record_id] = record
    return indexed


def _same_typed_value(left: Any, right: Any) -> bool:
    # Python considers False == 0 and True == 1; the extraction contract does not.
    return type(left) is type(right) and left == right


def _fraction(numerator: int, denominator: int) -> dict[str, Any]:
    return {
        "numerator": numerator,
        "denominator": denominator,
        "value": numerator / denominator if denominator else None,
    }


def evaluate_records(records: list[dict[str, Any]], gold: Any) -> dict[str, Any]:
    """Validate structures and measure this fixture; never read source snapshots."""
    predicted = _index_candidates(records)
    expected = validate_gold(gold)
    matching_ids = predicted.keys() & expected.keys()
    unknown_ids = predicted.keys() - expected.keys()
    missing_ids = expected.keys() - predicted.keys()

    observed_predictions = 0
    correct_observed = 0
    unknown_fields_on_known_entities = 0
    unknown_entity_fields = 0

    for record_id, record in predicted.items():
        gold_record = expected.get(record_id)
        gold_fields = gold_record["fields"] if gold_record is not None else {}
        for name, field in record["fields"].items():
            if gold_record is None:
                unknown_entity_fields += 1
            elif name not in gold_fields:
                unknown_fields_on_known_entities += 1
            if field["status"] != "observed":
                continue
            observed_predictions += 1
            gold_field = gold_fields.get(name)
            if (
                gold_field is not None
                and gold_field["status"] == "observed"
                and _same_typed_value(field["value"], gold_field["value"])
            ):
                correct_observed += 1

    gold_observed = 0
    gold_field_count = 0
    correct_states = 0
    for record_id, record in expected.items():
        predicted_record = predicted.get(record_id)
        predicted_fields = predicted_record["fields"] if predicted_record is not None else {}
        for name, field in record["fields"].items():
            gold_field_count += 1
            gold_observed += int(field["status"] == "observed")
            predicted_field = predicted_fields.get(name)
            if predicted_field is not None and predicted_field["status"] == field["status"]:
                correct_states += 1

    return {
        "schema_version": "1.0",
        "universe": "supplied_gold_fixture_only",
        "evidence_checked": False,
        "matching": "exact_record_id_field_name_status_and_typed_value",
        "counts": {
            "predicted_entities": len(predicted),
            "gold_entities": len(expected),
            "matched_entities": len(matching_ids),
            "unknown_entities": len(unknown_ids),
            "missing_entities": len(missing_ids),
            "unknown_fields": unknown_fields_on_known_entities + unknown_entity_fields,
            "unknown_fields_on_known_entities": unknown_fields_on_known_entities,
            "unknown_entity_fields": unknown_entity_fields,
        },
        "unknown_fields_definition": (
            "Predicted entity/field pairs absent from supplied gold, including fields on unknown entities."
        ),
        "metrics": {
            "entity_precision": _fraction(len(matching_ids), len(predicted)),
            "entity_recall": _fraction(len(matching_ids), len(expected)),
            "observed_value_precision": _fraction(correct_observed, observed_predictions),
            "observed_value_recall": _fraction(correct_observed, gold_observed),
            "field_state_accuracy": _fraction(correct_states, gold_field_count),
        },
    }


def _load_gold(path: Path) -> Any:
    with path.open("rb") as handle:
        raw = handle.read(MAX_GOLD_BYTES + 1)
    if len(raw) > MAX_GOLD_BYTES:
        raise ValueError("gold file exceeds the 16 MiB input limit")
    return strict_loads(raw.decode("utf-8"))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("records", type=Path, help="Candidate JSONL using extraction schema 1.0")
    parser.add_argument("--gold", type=Path, required=True, help="Nonempty gold fixture JSON")
    args = parser.parse_args(argv)
    try:
        records = load_records(args.records, allow_empty=True)
        result = evaluate_records(records, _load_gold(args.gold))
    except (ValueError, OSError, UnicodeError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=True, allow_nan=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=True, allow_nan=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
