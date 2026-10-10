# Packet captures, TLS key logs and evidence handling

**Read when:** the handshake or application exchange requires packet-level analysis.

## Start without decryption

A scoped capture can reveal address selection, TCP resets, retransmissions, handshake timing and some visible negotiation metadata. TLS 1.3 encrypts much of the handshake after ServerHello, and ECH can further change visibility. Lack of visible certificate details in a capture does not prove that no certificate was exchanged.

Capture only the authorized endpoints/time window. Prefer a narrowly filtered trace over collecting an entire interface's unrelated traffic. Record time synchronization and the precise test request so packets can be correlated with server and client logs.

## Session secrets are sensitive credentials

Supported clients can write TLS traffic secrets in SSLKEYLOGFILE format, now specified by RFC 9850. Support is application/build-specific; setting an environment variable is not proof that a process honors it. Python exposes an explicit key-log mechanism in supported versions, while other clients require their own configuration.

Treat a key log and corresponding packet capture as potentially decrypted application data. Protect access, avoid normal log collectors, use a short retention period and remove the diagnostic setting afterward. Never upload them to a public analyzer without explicit authorization and data review.

## What a private key cannot do

For an ephemeral key-exchange session such as ordinary modern TLS 1.3, the server's long-term RSA private key is not a general decryption key for a recorded capture. Traffic secrets or a supported endpoint-side mechanism are needed. Do not ask an operator to export production private keys merely to “decrypt HTTPS.”

## Reproducible procedure

Create a minimal test account and non-sensitive request. Enable the selected process's supported key logging, capture a short connection, verify that the correct secrets were recorded, then configure Wireshark's TLS protocol preferences with the approved key-log file. Inspect negotiation and application framing. Disable logging and apply the evidence-retention procedure.

Key logs help analyze one observed session. They do not prove the certificate was accepted under the intended root/CT/revocation policy. Correlate the capture with the verifier's result and the application's authorization decision.

## Primary references

- **WIRESHARK** — [Wireshark TLS decryption and troubleshooting](https://wiki.wireshark.org/TLS).
- **RFC9850** — [The SSLKEYLOGFILE format](https://datatracker.ietf.org/doc/html/rfc9850).
- **RFC9846** — [TLS 1.3 — July 2026 revision](https://datatracker.ietf.org/doc/html/rfc9846).
- **RFC9849** — [TLS Encrypted Client Hello](https://datatracker.ietf.org/doc/html/rfc9849).
- **PY-SSL** — [Python ssl library](https://docs.python.org/3/library/ssl.html).

Reference snapshot: **2026-10-10**. For dated policy, distinguish current rules from future effective dates.
