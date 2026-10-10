# Protocol versions, algorithms and compatibility policy

**Read when:** selecting a TLS baseline or interpreting old hardening advice.

## Policy snapshot, not a timeless cipher string

As reviewed on 2026-10-10, RFC 9846 is the revised TLS 1.3 specification, superseding RFC 8446 while retaining the same protocol version. TLS 1.0 and 1.1 are deprecated; SSL 2 and SSL 3 are not deployment targets. RFC 9851 freezes TLS 1.2 feature development. RFC 9852 requires new application protocols using TLS to support TLS 1.3; that is not a declaration that every existing TLS 1.2 service is automatically unusable.

RFC 10015 changes older TLS/DTLS 1.2 guidance: finite-field DH/DHE and RSA key exchange are deprecated with mandatory non-use requirements; static ECDH is discouraged. This is not a ban on RSA signatures or ECDHE, and its scope must not be misapplied to TLS 1.3 finite-field groups.

## Proposed deployment baseline

For a new controlled environment, prefer TLS 1.3. Retain TLS 1.2 only for demonstrated client requirements, using modern ECDHE and AEAD suites supported by the implementation and organizational policy. Keep a removal owner and deadline for compatibility exceptions. Never enable an obsolete version across all services to accommodate one device.

Algorithm settings occur at several layers: protocol versions, TLS 1.2 cipher suites, TLS 1.3 cipher suites, signature schemes, certificate signatures, key-exchange groups, key sizes, providers and system security levels. A single `ciphers` directive rarely governs all of them.

## Compatibility procedure

Build the client matrix before removing algorithms. Include embedded clients, backup software, health checks, Java runtimes and outbound proxies. Test both RSA and ECDSA certificate paths when dual certificates are under consideration; choosing an ECDSA leaf also requires the client to validate every issuer signature in the selected path.

Change one policy dimension at a time in staging. Capture the negotiated result and rejection behavior, not just HTTP success. A client may silently use another endpoint, address family, proxy or protocol version.

Avoid perpetual copy-paste cipher strings. Record why each exception exists, which client needs it, and which patched backend enforces it. A crypto-policy change at OS level can affect unrelated services; prefer narrowly scoped service configuration and a tested rollback.

## Procurement and compliance

“Supports TLS 1.3,” “FIPS validated,” “post-quantum,” and “browser trusted” answer different questions. Require evidence for the exact module, build, operating mode, trust program, certificate profile and deployed client population. Refer compliance decisions to the applicable policy owner rather than treating a scanner grade as certification.

## Primary references

- **RFC9846** — [TLS 1.3 — July 2026 revision](https://datatracker.ietf.org/doc/html/rfc9846).
- **RFC8996** — [Deprecating TLS 1.0 and TLS 1.1](https://datatracker.ietf.org/doc/html/rfc8996).
- **RFC9851** — [TLS 1.2 feature freeze](https://datatracker.ietf.org/doc/html/rfc9851).
- **RFC9852** — [New protocols using TLS must require TLS 1.3](https://www.rfc-editor.org/rfc/rfc9852.html).
- **RFC10015** — [Deprecating obsolete key exchange methods in TLS 1.2 and DTLS 1.2](https://datatracker.ietf.org/doc/html/rfc10015).
- **RFC9325** — [Recommendations for secure use of TLS and DTLS](https://www.rfc-editor.org/rfc/rfc9325.html).
- **OPENSSL-MIGRATION** — [OpenSSL 3.5 migration guide](https://docs.openssl.org/3.5/man7/ossl-guide-migration/).
- **SCHANNEL** — [TLS cipher suites in Windows 11 / Schannel](https://learn.microsoft.com/en-us/windows/win32/secauthn/tls-cipher-suites-in-windows-11).

Reference snapshot: **2026-10-10**. For dated policy, distinguish current rules from future effective dates.
