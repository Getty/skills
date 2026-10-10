# SSL, TLS & PKI Engineering

An English, modular agent skill for designing, operating and debugging authenticated TLS systems—from individual client connections to public Web PKI and private CA infrastructures.

**53 topical reference files · 103 distinct primary sources · 108 executed laboratory assertions**  
**Documentation snapshot: 10 October 2026.** [Validation evidence and limits](validation/REPORT.md).

## Install and start

Install the **entire `ssl-tls-pki/` directory** in the skill directory supported by your agent or skill manager. Do not install only `SKILL.md`: it deliberately routes into relative references, examples, tools and the lab. No vendor-specific plugin manifest or companion skill is required. Check your agent's current skill-loading mechanism for the installation location.

The [506-word entry point](SKILL.md) gives the workflow; [CONTENTS.md](CONTENTS.md) indexes the material by situation. Every topical reference includes a **Read when** condition and its immediate **Primary references**. The full source register and critical-claim evidence ledger are separate, so documentation provenance does not overwhelm the entry point.

Suggested repository category: `system-and-network-administration`, or a dedicated `security-and-cryptography` / `pki` category when your collection warrants it. This is a classification suggestion, not a required directory layout.

## Coverage

| Area | Included material |
|---|---|
| Foundations | SSL versus TLS, TLS 1.2/1.3, handshakes, keys, signatures, certificate profiles, SAN/EKU, chain building, cross-signing, formats and protocol policy |
| Public international trust | Root stores and browser programs, CA/Browser Forum, CCADB, audit/governance boundaries, DV/OV/EV, CAA/DNSSEC, CT, revocation and dated rules |
| ACME and Let's Encrypt | Account/order/authorization/challenge/CSR/finalization, HTTP-01/DNS-01/TLS-ALPN-01, IPs/wildcards, topology, profiles, ARI, renewal, deployment and rate-limit recovery |
| Private infrastructure | Offline-root/issuing-CA separation, policy and profiles, enrollment, key custody, bootstrap, trust distribution, root/issuer rotation, recovery, mTLS authorization, OpenBao, step-ca and SPIFFE |
| Deployment | Termination and re-encryption, NGINX/Apache/Caddy, PostgreSQL, registries/containers/Kubernetes, email/STARTTLS/DANE, devices/EAP/VPN boundaries, QUIC/DTLS and non-X.509 options |
| Clients | Linux, Windows/Schannel, browsers, Apple/Android, Python, Node.js, Go, Java, .NET, Perl and C/C++/Rust; actual trust stores, provider differences and application-specific behavior |
| Debugging | Evidence-first runbook, OpenSSL/curl recipes, failure signatures, DNS/IPv4/IPv6/SNI/ALPN, chain/path/name/purpose failures, packet capture and protected key logs |
| Operations | Renewal/deployment convergence, inventories and monitoring, compromise response, authorized scanning, performance/resumption/0-RTT, crypto agility/PQC and acceptance matrices |

"All forms" is treated as a broad engineering map, not a false promise of implementing every TLS library, CA product, device or historical cipher. Areas without executed integrations are explicitly marked as documentary guidance. Code signing, S/MIME and unrelated PKI uses are distinguished from Web/server TLS rather than silently conflated with it.

## Runnable evidence

Read [the lab guide](labs/README.md), install its Python dependency in an isolated environment, then run from this directory:

```sh
python labs/run_lab.py --output /tmp/ssl-pki-results-01
python tools/validate_package.py
```

Use a **new** output directory. The full suite requires the documented optional runtimes; absent runtimes are reported as skipped. The lab makes no public ACME orders, modifies no OS trust and binds only loopback listeners. Private keys are temporary and never included in the distributed package.

The [examples](examples/README.md) include tested Go, Java, Node and Perl probes, a locally exercised NGINX re-encryption template, and clearly labeled cert-manager/deploy-hook templates. The [TLS CLI](tools/tls_probe.py) does not offer an insecure mode. The [certificate inspector](tools/inspect_cert.py) explicitly distinguishes metadata inspection from trust validation.

## Verification, honestly scoped

Three complementary layers were used: standards/policy review, implementation-documentation review, and local executable experiments. This is **not three independent security audits**. The final complete run reports **108 passed, none failed, none skipped**. A rerun exposed a client-authentication alert/reset observation issue; the harness now requires the matching server verifier evidence. The history and exact versions are preserved in [REPORT.md](validation/REPORT.md).

Go and Java provide implementation diversity; several other clients share OpenSSL and are not counted as independent cryptographic proofs. Browser/mobile/Windows/macOS policy, real ACME issuance, private-CA products, HSMs, QUIC/DTLS/ECH and PQC are not claimed to have been tested here.

## Current-policy maintenance

Read the [policy calendar](references/public-pki/policy-calendar.md) before reusing remembered certificate lifetimes or EKU rules. It separates policy maxima from CA defaults, current profiles from future changes, and operator announcements from implementation availability. In particular, the October 2026 Let's Encrypt staging announcement must not be mistaken for an already-active production default.

Recheck dated claims before production work. The [103-source register](sources/SOURCES.md) and [claim ledger](sources/CLAIMS.md) show where to start. Source text has not been bundled or silently treated as a permanent specification.

## Safety and adaptation

Read [SECURITY.md](SECURITY.md) before testing real endpoints, changing trust, handling private keys or enabling sensitive diagnostic logging. Use the [architecture decision template](examples/architecture-decision-template.md) to record topology, ownership, lifecycle, acceptance tests, rollback and unresolved compatibility. Never repair an error by weakening identity verification or trusting an unauthenticated peer's root.
