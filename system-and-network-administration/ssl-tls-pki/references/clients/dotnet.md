# .NET, SslStream and HTTP client policy

**Read when:** building .NET clients or comparing Windows and Linux behavior.

## Platform and API matter

SslStream uses platform-dependent TLS facilities. Windows and Linux can therefore differ in trust, supported algorithms, revocation behavior and diagnostics even with the same application source. Record .NET runtime, OS/backend and the actual handler configuration.

Use the intended TargetHost/reference identity and normal certificate validation. Prefer supported OS/runtime defaults unless a documented application policy requires explicit bounds. Do not return true unconditionally from a remote-certificate validation callback; that can disable both trust and name protection.

## HTTP versus raw TLS

HttpClient/SocketsHttpHandler add URL identity, connection pooling, proxies and HTTP behavior. A raw SslStream check is a useful lower-layer experiment but does not reproduce the entire application. Test the real handler's trust and client-certificate configuration.

If a custom validation callback is necessary, define precisely which additional constraint it enforces and preserve normal errors unless the application deliberately implements an alternative authenticated trust model. Include negative tests for every exception path.

## mTLS and certificate access

A client certificate must include a usable private key with permissions for the actual service identity. Certificate-store selection, provider support and key access can fail independently of server authentication. Avoid distributing an exportable shared client credential across unrelated services.

## Verification checklist

Reproduce with the same runtime and service account, verify target name and trust source, inspect OS/runtime chain errors, then test rotation using new connections. Document revocation policy explicitly. A successful HTTPS response does not prove that the application demanded a client certificate or enforced its identity's authorization.

## Primary references

- **DOTNET-SSL** — [Microsoft SslStream best practices](https://learn.microsoft.com/en-us/dotnet/core/extensions/sslstream-best-practices).
- **SCHANNEL** — [TLS cipher suites in Windows 11 / Schannel](https://learn.microsoft.com/en-us/windows/win32/secauthn/tls-cipher-suites-in-windows-11).
- **MS-ROOT** — [Microsoft Trusted Root Program requirements](https://learn.microsoft.com/en-us/security/trusted-root/program-requirements).
- **RFC9525** — [Service identity verification in TLS](https://www.rfc-editor.org/rfc/rfc9525.html).

Reference snapshot: **2026-10-10**. For dated policy, distinguish current rules from future effective dates.
