#!/usr/bin/env python3
"""Run offline and loopback TLS acceptance/rejection tests. No production CA calls.

Python >=3.11, cryptography >=42 and OpenSSL >=3.0 are required. Other runtimes
are optional and explicitly skipped when absent. Output directory must be new.
Private fixtures exist only in a TemporaryDirectory and are removed on exit.
"""
from __future__ import annotations
import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import platform
import re
import shutil
import socket
import ssl
import stat
import subprocess
import sys
import tempfile
import threading
import time
from typing import Any, Iterator
import cryptography
from cryptography import x509
sys.dont_write_bytecode = True
from generate_pki import generate

PACKAGE = Path(__file__).resolve().parents[1]
RESULTS: list[dict[str, Any]] = []
TEMP_ROOT = ''

def record(identifier: str, group: str, status: str, expected: str, observed: Any) -> None:
    detail = str(observed)
    if TEMP_ROOT:
        detail = detail.replace(TEMP_ROOT, '<TEMP>')
    RESULTS.append(dict(id=identifier, group=group, status=status, expected=expected, observed=detail[:2400]))
    print(f'{status:4} {identifier}: {expected}', flush=True)

def run(args: list[str], *, text: str | None = None, timeout: float = 12,
        env: dict[str,str] | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run([str(x) for x in args], input=text, capture_output=True,
                          text=True, timeout=timeout, env=env)

def version(args: list[str]) -> str:
    if not shutil.which(args[0]):
        return 'unavailable'
    try:
        p = run(args)
        return (p.stdout+p.stderr).strip()[:5000]
    except (OSError, subprocess.TimeoutExpired) as exc:
        return str(exc)

@contextmanager
def server(pki: Path, leaf: str = 'server', *, fullchain: bool = True,
           mtls: bool = False, min_version: ssl.TLSVersion = ssl.TLSVersion.TLSv1_2,
           max_version: ssl.TLSVersion = ssl.TLSVersion.MAXIMUM_SUPPORTED) -> Iterator[tuple[int, dict]]:
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.minimum_version, context.maximum_version = min_version, max_version
    context.set_alpn_protocols(['http/1.1'])
    context.load_cert_chain(pki/f'{leaf}.{"fullchain.pem" if fullchain else "pem"}', pki/f'{leaf}.key')
    events: dict[str, Any] = {'sni': [], 'errors': [], 'client_verified': False}
    def sni_callback(sock: ssl.SSLSocket, name: str | None, ctx: ssl.SSLContext) -> None:
        events['sni'].append(name)
    context.set_servername_callback(sni_callback)
    if mtls:
        context.verify_mode = ssl.CERT_REQUIRED
        context.verify_flags |= ssl.VERIFY_X509_STRICT
        context.load_verify_locations(cafile=str(pki/'root.pem'))
    listener = socket.socket()
    listener.bind(('127.0.0.1', 0))
    listener.listen(8)
    listener.settimeout(0.2)
    port = listener.getsockname()[1]
    stop = threading.Event()
    def serve() -> None:
        while not stop.is_set():
            try:
                raw, _ = listener.accept()
            except socket.timeout:
                continue
            except OSError:
                break
            raw.settimeout(4)
            tls = None
            try:
                tls = context.wrap_socket(raw, server_side=True)
                events.update(protocol=tls.version(), alpn=tls.selected_alpn_protocol())
                authorized = True
                if mtls:
                    peer = tls.getpeercert(binary_form=True)
                    if not peer:
                        raise RuntimeError('required client certificate missing after handshake')
                    cert = x509.load_der_x509_certificate(peer)
                    events['client_verified'] = True
                    try:
                        uris = cert.extensions.get_extension_for_class(x509.SubjectAlternativeName).value.get_values_for_type(x509.UniformResourceIdentifier)
                    except x509.ExtensionNotFound:
                        uris = []
                    # An explicit authorization rule, not a complete SPIFFE verifier.
                    authorized = uris == ['spiffe://lab.test/service/allowed']
                    events['client_uris'] = uris
                request = b''
                while b'\r\n\r\n' not in request and len(request) < 16384:
                    chunk = tls.recv(min(2048, 16384-len(request)))
                    if not chunk:
                        break
                    request += chunk
                if not request:
                    continue
                status, body = ('200 OK', b'ok\n') if authorized else ('403 Forbidden', b'denied\n')
                tls.sendall(f'HTTP/1.1 {status}\r\nContent-Length: {len(body)}\r\nConnection: close\r\n\r\n'.encode()+body)
                tls.settimeout(0.3)
                try:
                    plain = tls.unwrap()
                    plain.close()
                except (OSError, ssl.SSLError):
                    pass
            except (OSError, ssl.SSLError, ValueError, RuntimeError) as exc:
                events['errors'].append(f'{type(exc).__name__}: {exc}')
            finally:
                if tls is not None:
                    tls.close()
                raw.close()
    worker = threading.Thread(target=serve, daemon=True)
    worker.start()
    try:
        yield port, events
    finally:
        stop.set()
        listener.close()
        worker.join(6)
        if worker.is_alive():
            raise RuntimeError('loopback server did not shut down')

def python_client(pki: Path, port: int, *, name: str = 'api.svc.test',
                  ca: str = 'root.pem', client: str | None = None,
                  min_version: ssl.TLSVersion = ssl.TLSVersion.TLSv1_2,
                  max_version: ssl.TLSVersion = ssl.TLSVersion.MAXIMUM_SUPPORTED) -> dict:
    context = ssl.create_default_context(cafile=str(pki/ca))
    context.minimum_version, context.maximum_version = min_version, max_version
    context.hostname_checks_common_name = False
    context.verify_flags |= ssl.VERIFY_X509_STRICT
    context.set_alpn_protocols(['http/1.1'])
    if client:
        context.load_cert_chain(pki/f'{client}.fullchain.pem', pki/f'{client}.key')
    with socket.create_connection(('127.0.0.1', port), timeout=4) as raw:
        with context.wrap_socket(raw, server_hostname=name) as tls:
            metadata = dict(protocol=tls.version(), cipher=tls.cipher()[0], alpn=tls.selected_alpn_protocol())
            tls.sendall(f'GET / HTTP/1.1\r\nHost: {name}\r\nConnection: close\r\n\r\n'.encode())
            data = b''
            while b'\r\n' not in data and len(data)<16384:
                chunk = tls.recv(min(2048,16384-len(data)))
                if not chunk:
                    break
                data += chunk
            metadata['status'] = data.split(b'\r\n',1)[0].decode('ascii', errors='replace')
            return metadata

def offline_tests(pki: Path) -> None:
    def verify(identifier: str, leaf: str, expected: bool, description: str, *,
               root: str = 'root.pem', chain: str | None = 'intermediate.pem',
               name: str | None = 'api.svc.test', purpose: str = 'sslserver',
               extra: list[str] | None = None) -> None:
        command = ['openssl','verify','-x509_strict','-no-CApath','-no-CAstore','-CAfile',str(pki/root),'-purpose',purpose]
        if chain:
            command += ['-untrusted',str(pki/chain)]
        if name:
            command += ['-verify_hostname',name]
        command += extra or []
        command += [str(pki/f'{leaf}.pem')]
        p = run(command)
        diagnostic = p.stdout+p.stderr
        good = p.returncode == 0 if expected else (p.returncode != 0 and 'error' in diagnostic.lower() and 'verification failed' in diagnostic.lower())
        record(identifier,'OpenSSL offline path validation','PASS' if good else 'FAIL', description,
               {'exit':p.returncode,'output':diagnostic})
    verify('PATH-01','server',True,'Valid full path accepted')
    verify('PATH-02','server',False,'Unknown root rejected',root='root_b.pem')
    verify('PATH-03','server',False,'Missing intermediate rejected',chain=None)
    verify('NAME-01','wrong_name',False,'Wrong DNS SAN rejected')
    verify('NAME-02','server',True,'Matching iPAddress SAN accepted',name=None,extra=['-verify_ip','127.0.0.1'])
    verify('NAME-03','dns_ip_string',False,'IP encoded as DNS SAN rejected for IP identity',name=None,extra=['-verify_ip','127.0.0.1'])
    verify('NAME-04','wildcard',True,'Single-label wildcard accepted')
    verify('NAME-05','wildcard',False,'Wildcard does not cover apex',name='svc.test')
    verify('NAME-06','wildcard',False,'Wildcard does not cover nested labels',name='deep.api.svc.test')
    verify('NAME-07','cn_conflict',False,'CN cannot override a conflicting SAN')
    verify('NAME-08','cn_only',True,'OpenSSL legacy CN fallback observed, not a recommended profile')
    verify('EKU-01','client',True,'Client-auth EKU accepted for client purpose',purpose='sslclient',name=None)
    verify('EKU-02','client_only_server',False,'Client-only EKU rejected as server')
    verify('EKU-03','server',False,'Server-only EKU rejected as client',purpose='sslclient',name=None)
    verify('TIME-01','expired',False,'Expired leaf rejected')
    verify('TIME-02','future',False,'Not-yet-valid leaf rejected')
    verify('TIME-03','expired_issuer_leaf',False,'Expired intermediate rejected',chain='expired_intermediate.pem')
    verify('CONSTRAINT-01','signed_by_nonca',False,'Non-CA issuer rejected',chain='not_a_ca.pem')
    verify('CONSTRAINT-02','excess_depth',False,'Excess CA path length rejected',chain='excess-chain.pem')
    verify('CONSTRAINT-03','inside_constraint',True,'Permitted DNS constraint accepted',chain='constrained_intermediate.pem')
    verify('CONSTRAINT-04','outside_constraint',False,'Outside DNS name constraint rejected',chain='constrained_intermediate.pem',name='api.other.test')
    verify('CONSTRAINT-05','critical_unknown',False,'Unknown critical extension rejected')
    verify('CRL-01','revoked',True,'Without CRL policy revoked fixture is still accepted')
    verify('CRL-02','revoked',False,'Explicit fresh CRL rejects revoked leaf',extra=['-crl_check','-CRLfile',str(pki/'intermediate.crl.pem')])
    verify('CRL-03','server',True,'Explicit fresh CRL accepts non-revoked leaf',extra=['-crl_check','-CRLfile',str(pki/'intermediate.crl.pem')])
    verify('CRL-04','server',False,'Stale CRL rejected',extra=['-crl_check','-CRLfile',str(pki/'stale.crl.pem')])
    verify('ROOT-01','server_b',True,'Root B path accepted by Root B',root='root_b.pem',chain='intermediate_b.pem')
    verify('ROOT-02','server_b',False,'Root B rejected without trust distribution',chain='intermediate_b.pem')
    verify('ROOT-03','server_b',True,'Overlap trust bundle accepts new Root B',root='root-overlap.pem',chain='intermediate_b.pem')
    verify('CROSS-01','server',True,'Cross-signed issuer builds to Root B',root='root_b.pem',chain='cross_intermediate.pem')
    verify('CROSS-02','server',False,'Cross-signature alone does not trust Root B',chain='cross_intermediate.pem')

def local_tests(pki: Path) -> None:
    try:
        ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER).load_cert_chain(pki/'server.fullchain.pem',pki/'wrong_name.key')
        record('KEY-01','Local safety','FAIL','Mismatched private key rejected','loaded successfully')
    except ssl.SSLError as exc:
        record('KEY-01','Local safety','PASS','Mismatched private key rejected',exc)
    modes = {p.name:oct(stat.S_IMODE(p.stat().st_mode)) for p in pki.glob('*.key')}
    record('KEY-02','Local safety','PASS' if modes and set(modes.values())=={'0o600'} else 'FAIL','All disposable private keys have mode 0600',modes)
    try:
        generate(pki)
        record('LOCAL-01','Local safety','FAIL','Existing fixture directory cannot be overwritten','overwritten')
    except FileExistsError as exc:
        record('LOCAL-01','Local safety','PASS','Existing fixture directory cannot be overwritten',exc)
    for i,(file,count) in enumerate([('server.pem',1),('server.der',1),('server.fullchain.pem',2),('malformed.pem',0),('server.key',0)],1):
        p = run([sys.executable,str(PACKAGE/'tools/inspect_cert.py'),str(pki/file)])
        try:
            data = json.loads(p.stdout)
            good = (p.returncode==0 and data.get('trust_verified') is False and len(data.get('certificates',[]))==count) if count else p.returncode==2 and 'error' in data
        except ValueError:
            good = False
        record(f'INSPECT-{i:02}','Inspection tool','PASS' if good else 'FAIL',f'Inspection-only parser behavior for {file}',p.stdout+p.stderr)

