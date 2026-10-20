"""Strict, small cross-language sum.v1 contract; not a generic schema validator."""
from __future__ import annotations
import hashlib
import json
import re
import time
from typing import Any
MAX_BYTES = 65536
MAX_ITEMS = 1000
UUID = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$")


class ContractError(ValueError):
    pass


def _pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    obj: dict[str, Any] = {}
    for key, value in pairs:
        if key in obj:
            raise ContractError("duplicate JSON object key")
        obj[key] = value
    return obj


def parse(raw: bytes) -> dict[str, Any]:
    if len(raw) > MAX_BYTES:
        raise ContractError("request exceeds 64 KiB lab limit")
    try:
        obj = json.loads(raw.decode("utf-8"), object_pairs_hook=_pairs,
                         parse_constant=lambda value: (_ for _ in ()).throw(ContractError("non-finite number")))
    except (UnicodeError, ValueError, RecursionError) as error:
        raise ContractError("invalid JSON envelope") from error
    required = {"schema_version", "request_id", "operation", "payload"}
    optional = {"deadline_unix_ms"}
    if not isinstance(obj, dict) or not required <= obj.keys() or obj.keys() - required - optional:
        raise ContractError("incorrect envelope fields")
    if type(obj["schema_version"]) is not int or obj["schema_version"] != 1:
        raise ContractError("unsupported schema_version")
    if not isinstance(obj["request_id"], str) or not UUID.fullmatch(obj["request_id"]):
        raise ContractError("request_id must be a lowercase UUID-shaped string")
    if obj["operation"] != "sum.v1":
        raise ContractError("unsupported operation")
    payload = obj["payload"]
    if not isinstance(payload, dict) or set(payload) != {"numbers"}:
        raise ContractError("payload must contain only numbers")
    numbers = payload["numbers"]
    if not isinstance(numbers, list) or not 1 <= len(numbers) <= MAX_ITEMS:
        raise ContractError("numbers must contain 1..1000 integers")
    if any(type(n) is not int or abs(n) > 1_000_000_000 for n in numbers):
        raise ContractError("numbers must be JSON integers within +/-1000000000")
    if "deadline_unix_ms" in obj and (type(obj["deadline_unix_ms"]) is not int
                                    or not 0 <= obj["deadline_unix_ms"] <= 9_007_199_254_740_991):
        raise ContractError("invalid deadline_unix_ms")
    return obj


def fingerprint(obj: dict[str, Any]) -> str:
    business = {key: obj[key] for key in ("schema_version", "operation", "payload")}
    canonical = json.dumps(business, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()
    return hashlib.sha256(canonical).hexdigest()


def execute(obj: dict[str, Any], *, now_ms: int | None = None) -> dict[str, Any]:
    now_ms = int(time.time() * 1000) if now_ms is None else now_ms
    if obj.get("deadline_unix_ms", now_ms + 1) <= now_ms:
        raise ContractError("deadline expired before execution")
    return {"schema_version": 1, "request_id": obj["request_id"],
            "ok": True, "result": {"sum": sum(obj["payload"]["numbers"])}}


def encode(obj: dict[str, Any]) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")
