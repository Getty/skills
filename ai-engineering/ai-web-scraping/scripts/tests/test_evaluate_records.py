"""Offline tests of fixture-universe scoring and strict input rejection."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))
from evaluate_records import evaluate_records, validate_gold  # noqa: E402


def observed(value):
    if type(value) is bool:
        quote = "true" if value else "false"
        normalization = "boolean_literal"
    elif type(value) is int:
        quote = str(value)
        normalization = "integer"
    else:
        quote = value
        normalization = "exact"
    return {
        "status": "observed",
        "value": value,
        "normalization": normalization,
        "evidence": [{"start": 0, "end": len(quote), "quote": quote}],
    }


def absent():
    return {
        "status": "absent",
        "value": None,
        "normalization": None,
        "evidence": [],
        "note": "Not present within the inspected record.",
    }


def candidate(record_id="p1", fields=None):
    return {
        "schema_version": "1.0",
        "record_id": record_id,
        "source": {
            "url": "https://catalog.example/products",
            "fetched_at": "2026-10-29T12:00:00Z",
            "snapshot_ref": "never-read.txt",
            "snapshot_sha256": "a" * 64,
            "record_span": {"start": 0, "end": 100},
        },
        "fields": fields if fields is not None else {"name": observed("A")},
    }


def gold(*records):
    return {"schema_version": "1.0", "records": list(records)}


def gold_record(record_id="p1", fields=None):
    return {
        "record_id": record_id,
        "fields": fields if fields is not None else {
            "name": {"status": "observed", "value": "A"},
        },
    }


class EvaluationTests(unittest.TestCase):
    def assertFraction(self, report, metric, numerator, denominator):
        actual = report["metrics"][metric]
        self.assertEqual(actual["numerator"], numerator)
        self.assertEqual(actual["denominator"], denominator)
        expected = numerator / denominator if denominator else None
        self.assertEqual(actual["value"], expected)

    def test_perfect_fixture_does_not_claim_evidence_or_production_coverage(self):
        report = evaluate_records([candidate()], gold(gold_record()))
        self.assertEqual(report["universe"], "supplied_gold_fixture_only")
        self.assertIs(report["evidence_checked"], False)
        for metric in report["metrics"]:
            self.assertFraction(report, metric, 1, 1)

    def test_false_and_zero_are_different_in_both_directions(self):
        for supplied, expected in [(False, 0), (0, False), (True, 1), (1, True)]:
            with self.subTest(supplied=supplied, expected=expected):
                report = evaluate_records(
                    [candidate(fields={"value": observed(supplied)})],
                    gold(gold_record(fields={"value": {"status": "observed", "value": expected}})),
                )
                self.assertFraction(report, "observed_value_precision", 0, 1)
                self.assertFraction(report, "observed_value_recall", 0, 1)
                self.assertFraction(report, "field_state_accuracy", 1, 1)

    def test_missing_entity_penalizes_all_relevant_recall_metrics(self):
        expected = gold(gold_record(), gold_record("p2"))
        report = evaluate_records([candidate()], expected)
        self.assertFraction(report, "entity_precision", 1, 1)
        self.assertFraction(report, "entity_recall", 1, 2)
        self.assertFraction(report, "observed_value_recall", 1, 2)
        self.assertFraction(report, "field_state_accuracy", 1, 2)
        self.assertEqual(report["counts"]["missing_entities"], 1)

    def test_unknown_entities_and_fields_penalize_observed_precision(self):
        known = candidate(fields={"name": observed("A"), "unexpected": observed("X")})
        unknown = candidate("not-in-gold", {"name": observed("A")})
        report = evaluate_records([known, unknown], gold(gold_record()))
        self.assertFraction(report, "entity_precision", 1, 2)
        self.assertFraction(report, "observed_value_precision", 1, 3)
        self.assertFraction(report, "observed_value_recall", 1, 1)
        self.assertEqual(report["counts"]["unknown_entities"], 1)
        self.assertEqual(report["counts"]["unknown_fields"], 2)
        self.assertEqual(report["counts"]["unknown_fields_on_known_entities"], 1)
        self.assertEqual(report["counts"]["unknown_entity_fields"], 1)

    def test_missing_field_penalizes_recall_and_state_accuracy(self):
        expected = gold(gold_record(fields={
            "name": {"status": "observed", "value": "A"},
            "category": {"status": "absent", "value": None},
        }))
        report = evaluate_records([candidate()], expected)
        self.assertFraction(report, "field_state_accuracy", 1, 2)
        self.assertFraction(report, "observed_value_recall", 1, 1)

    def test_wrong_observed_value_can_have_correct_field_state(self):
        report = evaluate_records([candidate(fields={"name": observed("B")})], gold(gold_record()))
        self.assertFraction(report, "observed_value_precision", 0, 1)
        self.assertFraction(report, "field_state_accuracy", 1, 1)

    def test_absent_is_not_equivalent_to_explicit_null(self):
        report = evaluate_records(
            [candidate(fields={"value": absent()})],
            gold(gold_record(fields={"value": {"status": "explicit_null", "value": None}})),
        )
        self.assertFraction(report, "field_state_accuracy", 0, 1)

    def test_zero_observed_denominators_are_null(self):
        report = evaluate_records(
            [candidate(fields={"value": absent()})],
            gold(gold_record(fields={"value": {"status": "absent", "value": None}})),
        )
        self.assertFraction(report, "observed_value_precision", 0, 0)
        self.assertFraction(report, "observed_value_recall", 0, 0)
        self.assertFraction(report, "field_state_accuracy", 1, 1)

    def test_empty_predictions_measure_missing_gold(self):
        report = evaluate_records([], gold(gold_record()))
        self.assertFraction(report, "entity_precision", 0, 0)
        self.assertFraction(report, "entity_recall", 0, 1)
        self.assertFraction(report, "observed_value_precision", 0, 0)
        self.assertFraction(report, "observed_value_recall", 0, 1)
        self.assertFraction(report, "field_state_accuracy", 0, 1)

    def test_entity_only_gold_has_undefined_field_metrics(self):
        report = evaluate_records([], gold(gold_record(fields={})))
        self.assertFraction(report, "field_state_accuracy", 0, 0)
        self.assertFraction(report, "observed_value_recall", 0, 0)

    def test_duplicate_record_ids_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "duplicate record_id"):
            evaluate_records([candidate(), candidate()], gold(gold_record()))
        with self.assertRaisesRegex(ValueError, "duplicate record_id"):
            evaluate_records([candidate()], gold(gold_record(), gold_record()))

    def test_malformed_gold_is_rejected_without_coercion(self):
        bad_gold = [None, [], {}, gold(), {"schema_version": 1, "records": [gold_record()]}]
        for extra_location in ["root", "record", "field"]:
            value = gold(gold_record())
            target = {"root": value, "record": value["records"][0],
                      "field": value["records"][0]["fields"]["name"]}[extra_location]
            target["unexpected"] = True
            bad_gold.append(value)
        for field in [
            {"status": "invented", "value": None},
            {"status": "observed", "value": 1.0},
            {"status": "observed", "value": None},
            {"status": "observed", "value": []},
            {"status": "observed", "value": {}},
            {"status": "absent", "value": 0},
            {"status": "observed"},
        ]:
            bad_gold.append(gold(gold_record(fields={"name": field})))
        for value in bad_gold:
            with self.subTest(value=value), self.assertRaises(ValueError):
                validate_gold(value)

    def test_malformed_candidate_contract_is_rejected(self):
        mutations = []
        value = candidate()
        value["unexpected"] = 1
        mutations.append(value)
        value = candidate()
        value["source"]["unexpected"] = 1
        mutations.append(value)
        value = candidate()
        value["fields"]["name"]["value"] = []
        mutations.append(value)
        value = candidate()
        value["fields"]["name"]["status"] = "invented"
        mutations.append(value)
        for value in mutations:
            with self.subTest(value=value), self.assertRaises(ValueError):
                evaluate_records([value], gold(gold_record()))


class CommandLineTests(unittest.TestCase):
    def run_cli(self, records_text, gold_text):
        with tempfile.TemporaryDirectory() as directory:
            records_path = Path(directory) / "records.jsonl"
            gold_path = Path(directory) / "gold.json"
            records_path.write_text(records_text, encoding="utf-8")
            gold_path.write_text(gold_text, encoding="utf-8")
            return subprocess.run(
                [sys.executable, str(SCRIPTS / "evaluate_records.py"), str(records_path),
                 "--gold", str(gold_path)],
                capture_output=True, text=True, check=False, timeout=10,
            )

    def test_imperfect_metrics_exit_successfully_without_snapshot_files(self):
        result = self.run_cli(json.dumps(candidate(fields={"name": observed("B")})),
                              json.dumps(gold(gold_record())))
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["metrics"]["observed_value_precision"]["value"], 0)
        self.assertIs(report["evidence_checked"], False)

    def test_empty_prediction_file_is_a_valid_measurement(self):
        result = self.run_cli("", json.dumps(gold(gold_record())))
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertIsNone(report["metrics"]["entity_precision"]["value"])
        self.assertEqual(report["metrics"]["entity_recall"]["value"], 0)

    def test_duplicate_json_keys_and_nonfinite_numbers_are_rejected(self):
        records = json.dumps(candidate())
        expected = json.dumps(gold(gold_record()))
        corruptions = [
            (records.replace('"schema_version": "1.0"',
                             '"schema_version": "1.0", "schema_version": "1.0"'), expected),
            (records.replace('"value": "A"', '"value": NaN'), expected),
            (records, expected.replace('"schema_version": "1.0"',
                                      '"schema_version": "1.0", "schema_version": "1.0"')),
            (records, expected.replace('"value": "A"', '"value": Infinity')),
            (records, "{invalid"),
            (records, json.dumps(gold())),
            (records + "\n" + records, expected),
        ]
        for supplied, wanted in corruptions:
            with self.subTest(supplied=supplied, wanted=wanted):
                result = self.run_cli(supplied, wanted)
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(result.stdout, "")
                self.assertIn("error", json.loads(result.stderr))


if __name__ == "__main__":
    unittest.main()
