"""Synthetic tests only: no Craft application and no live provider is launched."""
from __future__ import annotations
import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parent))
import capture_capabilities as c
import run_example as e

MOCK = r'''
import json,sys,time
mode=sys.argv[1]
if mode=='cli':
    print(json.dumps({'arguments':sys.argv[2:]})); sys.exit(0)
if mode=='noise':
    print('not a protocol message',flush=True)
if mode=='sleep':
    time.sleep(30); sys.exit(0)
if mode=='flood':
    print('x'*50000,flush=True); time.sleep(5)
for line in sys.stdin:
    req=json.loads(line); method=req.get('method')
    if 'id' not in req: continue
    ident=req['id']
    if method=='initialize':
        version='2099-01-01' if mode=='revision' else '2025-06-18'
        result={'protocolVersion':version,'capabilities':{'tools':{},'resources':{}},'serverInfo':{'name':'mock','version':'1'}}
    elif method=='tools/list':
        if mode=='request':
            print(json.dumps({'jsonrpc':'2.0','id':99,'method':'sampling/createMessage','params':{}}),flush=True); continue
        if mode=='error':
            print(json.dumps({'jsonrpc':'2.0','id':ident,'error':{'code':-32602,'message':'mock error'}}),flush=True); continue
        cursor=req.get('params',{}).get('cursor')
        tool={'name':'second' if cursor else 'inspect','inputSchema':{'type':'object'}}
        result={'tools':[tool]}
        if mode=='duplicate': result['tools'].append(tool)
        if mode=='missing-schema': result['tools']=[{'name':'bad'}]
        if mode=='pagination' and not cursor: result['nextCursor']='page2'
        if mode=='cursor-loop': result['nextCursor']='again'
        if mode=='notification':
            print(json.dumps({'jsonrpc':'2.0','method':'notifications/message','params':{'data':'hello'}}),flush=True)
    elif method=='resources/list': result={'resources':[]}
    elif method=='resources/templates/list': result={'resourceTemplates':[]}
    else: raise RuntimeError('Unexpected method '+str(method))
    if mode=='wrong-id' and method=='tools/list': ident+=1
    print(json.dumps({'jsonrpc':'2.0','id':ident,'result':result}),flush=True)
'''

