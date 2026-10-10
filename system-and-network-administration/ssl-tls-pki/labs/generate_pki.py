#!/usr/bin/env python3
"""Generate disposable, deliberately mixed-validity PKI fixtures. Never production keys.

Requires Python >=3.11 and cryptography >=42. Creates a NEW directory only.
No network, system trust changes, secret logging, or external services at runtime.
"""
from __future__ import annotations
import argparse
import ipaddress
import json
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec, rsa
from cryptography.x509.oid import ExtendedKeyUsageOID, NameOID, ObjectIdentifier

Key = ec.EllipticCurvePrivateKey | rsa.RSAPrivateKey

def new_key(*, rsa_key: bool = False) -> Key:
    return rsa.generate_private_key(65537, 2048) if rsa_key else ec.generate_private_key(ec.SECP256R1())

def subject(cn: str) -> x509.Name:
    return x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, cn)])

def write_private(path: Path, data: bytes) -> None:
    """Exclusive creation prevents accidental overwrite; no shared-readable keys."""
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, 'wb') as stream:
        stream.write(data)

def generate(destination: Path) -> dict[str, Any]:
    destination.mkdir(mode=0o700, parents=False, exist_ok=False)
    now = datetime.now(timezone.utc).replace(microsecond=0)
    keys: dict[str, Key] = {}
    certs: dict[str, x509.Certificate] = {}
    manifest: dict[str, Any] = {
        'warning': 'Disposable educational fixtures, including intentionally invalid certificates. Never trust outside this lab.',
        'generated_at': now.isoformat(), 'fixtures': {}
    }

    def issue(name: str, *, issuer: str | None = None, ca: bool = False,
              path_length: int | None = None, cn: str | None = None,
              sans: list[x509.GeneralName] | None = None,
              eku: list[ObjectIdentifier] | None = None,
              start: datetime | None = None, end: datetime | None = None,
              key: Key | None = None, constraints: x509.NameConstraints | None = None,
              unknown_critical: bool = False, description: str = '') -> x509.Certificate:
        key = key or new_key()
        signer = key if issuer is None else keys[issuer]
        issuer_name = subject(cn or name) if issuer is None else certs[issuer].subject
        builder = (x509.CertificateBuilder()
                   .subject_name(subject(cn or name)).issuer_name(issuer_name)
                   .public_key(key.public_key()).serial_number(x509.random_serial_number())
                   .not_valid_before(start or now - timedelta(hours=1))
                   .not_valid_after(end or now + timedelta(days=2))
                   .add_extension(x509.BasicConstraints(ca=ca, path_length=path_length if ca else None), critical=True)
                   .add_extension(x509.KeyUsage(digital_signature=not ca, content_commitment=False,
                      key_encipherment=False, data_encipherment=False, key_agreement=False,
                      key_cert_sign=ca, crl_sign=ca, encipher_only=False, decipher_only=False), critical=True)
                   .add_extension(x509.SubjectKeyIdentifier.from_public_key(key.public_key()), critical=False)
                   .add_extension(x509.AuthorityKeyIdentifier.from_issuer_public_key(signer.public_key()), critical=False))
        if sans:
            builder = builder.add_extension(x509.SubjectAlternativeName(sans), critical=False)
        if eku:
            builder = builder.add_extension(x509.ExtendedKeyUsage(eku), critical=False)
        if constraints:
            builder = builder.add_extension(constraints, critical=True)
        if unknown_critical:
            builder = builder.add_extension(x509.UnrecognizedExtension(ObjectIdentifier('1.3.6.1.4.1.55555.42'), b'\x05\x00'), critical=True)
        cert = builder.sign(signer, hashes.SHA256())
        keys[name], certs[name] = key, cert
        write_private(destination / f'{name}.key', key.private_bytes(serialization.Encoding.PEM,
                      serialization.PrivateFormat.PKCS8, serialization.NoEncryption()))
        (destination / f'{name}.pem').write_bytes(cert.public_bytes(serialization.Encoding.PEM))
        manifest['fixtures'][name] = {'issuer': issuer or name, 'description': description,
              'serial_hex': format(cert.serial_number, 'x'), 'sha256': cert.fingerprint(hashes.SHA256()).hex(),
              'not_before': cert.not_valid_before_utc.isoformat(), 'not_after': cert.not_valid_after_utc.isoformat()}
        return cert

    server_eku = [ExtendedKeyUsageOID.SERVER_AUTH]
    client_eku = [ExtendedKeyUsageOID.CLIENT_AUTH]
    dns = lambda value: x509.DNSName(value)
    server_sans = [dns('api.svc.test'), x509.IPAddress(ipaddress.ip_address('127.0.0.1'))]
    root_time = dict(start=now-timedelta(days=30), end=now+timedelta(days=365))
    int_time = dict(start=now-timedelta(days=3), end=now+timedelta(days=30))
    issue('root', ca=True, path_length=1, cn='DISPOSABLE LAB Root A', **root_time)
    issue('root_b', ca=True, path_length=1, cn='DISPOSABLE LAB Root B', **root_time)
    issue('intermediate', issuer='root', ca=True, path_length=0, cn='DISPOSABLE LAB Issuer A', **int_time)
    issue('intermediate_b', issuer='root_b', ca=True, path_length=0, cn='DISPOSABLE LAB Issuer B', **int_time)
    issue('cross_intermediate', issuer='root_b', ca=True, path_length=0, cn='DISPOSABLE LAB Issuer A',
          key=keys['intermediate'], description='Same issuer key/subject, cross-signed by Root B', **int_time)
    issue('server', issuer='intermediate', cn='api.svc.test', sans=server_sans, eku=server_eku)
    issue('server_b', issuer='intermediate_b', cn='api.svc.test', sans=server_sans, eku=server_eku)
    issue('rsa_server', issuer='intermediate', cn='api.svc.test', sans=server_sans, eku=server_eku, key=new_key(rsa_key=True))
    issue('wrong_name', issuer='intermediate', cn='other.svc.test', sans=[dns('other.svc.test')], eku=server_eku)
    issue('cn_conflict', issuer='intermediate', cn='api.svc.test', sans=[dns('other.svc.test')], eku=server_eku)
    issue('cn_only', issuer='intermediate', cn='api.svc.test', eku=server_eku,
          description='Legacy CN-only server: intentional compatibility trap, not a modern profile')
    issue('wildcard', issuer='intermediate', cn='*.svc.test', sans=[dns('*.svc.test')], eku=server_eku)
    issue('dns_ip_string', issuer='intermediate', cn='127.0.0.1', sans=[dns('127.0.0.1')], eku=server_eku,
          description='IP text wrongly encoded as DNS SAN')
    issue('client_only_server', issuer='intermediate', cn='api.svc.test', sans=server_sans, eku=client_eku)
    issue('expired', issuer='intermediate', cn='api.svc.test', sans=server_sans, eku=server_eku,
          start=now-timedelta(days=2), end=now-timedelta(days=1))
    issue('future', issuer='intermediate', cn='api.svc.test', sans=server_sans, eku=server_eku,
          start=now+timedelta(days=1), end=now+timedelta(days=2))
    issue('critical_unknown', issuer='intermediate', cn='api.svc.test', sans=server_sans,
          eku=server_eku, unknown_critical=True)
    issue('revoked', issuer='intermediate', cn='api.svc.test', sans=server_sans, eku=server_eku)
    for name, identity in [('client', 'allowed'), ('unauthorized_client', 'denied')]:
        issue(name, issuer='intermediate', cn=name, eku=client_eku,
              sans=[x509.UniformResourceIdentifier(f'spiffe://lab.test/service/{identity}')])
    issue('client_b', issuer='intermediate_b', cn='foreign-client', eku=client_eku,
          sans=[x509.UniformResourceIdentifier('spiffe://lab.test/service/allowed')])
    issue('expired_client', issuer='intermediate', cn='expired-client', eku=client_eku,
          sans=[x509.UniformResourceIdentifier('spiffe://lab.test/service/allowed')],
          start=now-timedelta(days=2), end=now-timedelta(days=1))
    issue('constrained_intermediate', issuer='root', ca=True, path_length=0,
          constraints=x509.NameConstraints(permitted_subtrees=[dns('svc.test')], excluded_subtrees=None), **int_time)
    issue('inside_constraint', issuer='constrained_intermediate', cn='api.svc.test', sans=[dns('api.svc.test')], eku=server_eku)
    issue('outside_constraint', issuer='constrained_intermediate', cn='api.other.test', sans=[dns('api.other.test')], eku=server_eku)
    issue('not_a_ca', issuer='root', ca=False, cn='NOT A CA', eku=server_eku, **int_time)
    issue('signed_by_nonca', issuer='not_a_ca', cn='api.svc.test', sans=server_sans, eku=server_eku)
    issue('excess_ca', issuer='intermediate', ca=True, path_length=0, **int_time)
    issue('excess_depth', issuer='excess_ca', cn='api.svc.test', sans=server_sans, eku=server_eku)
    issue('expired_intermediate', issuer='root', ca=True, path_length=0,
          start=now-timedelta(days=3), end=now-timedelta(days=1))
    issue('expired_issuer_leaf', issuer='expired_intermediate', cn='api.svc.test', sans=server_sans, eku=server_eku)

    # Server/client chain files omit the self-signed root intentionally.
    for name, cert in certs.items():
        chain = [cert]
        current = manifest['fixtures'][name]['issuer']
        visited = {name}
        while current not in visited:
            visited.add(current)
            parent = manifest['fixtures'][current]['issuer']
            if parent == current:  # root must be a trust input, not a deployment dependency
                break
            chain.append(certs[current])
            current = parent
        (destination / f'{name}.fullchain.pem').write_bytes(b''.join(c.public_bytes(serialization.Encoding.PEM) for c in chain))
    (destination/'root-overlap.pem').write_bytes((destination/'root.pem').read_bytes()+(destination/'root_b.pem').read_bytes())
    (destination/'excess-chain.pem').write_bytes((destination/'excess_ca.pem').read_bytes()+(destination/'intermediate.pem').read_bytes())
    (destination/'server.der').write_bytes(certs['server'].public_bytes(serialization.Encoding.DER))
    (destination/'malformed.pem').write_text('not a certificate\n')
    revoked = (x509.RevokedCertificateBuilder().serial_number(certs['revoked'].serial_number)
               .revocation_date(now-timedelta(minutes=1)).build())
    def crl_file(filename: str, last: datetime, next_: datetime) -> None:
        crl = (x509.CertificateRevocationListBuilder().issuer_name(certs['intermediate'].subject)
               .last_update(last).next_update(next_).add_revoked_certificate(revoked)
               .add_extension(x509.AuthorityKeyIdentifier.from_issuer_public_key(keys['intermediate'].public_key()), False)
               .add_extension(x509.CRLNumber(1), False).sign(keys['intermediate'], hashes.SHA256()))
        (destination/filename).write_bytes(crl.public_bytes(serialization.Encoding.PEM))
    crl_file('intermediate.crl.pem', now-timedelta(minutes=2), now+timedelta(days=1))
    crl_file('stale.crl.pem', now-timedelta(days=2), now-timedelta(days=1))
    (destination/'manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
    return manifest

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', type=Path, help='New directory; never an existing one')
    args = parser.parse_args()
    try:
        data = generate(args.directory)
    except (OSError, ValueError) as exc:
        parser.exit(2, f'Fixture creation failed: {exc}\n')
    print(f'Generated {len(data["fixtures"])} disposable fixtures in {args.directory}. Never install their trust globally.')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
