#!/usr/bin/env python3
"""Inventory XACML XML and optionally validate caller-supplied local schemas."""
import argparse
from collections import Counter
import json
from pathlib import Path
import sys

NS = "urn:oasis:names:tc:xacml:3.0:core:schema:wd-17"
ROOTS = {"Policy", "PolicySet", "Request", "Response"}

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("artifact", type=Path)
    ap.add_argument("--xsd", type=Path)
    ap.add_argument("--xml-xsd", type=Path)
    ap.add_argument("--max-bytes", type=int, default=2 * 1024 * 1024)
    args = ap.parse_args()
    if args.max_bytes < 1:
        ap.error("max-bytes must be positive")
    if bool(args.xsd) != bool(args.xml_xsd):
        ap.error("--xsd and --xml-xsd must be supplied together")
    try:
        from lxml import etree as ET
    except ImportError:
        print(json.dumps({"accepted": False, "error": "Requires Python package lxml"}))
        return 2
    try:
        with args.artifact.open("rb") as stream:
            raw = stream.read(args.max_bytes + 1)
        if len(raw) > args.max_bytes:
            raise ValueError("byte limit exceeded")
        parser = ET.XMLParser(resolve_entities=False, no_network=True,
                              load_dtd=False, huge_tree=False)
        doc = ET.fromstring(raw, parser)
        if doc.getroottree().docinfo.doctype:
            raise ValueError("DTD declarations are outside this input profile")
        root = ET.QName(doc)
        if root.namespace != NS or root.localname not in ROOTS:
            raise ValueError("Expected an XACML 3.0 Policy, PolicySet, Request, or Response")
        schema_valid = None
        if args.xsd:
            schema_path = args.xsd.resolve()
            xml_path = args.xml_xsd.resolve()
            class LocalResolver(ET.Resolver):
                def resolve(self, url, public_id, context):
                    if url in {"http://www.w3.org/2001/xml.xsd",
                               "https://www.w3.org/2001/xml.xsd"}:
                        return self.resolve_filename(str(xml_path), context)
                    raise OSError("Unmapped schema dependency: " + url)
            sp = ET.XMLParser(resolve_entities=False, no_network=True, load_dtd=False)
            sp.resolvers.add(LocalResolver())
            sd = ET.fromstring(schema_path.read_bytes(), sp, base_url=str(schema_path))
            if sd.getroottree().docinfo.doctype:
                raise ValueError("DTD in supplied schema")
            ET.XMLSchema(sd).assertValid(doc)
            schema_valid = True
        tags = Counter(ET.QName(node).localname for node in doc.iter()
                       if isinstance(node.tag, str))
        algorithms = set()
        functions = set()
        ids = []
        attributes = []
        for node in doc.iter():
            if not isinstance(node.tag, str):
                continue
            for key in ("RuleCombiningAlgId", "PolicyCombiningAlgId"):
                if node.get(key):
                    algorithms.add(node.get(key))
            for key in ("FunctionId", "MatchId"):
                if node.get(key):
                    functions.add(node.get(key))
            for key in ("PolicyId", "PolicySetId", "RuleId"):
                if node.get(key):
                    ids.append({"kind": key, "value": node.get(key)})
            if ET.QName(node).localname == "AttributeDesignator":
                attributes.append(dict(node.attrib))
        print(json.dumps({"accepted": True, "root": root.localname,
                          "schema_valid": schema_valid, "elements": dict(sorted(tags.items())),
                          "identifiers": ids, "algorithms": sorted(algorithms),
                          "functions": sorted(functions), "designators": attributes,
                          "limitations": ["no policy evaluation", "no profile conformance proof",
                                          "no trust or enforcement validation"]}, indent=2))
        return 0
    except (OSError, ValueError, ET.Error) as exc:
        print(json.dumps({"accepted": False, "error": str(exc)}))
        return 2

if __name__ == "__main__":
    sys.exit(main())
