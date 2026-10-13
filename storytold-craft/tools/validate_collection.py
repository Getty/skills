#!/usr/bin/env python3
"""Offline structural validator; does NOT test Craft applications or LLM agents.

Python 3.10+, standard library. Checks independent skills, local links, JSON,
Python syntax, source references, helper consistency and file manifests.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import shutil
import sys
from typing import Any


def sha(path: Path) -> str:
    h=hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024*1024),b''): h.update(block)
    return h.hexdigest()


def load_json(path: Path) -> Any:
    def reject(value: str): raise ValueError('Non-finite JSON: '+value)
    return json.loads(path.read_text(encoding='utf-8'),parse_constant=reject)


def validate(root: Path) -> dict[str,Any]:
    root=root.resolve(); errors=[]; counts={'skills':0,'references':0,'evaluation_cases':0,
        'json_files':0,'jsonl_files':0,'python_files':0,'local_links':0,'external_links_not_refetched':0,'manifests':0}
    lengths={}; availability={}
    def error(path: Path, message: str): errors.append(f'{path.relative_to(root)}: {message}')
    skills=sorted(p for p in root.glob('storytold-*') if p.is_dir())
    if len(skills)!=16: errors.append(f'Expected 16 skills, found {len(skills)}')
    for folder in skills:
        counts['skills']+=1
        for name in ('SKILL.md','README.md','VALIDATION.md','LICENSE.md','MANIFEST.json','references/sources.md',
                     'assets/runtime-profile.json','assets/sources.json','tests/evaluation-cases.json'):
            if not (folder/name).is_file(): error(folder,'missing '+name)
        try:
            text=(folder/'SKILL.md').read_text(encoding='utf-8')
            front=re.match(r'\A---\nname: ([a-z0-9-]+)\ndescription: (.+)\n---\n',text)
            if not front: raise ValueError('Expected name and JSON-quoted description in YAML frontmatter')
            if front.group(1)!=folder.name: error(folder/'SKILL.md','frontmatter name differs from folder')
            desc=json.loads(front.group(2))
            if not isinstance(desc,str) or not desc.strip(): error(folder/'SKILL.md','empty description')
            words=len(text.split()); lengths[folder.name]=words
            if words>650: error(folder/'SKILL.md',f'{words} words exceeds 650-word ceiling')
            for ref in (folder/'references').glob('*.md'):
                counts['references']+=1
                if '**Read when:**' not in ref.read_text(encoding='utf-8'): error(ref,'no Read when routing')
            profile=load_json(folder/'assets/runtime-profile.json')
            sources=load_json(folder/'assets/sources.json')['sources']; ids={s['id'] for s in sources}
            if any(i not in ids for i in profile['source_ids']): error(folder,'runtime source ID missing from ledger')
            if profile['operator_cli_verified']:
                availability[profile['app']]=shutil.which(profile['binary_name'])
                for fname in ('capture_capabilities.py','run_example.py','test_helpers.py'):
                    local=folder/'scripts'/fname; canonical=root/'tools'/fname
                    if not local.is_file() or sha(local)!=sha(canonical): error(folder,'missing or inconsistent helper '+fname)
                recipe=load_json(folder/'assets/cli-example.json')
                if not recipe.get('steps'): error(folder,'empty smoke recipe')
                for step in recipe['steps']:
                    if not isinstance(step.get('argv'),list) or not step['argv'] or not all(isinstance(x,str) for x in step['argv']): error(folder,'invalid recipe argv')
                if any(i not in ids for i in recipe['source_ids']): error(folder,'recipe references unknown source')
            cases=load_json(folder/'tests/evaluation-cases.json')
            if cases['status']!='not_run_with_real_agent': error(folder,'unexpected unsubstantiated agent status')
            case_ids=set()
            for case in cases['cases']:
                counts['evaluation_cases']+=1
                if case['id'] in case_ids: error(folder,'duplicate evaluation case')
                case_ids.add(case['id'])
                for key in ('prompt','must_demonstrate','must_not'):
                    if not case.get(key): error(folder,'empty evaluation '+key)
        except (OSError,ValueError,KeyError,TypeError) as exc: error(folder,str(exc))
    for path in sorted(root.rglob('*')):
        if not path.is_file(): continue
        if path.is_symlink(): error(path,'symlink not allowed'); continue
        if path.suffix.lower() in ('.ttf','.otf','.woff','.woff2','.ttc','.exe','.dll','.so','.dylib'):
            error(path,'font or application binary must not be bundled')
        try:
            if path.suffix=='.json': load_json(path); counts['json_files']+=1
            elif path.suffix=='.jsonl':
                for i,line in enumerate(path.read_text(encoding='utf-8').splitlines(),1):
                    if line.strip() and not line.lstrip().startswith('#'): json.loads(line)
                counts['jsonl_files']+=1
            elif path.suffix=='.py': compile(path.read_text(encoding='utf-8'),str(path),'exec'); counts['python_files']+=1
            elif path.suffix=='.md':
                text=path.read_text(encoding='utf-8')
                # Ignore code fences when checking authored Markdown link targets.
                text=re.sub(r'```.*?```','',text,flags=re.S)
                for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',text):
                    if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:',target): counts['external_links_not_refetched']+=1; continue
                    target=target.split('#',1)[0]
                    if not target: continue
                    resolved=(path.parent/target).resolve()
                    counts['local_links']+=1
                    # The group README shows the library's shared banner; nothing else may leave the group.
                    if path==root/'README.md' and resolved.is_relative_to(root.parent/'assets') and resolved.exists(): continue
                    if not resolved.is_relative_to(root): error(path,'local link escapes bundle: '+target)
                    elif not resolved.exists(): error(path,'broken local link: '+target)
                    app_root=next((folder for folder in skills if path.is_relative_to(folder)),None)
                    if app_root and not resolved.is_relative_to(app_root): error(path,'cross-skill dependency: '+target)
        except (OSError,ValueError,TypeError,SyntaxError) as exc: error(path,str(exc))
    for manifest_path in sorted(root.rglob('MANIFEST.json')):
        counts['manifests']+=1
        try:
            manifest=load_json(manifest_path); parent=manifest_path.parent
            listed=set()
            for entry in manifest['files']:
                rel=entry['path']; p=(parent/rel).resolve()
                if not p.is_relative_to(parent.resolve()): raise ValueError('manifest path escapes root')
                if rel in listed: raise ValueError('duplicate manifest entry')
                listed.add(rel)
                if not p.is_file() or sha(p)!=entry['sha256'] or p.stat().st_size!=entry['bytes']: error(manifest_path,'file mismatch: '+rel)
            actual={str(p.relative_to(parent)) for p in parent.rglob('*') if p.is_file() and p!=manifest_path and '__pycache__' not in p.parts}
            if listed!=actual: error(manifest_path,'manifest inventory differs: '+str(sorted(listed^actual)))
        except (OSError,ValueError,KeyError,TypeError) as exc: error(manifest_path,str(exc))
    if counts['manifests']!=16: errors.append('Expected 16 independent skill manifests')
    return {'schema':'storytold-package-validation/1','validated_at':datetime.now(timezone.utc).isoformat(),
       'status':'passed' if not errors else 'failed','scope':'Offline structure, syntax, links, hashes and source/evaluation records only',
       'counts':counts,'skill_word_counts':lengths,'binary_path_discovery':availability,
       'application_tests':'not_run','fresh_agent_evaluations':'not_run','errors':errors,
       'limitations':['No real Craft application executed by this validator','External URLs not refetched','JSON validated for syntax and selected contracts, not complete upstream schemas']}


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root',type=Path,nargs='?',default=Path(__file__).resolve().parents[1])
    parser.add_argument('--report',type=Path)
    args=parser.parse_args(); result=validate(args.root)
    payload=json.dumps(result,indent=2,ensure_ascii=False)+'\n'
    if args.report: args.report.write_text(payload,encoding='utf-8')
    print(payload,end='')
    return 0 if result['status']=='passed' else 1
if __name__=='__main__': raise SystemExit(main())
