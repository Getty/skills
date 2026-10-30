# Offline examples and evidence contract

## Purpose and limits

The bundled helpers reject malformed or mechanically unsupported records and score output against a known fixture. They need Python 3.10+ and the standard library, fetch nothing, and call no model. All catalog data is synthetic.

Run from this skill directory:

```bash
python scripts/validate_evidence.py assets/fixtures/records.valid.jsonl --snapshots-dir assets/fixtures
python scripts/evaluate_records.py assets/fixtures/records.valid.jsonl --gold assets/fixtures/gold.json
python -m unittest discover -s scripts/tests -v
```

The validator checks its fixed versioned contract, not arbitrary JSON Schemas. The evaluator scores against the supplied gold universe; it says nothing about website completeness or about the extraction quality of an LLM, hosted service, or browser tool.

## Record structure

One object per JSONL line with `schema_version`, `record_id`, `source`, and `fields`. `assets/record.schema.json` is the structural companion for a Draft 2020-12 validator (enable format checks explicitly); the Python helper does not load it but additionally checks evidence, hashes, paths, and normalization.

`source` holds URL, offset-aware fetch timestamp (`YYYY-MM-DDTHH:MM:SS`, optional fractional seconds, required `Z` or `±HH:MM`), `snapshot_ref`, SHA-256 of the exact snapshot bytes, and a nonempty `record_span`. A snapshot is a UTF-8 text file; offsets count Python Unicode code points, start inclusive, end exclusive. Preserve decoded text exactly, line endings included. In a real pipeline, also keep the original response and transformation manifest when the snapshot came from HTML.

Each field has a status, scalar value, normalization name, evidence array, and optional note. Non-observed states require a note and null value and normalization. The general state semantics are in [extraction contracts](extraction-contracts.md); the demo enforces:

| Status | Value | Evidence |
| --- | --- | --- |
| `observed` | String, integer, or boolean | At least one exact source span |
| `absent` | Null | Empty; means not found in this available region |
| `explicit_null` | Null | Source indication of null; at least one span |
| `unparseable` | Null | Text exists but cannot be normalized; at least one span |
| `conflict` | Null | At least two distinct quoted candidates |

Spans must match the snapshot and lie inside the record region. The first observed quote is the exact lexical input to normalization; further spans add context. Arrays, nested objects, dates, quantities, and units are unsupported; extend a production contract deliberately.

## Normalizers

| Name | Expected relationship |
| --- | --- |
| `exact` | String equals the first quote |
| `whitespace` | String equals the first quote with whitespace collapsed |
| `decimal_dot` | Strict dot-decimal lexeme and string value represent the same finite decimal |
| `integer` | Integer lexeme produces a true integer; booleans are excluded |
| `boolean_literal` | Literal true/false produces a boolean |

Money is a decimal string, never a binary float. `decimal_dot` infers no currency, decimal comma, thousands separator, range, tax, or discount; keep currency and context as separate fields and add locale-aware normalization explicitly.

## Interpret validation correctly

The validator rejects malformed JSON, duplicate keys, nonfinite numbers, structural and type errors, invalid states, bad snapshot hashes, unsafe snapshot paths, mismatching or out-of-region quotes, inconsistent normalizers, and duplicate record IDs.

Passing proves only those checks: not that the source is truthful, that the URL and timestamp produced the file, that the declared region is the right entity, or that an `explicit_null` or `absent` judgment is correct. Trusted acquisition code must bind source metadata and entity boundaries; a model that writes both metadata and data defeats the check. Whether a quoted number is the active price needs labeled examples and domain checks. Keep inference out of observed fields.

## Evaluate against gold

The gold file defines entity IDs and field status/value pairs. The evaluator compares exact typed values (false ≠ zero) and reports entity precision/recall, observed-value precision/recall, and field-state accuracy with explicit denominators. Missing entities lower recall and state accuracy; unknown entities and extra observed fields lower precision; an undefined denominator yields null.

Run evidence validation and gold evaluation as separate gates and report both: valid evidence can carry a wrong value, a right value can have a broken pointer. Add representative gold examples before extending the contract, and never derive expected values from the extractor under test.
