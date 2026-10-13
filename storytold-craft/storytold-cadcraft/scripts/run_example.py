#!/usr/bin/env python3
"""Run an authored CLI smoke recipe in a NEW directory; plan-only by default.

The recipe is controller metadata, not a shared Craft command language. Trust the
binary and recipe before using --execute. This runner is not an OS sandbox.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import sys
from typing import Any
from capture_capabilities import digest, private_write, run_bounded, strict_json, validate_limits, write_json


def substitute(argv: list[str], replacements: dict[str, str]) -> list[str]:
    if not isinstance(argv, list) or not argv or not all(isinstance(v, str) and '\x00' not in v for v in argv):
        raise ValueError('Recipe argv must be a nonempty list of strings without NULs')
    result = []
    for value in argv:
        for token, replacement in replacements.items():
            value = value.replace(token, replacement)
        if any(token in value for token in ('@INPUT@', '@OUT@', '@ASSETS@')):
            raise ValueError('Unresolved recipe token')
        result.append(value)
    return result


def local_target(root: Path, relative: str) -> Path:
    rel = Path(relative)
    if rel.is_absolute() or '..' in rel.parts:
        raise ValueError('Expected output must be a relative path without parent traversal')
    target = (root / rel).resolve()
    if not target.is_relative_to(root.resolve()):
        raise ValueError('Expected output escapes working directory')
    return target


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--binary', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--input', type=Path)
    parser.add_argument('--recipe', type=Path, default=Path(__file__).resolve().parents[1]/'assets/cli-example.json')
    parser.add_argument('--timeout', type=float, default=120)
    parser.add_argument('--max-bytes', type=int, default=16*1024*1024)
    parser.add_argument('--execute', action='store_true')
    args = parser.parse_args()
    try:
        validate_limits(args.timeout, args.max_bytes)
        recipe = strict_json(args.recipe.read_text(encoding='utf-8'))
        binary = args.binary.expanduser().resolve(strict=True)
        if not binary.is_file():
            raise ValueError('binary must be a file')
        out = args.out.expanduser().absolute()
        if out.exists() or out.is_symlink():
            raise ValueError('Output directory must not already exist')
        source = args.input.expanduser().resolve(strict=True) if args.input else None
        if recipe.get('input_required') and source is None:
            raise ValueError('This recipe requires --input FILE')
        if source is not None and not source.is_file():
            raise ValueError('input must be a regular file')
        steps = recipe.get('steps')
        if not isinstance(steps, list) or not steps:
            raise ValueError('Recipe must have steps')
        copied = out/('source'+source.suffix) if source else None
        replacements = {'@OUT@':str(out), '@ASSETS@':str(args.recipe.resolve().parent)}
        if copied:
            replacements['@INPUT@'] = str(copied)
        commands = [[str(binary), *substitute(step['argv'], replacements)] for step in steps]
        expected = recipe.get('expected_outputs', [])
        for item in expected:
            local_target(out, item['path'])
            if item.get('kind') not in ('file', 'directory'):
                raise ValueError('Expected output kind must be file or directory')
        plan: dict[str, Any] = {'app':recipe['app'], 'commands':commands,
            'input_copy':str(copied) if copied else None, 'output_directory':str(out),
            'warning':'Trusted native code only; not an OS sandbox. External linked assets are not copied. No automatic retries.'}
        if not args.execute:
            print(json.dumps(plan, indent=2)); return 0
        out.mkdir(mode=0o700, parents=True, exist_ok=False)
        report: dict[str, Any] = {'schema':'storytold-cli-smoke/1','app':recipe['app'],
            'started_at':datetime.now(timezone.utc).isoformat(), 'binary_sha256':digest(binary),
            'recipe_sha256':digest(args.recipe), 'scope':'CLI execution and output existence only; not semantic, visual, or agent evaluation',
            'steps':[], 'expected_outputs':[], 'status':'failed_or_partial'}
        before = digest(source) if source else None
        try:
            if source and copied:
                # Streaming copy, exclusive creation. Do not load a large media file into memory.
                with source.open('rb') as inp, copied.open('xb') as dst:
                    while block := inp.read(1024*1024):
                        dst.write(block)
                copied.chmod(0o600)
                report['input'] = {'path':str(source),'sha256_before':before,'copy_sha256':digest(copied)}
                if digest(copied) != before:
                    raise ValueError('Input changed while copying; no application command executed')
            failed = False
            for index, command in enumerate(commands, 1):
                entry = run_bounded(command, timeout=args.timeout, max_bytes=args.max_bytes, cwd=out)
                entry['name'] = steps[index-1].get('name', str(index))
                for stream in ('stdout','stderr'):
                    filename = f'step-{index:02}-{stream}.log'
                    private_write(out/filename, entry.pop(stream))
                    entry[stream+'_file'] = filename
                report['steps'].append(entry)
                if entry['returncode'] != 0 or entry['reason'] is not None:
                    failed = True
                    break
            for item in expected:
                target = local_target(out, item['path'])
                ok = (target.is_file() and target.stat().st_size>0) if item['kind']=='file' else (target.is_dir() and any(target.iterdir()))
                report['expected_outputs'].append({**item, 'nonempty':bool(ok)})
                failed |= not ok
            if source:
                after = digest(source)
                report['input']['sha256_after'] = after
                report['input']['original_unchanged'] = before == after
                failed |= before != after
            report['status'] = 'smoke_executed' if not failed else 'failed_or_partial'
        except (OSError, ValueError, TypeError, KeyError) as exc:
            report['error'] = str(exc)
        report['output_files_sha256'] = {str(p.relative_to(out)):digest(p) for p in sorted(out.rglob('*'))
            if p.is_file() and not p.is_symlink()}
        write_json(out/'smoke-report.json', report)
        print(str(out/'smoke-report.json'))
        return 0 if report['status']=='smoke_executed' else 1
    except (OSError, ValueError, TypeError, KeyError) as exc:
        print(f'run_example: {exc}', file=sys.stderr); return 2

if __name__ == '__main__':
    raise SystemExit(main())