def python_tests(pki: Path) -> None:
    cases = [
      ('TLS-P01','server',{}, {},None,'200 OK','Valid DNS name and SNI',lambda m,e:e['sni']==['api.svc.test']),
      ('TLS-P02','server',{}, {'name':'127.0.0.1'},None,'200 OK','IP identity without DNS SNI',lambda m,e:e['sni']==[None]),
      ('TLS-P03','wrong_name',{}, {},ssl.SSLCertVerificationError,None,'Wrong DNS identity rejected',None),
      ('TLS-P04','server',{}, {'ca':'root_b.pem'},ssl.SSLCertVerificationError,None,'Unknown trust root rejected',None),
      ('TLS-P05','server',{'fullchain':False},{},ssl.SSLCertVerificationError,None,'Missing intermediate rejected',None),
      ('TLS-P06','client_only_server',{}, {},ssl.SSLCertVerificationError,None,'Wrong server EKU rejected',None),
      ('TLS-P07','expired',{}, {},ssl.SSLCertVerificationError,None,'Expired leaf rejected',None),
      ('TLS-P08','future',{}, {},ssl.SSLCertVerificationError,None,'Future leaf rejected',None),
      ('TLS-P09','cn_conflict',{}, {},ssl.SSLCertVerificationError,None,'Conflicting SAN wins over CN',None),
      ('TLS-P10','cn_only',{}, {},ssl.SSLCertVerificationError,None,'Explicit SAN-only policy rejects CN-only certificate',None),
      ('TLS-P11','wildcard',{}, {},None,'200 OK','Single-label wildcard accepted',None),
      ('TLS-P12','wildcard',{}, {'name':'deep.api.svc.test'},ssl.SSLCertVerificationError,None,'Nested wildcard name rejected',None),
      ('TLS-P13','server',{}, {},None,'200 OK','HTTP/1.1 ALPN negotiated',lambda m,e:m['alpn']=='http/1.1'),
      ('TLS-P14','server',{'max_version':ssl.TLSVersion.TLSv1_2},{'max_version':ssl.TLSVersion.TLSv1_2},None,'200 OK','TLS 1.2 can be explicitly negotiated',lambda m,e:m['protocol']=='TLSv1.2'),
      ('TLS-P15','server',{'min_version':ssl.TLSVersion.TLSv1_3},{'min_version':ssl.TLSVersion.TLSv1_3},None,'200 OK','TLS 1.3 can be explicitly negotiated',lambda m,e:m['protocol']=='TLSv1.3'),
      ('TLS-P16','server',{'min_version':ssl.TLSVersion.TLSv1_3},{'max_version':ssl.TLSVersion.TLSv1_2},ssl.SSLError,None,'No permitted protocol overlap is rejected',None),
      ('TLS-P17','rsa_server',{'max_version':ssl.TLSVersion.TLSv1_2},{'max_version':ssl.TLSVersion.TLSv1_2},None,'200 OK','RSA certificate works with ECDHE-RSA, not RSA key exchange',lambda m,e:m['cipher'].startswith('ECDHE-RSA-')),
      ('MTLS-01','server',{'mtls':True},{'client':'client'},None,'200 OK','Valid and explicitly authorized client accepted',lambda m,e:e['client_verified']),
      ('MTLS-02','server',{'mtls':True},{},ssl.SSLError,None,'Missing mandatory client certificate rejected',None),
      ('MTLS-03','server',{'mtls':True},{'client':'server'},ssl.SSLError,None,'Server-only certificate rejected as mTLS client',None),
      ('MTLS-04','server',{'mtls':True},{'client':'client_b'},ssl.SSLError,None,'Foreign client issuer rejected',None),
      ('MTLS-05','server',{'mtls':True},{'client':'unauthorized_client'},None,'403 Forbidden','Authenticated client can still be unauthorized',lambda m,e:e['client_verified']),
      ('MTLS-06','server',{'mtls':True},{'client':'expired_client'},ssl.SSLError,None,'Expired client certificate rejected',None),
    ]
    for identifier,leaf,server_options,client_options,error,status,description,check in cases:
        try:
            with server(pki,leaf,**server_options) as (port,events):
                try:
                    metadata = python_client(pki,port,**client_options)
                    good = error is None and metadata['status']==f'HTTP/1.1 {status}' and (check is None or check(metadata,events))
                    observed = {'client':metadata,'server':events}
                except (OSError, ssl.SSLError) as exc:
                    good = error is not None and isinstance(exc,error)
                    observed = {'error_type':type(exc).__name__,'error':str(exc),'server':events}
            # TLS 1.3 client-auth rejection can surface as a TLS alert or a
            # transport reset. A transport error alone is NEVER sufficient:
            # require the specific verifier failure from our controlled server.
            rejection_reasons = {
                'MTLS-02':'peer did not return a certificate',
                'MTLS-03':'unsuitable certificate purpose',
                'MTLS-04':'unable to get local issuer certificate',
                'MTLS-06':'certificate has expired',
            }
            if identifier in rejection_reasons:
                server_error = ' '.join(events['errors']).lower()
                good = (observed.get('error_type') in {'SSLError','SSLCertVerificationError','ConnectionResetError','BrokenPipeError','ConnectionAbortedError'}
                        and rejection_reasons[identifier] in server_error
                        and events['client_verified'] is False)
            record(identifier,'Python loopback TLS/mTLS','PASS' if good else 'FAIL',description,observed)
        except Exception as exc:
            record(identifier,'Python loopback TLS/mTLS','FAIL',description,f'harness error: {type(exc).__name__}: {exc}')

