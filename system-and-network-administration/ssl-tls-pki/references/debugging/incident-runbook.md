# TLS incident runbook: evidence before configuration changes

**Read when:** a TLS connection fails or behaves inconsistently.

## 1. Define the failing contract

Record exact application action, reference name, connection address/port, time, client/server versions, TLS backend, trust source, proxy environment and expected authentication purpose. Establish authorized diagnostic scope. Preserve the error before restarting services or changing trust.

A useful ticket begins: “Client build X, using trust bundle Y, connecting to address Z for identity N, fails at time T with error E.” “SSL broken” is not a reproducible report.

## 2. Walk the layers in order

| Layer | Evidence | Stop changing unrelated layers |
|---|---|---|
| DNS/network/time | A/AAAA, routes, port reachability, clock | No TLS fix can repair a missing route |
| Protocol initiation | Direct TLS versus STARTTLS/QUIC | A plaintext greeting is not an old TLS version |
| Negotiation | Offered/selected versions, groups, signatures, ALPN | Do not add roots for a no-shared-algorithm failure |
| Peer material | Exact leaf and transmitted chain | Compare all replicas and SNI choices |
| Validation | Path, trust, identity, time, purpose, constraints | A signature alone is not acceptance |
| Policy | CT/revocation/pinning/enterprise rules | Reproduce with the actual policy-enforcing client |
| Client identity | Certificate request, selected client key/chain | Separate “not presented” from “rejected” |
| Application | HTTP/database authorization and tenant routing | TLS success is not a login or permission grant |

## 3. Change one hypothesis at a time

Use a fixed destination with the intended TLS name to separate DNS/routing from identity. Use an explicit approved trust bundle to separate store configuration from the certificate itself. Force a protocol version only as a scoped experiment. Inspect the served chain separately from a chain downloaded from a CA website.

Log each experiment as **hypothesis → command/config → observation → inference → next check**. A test that changes the host, CA bundle and protocol simultaneously has low diagnostic value.

## 4. Make the smallest justified repair

Examples include deploying the missing intermediate, correcting the expected SAN, updating the intended application trust bundle, repairing an AAAA route, or enabling verified upstream TLS. Do not mask the evidence with insecure verification settings or an unreviewed global root installation.

## 5. Retest and close the loop

Repeat the original application action. Add a negative test that would detect recurrence of the same defect. Check all termination points and clean client environments. Verify live fingerprint and monitor after reload/rotation.

The final incident note should identify root cause, affected scope, evidence, repaired configuration, remaining uncertainty and prevention. Keep secrets and decrypted captures out of ordinary ticket attachments.

## Primary references

- **OPENSSL-SCLIENT** — [OpenSSL 3.5 s_client](https://docs.openssl.org/3.5/man1/openssl-s_client/).
- **CURL-MAN** — [curl command-line manual](https://curl.se/docs/manpage.html).
- **RFC9525** — [Service identity verification in TLS](https://www.rfc-editor.org/rfc/rfc9525.html).
- **PY-SSL** — [Python ssl library](https://docs.python.org/3/library/ssl.html).
- **WIRESHARK** — [Wireshark TLS decryption and troubleshooting](https://wiki.wireshark.org/TLS).
- **NGINX-PROXY** — [NGINX HTTP proxy module](https://nginx.org/en/docs/http/ngx_http_proxy_module.html).

Reference snapshot: **2026-10-10**. For dated policy, distinguish current rules from future effective dates.
