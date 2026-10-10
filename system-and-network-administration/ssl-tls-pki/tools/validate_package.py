#!/usr/bin/env python3
"""Validate package structure, local links, source references and example syntax.

No external URLs are fetched; no servers, hooks, certificate issuance, or system
trust changes are executed. Run labs/run_lab.py separately for live TLS tests.
"""
from __future__ import annotations
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
RESULTS: list[dict] = []

def check(name: str, errors: list[str], *, skipped: bool = False) -> None:
    RESULTS.append({'check':name,'status':'SKIP' if skipped else ('FAIL' if errors else 'PASS'),'details':errors})

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--json',type=Path,help='Also save this structural report to a file')
    args = parser.parse_args()
    required = ['SKILL.md','README.md','CONTENTS.md','SECURITY.md','sources/SOURCES.md','sources/sources.json',
                'sources/CLAIMS.md','labs/README.md','labs/run_lab.py','labs/generate_pki.py','validation/REPORT.md',
                'validation/results.json','validation/environment.json','validation/fixture-manifest.json','examples/README.md']
    check('Required package entry points',[x for x in required if not (ROOT/x).is_file()])
    files = [p for p in ROOT.rglob('*') if p.is_file() and '__pycache__' not in p.parts]
    check('No symlinks in package',[str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_symlink()])
    bad_material = []
    for p in files:
        if p.suffix in {'.key','.p12','.pfx','.class','.o','.so','.dll','.pyc'} or re.search(rb'-----BEGIN (?:[A-Z]+ )*PRIVATE KEY-----',p.read_bytes()):
            bad_material.append(str(p.relative_to(ROOT)))
    check('No private-key or compiled-binary artifacts',bad_material)
    skill = (ROOT/'SKILL.md').read_text()
    check('Slim SKILL.md with metadata',[] if len(skill.split()) <= 650 and skill.startswith('---\nname: ssl-tls-pki\n') and '\ndescription:' in skill else ['Invalid metadata or more than 650 whitespace-delimited words'])
    broken, fence_errors = [],[]
    for p in [x for x in files if x.suffix=='.md']:
        text = p.read_text()
        if len(re.findall(r'^```',text,re.M)) % 2:
            fence_errors.append(str(p.relative_to(ROOT)))
        for link in re.findall(r'(?<!!)\[[^\]]+\]\(([^\s)]+)\)',text):
            if urlsplit(link).scheme or link.startswith('#'):
                continue
            target = (p.parent/unquote(link.split('#',1)[0])).resolve()
            if not target.is_relative_to(ROOT) or not target.exists():
                broken.append(f'{p.relative_to(ROOT)} -> {link}')
    check('Relative Markdown file links resolve (fragments not validated)',broken)
    check('Markdown fenced code blocks are balanced',fence_errors)
    registry = json.loads((ROOT/'sources/sources.json').read_text())
    source_list = registry['sources']
    source_map = {x['id']:x for x in source_list}
    errors = []
    if len(source_map)!=len(source_list):
        errors.append('Duplicate source IDs')
    if len({x['url'] for x in source_list})!=len(source_list):
        errors.append('Duplicate source URLs')
    for x in source_list:
        if not x['url'].startswith('https://') or x['reviewed_on']!='2026-10-10':
            errors.append(x['id'])
    check('Source registry IDs, URLs and review snapshot',errors)
    errors = []
    for p in sorted((ROOT/'references').rglob('*.md')):
        text = p.read_text()
        if '**Read when:**' not in text or '## Primary references' not in text or 'Reference snapshot: **2026-10-10**' not in text:
            errors.append(f'{p.relative_to(ROOT)}: missing reference scaffolding')
        refs = re.findall(r'- \*\*([A-Z0-9-]+)\*\* — \[[^\]]+\]\((https://[^)]+)\)',text)
        if not refs:
            errors.append(f'{p.relative_to(ROOT)}: no primary references')
        for identifier,url in refs:
            if identifier not in source_map or source_map[identifier]['url']!=url:
                errors.append(f'{p.relative_to(ROOT)}: unregistered source {identifier}')
    check('Every topical reference has registered primary sources',errors)
    errors=[]
    for p in [x for x in files if x.suffix=='.json']:
        try:
            json.loads(p.read_text())
        except ValueError as exc:
            errors.append(f'{p.relative_to(ROOT)}: {exc}')
    check('JSON syntax',errors)
    errors=[]
    for p in [x for x in files if x.suffix=='.py']:
        try:
            ast.parse(p.read_text(),filename=str(p))
        except SyntaxError as exc:
            errors.append(f'{p.relative_to(ROOT)}: {exc}')
    check('Python source syntax (no bytecode generation)',errors)
    for label,executable,arguments in [
        ('Shell hook syntax only','sh',['-n',str(ROOT/'examples/certbot-nginx-deploy-hook.sh')]),
        ('Node.js probe syntax only','node',['--check',str(ROOT/'examples/node_probe.js')]),
        ('Perl probe syntax only','perl',['-c',str(ROOT/'examples/perl_probe.pl')]),
    ]:
        if not shutil.which(executable):
            check(label,[f'{executable} not installed'],skipped=True)
        else:
            try:
                p=subprocess.run([executable]+arguments,capture_output=True,text=True,timeout=10)
                check(label,[] if p.returncode==0 else [p.stdout+p.stderr])
            except (OSError,subprocess.TimeoutExpired) as exc:
                check(label,[str(exc)])
    try:
        import yaml
        documents=list(yaml.safe_load_all((ROOT/'examples/cert-manager-staging.yaml').read_text()))
        issuer,certificate=documents
        errors=[]
        if issuer['kind']!='Issuer' or certificate['kind']!='Certificate': errors.append('Unexpected resource kinds')
        if issuer['spec']['acme']['server']!='https://acme-staging-v02.api.letsencrypt.org/directory': errors.append('Not staging')
        if certificate['spec']['issuerRef']['name']!=issuer['metadata']['name']: errors.append('Issuer reference mismatch')
        if certificate['metadata']['namespace']!=issuer['metadata']['namespace']: errors.append('Namespace mismatch')
        check('YAML parse and local staging consistency (NOT CRD validation)',errors)
    except ImportError:
        check('YAML parse and local staging consistency (NOT CRD validation)',['PyYAML unavailable'],skipped=True)
    except Exception as exc:
        check('YAML parse and local staging consistency (NOT CRD validation)',[str(exc)])
    test_report=json.loads((ROOT/'validation/results.json').read_text())
    tests=test_report['tests']
    actual={s:sum(t['status']==s for t in tests) for s in ['PASS','FAIL','SKIP']}
    check('Bundled executed-test report is internally consistent',[] if actual==test_report['summary'] and len({t['id'] for t in tests})==len(tests) else ['Summary or unique IDs inconsistent'])
    check('Bundled executed-test report has no failures',[] if actual['FAIL']==0 else [str(actual)])
    sums=ROOT/'SHA256SUMS'
    if sums.exists():
        errors=[]
        names=[]
        for line in sums.read_text().splitlines():
            digest,name=line.split('  ',1)
            names.append(name)
            target=(ROOT/name).resolve()
            if not target.is_relative_to(ROOT) or not target.is_file() or hashlib.sha256(target.read_bytes()).hexdigest()!=digest:
                errors.append(name)
        expected_names={p.relative_to(ROOT).as_posix() for p in files if p!=sums}
        if set(names)!=expected_names or len(set(names))!=len(names):
            errors.append('Checksum file list is incomplete, duplicated, or contains extra entries')
        check('SHA256SUMS integrity and complete file coverage',errors)
    else:
        check('SHA256SUMS integrity and complete file coverage',['Not yet generated or not supplied'],skipped=True)
    result={'summary':{s:sum(x['status']==s for x in RESULTS) for s in ['PASS','FAIL','SKIP']},'checks':RESULTS,
            'limits':'Structural/syntax checks, not external-link freshness, full Markdown anchor validation, production deployment or certificate security certification.'}
    output=json.dumps(result,indent=2)+'\n'
    print(output)
    if args.json:
        args.json.write_text(output)
    return 1 if result['summary']['FAIL'] else 0

if __name__=='__main__':
    raise SystemExit(main())
