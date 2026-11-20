#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Inventory a local RUML rulemap without executing expressions, resolving URIs, or invoking tools."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import json
import sys

from validate_schema import InputError, load_json


def inspect(document):
    if not isinstance(document, dict) or document.get("$format") != "RUML":
        raise InputError("expected a RUML object")
    rulemap = document.get("rulemap")
    if not isinstance(rulemap, dict) or not isinstance(rulemap.get("nodes"), dict):
        raise InputError("missing rulemap.nodes object; run JSON Schema validation first")
    nodes = rulemap["nodes"]
    root_caps = document.get("capabilities", [])
    if not isinstance(root_caps, list) or any(not isinstance(c, dict) for c in root_caps):
        raise InputError("capabilities must be an array of objects")
    declarations = [c.get("id") for c in root_caps]
    refs = Counter()
    uuids = defaultdict(list)
    operators = Counter()
    node_capabilities = Counter()
    missing_refs = []
    undeclared = []
    self_refs = []
    for lexid, node in nodes.items():
        if not isinstance(node, dict):
            raise InputError(f"node {lexid} is not an object")
        children = node.get("children", [])
        caps = node.get("capabilities", [])
        if not isinstance(children, list) or any(not isinstance(x, str) for x in children):
            raise InputError(f"node {lexid} has malformed children")
        if not isinstance(caps, list) or any(not isinstance(c, dict) or not isinstance(c.get("id"), str) for c in caps):
            raise InputError(f"node {lexid} has malformed capabilities")
        if isinstance(node.get("id"), str):
            uuids[node["id"]].append(lexid)
        if isinstance(node.get("operator"), str):
            operators[node["operator"]] += 1
        for child in children:
            refs[child] += 1
            if child not in nodes:
                missing_refs.append({"from": lexid, "to": child})
            if child == lexid:
                self_refs.append(lexid)
        for cap in caps:
            node_capabilities[cap["id"]] += 1
            if cap["id"] not in declarations:
                undeclared.append({"node": lexid, "capability": cap["id"]})
    reachable = set()
    pending = ["1"]
    while pending:
        lexid = pending.pop()
        if lexid in reachable or lexid not in nodes:
            continue
        reachable.add(lexid)
        pending.extend(nodes[lexid].get("children", []))
    metadata = document.get("metadata", {})
    if not isinstance(metadata, dict):
        raise InputError("metadata is not an object")
    reused = [{"lexId": key, "references": count, "modular": nodes[key].get("modular") is True}
              for key, count in sorted(refs.items()) if count > 1 and key in nodes]
    findings = {
        "missing_root": "1" not in nodes, "missing_child_targets": missing_refs,
        "duplicate_node_uuids": {uid: ids for uid, ids in uuids.items() if len(ids) > 1},
        "document_uuid_reused_by_nodes": uuids.get(metadata.get("id"), []),
        "undeclared_node_capabilities": undeclared,
        "multiple_references_without_modular": [r for r in reused if not r["modular"]],
    }
    return {
        "scope": "inventory and selected static checks only; run full semantic validation separately",
        "specVersion": document.get("$specVersion"),
        "document": {k: metadata.get(k) for k in ("id", "version", "status", "title")},
        "node_count": len(nodes), "edge_count": sum(refs.values()), "operators": dict(operators),
        "declared_capabilities": declarations,
        "explicitly_required_capabilities": [c.get("id") for c in root_caps if c.get("required") is True],
        "node_capability_counts": dict(node_capabilities), "reused_nodes": reused,
        "self_references": self_refs,
        "unreachable_nodes": sorted(set(nodes) - reachable),
        "selected_check_failures": findings,
        "limits": ["does not validate schema, JSONata syntax, time rules, profiles, context bindings, or hashes",
                   "does not classify cross-node cycles or decide recursion conformance",
                   "unreachable nodes and self-references are inventory, not automatic errors"],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file")
    args = parser.parse_args()
    try:
        report = inspect(load_json(args.file))
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return int(any(report["selected_check_failures"].values()))
    except (OSError, ValueError, TypeError) as exc:
        print(json.dumps({"error": str(exc), "scope": "inspection could not complete"}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