def tool_tests(pki: Path) -> None:
    for i,(leaf,expected) in enumerate([('server',True),('wrong_name',False),('cn_only',False)],1):
        with server(pki,leaf) as (port,_):
            p = run([sys.executable,str(PACKAGE/'tools/tls_probe.py'),'--connect-host','127.0.0.1','--port',str(port),'--name','api.svc.test','--cafile',str(pki/'root.pem'),'--http'])
            try:
                data = json.loads(p.stdout)
                good = p.returncode==0 and data.get('verified') and data.get('application_ok') if expected else p.returncode==1 and data.get('error_type')=='SSLCertVerificationError'
            except ValueError:
                good = False
        record(f'PROBE-{i:02}','Secure probe CLI','PASS' if good else 'FAIL',f'{leaf}: '+('accept' if expected else 'certificate rejection'),p.stdout+p.stderr)

def external_tests(pki: Path, build: Path) -> None:
    clients: dict[str, Any] = {}
    if shutil.which('openssl'):
        clients['OPENSSL'] = lambda port,root:['openssl','s_client','-quiet','-connect',f'127.0.0.1:{port}','-servername','api.svc.test','-verify_hostname','api.svc.test','-verify_return_error','-CAfile',str(pki/root)]
    if shutil.which('curl'):
        clients['CURL'] = lambda port,root:['curl','--http1.1','--noproxy','*','--fail','--silent','--show-error','--include','--connect-timeout','4','--max-time','8','--cacert',str(pki/root),'--resolve',f'api.svc.test:{port}:127.0.0.1',f'https://api.svc.test:{port}/']
    if shutil.which('node'):
        clients['NODE'] = lambda port,root:['node',str(PACKAGE/'examples/node_probe.js'),'127.0.0.1',str(port),'api.svc.test',str(pki/root)]
    if shutil.which('perl') and run(['perl','-MIO::Socket::SSL','-e','1']).returncode==0:
        clients['PERL'] = lambda port,root:['perl',str(PACKAGE/'examples/perl_probe.pl'),'127.0.0.1',str(port),'api.svc.test',str(pki/root)]
    if shutil.which('go'):
        env = dict(os.environ, GOPROXY='off',GOSUMDB='off',GOTOOLCHAIN='local',CGO_ENABLED='0',GOCACHE=str(build/'go-cache'))
        p = run(['go','build','-o',str(build/'go_probe'),str(PACKAGE/'examples/go_probe.go')],timeout=120,env=env)
        record('BUILD-GO','Compile examples','PASS' if p.returncode==0 else 'FAIL','Compile Go probe without network/module downloads',p.stdout+p.stderr or 'compiled')
        if p.returncode==0:
            clients['GO'] = lambda port,root:[str(build/'go_probe'),'127.0.0.1',str(port),'api.svc.test',str(pki/root)]
    if shutil.which('java') and shutil.which('javac'):
        p = run(['javac','-d',str(build),str(PACKAGE/'examples/JavaTlsProbe.java')],timeout=30)
        record('BUILD-JAVA','Compile examples','PASS' if p.returncode==0 else 'FAIL','Compile Java JSSE probe',p.stdout+p.stderr or 'compiled')
        if p.returncode==0:
            clients['JAVA'] = lambda port,root:['java','-cp',str(build),'JavaTlsProbe','127.0.0.1',str(port),'api.svc.test',str(pki/root)]
    for missing in sorted(set(['OPENSSL','CURL','NODE','PERL','GO','JAVA'])-set(clients)):
        record(f'EXT-{missing}','External runtime loopback','SKIP',f'{missing} runtime available','Runtime or build unavailable; no acceptance coverage claimed')
    scenarios = [('GOOD','server',True,'root.pem',True),('NAME','wrong_name',True,'root.pem',False),
                 ('CHAIN','server',False,'root.pem',False),('EKU','client_only_server',True,'root.pem',False),
                 ('EXPIRED','expired',True,'root.pem',False),('TRUST','server',True,'root_b.pem',False)]
    for name,command in clients.items():
        for suffix,leaf,fullchain,root,expected in scenarios:
            with server(pki,leaf,fullchain=fullchain) as (port,events):
                try:
                    p = run(command(port,root),text='GET / HTTP/1.1\r\nHost: api.svc.test\r\nConnection: close\r\n\r\n' if name=='OPENSSL' else None)
                    diagnostic = p.stdout+p.stderr
                    good = p.returncode==0 and 'HTTP/1.1 200 ' in p.stdout if expected else p.returncode!=0 and re.search(r'certificate|hostname|verify|PKIX|extended key usage',diagnostic,re.I) is not None
                    observed = {'exit':p.returncode,'output':diagnostic,'server':events}
                except (OSError,subprocess.TimeoutExpired) as exc:
                    good,observed = False, str(exc)
            record(f'EXT-{name}-{suffix}','External runtime loopback','PASS' if good else 'FAIL',f'{name}: '+('verified HTTP request accepted' if expected else f'{suffix.lower()} certificate failure rejected'),observed)
    if 'GO' in clients:
        with server(pki,'cn_only') as (port,_):
            p = run(clients['GO'](port,'root.pem'))
        good = p.returncode!=0 and 'legacy Common Name' in p.stderr
        record('GO-CN-ONLY','External runtime loopback','PASS' if good else 'FAIL','Go rejects legacy CN-only identity',p.stdout+p.stderr)

