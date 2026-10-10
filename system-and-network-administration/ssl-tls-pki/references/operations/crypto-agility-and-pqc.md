# Crypto agility, post-quantum migration and compliance claims

**Read when:** planning algorithm transitions or evaluating “post-quantum TLS” claims.

## Distinguish three migrations

A post-quantum or hybrid **key exchange** addresses how connection secrets are established. A post-quantum **certificate signature** changes how an issuer authenticates a public key. A different **credential format or trust infrastructure** changes additional deployment assumptions. One does not automatically deliver the others.

NIST's post-quantum standardization work provides algorithm standards. It does not imply that every TLS library, browser, root program, HSM and certificate profile can already use each algorithm interoperably. Check the protocol integration and deployed implementation, not just the algorithm name.

## Current ecosystem caution

Let’s Encrypt's June 2026 Merkle Tree Certificates publication describes plans for a post-quantum direction. This package does not present that plan as an already generally available replacement for its ordinary public certificates.

Likewise, a TLS group appearing in a library's algorithm list does not establish browser trust for a new signature algorithm. Record specification status, exact code point/profile, implementation version, fallback behavior and supported client population.

## Migration inventory

Locate every place algorithms or credentials are constrained: CA/HSM, enrollment templates, CSR generators, TLS terminators, language libraries, old devices, scanners, certificate parsers, pinning, backup/recovery tools and monitoring. Rigid assumptions about RSA moduli, fixed certificate sizes or issuer subject fields can fail even before cryptographic compatibility does.

Measure handshake size, CPU/memory, fragmentation and latency on actual networks. Test middleboxes and clients with limited buffers. Do not respond to a larger handshake by silently removing verification or weakening the minimum protocol.

## Compliance evidence

Separate security intent from certification. “FIPS,” “publicly trusted,” “CA/B compliant,” and “post-quantum” refer to different evidence. Require the applicable document/version, exact module/build, mode of operation and permitted deployment scope. A general-purpose test lab does not certify compliance.

## Practical design recommendation

Keep algorithm policy in versioned profiles; use algorithm-independent key comparison; preserve alternate trusted deployment paths where justified; avoid hardcoded leaf/issuer assumptions; and build negative interoperability tests. Rehearse key and issuer replacement before an urgent ecosystem migration makes it mandatory.

## Primary references

- **NIST-PQC** — [NIST post-quantum cryptography project](https://csrc.nist.gov/projects/post-quantum-cryptography).
- **LE-PQC** — [Let’s Encrypt plans for Merkle Tree Certificates](https://letsencrypt.org/2026/06/03/pq-certs).
- **OPENSSL-MIGRATION** — [OpenSSL 3.5 migration guide](https://docs.openssl.org/3.5/man7/ossl-guide-migration/).
- **RFC9846** — [TLS 1.3 — July 2026 revision](https://datatracker.ietf.org/doc/html/rfc9846).
- **CHROME-ROOT** — [Chrome Root Program policy](https://googlechrome.github.io/chromerootprogram/crp/policy/).
- **CABF-BR** — [CA/Browser Forum TLS Baseline Requirements — current HTML](https://cabforum.org/working-groups/server/baseline-requirements/requirements/).

Reference snapshot: **2026-10-10**. For dated policy, distinguish current rules from future effective dates.
