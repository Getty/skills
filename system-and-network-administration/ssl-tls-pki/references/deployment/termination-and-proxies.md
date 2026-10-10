# TLS termination, load balancers and verified upstreams

**Read when:** designing a multi-hop deployment or debugging proxy-specific TLS failures.

## Draw every connection separately

```text
Browser --TLS A--> CDN/LB --TLS B--> reverse proxy --TLS C--> application
          public?          private?                  private/mTLS?
```

For each hop specify reference identity, presented certificate, verifying party, trust bundle, protocol policy and client authentication. Termination exposes plaintext at that component. Re-encryption protects a new connection; it is not uninterrupted end-to-end encryption from the browser to the application.

TCP passthrough leaves the handshake at the backend. It can preserve backend mTLS, but changes routing, observability and challenge handling. The PROXY protocol is connection metadata, not a cryptographic identity proof; restrict who can send it.

## Verified upstreams are explicit

NGINX's HTTPS proxying does not imply upstream certificate verification: `proxy_ssl_verify` defaults to off, and upstream SNI also needs deliberate configuration. A minimal reviewed pattern is:

```nginx
proxy_pass https://10.20.0.10:8443;
proxy_ssl_server_name on;
proxy_ssl_name api.internal.example.com;
proxy_ssl_verify on;
proxy_ssl_trusted_certificate /etc/nginx/pki/internal-roots.pem;
proxy_ssl_verify_depth 2;
proxy_set_header Host api.internal.example.com;
```

The trust file must hold approved issuer trust, and the configured name must be present in the backend certificate. The depth is an example for a small hierarchy, not a universal value. This excerpt does not configure inbound TLS, client authentication, DNS resolution or all application headers.

## Health checks and routing

A health checker can use a different SNI/name, CA bundle, port or TLS backend than ordinary traffic. Verify its actual connection. A TCP-only health check can report success while every authenticated application connection fails.

Probe each load-balancer address and backend while retaining the intended reference name. Compare IPv4/IPv6, region, SNI and ALPN. One healthy replica does not prove convergence. For a pinned backend address, set the TLS identity independently rather than changing the URL to an IP literal and only overriding HTTP Host.

## Multi-tenant controls

Never derive a privileged upstream TLS name directly from an untrusted incoming Host header without a validated routing policy. Keep tenant certificates, keys, challenge routes and issuance authorization separated. Shared wildcard keys magnify the consequences of one tenant or service compromise.

When forwarding authenticated client identity, overwrite untrusted incoming headers and protect the backend path. Test direct bypass access. A proxy that accepts any backend certificate can become an impersonation gateway despite a valid public certificate on its front door.

## Primary references

- **NGINX-PROXY** — [NGINX HTTP proxy module](https://nginx.org/en/docs/http/ngx_http_proxy_module.html).
- **NGINX-SSL** — [NGINX HTTP SSL module](https://nginx.org/en/docs/http/ngx_http_ssl_module.html).
- **RFC6066** — [TLS extensions, including SNI](https://datatracker.ietf.org/doc/html/rfc6066).
- **RFC9525** — [Service identity verification in TLS](https://www.rfc-editor.org/rfc/rfc9525.html).
- **CURL-MAN** — [curl command-line manual](https://curl.se/docs/manpage.html).
- **RFC8737** — [ACME TLS-ALPN challenge](https://www.rfc-editor.org/rfc/rfc8737.html).

Reference snapshot: **2026-10-10**. For dated policy, distinguish current rules from future effective dates.
