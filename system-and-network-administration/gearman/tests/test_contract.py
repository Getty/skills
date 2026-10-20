"""Domain and transaction tests; no Gearman dependency."""
import copy
import json
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import threading
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'examples/python'))
from contract import parse, encode, execute, fingerprint, ContractError
from result_store import ResultStore

def request():
    return {'schema_version':1,'request_id':'a0000000-0000-4000-8000-000000000001',
            'operation':'sum.v1','payload':{'numbers':[10,20,-3]}}

def wire(o): return json.dumps(o,separators=(',',':')).encode()

class ContractTests(unittest.TestCase):
    def test_success(self): self.assertEqual(execute(parse(wire(request())))['result']['sum'],27)
    def test_negative_and_zero(self):
        o=request(); o['payload']['numbers']=[0,-1000000000,1000000000]
        self.assertEqual(execute(parse(wire(o)))['result']['sum'],0)
    def test_integer_sum_bounds(self):
        o=request();o['payload']['numbers']=[1000000000]*1000
        self.assertEqual(execute(parse(wire(o)))['result']['sum'],1000000000000)
    def test_forbidden_numeric_types(self):
        for v in (True,False,1.5,1.0,'1',None,[],{},1000000001):
            o=request();o['payload']['numbers']=[v]
            with self.subTest(v=v),self.assertRaises(ContractError): parse(wire(o))
    def test_array_limits(self):
        for v in ([],[1]*1001,{},'123'):
            o=request();o['payload']['numbers']=v
            with self.subTest(v=str(v)[:30]),self.assertRaises(ContractError): parse(wire(o))
    def test_unknown_and_missing_fields(self):
        for key in request():
            o=request(); del o[key]
            with self.subTest(key=key),self.assertRaises(ContractError): parse(wire(o))
        o=request();o['extra']=1
        with self.assertRaises(ContractError): parse(wire(o))
    def test_schema_types_and_versions(self):
        for v in (True,1.0,'1',2):
            o=request();o['schema_version']=v
            with self.subTest(v=v),self.assertRaises(ContractError): parse(wire(o))
    def test_invalid_request_id(self):
        for v in ('A0000000-0000-4000-8000-000000000001','short',1,None):
            o=request();o['request_id']=v
            with self.subTest(v=v),self.assertRaises(ContractError): parse(wire(o))
    def test_operation_and_payload(self):
        for field,value in [('operation','other'),('payload',[]),('payload',{'numbers':[1],'extra':1})]:
            o=request();o[field]=value
            with self.subTest(value=value),self.assertRaises(ContractError): parse(wire(o))
    def test_duplicate_keys(self):
        raw=wire(request()).replace(b'"schema_version":1',b'"schema_version":2,"schema_version":1')
        with self.assertRaises(ContractError): parse(raw)
    def test_malformed_nonfinite_utf8(self):
        for raw in (b'{',b'\xff',b'null',b'[]',wire(request()).replace(b'[10,20,-3]',b'[NaN]')):
            with self.subTest(raw=raw[:30]),self.assertRaises(ContractError): parse(raw)
    def test_byte_limit(self):
        with self.assertRaises(ContractError): parse(b' '*65537)
    def test_deadline_types(self):
        for d in (True,'1',-1,1.5,9007199254740992):
            o=request();o['deadline_unix_ms']=d
            with self.subTest(d=d),self.assertRaises(ContractError): parse(wire(o))
    def test_expired_deadline(self):
        o=request();o['deadline_unix_ms']=100
        with self.assertRaises(ContractError): execute(parse(wire(o)),now_ms=100)
    def test_future_deadline(self):
        o=request();o['deadline_unix_ms']=101
        self.assertTrue(execute(parse(wire(o)),now_ms=100)['ok'])
    def test_fingerprint_excludes_delivery_metadata(self):
        a=request();b=copy.deepcopy(a);b['deadline_unix_ms']=123;b['request_id']='b0000000-0000-4000-8000-000000000001'
        self.assertEqual(fingerprint(a),fingerprint(b))
        b['payload']['numbers']=[99];self.assertNotEqual(fingerprint(a),fingerprint(b))

class StoreTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.path=Path(self.tmp.name)/'results.sqlite'
        self.store=ResultStore(self.path);self.addCleanup(self.store.close)
    def count(self): return self.store.db.execute("SELECT value FROM counters").fetchone()[0]
    def test_repeated_id_one_effect(self):
        a=self.store.apply(request());b=self.store.apply(request())
        self.assertEqual(a,b);self.assertEqual(self.count(),1)
    def test_conflicting_id_rejected(self):
        self.store.apply(request());o=request();o['payload']['numbers']=[99]
        with self.assertRaises(ContractError): self.store.apply(o)
        self.assertEqual(self.count(),1)
    def test_failure_rolls_back_effect_and_result(self):
        with self.assertRaises(RuntimeError): self.store.apply(request(),fail_before_commit=True)
        self.assertEqual(self.count(),0);self.assertIsNone(self.store.lookup(request()['request_id']))
        self.store.apply(request());self.assertEqual(self.count(),1)
    def test_reopen_preserves_result(self):
        self.store.apply(request());other=ResultStore(self.path)
        try: self.assertEqual(other.apply(request())['result']['sum'],27)
        finally: other.close()
        self.assertEqual(self.count(),1)
    def test_cached_result_after_deadline(self):
        o=request();o['deadline_unix_ms']=101
        self.store.apply(o,now_ms=100)
        self.assertTrue(self.store.apply(o,now_ms=102)['ok']);self.assertEqual(self.count(),1)
    def test_expired_new_operation_has_no_effect(self):
        o=request();o['deadline_unix_ms']=1
        with self.assertRaises(ContractError): self.store.apply(o,now_ms=2)
        self.assertEqual(self.count(),0)
    def test_concurrent_repeats_one_effect(self):
        errors=[];outputs=[];barrier=threading.Barrier(4)
        def apply():
            other=None
            try:
                other=ResultStore(self.path);barrier.wait(timeout=3);outputs.append(other.apply(request()))
            except BaseException as e: errors.append(e)
            finally:
                if other:other.close()
        ts=[threading.Thread(target=apply) for _ in range(4)]
        for t in ts:t.start()
        for t in ts:t.join(5)
        self.assertFalse(any(t.is_alive() for t in ts));self.assertEqual(errors,[])
        self.assertEqual(len(outputs),4);self.assertEqual(self.count(),1)

class CrossLanguageTests(unittest.TestCase):
    def invoke(self,lang,raw):
        if not shutil.which(lang): self.skipTest(f'{lang} runtime unavailable; native Gearman binding not needed')
        script=ROOT/f'examples/{lang}/contract_cli.{"pl" if lang=="perl" else "php"}'
        return subprocess.run([lang,str(script)],input=raw,capture_output=True,timeout=5)
    def test_perl_success(self):
        p=self.invoke('perl',wire(request()));self.assertEqual(p.returncode,0,p.stderr)
        self.assertEqual(json.loads(p.stdout),execute(request()))
    def test_php_success(self):
        p=self.invoke('php',wire(request()));self.assertEqual(p.returncode,0,p.stderr)
        self.assertEqual(json.loads(p.stdout),execute(request()))
    def test_perl_rejects_bad_types(self):
        for v in (True,1.0,1.5,'1',None,1000000001):
            o=request();o['payload']['numbers']=[v]
            with self.subTest(v=v):self.assertNotEqual(self.invoke('perl',wire(o)).returncode,0)
    def test_php_rejects_bad_types(self):
        for v in (True,1.0,1.5,'1',None,1000000001):
            o=request();o['payload']['numbers']=[v]
            with self.subTest(v=v):self.assertNotEqual(self.invoke('php',wire(o)).returncode,0)
    def test_perl_integer_boundaries(self):
        o=request();o['payload']['numbers']=[1000000000]*1000
        p=self.invoke('perl',wire(o));self.assertEqual(p.returncode,0,p.stderr)
        self.assertEqual(json.loads(p.stdout),execute(o))
    def test_php_integer_boundaries(self):
        o=request();o['payload']['numbers']=[-1000000000]*1000
        p=self.invoke('php',wire(o));self.assertEqual(p.returncode,0,p.stderr)
        self.assertEqual(json.loads(p.stdout),execute(o))
    def test_both_reject_expired_and_large_inputs(self):
        o=request();o['deadline_unix_ms']=0
        for lang in ('perl','php'):
            for raw in (wire(o),b' '*65537):
                with self.subTest(lang=lang,n=len(raw)):self.assertNotEqual(self.invoke(lang,raw).returncode,0)
