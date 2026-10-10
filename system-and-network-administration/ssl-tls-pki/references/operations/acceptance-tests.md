# Acceptance tests for TLS and PKI changes

**Read when:** approving a new service, certificate profile, client library or CA migration.

## Required result format

For every test record scope, versions, inputs, expected result, observed result, evidence and limitations. “Rejected” is a passing security test when rejection was expected. Mark unexecuted tests explicitly.

## Baseline matrix

| Area | Positive case | Negative / failure case |
|---|---|---|
| Trust/path | Approved leaf + intermediates + root | Unknown root, missing intermediate, invalid CA |
| Identity | Intended DNS/IP SAN | Wrong name, SAN/CN conflict, invalid wildcard scope |
| Purpose | ServerAuth server, clientAuth client | Client-only leaf as server, server-only leaf as client |
| Time | Valid path and correct clock | Expired leaf/issuer, future leaf, stale live deployment |
| Revocation | Accepted current status under policy | Revoked/stale/unreachable status with documented behavior |
| Protocol | Intended TLS versions and ALPN | Obsolete or unsupported negotiation, wrong initiation mode |
| mTLS | Approved client and authorization | Missing cert, untrusted issuer, wrong identity, denied role |
| Rotation | New key/cert/bundle reaches consumers | Mismatch, failed reload, one stale replica |
| Enrollment | Authorized profile request | Cross-tenant SAN, CA:true, excessive lifetime, replayed bootstrap |
| Recovery | Issuer/trust state restored safely | Expired recovery dependencies, missing key custody material |

## Test at the right layer

Offline certificate validation is fast and deterministic, but cannot prove deployment. A loopback TLS test exercises real handshakes but not public DNS, browser policy or production routing. A production-like staging test proves more integration but still needs scope-specific failure injection and monitoring.

Use at least one independent implementation when interoperability matters. Python, curl and the OpenSSL CLI can all share OpenSSL; treating them as three independent validators exaggerates the evidence. Go and Java provide additional implementation paths in this package's lab where available.

## Change gate

Before activation, require a validated candidate, known-good eligible rollback, tested deployment mechanism and observable endpoints. After activation, compare live fingerprints and repeat the original application workflows. For root changes, require client trust convergence before switching issuance broadly.

## Scope of this package

The [lab report](../../validation/REPORT.md) lists exactly which cases ran. It does not claim browser CT/revocation testing, public ACME validation, Windows/macOS/mobile coverage, live OpenBao/step-ca/SPIRE operation, Kubernetes integration, QUIC/DTLS support or formal compliance certification. Those remain deployment acceptance work even when the local suite is green.

## Primary references

- **OPENSSL-VERIFY** — [OpenSSL 3.5 verification options](https://docs.openssl.org/3.5/man1/openssl-verification-options/).
- **PY-SSL** — [Python ssl library](https://docs.python.org/3/library/ssl.html).
- **GO-TLS** — [Go crypto/tls](https://pkg.go.dev/crypto/tls).
- **JAVA-JSSE** — [Java 25 JSSE reference guide](https://docs.oracle.com/en/java/javase/25/security/java-secure-socket-extension-jsse-reference-guide.html).
- **CERTBOT** — [Certbot user guide](https://eff-certbot.readthedocs.io/en/stable/using.html).
- **CM-CERT** — [cert-manager Certificate resources and renewal](https://cert-manager.io/docs/usage/certificate/).
- **SSLYZE** — [SSLyze maintained documentation](https://nabla-c0d3.github.io/sslyze/documentation/).

Reference snapshot: **2026-10-10**. For dated policy, distinguish current rules from future effective dates.
