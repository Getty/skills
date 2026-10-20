#!/usr/bin/env python3
"""Check local skill structure, Markdown targets, JSON, and recorded file hashes offline."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import unquote
IGNORE = {'node_modules','.git','__pycache__','dist','build','.cache','.pytest_cache'}
def files(root: Path):
    return sorted(p for p in root.rglob('*') if p.is_file() and not any(part in IGNORE for part in p.relative_to(root).parts) and p.suffix != '.pyc')
def local_targets(root: Path):
    errors=[]; graph={}
    for file in files(root):
        if file.suffix != '.md': continue
        rel=file.relative_to(root).as_posix(); graph[rel]=[]
        for raw in re.findall(r'\[[^\]]*\]\(([^)]+)\)',file.read_text(encoding='utf-8')):
            target=raw.strip().split(' "',1)[0].strip('<>')
            if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:',target) or target.startswith('#'): continue
            target=unquote(target.split('#',1)[0])
            if not target: continue
            path=(file.parent/target).resolve()
            try: relative=path.relative_to(root.resolve()).as_posix()
            except ValueError: errors.append(f'{rel}: target escapes skill directory: {target}'); continue
            if not path.exists(): errors.append(f'{rel}: missing target: {target}')
            elif path.is_file(): graph[rel].append(relative)
    return errors,graph

def verify(root: Path) -> dict:
    root=root.resolve(); errors=[]
    required=['SKILL.md','README.md','SOURCES.md','VALIDATION.md','MANIFEST.json','references/00-index.md','assets/library-catalog.json']
    for name in required:
        if not (root/name).is_file(): errors.append(f'Missing {name}')
    if (root/'SKILL.md').is_file():
        text=(root/'SKILL.md').read_text()
        match=re.match(r'^---\n(.*?)\n---\n',text,re.S)
        if not match: errors.append('SKILL.md lacks YAML frontmatter')
        else:
            name=re.search(r'^name:\s*([a-z0-9-]+)\s*$',match.group(1),re.M)
            if not name or name.group(1)!=root.name: errors.append('Skill name must match directory')
            if not re.search(r'^description:\s*\S',match.group(1),re.M): errors.append('Missing description')
        if len(text.split())>650: errors.append('SKILL.md exceeds local 650-word budget')
    link_errors,graph=local_targets(root); errors.extend(link_errors)
    seen=set(); pending=['SKILL.md']
    while pending:
        item=pending.pop()
        if item in seen: continue
        seen.add(item); pending.extend(graph.get(item,[]))
    references=[p.relative_to(root).as_posix() for p in (root/'references').glob('*.md')]
    for ref in references:
        if ref not in seen: errors.append(f'Reference not reachable from SKILL.md: {ref}')
    for path in files(root):
        if path.is_symlink(): errors.append(f'Symlink not allowed: {path.relative_to(root)}')
        if path.suffix=='.json':
            try: json.loads(path.read_text())
            except (ValueError,OSError) as error: errors.append(f'Invalid JSON {path.relative_to(root)}: {type(error).__name__}')
    if (root/'MANIFEST.json').is_file():
        try:
            manifest=json.loads((root/'MANIFEST.json').read_text())
            recorded=manifest['files']
            actual={p.relative_to(root).as_posix():p for p in files(root) if p.name!='MANIFEST.json'}
            if set(recorded)!=set(actual): errors.append('Manifest file set differs from actual files (excluding manifest/generated directories)')
            for name,expected in recorded.items():
                path=(root/name).resolve()
                if not path.is_relative_to(root): errors.append(f'Unsafe manifest path: {name}'); continue
                if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest()!=expected: errors.append(f'Hash mismatch: {name}')
        except (ValueError,OSError,KeyError,TypeError) as error: errors.append(f'Manifest error: {type(error).__name__}')
    return {'ok':not errors,'errors':errors,'reference_files':len(references),'files':len(files(root)),'reachable_markdown_and_assets':len(seen),'external_urls':'not fetched by this offline validator','frontmatter':'basic local subset checks, not the full upstream schema'}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root',nargs='?',type=Path,default=Path(__file__).resolve().parents[1])
    args=parser.parse_args()
    report=verify(args.root)
    print(json.dumps(report,indent=2))
    raise SystemExit(0 if report['ok'] else 1)
if __name__=='__main__': main()
