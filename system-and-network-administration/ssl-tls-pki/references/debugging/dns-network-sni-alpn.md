# DNS, networking, SNI, ALPN and protocol routing

**Read when:** TLS changes across IPv4/IPv6, proxies, virtual hosts or transports.

## Four names/addresses that may differ

The **reference identity** is what the application intends to authenticate. The **connection address** is where packets go. **SNI** helps select the virtual TLS service. The **application Host/authority** selects the HTTP origin after TLS. They often match in simple deployments but remain separate concepts.

Create an evidence table containing all four. A test that changes the URL to an IP changes more than routing. Use curl `--resolve` or a TLS API's separate connect-address/reference-name inputs to isolate a backend.

## DNS and address family

Inspect A and AAAA answers, CNAMEs, authoritative delegation, split-horizon behavior and resolver caches. Test IPv4 and IPv6 independently. DNS TTL and negative caching affect what observers see, but unexplained inconsistency should not be dismissed as “propagation” indefinitely.

For ACME, the CA's public perspective differs from the operator's recursive resolver and a controller's self-check. Check challenge reachability from outside the network and across every relevant frontend.

## ALPN and protocol selection

ALPN selects an application protocol such as HTTP/2. Negotiating a protocol does not prove the client then speaks it correctly. An HTTP/1.1-only diagnostic request should not advertise HTTP/2 and send plaintext HTTP/1.1 frames afterward.

TLS-ALPN-01 uses a special challenge ALPN and certificate. Ordinary HTTPS termination can hide it. HTTP/3 uses QUIC and requires a separate transport-aware check; TCP success is not evidence of UDP-path health.

## Middleboxes and privacy

Proxies can terminate TLS, tunnel it with CONNECT, or alter routes. Record proxy variables and explicit proxy configuration, including NO_PROXY behavior for the actual library. An HTTPS proxy introduces its own TLS trust boundary in addition to the origin.

Encrypted Client Hello (ECH) is standardized in RFC 9849 at this snapshot. Availability and behavior remain implementation/deployment-specific. ECH affects which handshake metadata an observer can see; it does not hide destination IP addresses or fix a wrong application trust policy.

## Packet size and timeouts

Larger certificate chains or key-exchange messages can expose MTU/fragmentation and middlebox limits. Compare a stalled handshake's packet flow and retransmissions before changing cryptography. Keep network timeout, TLS alert and HTTP timeout as separate outcomes.

## Primary references

- **RFC6066** — [TLS extensions, including SNI](https://datatracker.ietf.org/doc/html/rfc6066).
- **RFC7301** — [Application-Layer Protocol Negotiation](https://datatracker.ietf.org/doc/html/rfc7301).
- **RFC9849** — [TLS Encrypted Client Hello](https://datatracker.ietf.org/doc/html/rfc9849).
- **RFC9001** — [Using TLS to secure QUIC](https://www.rfc-editor.org/rfc/rfc9001.html).
- **RFC8737** — [ACME TLS-ALPN challenge](https://www.rfc-editor.org/rfc/rfc8737.html).
- **LE-IPV6** — [Let’s Encrypt IPv6 validation behavior](https://letsencrypt.org/docs/ipv6-support/).
- **CURL-MAN** — [curl command-line manual](https://curl.se/docs/manpage.html).
- **CM-DNS** — [cert-manager DNS01 and delegation](https://cert-manager.io/docs/configuration/acme/dns01/).

Reference snapshot: **2026-10-10**. For dated policy, distinguish current rules from future effective dates.