def nginx_tests(pki: Path, build: Path) -> None:
    if not shutil.which('nginx') or not shutil.which('curl'):
        record('NGINX','NGINX verified upstream','SKIP','NGINX integration runtime available','nginx or curl absent')
        return
    for suffix,leaf,expected_status in [('GOOD','server','200'),('BAD-NAME','wrong_name','502')]:
        directory = build/f'nginx-{suffix.lower()}'
        directory.mkdir()
        for child in ['client-body','proxy-temp']:
            (directory/child).mkdir()
        with socket.socket() as reservation:
            reservation.bind(('127.0.0.1',0))
            front_port = reservation.getsockname()[1]
        with server(pki,leaf) as (back_port,events):
            config = (PACKAGE/'examples/nginx-verified-upstream.conf').read_text()
            replacements = {'127.0.0.1:8443':f'127.0.0.1:{front_port}','127.0.0.1:9443':f'127.0.0.1:{back_port}',
                            '/etc/nginx/pki/front.fullchain.pem':str(pki/'server.fullchain.pem'),
                            '/etc/nginx/pki/front.key':str(pki/'server.key'),
                            '/etc/nginx/pki/internal-roots.pem':str(pki/'root.pem'),
                            'api.internal.example.com':'api.svc.test','api.example.com':'api.svc.test'}
            for old,new in replacements.items():
                config = config.replace(old,new)
            config = f'pid {directory}/nginx.pid;\nerror_log {directory}/error.log info;\n'+config
            config = config.replace('http {',f'http {{\n    client_body_temp_path {directory}/client-body;\n    proxy_temp_path {directory}/proxy-temp;')
            configuration = directory/'nginx.conf'
            configuration.write_text(config)
            p = run(['nginx','-p',str(directory)+'/', '-c',str(configuration),'-t'])
            record(f'NGINX-CONFIG-{suffix}','NGINX verified upstream','PASS' if p.returncode==0 else 'FAIL','Validate substituted standalone NGINX template',p.stdout+p.stderr)
            if p.returncode!=0:
                continue
            process = subprocess.Popen(['nginx','-p',str(directory)+'/', '-c',str(configuration),'-g','daemon off;'],stdout=subprocess.DEVNULL,stderr=subprocess.PIPE,text=True)
            try:
                ready = False
                deadline = time.monotonic()+4
                while time.monotonic()<deadline and process.poll() is None:
                    try:
                        with socket.create_connection(('127.0.0.1',front_port),timeout=0.1):
                            ready=True
                        break
                    except OSError:
                        time.sleep(0.05)
                if not ready:
                    raise RuntimeError('NGINX did not become ready')
                p = run(['curl','--http1.1','--noproxy','*','--silent','--show-error','--connect-timeout','4','--max-time','8','--cacert',str(pki/'root.pem'),'--resolve',f'api.svc.test:{front_port}:127.0.0.1','-o',os.devnull,'-w','%{http_code}',f'https://api.svc.test:{front_port}/'])
                good = p.returncode==0 and p.stdout==expected_status
                logfile = (directory/'error.log').read_text()[-1500:] if (directory/'error.log').exists() else ''
                if suffix=='BAD-NAME':
                    good = good and 'does not match' in logfile
                record(f'NGINX-LIVE-{suffix}','NGINX verified upstream','PASS' if good else 'FAIL',f'Authenticated frontend receives {expected_status} for {leaf} upstream',{'exit':p.returncode,'status':p.stdout,'stderr':p.stderr,'server':events,'log':logfile})
            except Exception as exc:
                record(f'NGINX-LIVE-{suffix}','NGINX verified upstream','FAIL','Live reverse-proxy trust enforcement',f'{type(exc).__name__}: {exc}')
            finally:
                process.terminate()
                try:
                    process.communicate(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.communicate(timeout=5)

def main() -> int:
    global TEMP_ROOT
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True,help='New directory for public metadata and test outcomes only')
    args = parser.parse_args()
    try:
        args.output.mkdir(parents=False,exist_ok=False)
    except OSError as exc:
        parser.exit(2,f'Cannot create new output directory: {exc}\n')
    environment = {'executed_at_utc':datetime.now(timezone.utc).isoformat(),'platform':platform.platform(),
                   'python':sys.version,'python_ssl':ssl.OPENSSL_VERSION,'cryptography':cryptography.__version__,
                   'openssl':version(['openssl','version','-a']),'curl':version(['curl','--version']),
                   'go':version(['go','version']),'node':version(['node','-p','JSON.stringify(process.versions)']),
                   'java':version(['java','-version']),'javac':version(['javac','-version']),
                   'perl':version(['perl','-MIO::Socket::SSL','-MNet::SSLeay','-e','print "Perl $^V; IO::Socket::SSL $IO::Socket::SSL::VERSION; Net::SSLeay $Net::SSLeay::VERSION; ",Net::SSLeay::SSLeay_version(0)']),
                   'nginx':version(['nginx','-v'])}
    try:
        with tempfile.TemporaryDirectory(prefix='ssl-pki-lab-') as temporary:
            TEMP_ROOT = temporary
            workspace = Path(temporary)
            pki,build = workspace/'pki',workspace/'build'
            build.mkdir()
            manifest = generate(pki)
            (args.output/'fixture-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
            offline_tests(pki)
            local_tests(pki)
            python_tests(pki)
            tool_tests(pki)
            external_tests(pki,build)
            nginx_tests(pki,build)
    except Exception as exc:
        record('HARNESS','Harness integrity','FAIL','Complete loopback/offline test run',f'{type(exc).__name__}: {exc}')
    summary = {state:sum(t['status']==state for t in RESULTS) for state in ['PASS','FAIL','SKIP']}
    report = {'environment':environment,'summary':summary,'tests':RESULTS,
              'limitations':['Linux only; no browser/mobile/Windows/macOS execution.',
              'Python, curl, Perl and OpenSSL may share a backend. Go crypto/x509 and Java JSSE add independent implementation paths.',
              'Disposable private CA only; no production ACME, public-root qualification, live OCSP, CT, ECH, PQC, QUIC or OS-wide trust mutations.',
              'Client acceptance checks in this lab do not establish a complete browser policy implementation or all production configurations.']}
    (args.output/'results.json').write_text(json.dumps(report,indent=2)+'\n')
    (args.output/'environment.json').write_text(json.dumps(environment,indent=2)+'\n')
    print(json.dumps(summary),flush=True)
    return 1 if summary['FAIL'] else 0

if __name__ == '__main__':
    raise SystemExit(main())
