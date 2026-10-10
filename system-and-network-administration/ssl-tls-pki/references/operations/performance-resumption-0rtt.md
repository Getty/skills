# Performance, resumption, connection lifetime and 0-RTT

**Read when:** optimizing TLS without weakening authentication.

## Measure the right components

Separate DNS, connection establishment, handshake, certificate validation, application latency and transfer throughput. Record cold and warm connections, resumed sessions, address family, protocol and client hardware. A reused HTTP connection avoids a new handshake entirely; do not attribute all improvement to a cipher change.

Certificate-chain size, algorithm support, server CPU, network RTT, hardware acceleration and process architecture can affect costs. Benchmark representative clients and real network paths rather than selecting a key type solely from a server-side microbenchmark.

## Resumption is stateful security

TLS resumption reuses previously established security state. Manage ticket keys/state, lifetime, rotation, cluster sharing and compromise response. Sharing resumption material across unrelated services or tenants expands the compromise boundary.

Determine how certificate replacement, account revocation and authorization changes affect resumed sessions and existing connections. A new certificate on disk does not necessarily force a fresh identity check for every established or resumed session. Reconnect/drain policies belong in incident response.

## 0-RTT is not a free optimization

TLS 1.3 early data has replay considerations and weaker guarantees than ordinary post-handshake application data. Applications need a deliberate acceptance policy, replay defenses and safe operations. “GET request” is not sufficient proof that an endpoint has no side effects or replay consequences.

Disable early data where its security and authorization semantics are not explicitly designed. Do not enable it globally to improve a benchmark number. Test retransmission/replay, load-balancer routing and authentication state in an isolated environment.

## Resource safety

Bound handshake duration, connection counts, expensive verification work and per-peer resource use. Ensure error paths close sockets and release credentials. Rate limiting must preserve legitimate renewal and health-check behavior while controlling abusive traffic.

## Change procedure

Optimize one dimension at a time, preserve identity verification, and compare both performance and rejected cases. Record the exact stack and parameters. A performance win that changes the trust model is a different design, not a like-for-like optimization.

## Primary references

- **RFC9846** — [TLS 1.3 — July 2026 revision](https://datatracker.ietf.org/doc/html/rfc9846).
- **GO-TLS** — [Go crypto/tls](https://pkg.go.dev/crypto/tls).
- **NGINX-SSL** — [NGINX HTTP SSL module](https://nginx.org/en/docs/http/ngx_http_ssl_module.html).
- **SSLYZE** — [SSLyze maintained documentation](https://nabla-c0d3.github.io/sslyze/documentation/).
- **RFC9001** — [Using TLS to secure QUIC](https://www.rfc-editor.org/rfc/rfc9001.html).

Reference snapshot: **2026-10-10**. For dated policy, distinguish current rules from future effective dates.
