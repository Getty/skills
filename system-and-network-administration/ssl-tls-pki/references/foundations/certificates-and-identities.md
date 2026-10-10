# Certificate profiles and service identities

**Read when:** issuing certificates or determining why an apparently valid certificate is rejected.

## Validate meaning, not just signatures

Inspect the public key, issuer, serial, validity interval, subject alternative names (SAN), basic constraints, key usage (KU), extended key usage (EKU), name constraints, and critical extensions. A signature can be mathematically correct while the certificate is unusable for the requested purpose. Unknown critical extensions are not decorations that a conforming path validator can silently ignore.

For new server profiles, place DNS identities in `dNSName` SAN entries and literal addresses in `iPAddress` entries. A numeric string encoded as a DNS SAN is not a correct IP SAN. The intended reference identity comes from trusted application configuration or the URL, not from the certificate being checked.

Modern service-identity guidance does not use the subject Common Name as a fallback. Some real clients retain legacy behavior; PostgreSQL libpq is an explicit example. Design correct SAN-based profiles and test the actual client rather than assuming every library already behaves identically.

## Names and boundaries

`*.example.com` can cover a single leftmost label such as `api.example.com`; it is not a certificate for `example.com` or `a.b.example.com`. Do not invent partial-label wildcard rules. Normalize internationalized names with the application's supported IDNA handling and inspect the ASCII reference value. A DNS alias does not automatically change the identity the application intended to contact.

SNI selects a virtual TLS endpoint. Name verification decides whether that endpoint is authentic. Setting SNI alone does not enable name verification. The HTTP Host header arrives later and cannot retroactively fix a failed certificate check.

## Example profile decisions

| Profile | Identity and purpose | Issuance restrictions |
|---|---|---|
| Web/API server | DNS/IP SAN; serverAuth | Only authorized service names; CA false |
| Workload client | Defined URI or other application identity; clientAuth | Bound to attested workload/account and approved role |
| Issuing CA | CA true; certificate/CRL signing | Bounded delegation, protected signing key |
| Root CA | Explicit trust anchor and ceremony policy | No routine end-entity issuance in the proposed design |

Use separate leaf keys for separate workloads and environments. A server/client dual-use profile increases the consequences of key theft and makes future policy migrations harder. It is not a universal interoperability shortcut.

## CSR handling

A CSR proves possession of a key and requests fields; it does not prove entitlement to those fields. The CA must enforce SAN, EKU, validity and CA-status policy independently. Reject attempts to request another tenant's name, an issuer certificate, or an unconstrained application identity. Do not blindly copy all requested extensions.

Run the lab's wrong-purpose, SAN/CN conflict, wildcard and invalid-CA cases before relying on a new verifier configuration.

## Primary references

- **RFC5280** — [X.509 certificates and CRLs / PKIX](https://www.rfc-editor.org/rfc/rfc5280.html).
- **RFC9525** — [Service identity verification in TLS](https://www.rfc-editor.org/rfc/rfc9525.html).
- **RFC6066** — [TLS extensions, including SNI](https://datatracker.ietf.org/doc/html/rfc6066).
- **PG-CLIENT** — [PostgreSQL 18 libpq TLS](https://www.postgresql.org/docs/18/libpq-ssl.html).
- **OPENSSL-REQ** — [OpenSSL 3.5 req](https://docs.openssl.org/3.5/man1/openssl-req/).
- **OPENSSL-VERIFY** — [OpenSSL 3.5 verification options](https://docs.openssl.org/3.5/man1/openssl-verification-options/).

Reference snapshot: **2026-10-10**. For dated policy, distinguish current rules from future effective dates.
