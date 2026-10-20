#!/usr/bin/env python3
"""Find catalog routing entries without network access or modifying a project."""
import argparse
import json
from pathlib import Path

def lookup(term: str, catalog: list[dict]) -> list[dict]:
    term=term.strip().casefold()
    if not term: raise ValueError('Supply a nonempty search term')
    return [entry for entry in catalog if term in ' '.join([entry['name'],entry['category'],*entry['packages']]).casefold()]

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('term')
    args=parser.parse_args()
    try:
        catalog=json.loads((Path(__file__).resolve().parents[1]/'assets/library-catalog.json').read_text())
        result=lookup(args.term,catalog)
    except (ValueError,OSError) as error: parser.error(str(error))
    print(json.dumps(result,indent=2))
if __name__=='__main__': main()
