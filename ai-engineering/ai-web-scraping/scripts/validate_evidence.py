#!/usr/bin/env python3
"""Validate the deliberately narrow offline evidence contract (Python 3.10+).

Offsets count Unicode code points in the exact decoded UTF-8 snapshot, including
CR and LF separately. Hashes cover the original bytes. This checks consistency,
not source authenticity, semantic field ownership, factual truth, or coverage.
Acquisition code must attach trusted source metadata. No network access occurs.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sys
from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path, PurePosixPath
from typing import Any
from urllib.parse import urlsplit


MAX_FILE_BYTES = 8 * 1024 * 1024
MAX_LINE_BYTES = 1024 * 1024
MAX_SNAPSHOT_BYTES = 16 * 1024 * 1024
MAX_RECORDS = 10_000
MAX_NUMERIC_CHARS = 512
MAX_JSON_DEPTH = 64
MAX_FIELDS = 512
MAX_EVIDENCE_ITEMS = 128
STATUSES = {"observed", "absent", "explicit_null", "unparseable", "conflict"}
NORMALIZATIONS = {"exact", "whitespace", "decimal_dot", "integer", "boolean_literal"}
INTEGER_RE = re.compile(r"-?(?:0|[1-9][0-9]*)\Z")
DECIMAL_RE = re.compile(r"-?(?:0|[1-9][0-9]*)(?:\.[0-9]+)?\Z")
HASH_RE = re.compile(r"[0-9a-f]{64}\Z")
TIMESTAMP_RE = re.compile(
    r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-5][0-9]:[0-5][0-9]"
    r"(?:\.[0-9]+)?(?:Z|[+-](?:[01][0-9]|2[0-3]):[0-5][0-9])\Z"
)


class ContractError(ValueError):
    """Malformed, oversized, or unsupported offline input."""


def _object_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ContractError("duplicate JSON object key")
        result[key] = value
    return result


def _integer_token(token: str) -> int:
    if len(token) > MAX_NUMERIC_CHARS:
        raise ContractError("JSON integer exceeds numeric length cap")
    return int(token)


def _float_token(token: str) -> float:
    if len(token) > MAX_NUMERIC_CHARS:
        raise ContractError("JSON number exceeds numeric length cap")
    value = float(token)
    if not math.isfinite(value):
        raise ContractError("nonfinite JSON number or numeric overflow")
    return value


def _reject_constant(_token: str) -> Any:
    raise ContractError("nonfinite JSON number")


def strict_loads(text: str) -> Any:
    """Decode strict JSON; reject duplicates, nonfinite numbers and deep input."""
    if not isinstance(text, str):
        raise ContractError("JSON input must be text")
    try:
        value = json.loads(
            text,
            object_pairs_hook=_object_pairs,
            parse_int=_integer_token,
            parse_float=_float_token,
            parse_constant=_reject_constant,
        )
    except json.JSONDecodeError as exc:
        raise ContractError(
            f"invalid JSON at line {exc.lineno}, column {exc.colno}"
        ) from exc
    except (RecursionError, OverflowError) as exc:
        raise ContractError("JSON nesting or numeric limit exceeded") from exc
    pending = [(value, 0)]
    while pending:
        item, depth = pending.pop()
        if depth > MAX_JSON_DEPTH:
            raise ContractError("JSON nesting exceeds depth cap")
        if isinstance(item, dict):
            pending.extend((key, depth + 1) for key in item)
            pending.extend((child, depth + 1) for child in item.values())
        elif isinstance(item, list):
            pending.extend((child, depth + 1) for child in item)
        elif isinstance(item, str):
            if any(0xD800 <= ord(char) <= 0xDFFF for char in item):
                raise ContractError("JSON contains an unpaired Unicode surrogate")
    return value


def load_records(path: str | Path, *, allow_empty: bool = False) -> list[dict[str, Any]]:
    """Read bounded UTF-8 JSONL objects; schema and duplicate IDs are separate."""
    records: list[dict[str, Any]] = []
    try:
        with Path(path).open("rb") as stream:
            if Path(path).stat().st_size > MAX_FILE_BYTES:
                raise ContractError("records file exceeds byte cap")
            total = 0
            line_number = 0
            while True:
                line = stream.readline(MAX_LINE_BYTES + 1)
                if not line:
                    break
                line_number += 1
                total += len(line)
                if total > MAX_FILE_BYTES:
                    raise ContractError("records file exceeds byte cap")
                if len(line) > MAX_LINE_BYTES:
                    raise ContractError(f"line {line_number}: exceeds line byte cap")
                try:
                    text = line.decode("utf-8")
                except UnicodeDecodeError as exc:
                    raise ContractError(f"line {line_number}: invalid UTF-8") from exc
                if not text.strip():
                    continue
                try:
                    record = strict_loads(text)
                except ValueError as exc:
                    raise ContractError(f"line {line_number}: {exc}") from exc
                if not isinstance(record, dict):
                    raise ContractError(f"line {line_number}: record must be an object")
                records.append(record)
                if len(records) > MAX_RECORDS:
                    raise ContractError("records file exceeds record count cap")
    except OSError as exc:
        raise ContractError(f"cannot read records file: {exc.strerror or type(exc).__name__}") from exc
    if not records and not allow_empty:
        raise ContractError("records file contains no records")
    return records


def _keys(
    item: Any, required: set[str], optional: set[str], label: str, errors: list[str]
) -> bool:
    if not isinstance(item, dict):
        errors.append(f"{label}: must be an object")
        return False
    if any(not isinstance(key, str) for key in item):
        errors.append(f"{label}: keys must be strings")
        return False
    missing = required - item.keys()
    extra = item.keys() - required - optional
    if missing:
        errors.append(f"{label}: missing keys {', '.join(sorted(missing))}")
    if extra:
        errors.append(f"{label}: unexpected keys")
    return not missing and not extra


def _is_int(value: Any) -> bool:
    return type(value) is int


def _span(value: Any, label: str, errors: list[str]) -> tuple[int, int] | None:
    if not _keys(value, {"start", "end"}, set(), label, errors):
        return None
    start, end = value["start"], value["end"]
    if not _is_int(start) or not _is_int(end) or start < 0 or end <= start:
        errors.append(f"{label}: require integer bounds 0 <= start < end")
        return None
    return start, end


def _safe_ref(ref: Any) -> bool:
    if not isinstance(ref, str) or not ref or len(ref) > 1024:
        return False
    if "\\" in ref or "\x00" in ref or re.match(r"^[A-Za-z]:", ref):
        return False
    parts = ref.split("/")
    return (
        not PurePosixPath(ref).is_absolute()
        and all(part not in {"", ".", ".."} for part in parts)
    )


def _valid_url(value: Any) -> bool:
    if not isinstance(value, str) or not value:
        return False
    if any(char.isspace() or ord(char) < 32 or ord(char) == 127 for char in value):
        return False
    try:
        parsed = urlsplit(value)
        _ = parsed.port
        return (
            parsed.scheme in {"http", "https"}
            and bool(parsed.hostname)
            and parsed.username is None
            and parsed.password is None
            and "@" not in parsed.netloc
        )
    except ValueError:
        return False


def _valid_timestamp(value: Any) -> bool:
    if not isinstance(value, str) or not TIMESTAMP_RE.fullmatch(value):
        return False
    try:
        parsed = datetime.fromisoformat(value[:-1] + "+00:00" if value.endswith("Z") else value)
        return parsed.tzinfo is not None and parsed.utcoffset() is not None
    except ValueError:
        return False


def _normalization_error(kind: str, quote: str, value: Any) -> str | None:
    if kind == "exact":
        if not isinstance(value, str) or value != quote:
            return "exact requires the first quote as an equal string value"
    elif kind == "whitespace":
        if not isinstance(value, str) or value != " ".join(quote.split()):
            return "whitespace requires the first quote with collapsed whitespace"
    elif kind == "integer":
        if len(quote) > MAX_NUMERIC_CHARS or not INTEGER_RE.fullmatch(quote):
            return "integer requires a strict base-10 integer quote"
        if not _is_int(value) or value != int(quote):
            return "integer requires the matching integer value (not Boolean)"
    elif kind == "decimal_dot":
        if (
            not isinstance(value, str)
            or len(quote) > MAX_NUMERIC_CHARS
            or len(value) > MAX_NUMERIC_CHARS
            or not DECIMAL_RE.fullmatch(quote)
            or not DECIMAL_RE.fullmatch(value)
        ):
            return "decimal_dot requires strict dot-decimal quote and string value"
        try:
            if Decimal(quote) != Decimal(value):
                return "decimal_dot value differs numerically from first quote"
        except InvalidOperation:
            return "decimal_dot could not be parsed"
    elif kind == "boolean_literal":
        if quote.lower() not in {"true", "false"}:
            return "boolean_literal requires a true/false quote"
        if type(value) is not bool or value is not (quote.lower() == "true"):
            return "boolean_literal requires the matching Boolean value"
    return None


def validate_record_structure(rec: Any) -> list[str]:
    """Validate contract structure and claimed normalization without file reads."""
    errors: list[str] = []
    if not _keys(rec, {"schema_version", "record_id", "source", "fields"}, set(), "record", errors):
        return errors
    if rec["schema_version"] != "1.0":
        errors.append("schema_version: must equal '1.0'")
    if not isinstance(rec["record_id"], str) or not rec["record_id"].strip():
        errors.append("record_id: must be a nonempty string")
    source = rec["source"]
    source_keys = {"url", "fetched_at", "snapshot_ref", "snapshot_sha256", "record_span"}
    record_span = None
    if _keys(source, source_keys, set(), "source", errors):
        if not _valid_url(source["url"]):
            errors.append("source.url: require http/https URL with host and no userinfo")
        if not _valid_timestamp(source["fetched_at"]):
            errors.append("source.fetched_at: require offset-aware ISO datetime")
        if not _safe_ref(source["snapshot_ref"]):
            errors.append("source.snapshot_ref: require safe relative POSIX path")
        digest = source["snapshot_sha256"]
        if not isinstance(digest, str) or not HASH_RE.fullmatch(digest):
            errors.append("source.snapshot_sha256: require lowercase SHA-256 hex")
        record_span = _span(source["record_span"], "source.record_span", errors)
    fields = rec["fields"]
    if not isinstance(fields, dict) or not fields:
        errors.append("fields: require a nonempty object")
        return errors
    if len(fields) > MAX_FIELDS:
        errors.append("fields: exceeds field count cap")
        return errors
    for index, (name, field) in enumerate(fields.items(), 1):
        label = f"field {index}"
        if not isinstance(name, str) or not name.strip():
            errors.append(f"{label}: name must be a nonempty string")
        if not _keys(field, {"status", "value", "normalization", "evidence"}, {"note"}, label, errors):
            continue
        status, value, normalization = field["status"], field["value"], field["normalization"]
        if not isinstance(status, str) or status not in STATUSES:
            errors.append(f"{label}: unsupported status")
            continue
        if "note" in field and (
            not isinstance(field["note"], str) or not field["note"].strip()
        ):
            errors.append(f"{label}: note must be a nonempty string")
        evidence = field["evidence"]
        if not isinstance(evidence, list) or len(evidence) > MAX_EVIDENCE_ITEMS:
            errors.append(f"{label}: evidence must be a bounded list")
            continue
        valid_quotes: list[str] = []
        for evidence_index, item in enumerate(evidence, 1):
            evidence_label = f"{label} evidence {evidence_index}"
            if not _keys(item, {"start", "end", "quote"}, set(), evidence_label, errors):
                continue
            span = _span({"start": item["start"], "end": item["end"]}, evidence_label, errors)
            quote = item["quote"]
            if not isinstance(quote, str) or not quote:
                errors.append(f"{evidence_label}: quote must be a nonempty string")
                continue
            valid_quotes.append(quote)
            if span:
                if span[1] - span[0] != len(quote):
                    errors.append(f"{evidence_label}: quote length differs from code-point span")
                if record_span and not (record_span[0] <= span[0] <= span[1] <= record_span[1]):
                    errors.append(f"{evidence_label}: span lies outside record_span")
        if status == "observed":
            if type(value) not in {str, int, bool}:
                errors.append(f"{label}: observed value must be string, integer, or Boolean")
            if not isinstance(normalization, str) or normalization not in NORMALIZATIONS:
                errors.append(f"{label}: unsupported observed normalization")
            elif evidence and isinstance(evidence[0], dict) and isinstance(evidence[0].get("quote"), str):
                problem = _normalization_error(normalization, evidence[0]["quote"], value)
                if problem:
                    errors.append(f"{label}: {problem}")
            if not evidence:
                errors.append(f"{label}: observed requires evidence")
        else:
            if value is not None or normalization is not None:
                errors.append(f"{label}: non-observed value and normalization must be null")
            if not isinstance(field.get("note"), str) or not field["note"].strip():
                errors.append(f"{label}: non-observed status requires a nonempty note")
            if status == "absent" and evidence:
                errors.append(f"{label}: absent requires empty evidence")
            if status in {"explicit_null", "unparseable"} and not evidence:
                errors.append(f"{label}: {status} requires evidence")
            if status == "conflict" and len(set(valid_quotes)) < 2:
                errors.append(f"{label}: conflict requires two distinct evidence quotes")
    return errors


class SnapshotStore:
    """Read bounded immutable UTF-8 fixtures with resolved-path confinement.

    Retain only the most recently read snapshot, bounded by MAX_SNAPSHOT_BYTES.
    Fixture directories must not be changed concurrently by untrusted processes;
    this portable offline helper is not a hardened multi-tenant filesystem server.
    """

    def __init__(self, snapshots_dir: str | Path):
        try:
            self.root = Path(snapshots_dir).resolve(strict=True)
        except (OSError, RuntimeError) as exc:
            raise ContractError("snapshot directory is unavailable") from exc
        if not self.root.is_dir():
            raise ContractError("snapshots-dir is not a directory")
        self._cache: dict[Path, tuple[str, str]] = {}

    def read(self, snapshot_ref: str) -> tuple[str, str]:
        if not _safe_ref(snapshot_ref):
            raise ContractError("snapshot_ref is not a safe relative path")
        try:
            path = (self.root / snapshot_ref).resolve(strict=True)
            path.relative_to(self.root)
        except (OSError, ValueError, RuntimeError) as exc:
            raise ContractError("snapshot path is missing or escapes snapshots-dir") from exc
        if not path.is_file():
            raise ContractError("snapshot path is not a regular file")
        if path in self._cache:
            return self._cache[path]
        try:
            with path.open("rb") as stream:
                raw = stream.read(MAX_SNAPSHOT_BYTES + 1)
        except OSError as exc:
            raise ContractError("snapshot cannot be read") from exc
        if len(raw) > MAX_SNAPSHOT_BYTES:
            raise ContractError("snapshot exceeds byte cap")
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ContractError("snapshot is not valid UTF-8") from exc
        result = text, hashlib.sha256(raw).hexdigest()
        self._cache.clear()
        self._cache[path] = result
        return result


def validate_record(rec: Any, snapshots_dir: str | Path | SnapshotStore) -> list[str]:
    """Return validation errors; no errors means this narrow contract is valid."""
    errors = validate_record_structure(rec)
    if errors:
        return errors
    try:
        store = snapshots_dir if isinstance(snapshots_dir, SnapshotStore) else SnapshotStore(snapshots_dir)
        text, digest = store.read(rec["source"]["snapshot_ref"])
    except (ValueError, OSError, RuntimeError) as exc:
        return [f"snapshot: {exc}"]
    source = rec["source"]
    if source["snapshot_sha256"] != digest:
        errors.append("source.snapshot_sha256: does not match snapshot bytes")
    if source["record_span"]["end"] > len(text):
        errors.append("source.record_span: exceeds snapshot code-point length")
    for index, field in enumerate(rec["fields"].values(), 1):
        for evidence_index, evidence in enumerate(field["evidence"], 1):
            start, end = evidence["start"], evidence["end"]
            if end > len(text) or text[start:end] != evidence["quote"]:
                errors.append(f"field {index} evidence {evidence_index}: quote does not match snapshot slice")
    return errors


def validate_records_file(records_path: str | Path, snapshots_dir: str | Path) -> dict[str, Any]:
    """Validate a JSONL file, treating every occurrence of a duplicate ID as invalid."""
    try:
        records = load_records(records_path)
        store = SnapshotStore(snapshots_dir)
    except (ValueError, OSError) as exc:
        return {
            "records_total": 0, "records_valid": 0, "records_invalid": 0,
            "errors": [{"record_index": None, "errors": [str(exc)]}],
        }
    counts: dict[str, int] = {}
    for rec in records:
        record_id = rec.get("record_id")
        if isinstance(record_id, str):
            counts[record_id] = counts.get(record_id, 0) + 1
    failures = []
    for index, rec in enumerate(records, 1):
        errors = validate_record(rec, store)
        record_id = rec.get("record_id")
        if isinstance(record_id, str) and counts.get(record_id, 0) > 1:
            errors.append("record_id: duplicate across records file")
        if errors:
            failures.append({"record_index": index, "errors": errors})
    return {
        "records_total": len(records),
        "records_valid": len(records) - len(failures),
        "records_invalid": len(failures),
        "errors": failures,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("records", type=Path, help="UTF-8 JSONL candidate records")
    parser.add_argument("--snapshots-dir", required=True, type=Path)
    args = parser.parse_args(argv)
    report = validate_records_file(args.records, args.snapshots_dir)
    print(json.dumps(report, ensure_ascii=False, allow_nan=False, indent=2))
    return 1 if report["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
