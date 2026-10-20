#!/usr/bin/env python3
"""Read-only bounded project inventory. No commands, installs, network, or source rewrites."""
from __future__ import annotations
import argparse
import json
import os
from pathlib import Path
import re
import sys
SKIP = {'.git', 'node_modules', 'dist', 'build', 'coverage', '.next', '.cache', '__pycache__', '.venv', 'vendor'}
LOCKS = {'package-lock.json', 'npm-shrinkwrap.json', 'pnpm-lock.yaml', 'yarn.lock', 'bun.lock', 'bun.lockb'}
EXTS = {'.js', '.jsx', '.cjs', '.mjs', '.ts', '.tsx', '.html', '.json', '.yaml', '.yml'}
PATTERNS = {
    'node-integration-enabled': re.compile(r'nodeIntegration\s*:\s*true'),
    'context-isolation-disabled': re.compile(r'contextIsolation\s*:\s*false'),
    'sandbox-disabled': re.compile(r'(?:sandbox\s*:\s*false|--no-sandbox)'),
    'web-security-disabled': re.compile(r'webSecurity\s*:\s*false'),
    'html-injection-sink': re.compile(r'dangerouslySetInnerHTML'),
    'dynamic-eval': re.compile(r'\beval\s*\('),
    'generic-renderer-ipc-exposure': re.compile(r'exposeInMainWorld\s*\([^;]{0,300}\bipcRenderer\b', re.S),
}
def inventory(root: Path, max_files: int = 5000, max_bytes: int = 524288) -> dict:
    root = root.resolve()
    if not root.is_dir(): raise ValueError('Project root must be a directory')
    if not 1 <= max_files <= 100000 or not 1 <= max_bytes <= 16_777_216: raise ValueError('Invalid scan bounds')
    result = {'project': str(root), 'manifests': [], 'lockfiles': [], 'resolved_from_npm_lock': [], 'heuristic_findings': [], 'errors': [], 'scan': {'files_seen': 0, 'files_read': 0, 'oversized': 0, 'symlinks_skipped': 0, 'truncated': False}, 'warnings': []}
    def walk_error(error): result['errors'].append(str(error))
    for directory, directories, filenames in os.walk(root, followlinks=False, onerror=walk_error):
        base = Path(directory)
        kept=[]
        for name in sorted(directories):
            if (base/name).is_symlink(): result['scan']['symlinks_skipped'] += 1
            elif name not in SKIP: kept.append(name)
        directories[:] = kept
        for name in sorted(filenames):
            path=base/name
            if path.is_symlink(): result['scan']['symlinks_skipped'] += 1; continue
            if name not in LOCKS and path.suffix not in EXTS: continue
            if result['scan']['files_seen'] >= max_files: result['scan']['truncated']=True; break
            result['scan']['files_seen'] += 1
            relative=path.relative_to(root).as_posix()
            if name in LOCKS: result['lockfiles'].append(relative)
            try:
                if path.stat().st_size > max_bytes: result['scan']['oversized'] += 1; continue
                if name == 'bun.lockb': continue
                text=path.read_text(encoding='utf-8')
                result['scan']['files_read'] += 1
                if name == 'package.json':
                    data=json.loads(text)
                    if not isinstance(data,dict): raise ValueError('Manifest is not an object')
                    deps=[]
                    for section in ['dependencies','devDependencies','peerDependencies','optionalDependencies']:
                        values=data.get(section,{})
                        if not isinstance(values,dict): continue
                        deps.extend({'name': package, 'declared': version, 'section': section} for package,version in sorted(values.items()) if isinstance(version,str))
                    scripts=data.get('scripts',{})
                    result['manifests'].append({'file':relative,'name':data.get('name'),'packageManager':data.get('packageManager'),'engines':data.get('engines',{}),'script_names':sorted(scripts) if isinstance(scripts,dict) else [],'dependencies':deps})
                elif name in {'package-lock.json','npm-shrinkwrap.json'}:
                    data=json.loads(text)
                    packages=data.get('packages',{}) if isinstance(data,dict) else {}
                    if isinstance(packages,dict):
                        for package_path, package in packages.items():
                            if isinstance(package,dict) and isinstance(package.get('version'),str) and 'node_modules/' in package_path:
                                result['resolved_from_npm_lock'].append({'lockfile':relative,'package':package_path.rsplit('node_modules/',1)[-1],'version':package['version']})
                if name not in LOCKS:
                    for label,pattern in PATTERNS.items():
                        if len(result['heuristic_findings']) >= 100: break
                        match=pattern.search(text)
                        if match: result['heuristic_findings'].append({'file':relative,'line':text.count('\n',0,match.start())+1,'signal':label,'classification':'review-required; heuristic, possibly comment/test/false-positive'})
            except (OSError,UnicodeError,ValueError) as error:
                result['errors'].append({'file':relative,'error':type(error).__name__})
        if result['scan']['truncated']: break
    if len({Path(p).name for p in result['lockfiles']}) > 1: result['warnings'].append('Multiple lockfile kinds found; inspect workspace ownership before selecting a package manager.')
    if not result['manifests']: result['warnings'].append('No readable package manifest found within scan bounds.')
    result['limits'] = ['Declared ranges are not resolved versions.', 'Only bounded npm lockfile package entries are parsed; other lockfiles are identified, not resolved.', 'No dependency installation, advisory lookup, license audit, runtime check, or complete static analysis was performed.', 'Heuristics include comments/examples and can miss indirect configuration. No findings does not prove safety.', 'Output contains project paths and dependency metadata; redact before sharing externally.']
    return result

def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('project',type=Path)
    parser.add_argument('--max-files',type=int,default=5000)
    parser.add_argument('--max-bytes',type=int,default=524288)
    args=parser.parse_args()
    try: report=inventory(args.project,args.max_files,args.max_bytes)
    except (ValueError,OSError) as error: parser.error(str(error))
    print(json.dumps(report,indent=2,ensure_ascii=False))
    return 0
if __name__=='__main__': raise SystemExit(main())
