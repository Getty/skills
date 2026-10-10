# C/C++ OpenSSL and Rust TLS integration

**Read when:** integrating TLS below a high-level HTTP library.

## OpenSSL C API: two checks, not one

Configure peer certificate verification and load approved trust. Configure the expected DNS/IP identity through the supported verification API. For DNS virtual hosting, separately set SNI. `SSL_VERIFY_PEER` alone is not a hostname policy; `SSL_set_tlsext_host_name` alone is not hostname verification.

Use `SSL_set1_host` or the documented IP-address verification API as appropriate, check every return value, and handle handshake failure without falling back to plaintext. Do not manually compare subject strings or implement wildcard matching from scratch.

For nonblocking I/O, distinguish retryable WANT_READ/WANT_WRITE from terminal errors. Preserve deadlines and cancellation. Verify that application-level framing detects truncation even when the TLS connection ends unexpectedly. Never reuse a failed TLS object as though it were an authenticated stream.

## Rust

rustls separates protocol machinery, certificate verification, crypto-provider choices and root configuration. Determine whether the application uses bundled Web PKI roots, native roots or an explicit private pool. A crate being memory-safe does not make an intentionally disabled verifier safe.

Avoid dangerous custom verification interfaces unless implementing a reviewed alternative trust model. Check the selected crate/provider versions and supported algorithms. The native-tls ecosystem can instead inherit platform TLS behavior; do not assume all Rust programs use the same backend.

## Prefer higher-level abstractions where appropriate

For ordinary HTTPS, a maintained HTTP library typically handles URI identity, redirects, pooling and connection lifecycle more reliably than hand-built TLS sockets. Still audit its trust options, proxy handling and client-auth configuration.

The package does not provide a production TLS implementation in C or Rust. Use this checklist to review an integration, then create version-specific compile tests and negative handshake tests against its real backend. A successful build proves API compatibility, not correct authentication.

## Primary references

- **OPENSSL-HOST** — [OpenSSL 3.5 SSL_set1_host](https://docs.openssl.org/3.5/man3/SSL_set1_host/).
- **OPENSSL-VERIFY** — [OpenSSL 3.5 verification options](https://docs.openssl.org/3.5/man1/openssl-verification-options/).
- **RUSTLS** — [rustls crate documentation](https://docs.rs/rustls/latest/rustls/).
- **RFC9525** — [Service identity verification in TLS](https://www.rfc-editor.org/rfc/rfc9525.html).
- **RFC9846** — [TLS 1.3 — July 2026 revision](https://datatracker.ietf.org/doc/html/rfc9846).

Reference snapshot: **2026-10-10**. For dated policy, distinguish current rules from future effective dates.
