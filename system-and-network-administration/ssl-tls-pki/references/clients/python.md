# Python ssl, Requests and explicit verification

**Read when:** writing or debugging Python TLS clients.

## Standard-library TLS

Use `ssl.create_default_context()` for server authentication. Supply the expected DNS name through `server_hostname`; for a literal IP, use the correct IP identity. Keep hostname checking and required certificate verification enabled. Set protocol bounds intentionally when the application needs an explicit policy.

```python
import socket, ssl
ctx = ssl.create_default_context(cafile="approved-roots.pem")
ctx.minimum_version = ssl.TLSVersion.TLSv1_2
ctx.hostname_checks_common_name = False  # SAN-only identity policy
with socket.create_connection(("127.0.0.1", 8443), timeout=5) as raw:
    with ctx.wrap_socket(raw, server_hostname="api.svc.test") as tls:
        print(tls.version(), tls.getpeercert())
```

The connection address and reference name are intentionally different. The provided diagnostic tool uses this pattern without modifying system trust. An explicit CA file selects a deliberate trust input; decide separately whether public default roots should also be loaded.

## Requests is a separate trust configuration

Requests normally verifies HTTPS, but its CA bundle and environment handling can differ from Python's raw `ssl` defaults. Inspect Requests/certifi versions, the `verify` option, `REQUESTS_CA_BUNDLE`, `CURL_CA_BUNDLE`, proxies and prepared-request environment merging where relevant.

Use a CA bundle path, not `verify=False`. Client certificate/key options authenticate the client but do not replace server verification. Requests' convenience API has limitations around encrypted private-key handling; use supported key custody and transport mechanisms rather than hardcoding a passphrase.

## Failure interpretation

Catch certificate-verification errors distinctly from connection timeout, name resolution, HTTP errors and application authentication failure. Do not retry a permanent hostname mismatch indefinitely. Keep certificate details but exclude private key material and authorization headers from logs.

Python/OpenSSL version changes can alter default verification flags and security policy. Record `sys.version` and `ssl.OPENSSL_VERSION`. The local lab documents its actual versions and does not imply identical results on all Python builds.

## Primary references

- **PY-SSL** — [Python ssl library](https://docs.python.org/3/library/ssl.html).
- **REQUESTS** — [Requests advanced usage](https://requests.readthedocs.io/en/latest/user/advanced/).
- **OPENSSL-VERIFY** — [OpenSSL 3.5 verification options](https://docs.openssl.org/3.5/man1/openssl-verification-options/).

Reference snapshot: **2026-10-10**. For dated policy, distinguish current rules from future effective dates.
