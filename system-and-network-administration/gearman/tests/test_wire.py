"""Offline protocol tests. Socket pairs only; no Gearman service is contacted."""
import socket
import ssl
import struct
import sys
import threading
import time
import unittest
from pathlib import Path
from unittest.mock import patch
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from gearman_wire import (Session, Command as C, Packet, ProtocolError, JobFailed,
                         OutcomeUnknown, HEADER, REQUEST, RESPONSE, MAX_FRAME,
                         encode_packet, read_packet, recv_exact, field_bytes, make_tls_context)
from gearman_ops import admin_query, parse_status

class PairCase(unittest.TestCase):
    def setUp(self):
        self.a, self.b = socket.socketpair()
        self.addCleanup(self.a.close)
        self.addCleanup(self.b.close)
        self.session = Session(self.a, timeout=0.3)
    def feed(self, *pairs):
        self.b.sendall(b''.join(encode_packet(c, body, magic=RESPONSE) for c, body in pairs))
    def read_request(self):
        return read_packet(self.b, time.monotonic()+1, magic=REQUEST)

class FramingTests(PairCase):
    def test_network_order_header(self):
        self.assertEqual(encode_packet(7,b'x')[:12],b'\0REQ\0\0\0\x07\0\0\0\x01')
    def test_empty_body(self):
        self.feed((C.NO_JOB,b'')); self.assertEqual(self.session.recv(),Packet(C.NO_JOB,b''))
    def test_binary_nuls(self):
        self.feed((C.ECHO_RES,b'\0a\0\xff')); self.assertEqual(self.session.recv().body,b'\0a\0\xff')
    def test_coalesced_packets(self):
        self.feed((C.NOOP,b''),(C.ECHO_RES,b'x'))
        self.assertEqual(self.session.recv().command,C.NOOP)
        self.assertEqual(self.session.recv().body,b'x')
    def test_fragmented_header_body(self):
        raw=encode_packet(C.ECHO_RES,b'fragmented',magic=RESPONSE)
        def writer():
            for byte in raw:
                self.b.sendall(bytes([byte])); time.sleep(.001)
        t=threading.Thread(target=writer); t.start()
        self.assertEqual(self.session.recv().body,b'fragmented'); t.join(1)
        self.assertFalse(t.is_alive())
    def test_wrong_magic(self):
        self.b.sendall(HEADER.pack(REQUEST,17,0))
        with self.assertRaises(ProtocolError): self.session.recv()
    def test_oversize_header_before_body(self):
        self.b.sendall(HEADER.pack(RESPONSE,17,MAX_FRAME+1))
        with self.assertRaises(ProtocolError): self.session.recv()
    def test_truncated_header(self):
        self.b.sendall(b'\0RES'); self.b.shutdown(socket.SHUT_WR)
        with self.assertRaises(EOFError): self.session.recv()
    def test_truncated_body(self):
        self.b.sendall(HEADER.pack(RESPONSE,17,3)+b'a'); self.b.shutdown(socket.SHUT_WR)
        with self.assertRaises(EOFError): self.session.recv()
    def test_total_read_deadline(self):
        with self.assertRaises(TimeoutError): read_packet(self.a,time.monotonic()+.01)
    def test_encoder_limits(self):
        for c,b,kw,exc in [(1,'text',{},TypeError),(-1,b'',{},ValueError),(2**32,b'',{},ValueError),
                            (1,b'x',{'max_frame':0},ValueError),(1,b'',{'magic':b'HTTP'},ValueError)]:
            with self.subTest(c=c,b=b,kw=kw), self.assertRaises(exc): encode_packet(c,b,**kw)
    def test_negative_read_length(self):
        with self.assertRaises(ValueError): recv_exact(self.a,-1,time.monotonic()+1)
    def test_metadata_policy(self):
        self.assertEqual(field_bytes('a.v1','f'),b'a.v1')
        for text in ('','a b','a\0b','x'*65,'prefix\tf','é'):
            with self.subTest(text=text), self.assertRaises((ValueError,UnicodeError)): field_bytes(text,'f')
    def test_tls_options_fail_before_network(self):
        with patch('gearman_wire.socket.create_connection') as connect:
            for args in ({'cert':'x'},{'server_name':'s'},{'timeout':0},{'timeout':float('nan')},{'timeout':float('inf')},{'port':0}):
                with self.subTest(args=args), self.assertRaises(ValueError): Session.connect('127.0.0.1',**args)
            connect.assert_not_called()
    def test_tls_certificate_pair(self):
        with self.assertRaises(ValueError): make_tls_context('absent',cert='client',key=None)
    def test_tls_context_keeps_verification(self):
        ctx=ssl.create_default_context()
        with patch('gearman_wire.ssl.create_default_context',return_value=ctx):
            result=make_tls_context('not-read-by-mock')
        self.assertEqual(result.verify_mode,ssl.CERT_REQUIRED)
        self.assertTrue(result.check_hostname)
        self.assertEqual(result.minimum_version,ssl.TLSVersion.TLSv1_2)

