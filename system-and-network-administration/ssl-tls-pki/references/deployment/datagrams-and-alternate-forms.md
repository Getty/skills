# QUIC, DTLS, PSKs and raw public keys

**Read when:** the traffic is not conventional HTTPS over TCP, or no CA certificate is used.

## QUIC is not TLS records over UDP

QUIC uses the TLS 1.3 handshake for cryptographic establishment, while QUIC supplies its own transport and packet protection integration. TCP-oriented `openssl s_client` output is not a test of HTTP/3 over QUIC. Confirm the client's QUIC support, UDP reachability, ALPN and any fallback to TCP before interpreting a result.

A service can work over HTTP/2 while HTTP/3 fails due to UDP filtering, MTU behavior or a different termination path. Capture the negotiated transport, not merely a successful HTTP status. Diagnostic tools need protocol-specific support.

## DTLS

DTLS adapts TLS security concepts to datagram transport with its own loss, retransmission and message-handling behavior. DTLS 1.3 has a published specification, but library support must be checked by version. Do not infer DTLS 1.3 support from a library's TLS 1.3 support.

For IoT or media applications, inventory packet size, fragmentation, connection state, credential format, identity verification and resource limits. Certificate chains and modern key exchanges can stress constrained devices and networks; measure them rather than disabling authentication to make packets smaller.

## PSK authentication

A pre-shared key can authenticate TLS peers without ordinary certificate issuance in supported profiles. The design then needs secure key generation, unique identity mapping, distribution, rotation and compromise isolation. One PSK shared by a fleet makes it difficult to identify or revoke one member.

Distinguish external PSKs from resumption-derived PSKs. The security properties depend on the selected exchange mode and protocol integration. A server certificate is not “missing” when a deliberately designed PSK system uses a different authentication model.

## Raw public keys

Raw-public-key TLS/DTLS carries a key without an ordinary certificate chain. Authenticity must come from another provisioning or binding mechanism. Removing X.509 overhead does not remove the need to know which key belongs to which peer.

Treat a pinned raw key as a lifecycle object: initial binding, backup/replacement keys, revocation, replay resistance in enrollment and out-of-band recovery all need a design. A first-connection prompt accepted without verification merely moves the trust problem.

## Acceptance route

Use the protocol's actual implementation and application harness. Test loss, fragmentation, unsupported groups, wrong identities and replacement credentials. The supplied TCP lab deliberately does **not** claim QUIC, DTLS, PSK or raw-key interoperability coverage.

## Primary references

- **RFC9001** — [Using TLS to secure QUIC](https://www.rfc-editor.org/rfc/rfc9001.html).
- **RFC9147** — [DTLS 1.3](https://datatracker.ietf.org/doc/html/rfc9147).
- **RFC7250** — [Raw public keys in TLS and DTLS](https://www.rfc-editor.org/rfc/rfc7250.html).
- **RFC9846** — [TLS 1.3 — July 2026 revision](https://datatracker.ietf.org/doc/html/rfc9846).
- **OPENSSL-SCLIENT** — [OpenSSL 3.5 s_client](https://docs.openssl.org/3.5/man1/openssl-s_client/).

Reference snapshot: **2026-10-10**. For dated policy, distinguish current rules from future effective dates.
