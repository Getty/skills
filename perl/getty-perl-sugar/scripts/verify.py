#!/usr/bin/env python3
"""Verify the bundle locally. Never install dependencies or contact external services."""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / 'examples/reference'

def package_checks(update_manifest: bool = False) -> None:
    skill = (ROOT/'SKILL.md').read_text(encoding='utf-8')
    if not re.match(r'\A---\nname: getty-perl-sugar\ndescription: .+\n---\n', skill):
        raise ValueError('Invalid skill front matter')
    if len(skill.split()) > 650:
        raise ValueError('SKILL.md exceeds the 650-word entry-point budget')
    references = list((ROOT/'references').glob('*.md'))
    if len(references) != 20:
        raise ValueError(f'Expected 20 reference files, found {len(references)}')
    links = 0
    for path in ROOT.rglob('*'):
        if path.is_symlink():
            raise ValueError(f'Symlink not allowed in bundle: {path}')
        if path.is_file() and path.suffix == '.md':
            text = path.read_text(encoding='utf-8')
            if text.count('```') % 2:
                raise ValueError(f'Unbalanced fenced code block: {path}')
            for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', text):
                if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', target):
                    continue
                filepart = target.split('#', 1)[0]
                destination = (path.parent/filepart).resolve() if filepart else path
                if not destination.is_relative_to(ROOT):
                    raise ValueError(f'Local link escapes bundle: {path}: {target}')
                if not destination.exists():
                    raise ValueError(f'Broken local link: {path}: {target}')
                if '#' in target:
                    fragment = target.split('#', 1)[1]
                    body = destination.read_text(encoding='utf-8')
                    if f'id="{fragment}"' not in body:
                        raise ValueError(f'Missing explicit anchor: {path}: {target}')
                links += 1
    manifest_path = ROOT/'MANIFEST.json'
    if not manifest_path.exists():
        raise ValueError('MANIFEST.json is missing')
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    actual = {p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file()
              and p.name != 'MANIFEST.json' and '__pycache__' not in p.parts and p.suffix != '.pyc'}
    if update_manifest:
        manifest['files'] = [{'path': rel, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
                             for rel in sorted(actual) for data in [(ROOT/rel).read_bytes()]]
        manifest_path.write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
        print(f'MANIFEST.json rewritten: {len(actual)} files.', flush=True)
    expected = {entry['path'] for entry in manifest['files']}
    if actual != expected:
        raise ValueError(f'Manifest inventory mismatch: missing={expected-actual}; unexpected={actual-expected}')
    for entry in manifest['files']:
        path = (ROOT/entry['path']).resolve()
        if not path.is_relative_to(ROOT):
            raise ValueError('Manifest path escapes bundle')
        data = path.read_bytes()
        if hashlib.sha256(data).hexdigest() != entry['sha256'] or len(data) != entry['bytes']:
            raise ValueError(f'Manifest hash/size mismatch: {entry["path"]}')
    print(f'Package: 20 references, {len(skill.split())} entry-point words, {links} local links, '
          f'{len(expected)} file hashes verified.', flush=True)

def run(command: list[str], cwd: Path, env: dict[str, str], quiet: bool = False) -> str:
    result = subprocess.run(command, cwd=cwd, env=env, text=True, capture_output=True, timeout=120)
    output = result.stdout + result.stderr
    if not quiet or result.returncode:
        print(output, end='' if output.endswith('\n') else '\n', flush=True)
    if result.returncode:
        raise RuntimeError(f'Command failed ({result.returncode}): {" ".join(command)}')
    return result.stdout

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--require-integrations', action='store_true')
    parser.add_argument('--require-schema', action='store_true')
    parser.add_argument('--update-manifest', action='store_true',
                        help='rewrite MANIFEST.json from the files on disk, then verify')
    args = parser.parse_args()
    env = os.environ.copy()
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    if args.require_integrations:
        env['SUGAR_REQUIRE_INTEGRATIONS'] = '1'
    try:
        package_checks(args.update_manifest)
        run(['prove', '-Ilib', 't'], EXAMPLE, env)
        if args.require_schema and importlib.util.find_spec('jsonschema') is None:
            raise RuntimeError('jsonschema is required by --require-schema')
        run([sys.executable, '-m', 'unittest', 'discover', '-s', 'tests', '-v'], ROOT, env)
        baseline = None
        for seed in ('0', '1', '42', '123456'):
            seeded = {**env, 'PERL_HASH_SEED': seed, 'PERL_PERTURB_KEYS': '2'}
            run(['prove', '-Ilib', 't/30-plan.t'], EXAMPLE, seeded, quiet=True)
            output = run(['perl', 'demo-core.pl'], EXAMPLE, seeded, quiet=True)
            current = json.loads(output)
            if baseline is None:
                baseline = current
            elif current != baseline:
                raise RuntimeError(f'Nondeterministic core demo under hash seed {seed}')
        print('Determinism: planner tests and core demo agree across 4 hash-seed configurations.')
        print('Verification passed. Read explicit SKIP lines; skipped integrations were not executed.')
        return 0
    except (ValueError, OSError, RuntimeError, subprocess.TimeoutExpired) as exc:
        print(f'VERIFICATION FAILED: {exc}', file=sys.stderr)
        return 1

if __name__ == '__main__':
    raise SystemExit(main())
