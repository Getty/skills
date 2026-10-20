"""Offline tests for the read-only inventory and local package tooling."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(name):
    spec=importlib.util.spec_from_file_location(name,ROOT/'scripts'/f'{name}.py')
    module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module); return module
inventory=load('inventory_project').inventory
lookup=load('library_lookup').lookup
local_targets=load('validate_bundle').local_targets
class ToolingTests(unittest.TestCase):
    def setUp(self): self.temp=tempfile.TemporaryDirectory(); self.root=Path(self.temp.name)
    def tearDown(self): self.temp.cleanup()
    def put(self,name,text):
        p=self.root/name; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(text); return p
    def test_manifest_is_read_without_running_scripts(self):
        p=self.put('package.json',json.dumps({'name':'fixture','scripts':{'postinstall':'DO NOT EXECUTE'},'dependencies':{'react':'^19.3.0'}}))
        before=p.read_bytes(); r=inventory(self.root)
        self.assertEqual(r['manifests'][0]['script_names'],['postinstall']); self.assertEqual(p.read_bytes(),before)
        self.assertEqual(r['manifests'][0]['dependencies'][0]['declared'],'^19.3.0')
    def test_skips_dependency_directories(self):
        self.put('node_modules/a/package.json','{}'); self.put('package.json','{}')
        self.assertEqual(len(inventory(self.root)['manifests']),1)
    def test_heuristic_reports_but_does_not_rewrite(self):
        p=self.put('main.cjs','// sandbox: false\nconst options = { nodeIntegration: true };')
        r=inventory(self.root); self.assertEqual(len(r['heuristic_findings']),2); self.assertIn('true',p.read_text())
    def test_malformed_manifest_is_reported(self):
        self.put('package.json','{'); self.assertEqual(len(inventory(self.root)['errors']),1)
    def test_scan_is_bounded(self):
        for i in range(4): self.put(f'{i}.js','let a=1;')
        r=inventory(self.root,max_files=2); self.assertTrue(r['scan']['truncated']); self.assertEqual(r['scan']['files_seen'],2)
    def test_oversized_file_is_not_read(self):
        self.put('large.js','x'*100); r=inventory(self.root,max_bytes=10); self.assertEqual(r['scan']['oversized'],1); self.assertEqual(r['scan']['files_read'],0)
    def test_symlink_file_is_skipped(self):
        p=self.put('real.js','sandbox: false')
        try: (self.root/'linked.js').symlink_to(p)
        except OSError: self.skipTest('Symlink unsupported')
        r=inventory(self.root); self.assertEqual(r['scan']['symlinks_skipped'],1); self.assertEqual(len(r['heuristic_findings']),1)
    def test_npm_resolved_versions_distinguished(self):
        self.put('package-lock.json',json.dumps({'packages':{'node_modules/react':{'version':'19.3.0'}}}))
        r=inventory(self.root); self.assertEqual(r['resolved_from_npm_lock'][0]['version'],'19.3.0')
    def test_multiple_lockfile_kinds_warn(self):
        self.put('package-lock.json','{}'); self.put('yarn.lock','# fixture')
        self.assertTrue(any('Multiple' in x for x in inventory(self.root)['warnings']))
    def test_invalid_scan_bounds(self):
        with self.assertRaises(ValueError): inventory(self.root,max_files=0)
    def test_catalog_lookup_matches_package(self):
        rows=[{'name':'React Flow','category':'Graphs','packages':['@xyflow/react']}]
        self.assertEqual(len(lookup('XYFLOW',rows)),1); self.assertEqual(lookup('absent',rows),[])
    def test_catalog_lookup_rejects_empty(self):
        with self.assertRaises(ValueError): lookup(' ',[])
    def test_local_markdown_link_resolution(self):
        self.put('a.md','[Exists](sub/b.md) [Web](https://example.com/x)'); self.put('sub/b.md','# B')
        errors,graph=local_targets(self.root); self.assertEqual(errors,[]); self.assertEqual(graph['a.md'],['sub/b.md'])
    def test_missing_and_escaping_links(self):
        self.put('a.md','[Missing](missing.md) [Escape](../outside.md)')
        errors,_=local_targets(self.root); self.assertEqual(len(errors),2)
if __name__=='__main__': unittest.main()
