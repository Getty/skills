# Incident response, certificate linting and authorized scanning

**Read when:** checking deployment security or responding to possible compromise.

## Tools answer different questions

OpenSSL/curl and the supplied probe can test a particular connection and verification policy. SSLyze can inspect server TLS configuration and selected known vulnerability conditions. ZLint checks certificate/profile consistency against its supported rules. SSL Labs offers an externally hosted assessment/API for suitable public endpoints.

None of these independently proves complete application security, correct enrollment authorization, recoverable CA operations or every supported client's behavior. Linting is not path validation; a scanner grade is not a certificate of compliance.

## Safe assessment plan

Obtain scope approval, target names/addresses, time window, rate/concurrency limits and permitted test classes. Check scanner version and supported options before execution. Start with a narrow test and preserve structured results. Some scans make many handshakes and vulnerability probes; do not run them indiscriminately against fragile appliances.

External scanners can disclose internal names and endpoint metadata and may not reach private networks. Do not upload confidential certificates, keys or captures. The local lab does not run any external scanner or scan public services.

## Triage findings

Classify failures by actual risk and affected clients: missing identity verification, unauthorized trust, obsolete protocol acceptance, weak issuance policy, incomplete chain, expiry, revocation or operational drift. Confirm surprising findings with another method and the server's actual configuration.

A test that a tool cannot perform is “not assessed,” not “passed.” Scanner defaults and grading policies evolve; retain raw evidence and versions so results can be compared meaningfully.

## Compromise response

Identify the exposed authority: leaf key, account key, DNS credential, enrollment token, intermediate or root. Contain that authority, preserve audit evidence, enumerate potentially issued/used identities and execute the appropriate replacement/revocation/trust-removal plan. Review long-lived sessions and repeated enrollment.

Replace keys where needed, not merely certificates containing the same compromised key. Investigate the path of exposure before redistributing replacements through it. Use authenticated communications for new trust material and verify containment with negative tests.

## Primary references

- **SSLYZE** — [SSLyze maintained documentation](https://nabla-c0d3.github.io/sslyze/documentation/).
- **ZLINT** — [ZLint project documentation](https://github.com/zmap/zlint).
- **SSLLABS** — [Qualys SSL Labs API/project documentation](https://www.ssllabs.com/projects/ssllabs-apis/).
- **OPENSSL-VERIFY** — [OpenSSL 3.5 verification options](https://docs.openssl.org/3.5/man1/openssl-verification-options/).
- **OPENBAO-CONSIDER** — [OpenBao PKI design considerations](https://openbao.org/docs/secrets/pki/considerations/).
- **RFC5280** — [X.509 certificates and CRLs / PKIX](https://www.rfc-editor.org/rfc/rfc5280.html).

Reference snapshot: **2026-10-10**. For dated policy, distinguish current rules from future effective dates.
