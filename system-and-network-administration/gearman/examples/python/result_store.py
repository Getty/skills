"""Transactional local dedup/result example, NOT distributed exactly-once.

The demo counter and result commit in one SQLite transaction. External services
must provide their own idempotency/fencing; never put arbitrary HTTP calls here.
"""
from __future__ import annotations
import json
import sqlite3
from pathlib import Path
from typing import Any
from contract import ContractError, execute, fingerprint


class ResultStore:
    def __init__(self, path: str | Path):
        self.db = sqlite3.connect(path, timeout=5, isolation_level=None)
        self.db.execute("PRAGMA synchronous=FULL")
        self.db.executescript("""
            CREATE TABLE IF NOT EXISTS operations (
                request_id TEXT PRIMARY KEY, fingerprint TEXT NOT NULL,
                result_json TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS counters (
                name TEXT PRIMARY KEY, value INTEGER NOT NULL
            );
            INSERT OR IGNORE INTO counters VALUES ('completed_operations', 0);
        """)

    def close(self) -> None:
        self.db.close()

    def lookup(self, request_id: str) -> dict[str, Any] | None:
        row = self.db.execute("SELECT result_json FROM operations WHERE request_id=?",
                              (request_id,)).fetchone()
        return json.loads(row[0]) if row else None

    def apply(self, obj: dict[str, Any], *, fail_before_commit: bool = False,
              now_ms: int | None = None) -> dict[str, Any]:
        digest = fingerprint(obj)
        self.db.execute("BEGIN IMMEDIATE")
        try:
            row = self.db.execute("SELECT fingerprint, result_json FROM operations WHERE request_id=?",
                                  (obj["request_id"],)).fetchone()
            if row:
                if row[0] != digest:
                    raise ContractError("request_id reused with different business payload")
                result = json.loads(row[1])
            else:
                result = execute(obj, now_ms=now_ms)
                self.db.execute("UPDATE counters SET value=value+1 WHERE name='completed_operations'")
                self.db.execute("INSERT INTO operations VALUES (?, ?, ?)",
                                (obj["request_id"], digest, json.dumps(result, sort_keys=True)))
                if fail_before_commit:
                    raise RuntimeError("injected pre-commit failure")
            self.db.execute("COMMIT")
            return result
        except BaseException:
            self.db.execute("ROLLBACK")
            raise
