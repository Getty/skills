# ACME challenges across DNS, proxies and private networks

**Read when:** choosing HTTP-01, DNS-01 or TLS-ALPN-01 for a real topology.

## Select by the validation path

| Method | Evidence exposed to CA | Inbound need | Important restrictions |
|---|---|---|---|
| HTTP-01 | Account-bound response under the challenge URL | Public TCP 80 | No wildcard issuance; redirect behavior is CA-specific |
| DNS-01 | Derived TXT value at `_acme-challenge` | Public authoritative DNS, not the service | Supports wildcards; secure DNS update credentials required |
| TLS-ALPN-01 | Special challenge certificate via `acme-tls/1` | Public TCP 443 reaching the solver | Proxy must preserve/route the ALPN challenge; no wildcard |

For Let’s Encrypt, public IP identifiers can use supported HTTP/TLS-ALPN validation, not DNS-01. Its HTTP-01 policy follows a limited number of HTTP/HTTPS redirects on ports 80/443. A redirect to HTTPS during this bootstrap is not ordinary browser certificate verification; do not generalize its special behavior into a client verification policy.

## DNS-01 precision

The TXT response is derived from the challenge's key authorization; it is not just the raw token. Apex and wildcard authorizations can need multiple simultaneous TXT values at one owner name. Preserve unrelated active values, clean up only the value your job created, and avoid deleting a record another renewal is using.

A CNAME or NS delegation can isolate challenge updates into a constrained zone. Check both CA support and client behavior: cert-manager's CNAME following requires the appropriate solver configuration. Recursive self-checks, authoritative CA observations and split-horizon answers are separate viewpoints.

## Typical topology decisions

**Private service, owned public DNS name:** DNS-01 can establish public control without exposing the service. The relying client must still reach and validate that service, and its public certificate names may appear in CT.

**Several web frontends:** Route every challenge request to a shared solver or replicate the exact response before notifying the CA. Do not rely on one successful local request behind a load balancer.

**CDN/WAF:** Ensure the challenge path bypasses login, bot challenges and content rewriting without bypassing unrelated application controls. For TLS-ALPN, a terminating CDN may prevent the solver's special handshake from reaching the CA entirely.

**Dual stack:** Check A and AAAA separately. Let’s Encrypt prefers IPv6 when present; not every IPv6 validation failure triggers IPv4 fallback. An incorrect content response is different from an initial network failure.

## Preflight checklist

Confirm public authoritative answers, ports, redirects, solver selection, proxy behavior, account identity, CAA and clock. Test from outside the protected network. Ensure the chosen renewal method works unattended after a reboot and after a DNS token rotation—not only during the initial interactive issuance.

## Primary references

- **RFC8555** — [Automated Certificate Management Environment](https://www.rfc-editor.org/rfc/rfc8555.html).
- **RFC8737** — [ACME TLS-ALPN challenge](https://www.rfc-editor.org/rfc/rfc8737.html).
- **RFC8738** — [ACME IP identifier validation](https://www.rfc-editor.org/rfc/rfc8738.html).
- **LE-CHALLENGES** — [Let’s Encrypt challenge types](https://letsencrypt.org/docs/challenge-types/).
- **LE-IPV6** — [Let’s Encrypt IPv6 validation behavior](https://letsencrypt.org/docs/ipv6-support/).
- **CM-DNS** — [cert-manager DNS01 and delegation](https://cert-manager.io/docs/configuration/acme/dns01/).
- **LE-CAA** — [Let’s Encrypt CAA processing](https://letsencrypt.org/docs/caa/).

Reference snapshot: **2026-10-10**. For dated policy, distinguish current rules from future effective dates.
