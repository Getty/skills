#!/usr/bin/env python3
"""Summarize an already downloaded TR-064 device or service description.

No network operations, router calls, credentials, or file writes are performed.
The input is capped at 4 MiB and XML DTDs/entities are rejected.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
import xml.etree.ElementTree as ET


MAX_XML_BYTES = 4 * 1024 * 1024


class NoDtdTreeBuilder(ET.TreeBuilder):
    def doctype(self, name: str, pubid: str | None, system: str | None) -> None:
        raise ValueError("DTD declarations are not allowed")


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def children(element: ET.Element, name: str) -> list[ET.Element]:
    return [child for child in element if local_name(child.tag) == name]


def child_text(element: ET.Element, name: str) -> str | None:
    matches = children(element, name)
    if not matches or matches[0].text is None:
        return None
    return matches[0].text.strip()


def read_xml(path: Path) -> ET.Element:
    with path.open("rb") as handle:
        data = handle.read(MAX_XML_BYTES + 1)
    if len(data) > MAX_XML_BYTES:
        raise ValueError("XML exceeds the 4 MiB input limit")
    # The parser callback also catches DTDs independent of XML encoding.
    normalized = data.replace(b"\x00", b"").upper()
    if b"<!DOCTYPE" in normalized or b"<!ENTITY" in normalized:
        raise ValueError("DTD/entity declarations are not allowed")
    parser = ET.XMLParser(target=NoDtdTreeBuilder())
    return ET.fromstring(data, parser=parser)


def inspect_device(root: ET.Element) -> dict:
    if local_name(root.tag) not in {"root", "device"}:
        raise ValueError("Expected a device description; try --kind scpd for a service")
    services = []
    models = set()
    for element in root.iter():
        if local_name(element.tag) == "modelName" and element.text:
            models.add(element.text.strip())
        if local_name(element.tag) == "service":
            services.append({
                field: child_text(element, field)
                for field in (
                    "serviceType", "serviceId", "controlURL", "eventSubURL", "SCPDURL"
                )
            })
    return {
        "kind": "device",
        "models": sorted(models),
        "services": services,
        "note": "URLs are reported as advertised; none were contacted or resolved.",
    }


def inspect_scpd(root: ET.Element) -> dict:
    if local_name(root.tag) != "scpd":
        raise ValueError("Expected an SCPD service description")
    state_variables = {}
    for element in root.iter():
        if local_name(element.tag) != "stateVariable":
            continue
        name = child_text(element, "name")
        if name:
            state_variables[name] = child_text(element, "dataType")
    actions = []
    for element in root.iter():
        if local_name(element.tag) != "action":
            continue
        arguments = []
        for arg_list in children(element, "argumentList"):
            for argument in children(arg_list, "argument"):
                variable = child_text(argument, "relatedStateVariable")
                arguments.append({
                    "name": child_text(argument, "name"),
                    "direction": child_text(argument, "direction"),
                    "relatedStateVariable": variable,
                    "dataType": state_variables.get(variable),
                })
        actions.append({"name": child_text(element, "name"), "arguments": arguments})
    return {"kind": "scpd", "actions": actions}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("xml_file", type=Path, help="Local XML file to inspect")
    parser.add_argument("--kind", choices=("device", "scpd"), default="device")
    args = parser.parse_args()
    try:
        root = read_xml(args.xml_file)
        result = inspect_device(root) if args.kind == "device" else inspect_scpd(root)
    except (OSError, ET.ParseError, ValueError) as error:
        print(f"Cannot inspect XML: {error}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
