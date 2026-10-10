# Windows, Schannel and application-specific trust

**Read when:** Windows behaves differently from a Linux/OpenSSL test.

## Identify the backend and security context

Many Windows applications use Schannel and Windows certificate stores; others bundle OpenSSL, NSS, Java or their own roots. Record the application's actual backend before modifying Schannel settings. A curl build on Windows is not necessarily a Schannel build.

Distinguish Current User and Local Machine stores and the account running a service or scheduled task. An interactive user's imported root or client certificate may be invisible to a service. A client certificate also requires access to its private key, possibly through a CSP/KSP or hardware provider.

## Diagnostic sequence

Inspect the expected root/intermediate/client-certificate stores in the correct context. Check certificate validity, intended purposes, chain-building/revocation events and application logs. Enable relevant Windows certificate-chain/Schannel diagnostics only within approved logging scope, then correlate timestamps with a reproducible request.

Do not conclude “Windows trusts it” from one browser. The application may have an explicit trust configuration, different revocation behavior or a service-account permission problem. Test the exact application path.

## Configuration safety

Schannel protocol and cipher policies depend on OS release and administrative policy. Group Policy or security baselines can override local changes. Use the current Microsoft documentation for the deployed Windows build and test the scope of any change.

Avoid blanket registry recipes that disable verification or re-enable obsolete protocols for every process. Resolve missing roots, wrong identities and key permissions directly. Exporting a certificate without its private key will not create a usable mTLS credential; exporting with the key creates a sensitive artifact requiring custody controls.

## Migration acceptance

Test the intended root installation, unknown-root rejection, server name mismatch, expired certificate and client-key access under the service account. Reproduce after reboot and policy refresh. Document trust removal and credential cleanup, including dormant user profiles or service identities where relevant.

## Primary references

- **SCHANNEL** — [TLS cipher suites in Windows 11 / Schannel](https://learn.microsoft.com/en-us/windows/win32/secauthn/tls-cipher-suites-in-windows-11).
- **MS-ROOT** — [Microsoft Trusted Root Program requirements](https://learn.microsoft.com/en-us/security/trusted-root/program-requirements).
- **CURL-TRUST** — [curl TLS certificate verification](https://curl.se/docs/sslcerts.html).
- **DOTNET-SSL** — [Microsoft SslStream best practices](https://learn.microsoft.com/en-us/dotnet/core/extensions/sslstream-best-practices).

Reference snapshot: **2026-10-10**. For dated policy, distinguish current rules from future effective dates.
