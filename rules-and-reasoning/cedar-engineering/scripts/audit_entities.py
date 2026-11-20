#!/usr/bin/env python3
"""Audit explicit Cedar entity JSON graph structure; not a Cedar validator."""
import argparse
import json
import sys
from pathlib import Path


def unique_object(pairs):
    out = {}
    for key, value in pairs:
        if key in out:
            raise ValueError(f"duplicate JSON key: {key}")
        out[key] = value
    return out


def uid(value):
    if isinstance(value, dict) and set(value) == {"__entity"}:
        value = value["__entity"]
    if not isinstance(value, dict) or set(value) != {"type", "id"}:
        raise ValueError("UID must contain exactly type and id")
    if not all(isinstance(value[k], str) and value[k] for k in ("type", "id")):
        raise ValueError("UID type and id must be nonempty strings")
    return (value["type"], value["id"])


def audit(data, require_parents=False):
    if not isinstance(data, list):
        raise ValueError("entity collection must be a JSON array")
    graph = {}
    for index, entity in enumerate(data):
        if not isinstance(entity, dict):
            raise ValueError(f"entity {index} must be an object")
        key = uid(entity.get("uid"))
        if key in graph:
            raise ValueError(f"duplicate entity UID: {key}")
        if not isinstance(entity.get("attrs"), dict):
            raise ValueError(f"entity {index}: attrs must be an object")
        if not isinstance(entity.get("parents"), list):
            raise ValueError(f"entity {index}: parents must be an array")
        if "tags" in entity and not isinstance(entity["tags"], dict):
            raise ValueError(f"entity {index}: tags must be an object")
        graph[key] = [uid(parent) for parent in entity["parents"]]
    missing = sorted({p for ps in graph.values() for p in ps if p not in graph})
    if missing and require_parents:
        raise ValueError(f"parents absent from supplied closed snapshot: {missing}")
    # Iterative DFS avoids recursion limits on otherwise large graphs.
    color = {}
    for start in graph:
        if color.get(start) == 2:
            continue
        stack = [(start, False)]
        while stack:
            node, leaving = stack.pop()
            if leaving:
                color[node] = 2
                continue
            if color.get(node) == 1:
                raise ValueError(f"parent cycle involving UID: {node}")
            if color.get(node) == 2:
                continue
            color[node] = 1
            stack.append((node, True))
            for parent in reversed(graph.get(node, [])):
                if color.get(parent) == 1:
                    raise ValueError(f"parent cycle involving UID: {parent}")
                if parent in graph and color.get(parent) != 2:
                    stack.append((parent, False))
    return {
        "scope": "entity-json-graph-preflight-only",
        "entities": len(graph),
        "parent_edges": sum(map(len, graph.values())),
        "parents_absent_from_snapshot": [list(x) for x in missing],
        "schema_validated": False,
        "authorization_evaluated": False,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("entities", type=Path)
    parser.add_argument("--require-parents", action="store_true")
    args = parser.parse_args()
    try:
        data = json.loads(args.entities.read_text(), object_pairs_hook=unique_object,
                          parse_constant=lambda x: (_ for _ in ()).throw(ValueError(f"invalid JSON constant: {x}")))
        print(json.dumps(audit(data, args.require_parents), indent=2))
    except (ValueError, OSError) as exc:
        print(json.dumps({"error": str(exc), "scope": "entity-json-graph-preflight-only"}), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
