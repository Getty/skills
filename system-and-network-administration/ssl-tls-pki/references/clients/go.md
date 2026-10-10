# Go crypto/tls and crypto/x509

**Read when:** building Go clients, trust pools or mTLS services.

## Explicit roots and expected identity

Use a `tls.Config` with the intended `ServerName`, an appropriate root pool and a minimum protocol version. Leave `InsecureSkipVerify` false. A nil RootCAs requests system roots; a custom pool creates a different trust decision. Check errors from loading system roots and verify that `AppendCertsFromPEM` actually parsed certificates.

When connecting to a fixed IP for a DNS service, keep the DNS identity in `ServerName`. Use a dialer/context deadline, close the connection and handle handshake and subsequent I/O errors. The included Go probe is compiled without third-party dependencies.

## Client authentication

For servers requiring mTLS, use a policy such as `RequireAndVerifyClientCert` with a deliberate ClientCAs set. Loading a server certificate does not configure client trust. After TLS verification, apply explicit authorization to the accepted certificate identity.

Review custom verification callbacks carefully. A callback can add constraints to normal verification or replace parts of it depending on configuration. Never set `InsecureSkipVerify` merely because a callback “will probably check it later.”

## Validation boundaries

Go's X.509 package does not automatically become a browser CT/revocation-policy engine. Document any required revocation checking, pinning, trust-domain or URI-identity handling separately. Modern Go name verification does not rescue a certificate that lacks the required SAN by treating a legacy Common Name as its service identity.

Certificate and crypto defaults evolve across Go releases. Record the actual toolchain and relevant environment/GODEBUG overrides in compatibility investigations. A current package website can describe behavior newer than the deployed binary.

## Tests

Use the real `http.Transport`, database driver or RPC stack after the raw TLS check. Test wrong names, unknown roots, wrong EKU, incomplete chains and rotation with pooled connections. The lab also runs a Go/OpenSSL cross-implementation comparison, which is stronger evidence than repeating one OpenSSL command through several wrappers, but still not universal interoperability proof.

## Primary references

- **GO-TLS** — [Go crypto/tls](https://pkg.go.dev/crypto/tls).
- **GO-X509** — [Go crypto/x509](https://pkg.go.dev/crypto/x509).
- **RFC9525** — [Service identity verification in TLS](https://www.rfc-editor.org/rfc/rfc9525.html).

Reference snapshot: **2026-10-10**. For dated policy, distinguish current rules from future effective dates.