class ClientTests(PairCase):
    def test_echo(self):
        self.feed((C.ECHO_RES,b'hello')); self.session.echo(b'hello')
        self.assertEqual(self.read_request(),Packet(C.ECHO_REQ,b'hello'))
    def test_echo_mismatch(self):
        self.feed((C.ECHO_RES,b'other'))
        with self.assertRaises(ProtocolError): self.session.echo(b'hello')
    def test_option_negotiation(self):
        self.feed((C.OPTION_RES,b'exceptions')); self.session.enable_exceptions()
        self.assertEqual(self.read_request(),Packet(C.OPTION_REQ,b'exceptions'))
    def test_option_not_acknowledged(self):
        self.feed((C.OPTION_RES,b'other'))
        with self.assertRaises(ProtocolError): self.session.enable_exceptions()
    def test_foreground_success_and_binary_payload(self):
        self.feed((C.JOB_CREATED,b'H:1'),(C.WORK_COMPLETE,b'H:1\0x\0y'))
        r=self.session.submit('a.v1',b'a\0b','id')
        self.assertEqual(r.result,b'x\0y')
        self.assertEqual(self.read_request(),Packet(C.SUBMIT_JOB,b'a.v1\0id\0a\0b'))
    def test_empty_success(self):
        self.feed((C.JOB_CREATED,b'H:1'),(C.WORK_COMPLETE,b'H:1\0'))
        self.assertEqual(self.session.submit('a',b'','id').result,b'')
    def test_background_is_acceptance_only(self):
        self.feed((C.JOB_CREATED,b'H:2'))
        r=self.session.submit('a',b'x','id',background=True,priority='high')
        self.assertIsNone(r.result); self.assertEqual(r.handle,b'H:2')
        self.assertEqual(self.read_request().command,C.SUBMIT_JOB_HIGH_BG)
    def test_explicit_failure(self):
        self.feed((C.JOB_CREATED,b'H:1'),(C.WORK_FAIL,b'H:1'))
        with self.assertRaises(JobFailed): self.session.submit('a',b'x','id')
    def test_exception_is_terminal(self):
        self.feed((C.JOB_CREATED,b'H:1'),(C.WORK_EXCEPTION,b'H:1\0secret'))
        with self.assertRaises(JobFailed) as e: self.session.submit('a',b'x','id')
        self.assertNotIn('secret',str(e.exception))
    def test_intermediate_events(self):
        self.feed((C.JOB_CREATED,b'H'),(C.WORK_STATUS,b'H\0'+b'1\0'+b'2'),
                  (C.WORK_DATA,b'H\0chunk'),(C.WORK_WARNING,b'H\0warn'),(C.WORK_COMPLETE,b'H\0done'))
        seen=[]; r=self.session.submit('a',b'x','id',on_event=seen.append)
        self.assertEqual(len(seen),3); self.assertEqual(r.result,b'done')
    def test_event_byte_cap(self):
        self.feed((C.JOB_CREATED,b'H'),(C.WORK_DATA,b'H\0long'))
        with self.assertRaises(ProtocolError): self.session.submit('a',b'x','id',max_event_bytes=2)
    def test_progress_requires_two_numeric_fields(self):
        self.feed((C.JOB_CREATED,b'H'),(C.WORK_STATUS,b'H\0NaN\0two'))
        with self.assertRaises(ProtocolError): self.session.submit('a',b'x','id')
    def test_handle_mismatch(self):
        self.feed((C.JOB_CREATED,b'H'),(C.WORK_COMPLETE,b'other\0result'))
        with self.assertRaises(ProtocolError): self.session.submit('a',b'x','id')
    def test_work_before_created_rejected(self):
        self.feed((C.WORK_COMPLETE,b'H\0result'))
        with self.assertRaises(ProtocolError): self.session.submit('a',b'x','id')
    def test_duplicate_created_rejected(self):
        self.feed((C.JOB_CREATED,b'H'),(C.JOB_CREATED,b'H2'))
        with self.assertRaises(ProtocolError): self.session.submit('a',b'x','id')
    def test_server_error_sanitized(self):
        self.feed((C.ERROR,b'code\0secret detail'))
        with self.assertRaises(ProtocolError) as e: self.session.submit('a',b'x','id')
        self.assertNotIn('secret',str(e.exception))
    def test_disconnect_is_unknown_and_not_resent(self):
        self.feed((C.JOB_CREATED,b'H')); self.b.shutdown(socket.SHUT_WR)
        with self.assertRaises(OutcomeUnknown): self.session.submit('a',b'x','id')
        self.assertEqual(self.read_request().command,C.SUBMIT_JOB)
        self.b.settimeout(.01)
        with self.assertRaises(TimeoutError): self.b.recv(1)
    def test_invalid_priority_before_send(self):
        with self.assertRaises(ValueError): self.session.submit('a',b'x','id',priority='urgent')
        self.b.settimeout(.01)
        with self.assertRaises(TimeoutError): self.b.recv(1)

