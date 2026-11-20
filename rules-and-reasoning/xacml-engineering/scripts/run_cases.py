#!/usr/bin/env python3
"""Execute original XACML fixtures with a supplied trusted AuthzForce CLI jar."""
import argparse
import json
from pathlib import Path
import subprocess
import sys

BASE = Path(__file__).resolve().parents[1] / "assets" / "examples"
NS = {"x": "urn:oasis:names:tc:xacml:3.0:core:schema:wd-17"}

def response(raw, format_name):
    if format_name == "XACML_JSON":
        envelope = json.loads(raw)
        results = envelope.get("Response")
        if not isinstance(results, list) or len(results) != 1:
            raise ValueError("Expected exactly one JSON result")
        item = results[0]
        return item.get("Decision"), sorted(x["Id"] for x in item.get("Obligations", []))
    from lxml import etree as ET
    parser = ET.XMLParser(resolve_entities=False, no_network=True, load_dtd=False)
    doc = ET.fromstring(raw.encode("utf-8"), parser)
    if doc.getroottree().docinfo.doctype:
        raise ValueError("Unexpected DTD in response")
    results = doc.findall("x:Result", NS)
    if len(results) != 1:
        raise ValueError("Expected exactly one XML result")
    item = results[0]
    return (item.findtext("x:Decision", namespaces=NS),
            sorted(x.get("ObligationId") for x in item.findall("x:Obligations/x:Obligation", NS)))

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--jar", type=Path, required=True)
    ap.add_argument("--java", default="java")
    ap.add_argument("--cases", type=Path, default=BASE / "cases.json")
    ap.add_argument("--config", type=Path, default=BASE / "authzforce-pdp.xml")
    ap.add_argument("--timeout", type=float, default=20)
    args = ap.parse_args()
    if args.timeout <= 0:
        ap.error("timeout must be positive")
    try:
        if not args.jar.is_file():
            raise ValueError("trusted local jar not found")
        cases = json.loads(args.cases.read_text())
        if not isinstance(cases, list) or not cases:
            raise ValueError("expected nonempty case list")
        passed, failures = 0, []
        for case in cases:
            try:
                kind = case["format"]
                if kind not in {"XACML_XML", "XACML_JSON"}:
                    raise ValueError("unsupported request format")
                request = (args.cases.parent / case["request"]).resolve()
                cmd = [args.java, "-jar", str(args.jar.resolve()), "-p", "-t", kind,
                       str(args.config.resolve()), str(request)]
                proc = subprocess.run(cmd, capture_output=True, text=True,
                                      timeout=args.timeout, check=False)
                if proc.returncode:
                    raise ValueError("CLI failed: " + proc.stderr[-1500:])
                decision, obligations = response(proc.stdout, kind)
                if decision != case["expectedDecision"]:
                    raise ValueError("decision " + repr(decision) + " != " +
                                     repr(case["expectedDecision"]))
                if obligations != sorted(case.get("expectedObligations", [])):
                    raise ValueError("unexpected obligation IDs: " + repr(obligations))
                passed += 1
            except Exception as exc:
                failures.append({"id": case.get("id"), "error": str(exc)})
        print(json.dumps({"total": len(cases), "passed": passed, "failed": len(failures),
                          "failures": failures, "obligations_executed": False}, indent=2))
        return 1 if failures else 0
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(json.dumps({"error": str(exc)}))
        return 2

if __name__ == "__main__":
    sys.exit(main())