class Helpers(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.root=Path(self.temp.name)
        self.mock=self.root/'mock.py'; self.mock.write_text(MOCK)
    def tearDown(self): self.temp.cleanup()
    def probe(self, mode, **kw):
        return c.probe_mcp([sys.executable,str(self.mock),mode],timeout=0.8,max_bytes=65536,**kw)
    def test_strict_json(self): self.assertEqual(c.strict_json('{"a":1}'),{'a':1})
    def test_reject_nonfinite(self):
        for text in ('NaN','Infinity','-Infinity'):
            with self.assertRaises(ValueError): c.strict_json(text)
    def test_limits(self):
        for timeout, size in ((0,1024),(float('nan'),1024),(1,32),(1,300000000)):
            with self.assertRaises(ValueError): c.validate_limits(timeout,size)
    def test_private_write_no_overwrite(self):
        p=self.root/'a'; c.private_write(p,b'one')
        with self.assertRaises(FileExistsError): c.private_write(p,b'two')
        self.assertEqual(p.read_bytes(),b'one')
        if os.name=='posix': self.assertEqual(p.stat().st_mode&0o777,0o600)
    def test_digest(self):
        p=self.root/'a'; p.write_bytes(b'abc')
        self.assertEqual(c.digest(p),'ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad')
    def test_bounded_streams(self):
        r=c.run_bounded([sys.executable,'-c','import sys; print("out"); print("err",file=sys.stderr)'])
        self.assertEqual(r['returncode'],0); self.assertIsNone(r['reason'])
        self.assertEqual(r['stdout'],b'out\n'); self.assertEqual(r['stderr'],b'err\n')
    def test_bounded_timeout(self):
        r=c.run_bounded([sys.executable,str(self.mock),'sleep'],timeout=.1)
        self.assertEqual(r['reason'],'timeout')
    def test_bounded_output_limit(self):
        r=c.run_bounded([sys.executable,str(self.mock),'flood'],timeout=2,max_bytes=128)
        self.assertEqual(r['reason'],'output_limit')
        self.assertLessEqual(len(r['stdout'])+len(r['stderr']),128)
    def test_no_shell_interpolation(self):
        r=c.run_bounded([sys.executable,str(self.mock),'cli','$(touch NEVER)','a b'])
        self.assertEqual(json.loads(r['stdout'])['arguments'],['$(touch NEVER)','a b'])
    def test_nonzero_is_preserved(self):
        r=c.run_bounded([sys.executable,'-c','raise SystemExit(7)'])
        self.assertEqual(r['returncode'],7)
    def test_mcp_metadata(self):
        r=self.probe('ok',include_resources=True)
        self.assertEqual(r['status'],'metadata_observed'); self.assertEqual(r['tools'][0]['name'],'inspect')
        self.assertFalse(r['tools_call_sent']); self.assertFalse(r['resources_read_sent'])
        self.assertEqual(r['resources'],[]); self.assertFalse(r['forced_shutdown'])
    def test_mcp_pagination(self):
        r=self.probe('pagination')
        self.assertEqual([t['name'] for t in r['tools']],['inspect','second'])
    def test_mcp_notifications(self): self.assertEqual(self.probe('notification')['status'],'metadata_observed')
    def test_mcp_noise(self): self.assertIn('Non-JSON',self.probe('noise')['error'])
    def test_mcp_wrong_id(self): self.assertIn('response id',self.probe('wrong-id')['error'])
    def test_mcp_rpc_error(self): self.assertIn('RPC error',self.probe('error')['error'])
    def test_mcp_duplicate_names(self): self.assertIn('duplicate',self.probe('duplicate')['error'])
    def test_mcp_missing_schema(self): self.assertIn('inputSchema',self.probe('missing-schema')['error'])
    def test_mcp_cursor_loop(self): self.assertIn('cursor',self.probe('cursor-loop')['error'])
    def test_mcp_unoffered_capability(self): self.assertIn('unoffered',self.probe('request')['error'])
    def test_mcp_unimplemented_revision(self): self.assertIn('protocol version',self.probe('revision')['error'])
    def test_mcp_timeout(self): self.assertIn('timeout',self.probe('sleep')['error'])
    def test_mcp_forbids_tool_calls(self):
        wire=c.McpWire([sys.executable,str(self.mock),'ok'],timeout=.8,max_bytes=65536)
        try:
            with self.assertRaises(c.ProbeError): wire.request('tools/call',{})
        finally: wire.close()
    def test_substitution_keeps_json(self):
        self.assertEqual(e.substitute(['run','{"x":1}','@OUT@/a'],{'@OUT@':'/tmp/test'}),['run','{"x":1}','/tmp/test/a'])
    def test_substitution_missing_token(self):
        with self.assertRaises(ValueError): e.substitute(['@INPUT@'],{})
    def test_expected_path_traversal(self):
        for value in ('../escape','/absolute'):
            with self.assertRaises(ValueError): e.local_target(self.root,value)
    def test_probe_plan_does_not_launch(self):
        profile=self.root/'profile.json'; profile.write_text(json.dumps({'app':'mock','operator_cli_verified':True,'catalog_argv':[['--version']],'mcp_argv':['mcp']}))
        out=self.root/'absent'
        with patch.object(sys,'argv',['capture','--binary',sys.executable,'--profile',str(profile),'--out',str(out)]),patch.object(c,'run_bounded',side_effect=AssertionError('launched')),contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(c.main(),0)
        self.assertFalse(out.exists())
    def test_probe_refuses_unverified_cli(self):
        profile=self.root/'profile.json'; profile.write_text('{"operator_cli_verified":false}')
        with patch.object(sys,'argv',['capture','--binary',sys.executable,'--profile',str(profile),'--out',str(self.root/'absent')]),contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(c.main(),2)
    def test_probe_executes_mock_catalog(self):
        profile=self.root/'profile.json'; profile.write_text(json.dumps({'app':'mock','operator_cli_verified':True,'catalog_argv':[[str(self.mock),'cli']],'mcp_argv':None}))
        out=self.root/'capture'
        with patch.object(sys,'argv',['capture','--binary',sys.executable,'--profile',str(profile),'--out',str(out),'--execute']),contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(c.main(),0)
        self.assertEqual(json.loads((out/'report.json').read_text())['status'],'metadata_observed')
    def test_recipe_plan_does_not_execute(self):
        recipe=self.root/'recipe.json'; recipe.write_text(json.dumps({'app':'mock','steps':[{'argv':['-c','print(1)']}]}))
        out=self.root/'absent'
        with patch.object(sys,'argv',['example','--binary',sys.executable,'--recipe',str(recipe),'--out',str(out)]),patch.object(e,'run_bounded',side_effect=AssertionError('launched')),contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(e.main(),0)
        self.assertFalse(out.exists())
    def test_recipe_executes_mock_and_preserves_original(self):
        inp=self.root/'original.txt'; inp.write_text('original')
        recipe=self.root/'recipe.json'; recipe.write_text(json.dumps({'app':'mock','input_required':True,
            'steps':[{'argv':['-c','from pathlib import Path; import sys; Path(sys.argv[1]).write_text("result")','@OUT@/result.txt']}],
            'expected_outputs':[{'path':'result.txt','kind':'file'}]}))
        out=self.root/'smoke'
        with patch.object(sys,'argv',['example','--binary',sys.executable,'--recipe',str(recipe),'--input',str(inp),'--out',str(out),'--execute']),contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(e.main(),0)
        report=json.loads((out/'smoke-report.json').read_text())
        self.assertEqual(report['status'],'smoke_executed'); self.assertTrue(report['input']['original_unchanged'])
        self.assertEqual(inp.read_text(),'original')
    def test_recipe_stops_first_failure(self):
        recipe=self.root/'recipe.json'; recipe.write_text(json.dumps({'app':'mock','steps':[{'argv':['-c','raise SystemExit(3)']},{'argv':['-c','print("never")']}]}))
        out=self.root/'failed'
        with patch.object(sys,'argv',['example','--binary',sys.executable,'--recipe',str(recipe),'--out',str(out),'--execute']),contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(e.main(),1)
        self.assertEqual(len(json.loads((out/'smoke-report.json').read_text())['steps']),1)

if __name__=='__main__': unittest.main(verbosity=2)
