#!/usr/bin/env python3
"""Offline package integrity checks. Rewriting hashes requires --write-manifest."""
from __future__ import annotations
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import sys
ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / 'MANIFEST.json'


def files() -> list[Path]:
    return sorted(p for p in ROOT.rglob('*') if p.is_file() and '__pycache__' not in p.parts
                  and p.suffix != '.pyc' and p != MANIFEST and '.git' not in p.parts)


def snapshot() -> dict:
    return {p.relative_to(ROOT).as_posix(): {'sha256': hashlib.sha256(p.read_bytes()).hexdigest(),
                                           'bytes': p.stat().st_size} for p in files()}


def check(*, hashes: bool = True) -> tuple[list[str], dict]:
    errors = []
    counts = {'files': 0, 'python': 0, 'json': 0, 'markdown_links': 0}
    for name in ('SKILL.md', 'references/INDEX.md', 'references/sources.md', 'VALIDATION.md',
                 'examples/README.md', 'scripts/run_lab.py', 'tests/test_wire.py'):
        if not (ROOT / name).is_file(): errors.append(f'missing required file: {name}')
    skill = (ROOT / 'SKILL.md').read_text()
    if not skill.startswith('---\n') or '\nname: gearman\n' not in skill:
        errors.append('invalid skill frontmatter/name')
    for p in files():
        counts['files'] += 1
        relative = p.relative_to(ROOT).as_posix()
        if p.is_symlink(): errors.append(f'symlink not allowed: {relative}')
        try:
            if p.suffix == '.py':
                ast.parse(p.read_text(), filename=relative); counts['python'] += 1
            elif p.suffix == '.json':
                json.loads(p.read_text()); counts['json'] += 1
            elif p.suffix == '.md':
                text = re.sub(r'```.*?```', '', p.read_text(), flags=re.S)
                for target in re.findall(r'\[[^\]\n]*\]\(([^)\s]+)\)', text):
                    if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', target) or target.startswith('#'):
                        continue
                    target = target.split('#', 1)[0]
                    resolved = (p.parent / target).resolve()
                    if not resolved.is_relative_to(ROOT) or not resolved.exists():
                        errors.append(f'broken/outside link: {relative} -> {target}')
                    counts['markdown_links'] += 1
        except (ValueError, SyntaxError, UnicodeError) as error:
            errors.append(f'{relative}: {error}')
    if hashes:
        if not MANIFEST.exists():
            errors.append('MANIFEST.json missing; deliberate creation requires --write-manifest')
        else:
            try:
                expected = json.loads(MANIFEST.read_text())['files']
                actual = snapshot()
                for name in sorted(set(expected) | set(actual)):
                    if expected.get(name) != actual.get(name): errors.append(f'manifest mismatch: {name}')
            except (ValueError, KeyError, TypeError) as error:
                errors.append(f'invalid manifest: {error}')
    return errors, counts


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write-manifest', action='store_true', help='explicitly replace file hashes after intentional edits')
    parser.add_argument('--skip-hashes', action='store_true', help='structure check only; not an integrity assertion')
    args = parser.parse_args()
    if args.write_manifest:
        errors, counts = check(hashes=False)
        if errors:
            print(json.dumps({'ok': False, 'errors': errors}, indent=2)); return 1
        MANIFEST.write_text(json.dumps({'format_version': 1, 'package': 'gearman', 'package_version': '1.0.0',
            'evidence_date': '2026-10-14', 'server_source_baseline': 'gearmand 2.1.0',
            'hash_algorithm': 'sha256', 'note': 'Manifest excludes itself, .git and Python bytecode caches.',
            'files': snapshot()}, indent=2, sort_keys=True) + '\n')
    errors, counts = check(hashes=not args.skip_hashes)
    print(json.dumps({'ok': not errors, 'hashes_checked': not args.skip_hashes,
                      'counts': counts, 'errors': errors}, indent=2))
    return 1 if errors else 0

if __name__ == '__main__':
    raise SystemExit(main())
