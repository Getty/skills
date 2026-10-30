"""Offline contract tests; synthetic fixtures, no network or model calls."""

from __future__ import annotations

import copy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))
import validate_evidence as ve


FIXTURES = SCRIPTS.parent / "assets" / "fixtures"


class EvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixtures = ve.load_records(FIXTURES / "records.valid.jsonl")
        cls.raw = (FIXTURES / "catalog.txt").read_bytes()

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.snapshots = self.root / "snapshots"
        self.snapshots.mkdir()
        (self.snapshots / "catalog.txt").write_bytes(self.raw)

    def record(self, index=0):
        return copy.deepcopy(self.fixtures[index])

    def assert_invalid(self, record, fragment):
        errors = ve.validate_record(record, self.snapshots)
        self.assertTrue(errors, "mutation unexpectedly passed validation")
        self.assertIn(fragment, "\n".join(errors))

    def write_records(self, records, name="candidates.jsonl"):
        path = self.root / name
        path.write_text(
            "".join(json.dumps(rec, ensure_ascii=False, allow_nan=False) + "\n" for rec in records),
            encoding="utf-8",
        )
        return path

    def test_valid_fixture_unicode_crlf_and_three_records(self):
        self.assertEqual(len(self.fixtures), 3)
        self.assertIn(b"\r\n", self.raw)
        text = self.raw.decode("utf-8")
        self.assertIn("🪔", text)
        self.assertNotEqual(len(text), len(self.raw))
        for rec in self.fixtures:
            with self.subTest(record_id=rec["record_id"]):
                self.assertEqual(ve.validate_record(rec, self.snapshots), [])

    def test_crlf_and_code_points_are_not_normalized(self):
        rec = self.record(2)
        evidence = rec["fields"]["name"]["evidence"][0]
        text = self.raw.decode("utf-8")
        self.assertEqual(text[evidence["start"]:evidence["end"]], evidence["quote"])
        old = evidence["start"]
        evidence["start"] = len(text[:old].encode("utf-8"))
        evidence["end"] = evidence["start"] + len(evidence["quote"])
        self.assertTrue(ve.validate_record(rec, self.snapshots))
        (self.snapshots / "catalog.txt").write_bytes(self.raw.replace(b"\r\n", b"\n"))
        self.assert_invalid(self.record(), "does not match snapshot bytes")

    def test_hash_mismatch(self):
        rec = self.record()
        rec["source"]["snapshot_sha256"] = "0" * 64
        self.assert_invalid(rec, "does not match snapshot bytes")

    def test_source_quote_mismatch_even_when_normalization_is_consistent(self):
        rec = self.record()
        field = rec["fields"]["currency"]
        field["value"] = "USD"
        field["evidence"][0]["quote"] = "USD"
        self.assert_invalid(rec, "quote does not match snapshot slice")

    def test_neighbor_record_evidence_is_rejected(self):
        rec = self.record()
        rec["fields"]["currency"]["evidence"] = copy.deepcopy(
            self.fixtures[1]["fields"]["currency"]["evidence"]
        )
        self.assert_invalid(rec, "outside record_span")

    def test_record_span_out_of_bounds(self):
        rec = self.record()
        rec["source"]["record_span"]["end"] = len(self.raw) + 100
        self.assert_invalid(rec, "exceeds snapshot code-point length")

    def test_boolean_is_not_an_integer_offset(self):
        rec = self.record()
        rec["fields"]["name"]["evidence"][0]["start"] = True
        self.assert_invalid(rec, "integer bounds")

    def test_reversed_or_negative_spans_are_rejected(self):
        for span in ({"start": -1, "end": 2}, {"start": 3, "end": 2}):
            with self.subTest(span=span):
                rec = self.record()
                rec["source"]["record_span"] = span
                self.assert_invalid(rec, "integer bounds")

    def test_traversal_absolute_and_windows_paths_are_rejected(self):
        for ref in ("../outside.txt", "/tmp/outside.txt", "C:\\outside.txt", "a/../catalog.txt", "a//b"):
            with self.subTest(ref=ref):
                rec = self.record()
                rec["source"]["snapshot_ref"] = ref
                self.assert_invalid(rec, "safe relative")

    def test_symlink_escape_is_rejected(self):
        outside = self.root / "outside.txt"
        outside.write_bytes(self.raw)
        link = self.snapshots / "escape.txt"
        try:
            link.symlink_to(outside)
        except (OSError, NotImplementedError):
            self.skipTest("symlink creation is unavailable")
        rec = self.record()
        rec["source"]["snapshot_ref"] = "escape.txt"
        self.assert_invalid(rec, "escapes snapshots-dir")

    def test_missing_snapshot_is_rejected(self):
        rec = self.record()
        rec["source"]["snapshot_ref"] = "missing.txt"
        self.assert_invalid(rec, "snapshot path is missing")

    def test_invalid_utf8_snapshot_is_rejected(self):
        (self.snapshots / "catalog.txt").write_bytes(b"\xff")
        self.assert_invalid(self.record(), "not valid UTF-8")

    def test_snapshot_byte_cap(self):
        with patch.object(ve, "MAX_SNAPSHOT_BYTES", 10):
            self.assert_invalid(self.record(), "snapshot exceeds byte cap")

    def test_snapshot_cache_retains_only_one_file(self):
        store = ve.SnapshotStore(self.snapshots)
        for index in range(5):
            name = f"snapshot-{index}.txt"
            (self.snapshots / name).write_bytes(self.raw)
            self.assertEqual(store.read(name)[0], self.raw.decode("utf-8"))
            self.assertEqual(len(store._cache), 1)
        self.assertIn((self.snapshots / "snapshot-4.txt").resolve(), store._cache)

    def test_source_url_scheme_userinfo_and_invalid_port(self):
        for url in ("file:///tmp/data", "https://name:secret@example.test/x", "https://example.test:99999", "https://example.test/a\nb"):
            with self.subTest(url=url):
                rec = self.record()
                rec["source"]["url"] = url
                self.assert_invalid(rec, "source.url")

    def test_timestamp_requires_timezone(self):
        for timestamp in ("2026-10-29T12:00:00", "2026-10-29", "yesterday"):
            with self.subTest(timestamp=timestamp):
                rec = self.record()
                rec["source"]["fetched_at"] = timestamp
                self.assert_invalid(rec, "offset-aware")

    def test_timestamp_rejects_missing_seconds_basic_form_and_bad_offset(self):
        for timestamp in (
            "2026-10-29T12:00Z", "20261029T120000+0000",
            "2026-10-29T12:00:00+0000", "2026-10-29T12:00:00+00:60",
        ):
            with self.subTest(timestamp=timestamp):
                rec = self.record()
                rec["source"]["fetched_at"] = timestamp
                self.assert_invalid(rec, "offset-aware")

    def test_exact_keys_at_every_contract_level(self):
        for place in ("record", "source", "field", "evidence"):
            with self.subTest(place=place):
                rec = self.record()
                target = {
                    "record": rec,
                    "source": rec["source"],
                    "field": rec["fields"]["name"],
                    "evidence": rec["fields"]["name"]["evidence"][0],
                }[place]
                target["unexpected"] = "value"
                self.assert_invalid(rec, "unexpected keys")

    def test_observed_rejects_null_float_array_and_object(self):
        for value in (None, 19.95, [], {}):
            with self.subTest(value=value):
                rec = self.record()
                rec["fields"]["price"]["value"] = value
                self.assert_invalid(rec, "observed value must be")

    def test_integer_and_boolean_types_do_not_coerce(self):
        rec = self.record()
        rec["fields"]["stock_count"]["value"] = False
        self.assert_invalid(rec, "not Boolean")
        rec = self.record()
        rec["fields"]["is_available"]["value"] = 0
        self.assert_invalid(rec, "matching Boolean")

    def test_decimal_string_can_differ_only_by_numeric_format(self):
        rec = self.record()
        rec["fields"]["price"]["value"] = "19.9500"
        self.assertEqual(ve.validate_record(rec, self.snapshots), [])
        rec["fields"]["price"]["value"] = "19.96"
        self.assert_invalid(rec, "differs numerically")

    def test_decimal_rejects_comma_exponent_plus_and_nonfinite(self):
        for value in ("19,95", "1.995e1", "+19.95", "NaN", "Infinity"):
            with self.subTest(value=value):
                rec = self.record()
                rec["fields"]["price"]["value"] = value
                self.assert_invalid(rec, "strict dot-decimal")

    def test_observed_requires_evidence_and_known_normalization(self):
        rec = self.record()
        rec["fields"]["name"]["evidence"] = []
        self.assert_invalid(rec, "observed requires evidence")
        rec = self.record()
        rec["fields"]["name"]["normalization"] = "guess"
        self.assert_invalid(rec, "unsupported observed normalization")

    def test_empty_quote_and_zero_width_evidence_are_rejected(self):
        for status in ("observed", "explicit_null", "unparseable", "conflict"):
            with self.subTest(status=status):
                rec = self.record()
                evidence = copy.deepcopy(rec["fields"]["name"]["evidence"][0])
                evidence["end"] = evidence["start"]
                evidence["quote"] = ""
                rec["fields"]["name"] = {
                    "status": status,
                    "value": "" if status == "observed" else None,
                    "normalization": "exact" if status == "observed" else None,
                    "evidence": [evidence],
                    "note": "Synthetic empty-evidence mutation.",
                }
                self.assert_invalid(rec, "quote must be a nonempty string")

    def test_empty_record_span_even_with_all_absent_fields_is_rejected(self):
        rec = self.record()
        rec["source"]["record_span"] = {"start": 0, "end": 0}
        rec["fields"] = {
            "name": {
                "status": "absent", "value": None, "normalization": None,
                "evidence": [], "note": "No content in the inspected empty region.",
            }
        }
        self.assert_invalid(rec, "integer bounds")

    def test_supplied_observed_note_must_be_nonempty(self):
        for note in ("", " ", None):
            with self.subTest(note=note):
                rec = self.record()
                rec["fields"]["name"]["note"] = note
                self.assert_invalid(rec, "note must be a nonempty string")

    def test_absent_requires_nulls_note_and_no_evidence(self):
        for mutation in ("value", "normalization", "note", "evidence"):
            with self.subTest(mutation=mutation):
                rec = self.record(2)
                field = rec["fields"]["price"]
                if mutation == "value":
                    field["value"] = 0
                elif mutation == "normalization":
                    field["normalization"] = "integer"
                elif mutation == "note":
                    del field["note"]
                else:
                    field["evidence"] = copy.deepcopy(rec["fields"]["currency"]["evidence"])
                self.assertTrue(ve.validate_record(rec, self.snapshots))

    def test_explicit_null_and_unparseable_require_evidence(self):
        for status in ("explicit_null", "unparseable"):
            with self.subTest(status=status):
                rec = self.record(2)
                rec["fields"]["stock_count"]["status"] = status
                self.assertEqual(ve.validate_record(rec, self.snapshots), [])
                rec["fields"]["stock_count"]["evidence"] = []
                self.assert_invalid(rec, "requires evidence")

    def test_conflict_requires_distinct_quotes(self):
        rec = self.record()
        first = copy.deepcopy(rec["fields"]["price"]["evidence"][0])
        second = copy.deepcopy(rec["fields"]["stock_count"]["evidence"][0])
        rec["fields"]["price"] = {
            "status": "conflict", "value": None, "normalization": None,
            "evidence": [first, second], "note": "Synthetic competing observations.",
        }
        # Mechanical acceptance does not establish that these quotes semantically conflict.
        self.assertEqual(ve.validate_record(rec, self.snapshots), [])
        rec["fields"]["price"]["evidence"] = [first, copy.deepcopy(first)]
        self.assert_invalid(rec, "two distinct evidence quotes")

    def test_blank_names_invalid_ids_and_unknown_status(self):
        rec = self.record()
        rec["fields"][""] = rec["fields"].pop("name")
        self.assert_invalid(rec, "name must be")
        rec = self.record()
        rec["record_id"] = " "
        self.assert_invalid(rec, "record_id")
        rec = self.record()
        rec["fields"]["name"]["status"] = "inferred"
        self.assert_invalid(rec, "unsupported status")

    def test_strict_json_rejects_duplicate_keys(self):
        for text in ('{"x":1,"x":2}', '{"outer":{"x":1,"x":2}}'):
            with self.subTest(text=text), self.assertRaisesRegex(ValueError, "duplicate"):
                ve.strict_loads(text)

    def test_strict_json_rejects_nonfinite_and_overflow(self):
        for token in ("NaN", "Infinity", "-Infinity", "1e9999", "-1e9999"):
            with self.subTest(token=token), self.assertRaisesRegex(ValueError, "nonfinite"):
                ve.strict_loads('{"number":' + token + '}')

    def test_strict_json_depth_and_surrogate_limits(self):
        with self.assertRaisesRegex(ValueError, "depth"):
            ve.strict_loads("[" * 70 + "0" + "]" * 70)
        with self.assertRaisesRegex(ValueError, "surrogate"):
            ve.strict_loads('"\\ud800"')

    def test_load_records_caps_empty_and_nonobject(self):
        empty = self.root / "empty.jsonl"
        empty.write_text("\n \n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "no records"):
            ve.load_records(empty)
        self.assertEqual(ve.load_records(empty, allow_empty=True), [])
        wrong = self.root / "wrong.jsonl"
        wrong.write_text("[]\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "must be an object"):
            ve.load_records(wrong)
        path = self.write_records([self.record()])
        with patch.object(ve, "MAX_FILE_BYTES", 10), self.assertRaisesRegex(ValueError, "file exceeds"):
            ve.load_records(path)
        with patch.object(ve, "MAX_LINE_BYTES", 10), self.assertRaisesRegex(ValueError, "line byte cap"):
            ve.load_records(path)

    def test_load_records_rejects_invalid_utf8_and_duplicates(self):
        path = self.root / "bad.jsonl"
        path.write_bytes(b"\xff\n")
        with self.assertRaisesRegex(ValueError, "invalid UTF-8"):
            ve.load_records(path)
        path.write_text('{"x":1,"x":2}\n', encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "duplicate"):
            ve.load_records(path)

    def test_duplicate_ids_invalidate_both_occurrences(self):
        path = self.write_records([self.record(), self.record()])
        report = ve.validate_records_file(path, self.snapshots)
        self.assertEqual(report["records_total"], 2)
        self.assertEqual(report["records_invalid"], 2)
        self.assertEqual(report["records_valid"], 0)
        self.assertTrue(all("duplicate" in " ".join(item["errors"]) for item in report["errors"]))

    def test_cli_success_and_nonzero_for_invalid_or_empty(self):
        good = self.write_records(self.fixtures)
        empty = self.root / "empty.jsonl"
        empty.write_text("", encoding="utf-8")
        bad_rec = self.record()
        bad_rec["source"]["snapshot_sha256"] = "0" * 64
        bad = self.write_records([bad_rec], "bad.jsonl")
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
        for path, expected_code in ((good, 0), (bad, 1), (empty, 1)):
            with self.subTest(path=path.name):
                result = subprocess.run(
                    [sys.executable, str(SCRIPTS / "validate_evidence.py"), str(path), "--snapshots-dir", str(self.snapshots)],
                    capture_output=True, text=True, env=env, check=False,
                )
                self.assertEqual(result.returncode, expected_code, result.stderr)
                report = ve.strict_loads(result.stdout)
                self.assertEqual(bool(report["errors"]), bool(expected_code))


if __name__ == "__main__":
    unittest.main()
