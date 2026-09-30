#!/usr/bin/env python3
"""Inventory Prometheus HELP/TYPE/sample NAMES, never sample labels or values."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
from urllib.request import Request
from urllib.error import HTTPError, URLError
from _common import api_key, http_opener, positive_float, validate_url, write_json

MAX_BYTES = 16 * 1024 * 1024
NAME = r"[a-zA-Z_:][a-zA-Z0-9_:]*"


def parse_metrics(text: str) -> dict:
    families: dict[str, dict] = {}
    names: set[str] = set()
    unparsed_lines = 0
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        m = re.match(rf"# (HELP|TYPE) ({NAME})\s+(.*)$", line)
        if m:
            kind, name, value = m.groups()
            entry = families.setdefault(name, {"name": name, "type": None, "help": None})
            entry["type" if kind == "TYPE" else "help"] = value
        elif line.startswith("#"):
            continue
        else:
            m = re.match(rf"({NAME})(?:\{{|\s)", line)
            if m:
                names.add(m.group(1))
            else:
                unparsed_lines += 1
    assigned = set()
    for name, family in families.items():
        kind = family["type"]
        candidates = {name}
        if kind == "counter":
            candidates |= {name + "_total", name + "_created"}
            if name.endswith("_total"):
                candidates.add(name[:-6] + "_created")
        elif kind in {"histogram", "summary"}:
            candidates |= {name + suffix for suffix in ("_bucket", "_count", "_sum", "_created")}
        family["sample_names"] = sorted(names & candidates)
        assigned |= names & candidates
    return {
        "families": [families[n] for n in sorted(families)],
        "untyped_or_unassigned_sample_names": sorted(names - assigned),
        "unparsed_noncomment_line_count": unparsed_lines,
        "notes": [
            "Only metric family metadata and sample names retained; no sample label values or measurements.",
            "Counter families may expose _total samples; inspect actual names, not just documentation headings.",
            "Missing metrics are unknown/unsupported/disabled, not zero.",
            "Legacy unquoted Prometheus metric-name grammar; newer quoted/unicode forms are reported as unparsed."
        ]
    }


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    group = p.add_mutually_exclusive_group(required=True)
    group.add_argument("--file", type=Path)
    group.add_argument("--url")
    p.add_argument("--out", type=Path)
    p.add_argument("--timeout", type=positive_float, default=10)
    p.add_argument("--allow-insecure-http", action="store_true")
    a = p.parse_args()
    try:
        if a.out and a.out.exists():
            raise ValueError("output exists; choose a fresh path")
        if a.file:
            with a.file.open("rb") as f:
                raw = f.read(MAX_BYTES + 1)
        else:
            url = validate_url(a.url, allow_insecure_http=a.allow_insecure_http)
            headers = {"Accept": "text/plain"}
            key = api_key()
            if key:
                headers["Authorization"] = "Bearer " + key
            with http_opener().open(Request(url, headers=headers), timeout=a.timeout) as r:
                raw = r.read(MAX_BYTES + 1)
        if len(raw) > MAX_BYTES:
            raise ValueError("scrape exceeds 16 MiB limit")
        result = parse_metrics(raw.decode("utf-8"))
        if a.out:
            write_json(a.out, result)
            print(f"Wrote {len(result['families'])} metric families to {a.out}")
        else:
            print(json.dumps(result, ensure_ascii=False, indent=2))
    except HTTPError as exc:
        code = exc.code
        exc.close()
        p.exit(1, f"HTTP {code}; response body not logged. Redirects are not followed.\n")
    except (OSError, URLError, ValueError, UnicodeError) as exc:
        # Avoid echoing URLs/secrets returned by a remote service.
        p.exit(1, f"Inventory failed ({type(exc).__name__}); check path, URL, auth and connectivity.\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
