#!/usr/bin/env python3
"""Summarize a Home Assistant state export, or GET an explicit instance only."""
import argparse
from collections import Counter
import json
import os
from pathlib import Path
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def summarize(states, include_entities=False):
    if not isinstance(states, list):
        raise ValueError("State input must be a JSON array")
    domains, unavailable, unknown, entities = Counter(), 0, 0, []
    for item in states:
        if not isinstance(item, dict):
            raise ValueError("Every state must be a JSON object")
        entity_id, state = item.get("entity_id"), item.get("state")
        if not isinstance(entity_id, str) or "." not in entity_id or not isinstance(state, str):
            raise ValueError("State objects need entity_id and string state fields")
        domains[entity_id.split(".", 1)[0]] += 1
        unavailable += state == "unavailable"
        unknown += state == "unknown"
        if include_entities:
            entities.append({"entity_id": entity_id, "state": state})
    result = {"entity_count": len(states), "domains": dict(sorted(domains.items())),
              "unavailable_count": unavailable, "unknown_count": unknown}
    if include_entities:
        result["entities"] = sorted(entities, key=lambda x: x["entity_id"])
    return result


def get_json(opener, base, token, endpoint):
    req = Request(base + endpoint, method="GET", headers={
        "Authorization": "Bearer " + token, "Accept": "application/json"})
    try:
        with opener.open(req, timeout=15) as response:
            # Bound response size; avoid accidental unbounded downloads.
            data = response.read(16 * 1024 * 1024 + 1)
        if len(data) > 16 * 1024 * 1024:
            raise ValueError("Response exceeds 16 MiB limit")
        return json.loads(data)
    except HTTPError as exc:
        raise ValueError("HTTP status " + str(exc.code) + " for " + endpoint) from None
    except (URLError, TimeoutError):
        raise ValueError("Connection failed for " + endpoint + "; check URL, TLS, and reachability") from None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--offline-states", type=Path)
    source.add_argument("--live", action="store_true")
    parser.add_argument("--include-entities", action="store_true")
    args = parser.parse_args()
    try:
        if args.offline_states:
            result = summarize(json.loads(args.offline_states.read_text(encoding="utf-8")),
                               args.include_entities)
            result["source"] = "offline_states"
        else:
            base = os.environ.get("HA_BASE_URL", "").rstrip("/")
            token = os.environ.get("HA_TOKEN", "")
            url = urlsplit(base)
            if url.scheme not in ("http", "https") or not url.hostname:
                raise ValueError("Set HA_BASE_URL to the verified http(s) instance URL")
            if url.username or url.password or url.query or url.fragment:
                raise ValueError("Base URL must not contain credentials, a query, or a fragment")
            if not token or any(c in token for c in "\r\n"):
                raise ValueError("Set HA_TOKEN securely; do not put it in the URL or arguments")
            opener = build_opener(NoRedirect())
            config = get_json(opener, base, token, "/api/config")
            states = get_json(opener, base, token, "/api/states")
            services = get_json(opener, base, token, "/api/services")
            if not isinstance(config, dict) or not isinstance(services, list):
                raise ValueError("Unexpected configuration or service-list response")
            result = summarize(states, args.include_entities)
            result.update(source="live_read_only", core_version=config.get("version"),
                          action_domains=len(services),
                          action_count=sum(len(x.get("services", {})) for x in services
                                           if isinstance(x, dict) and isinstance(x.get("services", {}), dict)))
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (ValueError, OSError) as exc:
        # Never include response bodies, URLs, headers, or token values in errors.
        print("Snapshot failed: " + str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
