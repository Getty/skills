# Handshake, keys and the security properties

**Read when:** explaining what TLS actually proves, or locating a negotiation failure.

## Read a handshake as a sequence of decisions

For a typical full certificate-based TLS 1.3 connection, the client advertises supported versions, algorithms and key shares. The server chooses compatible parameters; the peers derive handshake secrets. The server presents its certificate material and proves possession of the corresponding private key. Finished messages bind the negotiation to the resulting secrets. Application data uses symmetric authenticated encryption. Optional client-certificate authentication adds a second identity proof.

These are conceptual phases, not a packet-by-packet transcript: resumption, HelloRetryRequest, early data, client authentication and transport integration change the messages. Use the implementation's negotiated output and a protocol decoder before assigning a failure to a phase.

## Do not mix the keys

| Material | Function | Consequence of mishandling |
|---|---|---|
| CA signing key | Authorizes certificate statements | Potential impersonation across its issuance scope |
| Leaf private key | Proves the endpoint's identity | Endpoint impersonation until effective containment |
| Ephemeral key-exchange material | Establishes connection secrets | Session security and forward secrecy affected |
| Traffic secrets | Protect individual directions/epochs | Captured traffic may become readable |
| Resumption/ticket material | Allows subsequent sessions | Authentication lifetime and incident response affected |
| ACME account key | Authenticates certificate-management requests | Issuance-account compromise, not identical to leaf compromise |

A certificate containing an RSA public key can be used to authenticate an ephemeral elliptic-curve exchange. “RSA certificate” does not mean obsolete RSA key transport. In TLS 1.3, the cipher-suite name specifies record protection and the associated hash, not the whole identity and key-exchange configuration.

## What the channel does not establish

Encryption cannot compensate for accepting the wrong identity. A complete chain to a trusted CA is still insufficient when the expected service name differs. An authenticated client is still not necessarily allowed to access a resource. TLS termination at a proxy makes that proxy an endpoint with access to plaintext.

Forward secrecy limits what later compromise of a long-term authentication key reveals about appropriately established past sessions. It is not a guarantee against a compromised process, saved traffic secrets, a malicious trusted intermediary, or all resumption configurations.

## Practical inspection

Record protocol version, cipher, key-exchange group where available, peer signature algorithm, ALPN, whether a session was resumed, and whether client authentication was requested. Record the software/backend version too: two tools displaying “TLS 1.3” can have different certificate validation and trust behavior.

For high assurance, review the application's handling of abrupt EOF, `close_notify`, partial writes, deadlines and cancellation. A correct handshake does not prove that the application rejects a truncated or incomplete transaction.

## Primary references

- **RFC9846** — [TLS 1.3 — July 2026 revision](https://datatracker.ietf.org/doc/html/rfc9846).
- **RFC10015** — [Deprecating obsolete key exchange methods in TLS 1.2 and DTLS 1.2](https://datatracker.ietf.org/doc/html/rfc10015).
- **RFC7301** — [Application-Layer Protocol Negotiation](https://datatracker.ietf.org/doc/html/rfc7301).
- **OPENSSL-SCLIENT** — [OpenSSL 3.5 s_client](https://docs.openssl.org/3.5/man1/openssl-s_client/).
- **RFC9850** — [The SSLKEYLOGFILE format](https://datatracker.ietf.org/doc/html/rfc9850).

Reference snapshot: **2026-10-10**. For dated policy, distinguish current rules from future effective dates.
