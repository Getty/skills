# Critical-claim evidence ledger

**Three complementary review layers, not three independent audits.** Standards/policies define obligations; implementation documentation identifies real interfaces and defaults; executable tests check a deliberately bounded subset. Policy announcements cannot be proved by a local handshake. When a layer does not apply or was not executed, the table says so.

Test IDs refer to [results.json](../validation/results.json). `EXT-*` denotes the six concrete runtime groups recorded there. Source IDs resolve through [SOURCES.md](SOURCES.md). The run’s strengths and limits are in [REPORT.md](../validation/REPORT.md).

| Critical claim | Standards / policy authority | Implementation / operator evidence | Executed evidence | Limits |
|---|---|---|---|---|
| Trust is configured, not created by sending a root | RFC5280; RFC9846 | OPENSSL-VERIFY; GO-X509 | PATH-02; ROOT-02; ROOT-03 | Only the selected test roots and path rules were exercised. |
| A presented chain is not a successfully built path | RFC5280 | OPENSSL-SCLIENT; OPENSSL-VERIFY | PATH-01; PATH-03; EXT-*-CHAIN | AIA retrieval and browser intermediate caches were not reproduced. |
| Reference identity and SNI are different inputs | RFC9525; RFC6066 | PY-SSL; CURL-MAN | TLS-P01; TLS-P02; TLS-P03 | IP reference verification works without a DNS SNI value. |
| IP identity needs an IP SAN, not a numeric DNS SAN | RFC9525 | OPENSSL-VERIFY; GO-X509 | NAME-02; NAME-03; TLS-P02 | Other application-specific legacy behavior must be tested separately. |
| Wildcard matching does not cover the apex or arbitrary depth | RFC9525 | OPENSSL-VERIFY; PY-SSL | NAME-04; NAME-05; NAME-06; TLS-P11; TLS-P12 | Test identities use an owned-by-nobody .test namespace. |
| Legacy CN fallback varies; modern policy must be explicit | RFC9525 | OPENSSL-VERIFY; PY-SSL; GO-X509 | NAME-07; NAME-08; TLS-P09; TLS-P10; GO-CN-ONLY | OpenSSL legacy acceptance is intentionally recorded rather than presented as best practice. |
| EKU limits intended certificate use | RFC5280 | OPENSSL-VERIFY; JAVA-JSSE | EKU-01; EKU-02; EKU-03; EXT-*-EKU; MTLS-03 | Omission of EKU and application-specific EKU processing require additional profile tests. |
| Leaf and issuer validity both matter | RFC5280 | OPENSSL-VERIFY; PY-SSL | TIME-01; TIME-02; TIME-03; TLS-P07; TLS-P08 | Real CA clocks and public-chain expiry events were not tested. |
| Basic constraints, name constraints and critical extensions must be enforced | RFC5280 | OPENSSL-VERIFY | CONSTRAINT-01 through CONSTRAINT-05 | Not an exhaustive X.509 conformance suite. |
| Cross-signing changes available paths, not trust by itself | RFC5280 | OPENSSL-VERIFY | CROSS-01; CROSS-02 | One cross-signed intermediate and two trust anchors; not every path-building heuristic. |
| Revocation knowledge is not automatically enforced | RFC5280; RFC6960 | OPENSSL-VERIFY; PY-SSL | CRL-01 through CRL-04 | Local leaf CRL policy only; no live OCSP, browser CRLSet or complete-issuer CRL enforcement. |
| TLS versions and RSA authentication are distinct from RSA key exchange | RFC9846; RFC9325; RFC10015 | OPENSSL-SCLIENT; PY-SSL | TLS-P14; TLS-P15; TLS-P16; TLS-P17 | Demonstrates TLS 1.2 ECDHE-RSA, not certification of every new RFC requirement. |
| TLS client authentication is not application authorization | RFC9846; RFC5280 | PY-SSL; SPIFFE | MTLS-01 through MTLS-06 | Exact URI allowlist is a lab authorization rule, not a full SPIFFE implementation. |
| mTLS failure may be seen after the client handshake | RFC9846 | PY-SSL | MTLS-02; MTLS-03; MTLS-04; MTLS-06 | Specific server verifier evidence is required when the client sees a transport reset. |
| Certificate/key consistency and custody are distinct checks | RFC5280 | OPENSSL-X509; PY-SSL; CRYPTO-X509 | KEY-01; KEY-02; LOCAL-01 | 0600 lab keys do not constitute HSM custody or a production root ceremony. |
| Parsing or printing a certificate does not validate its trust | RFC5280 | OPENSSL-X509; CRYPTO-X509 | INSPECT-01 through INSPECT-05 | The bundled inspector explicitly reports inspection_only and trust_verified=false. |
| A secure reverse proxy must authenticate its upstream independently | RFC9525 | NGINX-PROXY | NGINX-CONFIG-*; NGINX-LIVE-GOOD; NGINX-LIVE-BAD-NAME | Template was tested after local identity/path/port substitutions; no production proxy was modified. |
| CA/B lifetime limits depend on issuance date and purpose | CABF-BR; CABF-SC081 | LE-PROFILES; LE-64D; LE-45D | Documentary only; see policy calendar | Not experimentally established by a two-day private laboratory certificate. |
| Let’s Encrypt profiles, default lifetimes and future changes differ | LE-PROFILES; LE-64D; LE-45D | CERTBOT | Documentary only; no production ACME order | The 2026-10-14 staging and 2027-02-10 production changes were still future at this snapshot. |
| Let’s Encrypt stopped clientAuth issuance before the Chrome leaf deadline | LE-CLIENTAUTH; CHROME-ROOT | LE-PROFILES | Documentary only | Do not confuse 2026 subordinate policy with 2027 subscriber-certificate requirements. |
| Let’s Encrypt OCSP end of life is not an end to all revocation | LE-OCSP; RFC5280 | LE-PROFILES | Documentary plus generic CRL tests; no live LE revocation test | The CRL fixtures prove the mechanism, not the operator’s production service. |
| ARI, renewal eligibility and deployment success are separate | RFC9773; RFC8555 | LE-LIMITS; CERTBOT; CM-CERT | No live ACME or deployment-hook execution | A successful YAML parse or hook syntax check is not a successful renewal. |
| DNS-PERSIST-01 announcement does not prove general availability | LE-PERSIST; LE-45D | LE-CHALLENGES | Documentary only; recheck before using | No undocumented API or challenge implementation is invented. |
| CT protocol publication and deployed browser/log policy differ | RFC9162 | CHROME-CT; LE-CT-STATIC | Documentary only | No CT inclusion/consistency-proof or browser acceptance test was executed. |
| Client trust behavior depends on OS, runtime and backend | RFC5280; RFC9525 | PY-SSL; GO-X509; JAVA-JSSE; NODE-TLS; PERL-SSL; CURL-TRUST | EXT-OPENSSL-*; EXT-CURL-*; EXT-NODE-*; EXT-PERL-*; EXT-GO-*; EXT-JAVA-* | Linux matrix only; Windows, macOS, Android, iOS and browser behavior remains documentary. |
| PostgreSQL encryption-only modes are not verify-full | PG-CLIENT; PG-SERVER | OPENSSL-SCLIENT | Documentary only; no PostgreSQL service started | The single-line conninfo example is reviewed guidance, not a live database acceptance result. |
| Post-quantum key establishment is not a complete post-quantum Web PKI | RFC9846; NIST-PQC | OPENSSL-MIGRATION; LE-PQC | Documentary only | No PQC interoperability, ECH, QUIC or DTLS laboratory is claimed. |

## Reverification procedure

Before changing a security control, re-open the actual source, inspect its effective date and version, identify the real consumer and trust store, reproduce a positive connection, then reproduce the specific rejection that the change must preserve. Keep failure evidence, make the smallest scoped fix, and rerun the consuming application. A tool exit code alone does not identify the cause.

For service policy, record the directory, advertised feature/profile, CA announcement date and effective date. A planned rollout, staging success or draft document must never be upgraded to a production-availability claim without new evidence.
