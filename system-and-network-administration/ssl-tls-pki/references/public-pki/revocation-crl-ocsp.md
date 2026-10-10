# Revocation, CRLs, OCSP and actual client enforcement

**Read when:** designing compromise containment or interpreting revocation-related failures.

## Revoked is not the same as rejected everywhere

A CA can publish revocation information, but a relying client must obtain and enforce it. Behavior differs between browsers, operating systems, libraries and application configuration. Some environments use online OCSP, some CRLs or browser-distributed mechanisms, some soft-fail on network problems, and some perform no automatic revocation checking.

An OCSP status of “good” is not a replacement for normal path, validity, name and purpose checks. CRLs must be authenticated and evaluated for issuer scope and freshness. An unreachable responder is not itself proof of a revoked certificate; it is an availability/policy event that the application must handle deliberately.

## Service-specific facts

Let’s Encrypt shut down its OCSP service on **2025-08-06** and uses CRL-based publication. Therefore “enable OCSP stapling for every Let's Encrypt certificate” is stale universal advice. Inspect the certificate's actual extensions and current issuer documentation. Do not add an OCSP Must-Staple dependency where the selected CA and client population cannot satisfy it.

Other CAs and private infrastructures may still use OCSP. Stapling can avoid a separate client-to-responder lookup, but the server must obtain and refresh acceptable responses. A configured stapling directive is not evidence that a fresh response is being served or required by the client.

## Design a revocation service, not just an extension

Choose the emergency containment objective first. Identify every relying client and its supported enforcement mechanism. Specify distribution URLs, cache lifetimes, freshness alarms, responder/CRL availability, offline behavior and the consequences of failure. Keep publication reachable during CA maintenance and recovery.

Short-lived credentials reduce the time until natural expiration but do not guarantee immediate invalidation. Existing connections and resumable sessions can require separate termination or ticket-state rotation. A root compromise generally requires trust-anchor removal/replacement, not merely publishing a CRL underneath the compromised hierarchy.

## Test both modes

The lab contains a revoked leaf and a signed CRL. Ordinary chain verification can accept that leaf when revocation checking is not enabled. Explicit OpenSSL CRL checking rejects it. This deliberately demonstrates the difference between published status and enforced status.

For production acceptance, simulate stale CRLs, unreachable distribution points and a known revoked leaf in a non-production trust domain. Record the real client's response. Do not claim the Python or Go example provides OCSP/CRL policy merely because its certificate chain verification succeeds.

## Primary references

- **RFC6960** — [Online Certificate Status Protocol](https://www.rfc-editor.org/rfc/rfc6960.html).
- **RFC5280** — [X.509 certificates and CRLs / PKIX](https://www.rfc-editor.org/rfc/rfc5280.html).
- **LE-OCSP** — [Let’s Encrypt OCSP end of life](https://letsencrypt.org/2025/08/06/ocsp-service-has-reached-end-of-life).
- **OPENSSL-VERIFY** — [OpenSSL 3.5 verification options](https://docs.openssl.org/3.5/man1/openssl-verification-options/).
- **GO-X509** — [Go crypto/x509](https://pkg.go.dev/crypto/x509).
- **PY-SSL** — [Python ssl library](https://docs.python.org/3/library/ssl.html).
- **CHROME-ROOT** — [Chrome Root Program policy](https://googlechrome.github.io/chromerootprogram/crp/policy/).

Reference snapshot: **2026-10-10**. For dated policy, distinguish current rules from future effective dates.
