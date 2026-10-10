# Client capability and trust matrix

**Read when:** choosing compatible certificates or explaining different results between clients.

## The client is more than its application name

Record application version, TLS backend/build, OS version, root-store source, application overrides, proxy path and process restart time. “curl works” is weak evidence unless its backend and trust match the failing consumer.

| Dimension | Collect | Test case |
|---|---|---|
| Transport | TCP TLS, STARTTLS, QUIC or DTLS | Correct protocol initiation |
| Cryptography | Versions, suites, groups, signatures, key formats | Supported and intentionally unsupported choices |
| Identity | SNI and reference DNS/IP/URI rules | Wrong name and SAN/CN conflict |
| Trust | System, bundled or explicit anchors; update/reload | Unknown root and root migration |
| Path building | Intermediate cache/AIA, constraints | Missing intermediate and alternate chain |
| Policy | EKU, CT, revocation, local restrictions | Wrong purpose, revoked leaf where enforced |
| Client auth | Key store, selection, chain and authorization | No client cert and unauthorized identity |
| Environment | Time, proxies, IPv4/IPv6, containers | Reboot, clean image and alternate route |

## Minimum evidence record

For each supported client population capture a repeatable invocation or application test, expected identity, trust source and observed result. Do not record only a screenshot of a browser padlock. Include freshly provisioned clients so cached intermediates and legacy exceptions cannot conceal missing deployment material.

## Secure API contract

The API must require certificate-chain validation and the intended identity. These are separate settings in several low-level APIs. Supply SNI where needed for DNS virtual hosts, but do not mistake it for identity enforcement. Require an explicit purpose and handle handshake/verification errors as failures.

Library defaults differ and change. A high-level HTTPS client may enable name verification that a raw socket API does not. A custom CA option may replace, rather than extend, default roots. A certificate-verification callback can silently nullify the library's normal protection.

## What success does not prove

A successful handshake is not proof of revocation enforcement, CT compliance, the right application response, client authorization, secure redirects or absence of a TLS-intercepting corporate proxy. Test each property required by the threat model.

Use the OS and language-specific references next. The examples in this package use explicit trust and identity, but they are not a replacement for production tests of the application's exact HTTP/database stack.

## Primary references

- **CURL-TRUST** — [curl TLS certificate verification](https://curl.se/docs/sslcerts.html).
- **PY-SSL** — [Python ssl library](https://docs.python.org/3/library/ssl.html).
- **NODE-TLS** — [Node.js TLS API](https://nodejs.org/api/tls.html).
- **GO-TLS** — [Go crypto/tls](https://pkg.go.dev/crypto/tls).
- **JAVA-JSSE** — [Java 25 JSSE reference guide](https://docs.oracle.com/en/java/javase/25/security/java-secure-socket-extension-jsse-reference-guide.html).
- **DOTNET-SSL** — [Microsoft SslStream best practices](https://learn.microsoft.com/en-us/dotnet/core/extensions/sslstream-best-practices).
- **PERL-SSL** — [IO::Socket::SSL author-maintained POD](https://metacpan.org/pod/IO::Socket::SSL).

Reference snapshot: **2026-10-10**. For dated policy, distinguish current rules from future effective dates.
