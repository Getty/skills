#!/usr/bin/env python3
"""Inspect certificate metadata only. Does NOT validate trust, names or revocation.

Accepts a PEM certificate list or one DER certificate. Rejects private-key input.
Requires cryptography >=42; never fetches AIA, CRL or other network resources.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization

def describe(cert: x509.Certificate) -> dict:
    now = datetime.now(timezone.utc)
    key = cert.public_key()
    data = {'subject':cert.subject.rfc4514_string(), 'issuer':cert.issuer.rfc4514_string(),
            'serial_hex':format(cert.serial_number,'x'), 'sha256':cert.fingerprint(hashes.SHA256()).hex(),
            'spki_sha256':hashlib.sha256(key.public_bytes(serialization.Encoding.DER, serialization.PublicFormat.SubjectPublicKeyInfo)).hexdigest(),
            'key_type':type(key).__name__, 'key_size':getattr(key,'key_size',None),
            'not_before':cert.not_valid_before_utc.isoformat(), 'not_after':cert.not_valid_after_utc.isoformat(),
            'within_own_validity_interval':cert.not_valid_before_utc <= now <= cert.not_valid_after_utc,
            'remaining_seconds':int((cert.not_valid_after_utc-now).total_seconds()),
            'critical_extension_oids':[e.oid.dotted_string for e in cert.extensions if e.critical]}
    for cls, name, transform in [
        (x509.SubjectAlternativeName, 'sans', lambda e:[{'type':type(n).__name__,'value':str(n.value)} for n in e]),
        (x509.ExtendedKeyUsage, 'extended_key_usage', lambda e:[n.dotted_string for n in e]),
        (x509.BasicConstraints, 'basic_constraints', lambda e:{'ca':e.ca,'path_length':e.path_length}),
    ]:
        try: data[name] = transform(cert.extensions.get_extension_for_class(cls).value)
        except x509.ExtensionNotFound: data[name] = None
    return data

def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('certificate', type=Path)
    args = p.parse_args()
    try:
        with args.certificate.open('rb') as stream:
            raw = stream.read(2_000_001)
        if len(raw)>2_000_000: raise ValueError('input exceeds 2 MB limit')
        if b'PRIVATE KEY' in raw: raise ValueError('refusing input containing private-key material')
        certs = x509.load_pem_x509_certificates(raw) if b'-----BEGIN CERTIFICATE-----' in raw else [x509.load_der_x509_certificate(raw)]
        if not certs: raise ValueError('no certificates found')
        print(json.dumps({'inspection_only':True,'trust_verified':False,'certificates':[describe(c) for c in certs]}, indent=2))
    except (OSError, ValueError) as exc:
        print(json.dumps({'inspection_only':True,'error':str(exc)})); return 2
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
