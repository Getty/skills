"""Exercise the actual Python worker against an offline scripted socket peer."""
import json
import socket
import sys
import threading
import time
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'scripts'),str(ROOT/'examples/python')]
from gearman_wire import Session, Command as C, Packet, REQUEST, RESPONSE, encode_packet, read_packet, ProtocolError
from worker import serve

class WorkerTests(unittest.TestCase):
    def setUp(self):
        self.a,self.b=socket.socketpair();self.addCleanup(self.a.close);self.addCleanup(self.b.close)
        self.stop=threading.Event();self.errors=[];self.count=[]
    def read(self): return read_packet(self.b,time.monotonic()+1,magic=REQUEST)
    def send(self,c,b=b''): self.b.sendall(encode_packet(c,b,magic=RESPONSE))
    def start(self,handler=None,max_jobs=1):
        def run():
            try:self.count.append(serve(Session(self.a,.5),'f.v1',stop=self.stop,max_jobs=max_jobs,handler=handler))
            except BaseException as e:self.errors.append(e)
        self.t=threading.Thread(target=run,daemon=True);self.t.start()
        self.assertEqual(self.read(),Packet(C.CAN_DO,b'f.v1'))
        self.assertEqual(self.read().command,C.GRAB_JOB_UNIQ)
    def finish(self):
        self.t.join(2);self.assertFalse(self.t.is_alive());self.assertEqual(self.errors,[])
    def test_success_binary_workload(self):
        self.start(handler=lambda b:b)
        self.send(C.JOB_ASSIGN_UNIQ,b'H\0f.v1\0id\0x\0y')
        self.assertEqual(self.read(),Packet(C.WORK_COMPLETE,b'H\0x\0y'))
        self.finish();self.assertEqual(self.count,[1])
    def test_expected_failure_sends_only_fail(self):
        def reject(_):raise ValueError('private detail')
        self.start(handler=reject);self.send(C.JOB_ASSIGN_UNIQ,b'H\0f.v1\0id\0bad')
        self.assertEqual(self.read(),Packet(C.WORK_FAIL,b'H'));self.finish()
        self.b.settimeout(.01)
        with self.assertRaises(TimeoutError):self.b.recv(1)
    def test_idle_sleep_wakeup(self):
        self.start(handler=lambda b:b)
        self.send(C.NO_JOB);self.assertEqual(self.read().command,C.PRE_SLEEP)
        self.send(C.NOOP);self.assertEqual(self.read().command,C.GRAB_JOB_UNIQ)
        self.send(C.JOB_ASSIGN_UNIQ,b'H\0f.v1\0id\0ok')
        self.assertEqual(self.read().command,C.WORK_COMPLETE);self.finish()
    def test_idle_stop(self):
        self.start(handler=lambda b:b,max_jobs=0)
        self.send(C.NO_JOB);self.assertEqual(self.read().command,C.PRE_SLEEP)
        self.stop.set();self.finish();self.assertEqual(self.count,[0])
    def test_assignment_after_signal_is_finished(self):
        self.start(handler=lambda b:b);self.stop.set()
        self.send(C.JOB_ASSIGN_UNIQ,b'H\0f.v1\0id\0ok')
        self.assertEqual(self.read().command,C.WORK_COMPLETE);self.finish()
    def test_wrong_function_rejected(self):
        self.start(handler=lambda b:b);self.send(C.JOB_ASSIGN_UNIQ,b'H\0other\0id\0ok')
        self.t.join(2);self.assertFalse(self.t.is_alive());self.assertIsInstance(self.errors[0],ProtocolError)
    def test_unexpected_handler_crash_is_not_fake_completion(self):
        def fail(_):raise RuntimeError('injected systemic failure')
        self.start(handler=fail);self.send(C.JOB_ASSIGN_UNIQ,b'H\0f.v1\0id\0ok')
        self.t.join(2);self.assertIsInstance(self.errors[0],RuntimeError)
        self.b.settimeout(.01)
        with self.assertRaises(TimeoutError):self.b.recv(1)
