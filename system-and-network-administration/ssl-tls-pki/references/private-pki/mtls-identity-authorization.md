# Mutual TLS: identity proof is not authorization

**Read when:** using client certificates for APIs, workloads, devices or administrative access.

## Two independent verification decisions

The client validates the server's identity and trust path. The server requests and verifies the client's certificate and possession of its private key. Each side can use a different CA hierarchy. Successful server authentication says nothing about client authentication unless the server actually required and verified the client certificate.

For client credentials, enforce an appropriate clientAuth purpose and a constrained issuer trust set. Then map an approved certificate identity to an application principal and authorization policy. Do not grant administrative access to any certificate signed by a familiar public or corporate CA.

## Identity mapping

Define a canonical identity field and parser. For example, a controlled URI namespace can identify a workload; a DNS name can identify a server; an enterprise mapping may bind a specific subject to an account. Avoid string-substring matching across arbitrary subject text. Handle multiple SAN entries and duplicate/ambiguous identity forms deliberately.

A SPIFFE URI inside a certificate is not enough to claim SPIFFE conformance. Use the SPIFFE/SVID validation and workload-API libraries when adopting that identity system. The lab's URI authorization example is intentionally a small application policy, not a complete SPIFFE verifier.

## Terminating proxies

When a proxy terminates mTLS, the backend's peer is the proxy, not the original client. Forwarded identity must be authenticated and protected across that boundary. The proxy must remove/overwrite client-supplied identity headers, and the backend must accept them only from the intended authenticated proxy path.

For stronger separation, keep direct mTLS to the application or establish a separately authenticated proxy-to-backend connection with a documented identity assertion mechanism. Never assume HTTPS re-encryption automatically preserves the original client-certificate proof.

## Connection lifetime

Authorization decisions may outlive a certificate through connection pooling, sessions or tickets. Decide how revocation, role removal and credential rotation affect existing connections. A server's advertised acceptable-CA list assists certificate selection; it is not itself the complete authorization policy.

## Required negative tests

Reject missing client certificates, untrusted client issuers, serverAuth-only leaves presented as clients, expired credentials, wrong identity namespaces and authenticated-but-unauthorized identities. Also reject spoofed proxy identity headers and direct backend access bypassing the authenticating proxy.

The local lab exercises the first group with real TLS and a separate application-level 403 outcome. Production tests must additionally cover the actual gateway, authorization engine and session behavior.

## Primary references

- **RFC9846** — [TLS 1.3 — July 2026 revision](https://datatracker.ietf.org/doc/html/rfc9846).
- **RFC5280** — [X.509 certificates and CRLs / PKIX](https://www.rfc-editor.org/rfc/rfc5280.html).
- **GO-TLS** — [Go crypto/tls](https://pkg.go.dev/crypto/tls).
- **PY-SSL** — [Python ssl library](https://docs.python.org/3/library/ssl.html).
- **SPIFFE** — [SPIFFE concepts, identities and workload API](https://spiffe.io/docs/latest/spiffe-about/spiffe-concepts/).
- **NGINX-PROXY** — [NGINX HTTP proxy module](https://nginx.org/en/docs/http/ngx_http_proxy_module.html).
- **PG-SERVER** — [PostgreSQL 18 server TLS](https://www.postgresql.org/docs/18/ssl-tcp.html).

Reference snapshot: **2026-10-10**. For dated policy, distinguish current rules from future effective dates.
