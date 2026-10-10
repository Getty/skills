# Failure signatures and discriminating tests

**Read when:** an error message needs interpretation without guessing a fix.

Error strings and numeric codes vary by backend. Treat them as clues, not universal diagnoses.

| Symptom | Competing causes | Discriminating test |
|---|---|---|
| Unknown issuer / unable to get local issuer | Missing intermediate, wrong roots, alternate-path issue | Save transmitted chain; verify with explicit untrusted intermediates and approved anchors |
| Hostname mismatch | Wrong SAN, wrong SNI/vhost, wrong reference name | Compare URL/configured identity with SAN and per-address live certificate |
| Expired / not yet valid | Leaf/issuer time bounds, wrong client clock, stale deployment | Check every selected path certificate and both clocks; compare live fingerprint |
| Wrong version number | Plaintext port, proxy greeting, STARTTLS mismatch | Inspect protocol greeting and use the correct upgrade mode |
| No shared cipher / handshake failure | Version, group, signature, key-type or policy conflict | Force one compatible dimension and inspect offers/server logs |
| Unsupported certificate / unsuitable purpose | Wrong EKU/KU, CA status or profile | Offline purpose validation with the exact leaf and chain |
| Certificate required | mTLS demanded, client sent none | Inspect certificate request, key selection and application configuration |
| Unknown CA alert after client cert | Server rejects client issuer/chain | Server-side client trust and transmitted client intermediates |
| HTTP 403 after TLS succeeds | Application authorization, WAF or tenant routing | Inspect authenticated principal and authorization decision |
| Works only after browser visit | Cached/fetched intermediate | Fresh client/store and complete server-sent chain |
| Works on one node/address family | Uneven deployment, DNS or network path | Address-pinned probes retaining the same identity |
| Renewal success, old certificate live | Reload/mount/replica mismatch | Candidate/live fingerprints and process reload evidence |

## Determine which peer rejected which certificate

A TLS alert received by the client may describe the server's rejection of a client certificate, not the client's validation of the server. Correlate both endpoints. TLS 1.3 client-authentication failures can appear during subsequent reads/writes rather than at the first apparent client-side handshake completion.

## Do not overinterpret expiry

An expired leaf is only one possibility. An intermediate can expire while the leaf remains within its own dates. A process can continue serving an older generation after successful issuance. A client with a wrong clock can reject a perfectly current deployment.

## Minimal experiment design

Preserve the failed certificate and configuration before replacement. Choose one small test that distinguishes the competing causes. Record rejected cases as successes of the security policy, not necessarily as bugs. A test suite should fail when a wrong-name certificate is accepted, not when it is correctly refused.

## Primary references

- **OPENSSL-SCLIENT** — [OpenSSL 3.5 s_client](https://docs.openssl.org/3.5/man1/openssl-s_client/).
- **OPENSSL-VERIFY** — [OpenSSL 3.5 verification options](https://docs.openssl.org/3.5/man1/openssl-verification-options/).
- **PY-SSL** — [Python ssl library](https://docs.python.org/3/library/ssl.html).
- **GO-TLS** — [Go crypto/tls](https://pkg.go.dev/crypto/tls).
- **JAVA-JSSE** — [Java 25 JSSE reference guide](https://docs.oracle.com/en/java/javase/25/security/java-secure-socket-extension-jsse-reference-guide.html).
- **PG-SERVER** — [PostgreSQL 18 server TLS](https://www.postgresql.org/docs/18/ssl-tcp.html).
- **CERTBOT** — [Certbot user guide](https://eff-certbot.readthedocs.io/en/stable/using.html).

Reference snapshot: **2026-10-10**. For dated policy, distinguish current rules from future effective dates.
