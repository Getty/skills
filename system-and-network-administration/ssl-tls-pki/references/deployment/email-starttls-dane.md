# Email TLS, STARTTLS, DANE and MTA-STS

**Read when:** debugging mail transport or confusing implicit TLS with a STARTTLS upgrade.

## Identify the application phase

Implicit TLS starts before application commands. STARTTLS begins with a plaintext protocol exchange that requests an upgrade. Connecting a raw TLS client to a port expecting an SMTP or IMAP greeting often produces a misleading “wrong version” error.

Common configurations include SMTP submission over implicit TLS on 465, submission with STARTTLS on 587, and IMAP over implicit TLS on 993. Server-to-server SMTP on port 25 has a different delivery and downgrade model from authenticated user submission. Confirm actual configuration instead of treating port numbers as proof.

```sh
openssl s_client -starttls smtp -connect mail.example.com:587 \
  -servername mail.example.com -verify_hostname mail.example.com \
  -verify_return_error -CAfile approved-roots.pem
```

The command tests an authenticated TLS upgrade under explicit trust; it does not send mail or prove SMTP authorization. For implicit TLS, omit `-starttls` and use the appropriate endpoint.

## Policy mechanisms solve different problems

DANE for SMTP uses DNSSEC-authenticated TLSA information to bind transport authentication under its defined rules. TLSA certificate/key associations require coordinated updates during certificate or key rotation. Ordinary browsers do not thereby switch to DNSSEC-based Web PKI trust.

MTA-STS publishes an HTTPS-fetched transport policy for receiving mail domains, with DNS discovery and caching. It introduces policy-hosting, certificate, DNS and max-age dependencies. TLS reporting provides visibility into transport-policy failures; reports are not an enforcement mechanism and can contain sensitive operational detail.

These systems complement a deliberate mail-delivery policy; “the SMTP server has a valid certificate” is not equivalent to downgrade-resistant authenticated delivery from every sender.

## Debug in two layers

First inspect MX lookup, chosen mail host, address family, reachability, greeting and advertised STARTTLS. Then inspect the handshake's reference name, chain, protocol and certificate purpose. For DANE, verify DNSSEC status and TLSA matching rules. For MTA-STS, inspect policy mode, permitted MX patterns, HTTPS authentication and cache state.

Do not force a mail-specific certificate name rule from memory. SMTP DANE, submission clients and generic HTTPS clients use different identity discovery contexts. Apply the relevant protocol specification and deployed MTA/client behavior.

## Rotation tests

Test new certificates against cached policy and TLSA records before retiring old material. Coordinate any overlapping TLSA records with DNS TTL and validator behavior. Verify SMTP delivery and reporting after the change, not just port 443 on the policy host.

## Primary references

- **RFC8314** — [TLS for email submission and access](https://datatracker.ietf.org/doc/html/rfc8314).
- **RFC7672** — [SMTP security with DANE](https://datatracker.ietf.org/doc/html/rfc7672).
- **RFC8461** — [SMTP MTA Strict Transport Security](https://datatracker.ietf.org/doc/html/rfc8461).
- **RFC8460** — [SMTP TLS reporting](https://datatracker.ietf.org/doc/html/rfc8460).
- **OPENSSL-SCLIENT** — [OpenSSL 3.5 s_client](https://docs.openssl.org/3.5/man1/openssl-s_client/).
- **RFC9525** — [Service identity verification in TLS](https://www.rfc-editor.org/rfc/rfc9525.html).

Reference snapshot: **2026-10-10**. For dated policy, distinguish current rules from future effective dates.
