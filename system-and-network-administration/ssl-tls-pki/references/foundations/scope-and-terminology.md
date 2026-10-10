# Scope: SSL, TLS, PKI and adjacent systems

**Read when:** the request says “SSL”, or several security technologies are being conflated.

## Separate four layers

**TLS is the channel protocol.** It authenticates peers according to the application's rules and protects traffic between its endpoints. **X.509 is a certificate format and validation ecosystem.** **PKI is the operating system around keys, identities, issuers and relying parties.** **HTTPS is HTTP carried over an authenticated TLS connection.** A certificate does not itself encrypt a database, authorize a user, or make a website honest.

In a design discussion, replace “we need SSL” with a precise statement: “The service at reference identity `api.example.com` must authenticate to these clients; traffic must be encrypted across these links; selected workloads must also authenticate with client certificates.” This exposes which trust stores and enrollment systems are necessary.

## Technology map

| Form | What to establish first | Correct branch |
|---|---|---|
| TLS over a byte stream, including HTTPS | Server identity, trust, application protocol | Handshake, clients, deployment |
| Implicit TLS or STARTTLS | Whether TLS starts immediately or after an application exchange | Email and protocol debugging |
| Mutual TLS | Client identity, enrollment entitlement and authorization | Private PKI and mTLS |
| QUIC / HTTP/3 | QUIC transport and TLS handshake support, usually UDP | Datagram and alternate forms |
| DTLS | Datagram application, peer identity and library version | Datagram and alternate forms |
| TLS with PSKs or raw public keys | Secure identity/key provisioning without ordinary Web PKI | Datagram and alternate forms |
| EAP-TLS / certificate-based access | Supplicant, authenticator, authentication server, identity policy | Devices and access networks |
| S/MIME, code/document signing, SSH certificates | Different purposes, trust models and validation rules | Separate specialist design |

WireGuard and ordinary SSH are not TLS. IPsec certificate authentication is not automatically “SSL VPN.” A product's marketing name cannot establish its wire protocol.

## Baseline vocabulary

A **subject** is the entity described by a certificate, an **issuer** signs it, a **subscriber** obtains it, and a **relying party** decides whether to accept it. A **trust anchor** is an input to validation, installed by policy; self-signing does not create universal trust. A **leaf** is an end-entity certificate, not an issuer. An **intermediate CA** delegates issuance beneath an anchor.

A **trust domain** is an administrative boundary, not simply a DNS suffix. DNS names, workload URIs, organization names and application account IDs are different identity namespaces. Do not interchange them because they appear in one certificate.

## Scope discipline

This package covers the shared engineering mechanisms and decision procedures. It does not claim to enumerate every vendor switch or every national accreditation scheme. When a task involves a regulated identity/signature purpose, introduce the applicable specialist standards and legal requirements instead of transplanting Web PKI rules.

## Primary references

- **RFC9846** — [TLS 1.3 — July 2026 revision](https://datatracker.ietf.org/doc/html/rfc9846).
- **RFC5280** — [X.509 certificates and CRLs / PKIX](https://www.rfc-editor.org/rfc/rfc5280.html).
- **RFC9525** — [Service identity verification in TLS](https://www.rfc-editor.org/rfc/rfc9525.html).
- **RFC9001** — [Using TLS to secure QUIC](https://www.rfc-editor.org/rfc/rfc9001.html).
- **RFC9147** — [DTLS 1.3](https://datatracker.ietf.org/doc/html/rfc9147).
- **SPIFFE** — [SPIFFE concepts, identities and workload API](https://spiffe.io/docs/latest/spiffe-about/spiffe-concepts/).

Reference snapshot: **2026-10-10**. For dated policy, distinguish current rules from future effective dates.
