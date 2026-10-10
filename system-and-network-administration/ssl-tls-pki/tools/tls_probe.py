#!/usr/bin/env python3
"""Verify one authorized TCP TLS endpoint without changing trust stores.

Separates the network destination from the expected DNS/IP identity. No insecure
mode. Does not implement STARTTLS, QUIC, OCSP/CRL, browser CT, or full HTTP.
"""
from __future__ import annotations
import argparse
import hashlib
import ipaddress
import json
import re
import socket
import ssl
import sys
import time
from pathlib import Path

def port_value(text: str) -> int:
    value = int(text)
    if not 1 <= value <= 65535:
        raise argparse.ArgumentTypeError('port must be 1..65535')
    return value

def reference_name(text: str) -> str:
    try:
        return str(ipaddress.ip_address(text))
    except ValueError:
        if not re.fullmatch(r'[A-Za-z0-9](?:[A-Za-z0-9.-]{0,251}[A-Za-z0-9])?\.?', text) or '..' in text:
            raise argparse.ArgumentTypeError('use an ASCII DNS reference name (IDNA A-labels) or literal IP')
        return text

def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--connect-host', required=True, help='Network destination, not the verification identity')
    p.add_argument('--port', type=port_value, default=443)
    p.add_argument('--name', required=True, type=reference_name, help='Expected DNS/IP identity; DNS also supplies SNI')
    p.add_argument('--cafile', type=Path, help='Approved roots; omission uses Python default trust')
    p.add_argument('--cert', type=Path, help='Optional client certificate plus intermediate chain')
    p.add_argument('--key', type=Path, help='Optional client key; do not pass secrets on the CLI')
    p.add_argument('--timeout', type=float, default=5)
    p.add_argument('--min-version', choices=['1.2','1.3'], default='1.2')
    p.add_argument('--max-version', choices=['1.2','1.3'])
    p.add_argument('--http', action='store_true', help='Also send a minimal HTTP/1.1 GET / and require status 200')
    args = p.parse_args()
    if not 0 < args.timeout <= 60:
        p.error('timeout must be >0 and <=60 seconds')
    if bool(args.cert) != bool(args.key):
        p.error('--cert and --key must be supplied together')
    if args.max_version and args.max_version < args.min_version:
        p.error('maximum TLS version cannot be below minimum')
    for path in (args.cafile, args.cert, args.key):
        if path and not path.is_file():
            p.error(f'file not found: {path}')
    versions = {'1.2': ssl.TLSVersion.TLSv1_2, '1.3': ssl.TLSVersion.TLSv1_3}
    result = {'verified': False, 'connect_host': args.connect_host, 'port': args.port,
              'reference_identity': args.name, 'backend': ssl.OPENSSL_VERSION,
              'trust_source': str(args.cafile) if args.cafile else 'Python default trust',
              'scope': 'TCP TLS path/name/purpose; no browser CT or revocation enforcement',
              'application_checked': args.http}
    try:
        ctx = ssl.create_default_context(cafile=str(args.cafile) if args.cafile else None)
        ctx.minimum_version = versions[args.min_version]
        if args.max_version:
            ctx.maximum_version = versions[args.max_version]
        ctx.hostname_checks_common_name = False
        ctx.verify_flags |= ssl.VERIFY_X509_STRICT
        if args.cert:
            ctx.load_cert_chain(str(args.cert), str(args.key))
        if args.http:
            ctx.set_alpn_protocols(['http/1.1'])
        started = time.monotonic()
        with socket.create_connection((args.connect_host, args.port), timeout=args.timeout) as raw:
            with ctx.wrap_socket(raw, server_hostname=args.name) as tls:
                der = tls.getpeercert(binary_form=True)
                if der is None:
                    raise ssl.SSLError('peer did not present a certificate')
                result.update(verified=True, protocol=tls.version(), cipher=tls.cipher(),
                    alpn=tls.selected_alpn_protocol(), leaf_sha256=hashlib.sha256(der).hexdigest(),
                    peer_leaf=tls.getpeercert(), handshake_seconds=round(time.monotonic()-started, 6))
                if args.http:
                    authority = f'[{args.name}]' if ':' in args.name else args.name
                    if args.port != 443:
                        authority += f':{args.port}'
                    tls.sendall(f'GET / HTTP/1.1\r\nHost: {authority}\r\nConnection: close\r\n\r\n'.encode('ascii'))
                    data = b''
                    deadline = time.monotonic()+args.timeout
                    while b'\r\n' not in data and len(data) < 16384:
                        remaining = deadline-time.monotonic()
                        if remaining <= 0:
                            raise TimeoutError('HTTP status deadline exceeded')
                        tls.settimeout(remaining)
                        chunk = tls.recv(min(2048,16384-len(data)))
                        if not chunk: break
                        data += chunk
                    line = data.split(b'\r\n',1)[0].decode('ascii', errors='replace')
                    result['http_status_line'] = line
                    if b'\r\n' not in data or not line.startswith('HTTP/1.1 200 '):
                        result['application_ok'] = False
                        print(json.dumps(result, indent=2)); return 1
                    result['application_ok'] = True
                else:
                    result['limitation'] = 'Handshake-only: later client-auth alerts and application authorization are not proven.'
    except (OSError, ssl.SSLError, ValueError) as exc:
        result.update(error_type=type(exc).__name__, error=str(exc))
        if isinstance(exc, ssl.SSLCertVerificationError):
            result.update(verify_code=exc.verify_code, verify_message=exc.verify_message)
        print(json.dumps(result, indent=2)); return 1
    print(json.dumps(result, indent=2)); return 0

if __name__ == '__main__':
    raise SystemExit(main())
