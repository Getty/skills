#!/usr/bin/env python3
"""Inventory UTF-8 DMN XML and selected structural checks; optionally validate XSD.
This is not a FEEL evaluator or a complete DMN semantic validator.
"""
import argparse
import json
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

LIMIT = 10 * 1024 * 1024
POLICIES = {"UNIQUE", "ANY", "PRIORITY", "FIRST", "COLLECT", "RULE ORDER", "OUTPUT ORDER"}
AGGREGATES = {"SUM", "MIN", "MAX", "COUNT"}


def inspect(path, schema_path=None):
    if path.stat().st_size > LIMIT:
        raise ValueError("model exceeds the 10 MiB helper limit")
    raw = path.read_bytes()
    source = raw.decode("utf-8-sig")
    if "<!DOCTYPE" in source.upper() or "<!ENTITY" in source.upper():
        raise ValueError("DTD/entity declarations are not accepted")
    root = ET.fromstring(source)
    if not root.tag.startswith("{") or root.tag.split("}", 1)[1] != "definitions":
        raise ValueError("expected a namespace-qualified definitions root")
    ns = root.tag[1:].split("}", 1)[0]
    if "/DMN/" not in ns or not ns.endswith("/MODEL/"):
        raise ValueError("root namespace is not a recognized DMN MODEL URI form")
    tag = lambda name: "{" + ns + "}" + name
    ids, errors, external = {}, [], []
    for node in root.iter():
        identifier = node.get("id")
        if identifier:
            if identifier in ids:
                errors.append("duplicate id: " + identifier)
            ids[identifier] = node
    for node in root.iter():
        href = node.get("href")
        if href is None:
            continue
        if href.startswith("#"):
            target = ids.get(href[1:])
            if target is None:
                errors.append("unresolved local reference: " + href)
            elif node.tag == tag("requiredInput") and target.tag != tag("inputData"):
                errors.append("requiredInput does not reference inputData: " + href)
            elif node.tag == tag("requiredDecision") and target.tag != tag("decision"):
                errors.append("requiredDecision does not reference decision: " + href)
        else:
            external.append(href)
    tables = []
    for table in root.iter(tag("decisionTable")):
        inputs, outputs = table.findall(tag("input")), table.findall(tag("output"))
        rules = table.findall(tag("rule"))
        policy, agg = table.get("hitPolicy", "UNIQUE"), table.get("aggregation")
        tid = table.get("id", "(unnamed table)")
        if policy not in POLICIES:
            errors.append(tid + ": unknown hitPolicy " + policy)
        if agg and (policy != "COLLECT" or agg not in AGGREGATES or len(outputs) != 1):
            errors.append(tid + ": aggregation requires COLLECT, a known aggregator, and one output")
        for rule in rules:
            rid = rule.get("id", "(unnamed rule)")
            if len(rule.findall(tag("inputEntry"))) != len(inputs):
                errors.append(rid + ": inputEntry count does not match table inputs")
            if len(rule.findall(tag("outputEntry"))) != len(outputs):
                errors.append(rid + ": outputEntry count does not match table outputs")
        tables.append({"id":tid,"hitPolicy":policy,"aggregation":agg,
                       "inputs":len(inputs),"outputs":len(outputs),"rules":len(rules)})
    graph = {}
    for decision in root.findall(tag("decision")):
        identifier = decision.get("id")
        if identifier:
            graph[identifier] = [r.get("href", "")[1:] for req in decision.findall(tag("informationRequirement"))
                                 for r in req.findall(tag("requiredDecision")) if r.get("href", "").startswith("#")]
    visiting, visited = set(), set()
    def visit(identifier):
        if identifier in visiting:
            errors.append("cycle in local decision information requirements at " + identifier)
            return
        if identifier in visited:
            return
        visiting.add(identifier)
        for child in graph.get(identifier, []):
            visit(child)
        visiting.remove(identifier)
        visited.add(identifier)
    for identifier in graph:
        visit(identifier)
    schema_result = "not-run"
    if schema_path:
        from lxml import etree
        parser = etree.XMLParser(resolve_entities=False, load_dtd=False, no_network=True)
        schema = etree.XMLSchema(etree.parse(str(schema_path), parser))
        document = etree.fromstring(raw, parser)
        if schema.validate(document):
            schema_result = "passed"
        else:
            schema_result = "failed"
            errors.extend("XSD: " + entry.message for entry in schema.error_log)
    return {"model":str(path),"modelNamespace":ns,"businessNamespace":root.get("namespace"),
            "decisions":[{"id":n.get("id"),"name":n.get("name")} for n in root.findall(tag("decision"))],
            "tables":tables,"externalReferencesNotResolved":sorted(set(external)),
            "xsd":schema_result,"errors":errors,
            "limits":"No FEEL evaluation, import resolution, complete semantic validation, or coverage proof."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("model", type=Path)
    parser.add_argument("--schema", type=Path, help="local complete official XSD set; requires lxml")
    args = parser.parse_args()
    try:
        result = inspect(args.model, args.schema)
    except ImportError:
        print(json.dumps({"error":"XSD validation requires lxml"}), file=sys.stderr)
        return 2
    except Exception as exc:
        print(json.dumps({"error":str(exc),"kind":type(exc).__name__}), file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    return 1 if result["errors"] else 0

if __name__ == "__main__":
    sys.exit(main())