class AdminTests(PairCase):
    def test_status_total_includes_running(self):
        self.assertEqual(parse_status('f\t7\t2\t3\n.')[0],
            {'function':'f','total':7,'running':2,'waiting':5,'capable_registrations':3})
    def test_empty_status(self): self.assertEqual(parse_status('.\n'),[])
    def test_invalid_status_rows(self):
        for text in ['f 1 0 2','f\t1\t2\t3','f\t-1\t0\t1','f\t1\t0\t٢','f\t1\t0\t1\nf\t1\t0\t1']:
            with self.subTest(text=text),self.assertRaises(ProtocolError): parse_status(text)
    def test_admin_does_not_wait_for_close(self):
        self.b.sendall(b'f\t2\t1\t3\r\n.\r\n')
        self.assertEqual(admin_query(self.session,'status'),'f\t2\t1\t3\n.')
        self.assertEqual(self.b.recv(32),b'status\n')
    def test_admin_version_single_line(self):
        self.b.sendall(b'2.1.0\n'); self.assertEqual(admin_query(self.session,'version'),'2.1.0')
    def test_admin_mutation_not_sent(self):
        for cmd in ('shutdown','maxqueue f 0','status\nshutdown'):
            with self.subTest(cmd=cmd),self.assertRaises(ValueError): admin_query(self.session,cmd)
        self.b.settimeout(.01)
        with self.assertRaises(TimeoutError): self.b.recv(1)
    def test_admin_cap(self):
        self.b.sendall(b'a'*32)
        with self.assertRaises(ProtocolError): admin_query(self.session,'status',max_bytes=10)
    def test_admin_requires_terminator(self):
        self.b.sendall(b'f\t2\t1\t3\n'); self.b.shutdown(socket.SHUT_WR)
        with self.assertRaises(EOFError): admin_query(self.session,'status')
