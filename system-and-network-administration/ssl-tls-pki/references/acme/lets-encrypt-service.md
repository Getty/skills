# Let’s Encrypt from the TLS and PKI perspective

**Read when:** selecting Let’s Encrypt or replacing outdated assumptions about its certificates.

## What the service supplies

Let’s Encrypt is a publicly trusted CA service operated by ISRG. It automates domain/IP-control validation and certificate issuance through ACME. Trust comes from supported paths into the clients' trust stores, not from ACME itself. A private ACME CA can use the same protocol without being publicly trusted.

The issued leaf still needs the correct SANs, appropriate purpose, a protected private key, a supported chain and working deployment. A free certificate is not intrinsically weaker TLS than a paid one; the relevant differences are validation policy, trust coverage, service characteristics and operations.

## Current profile selection

At the 2026-10-10 review, `classic` is the default 90-day profile; `tlsserver` is an opt-in 45-day profile; `shortlived` lasts 160 hours and supports public IP identifiers as well as DNS names. The profiles also differ in field/extension choices and limits. Applications must not depend on cosmetic subject fields or a permanently fixed issuer name.

Discover advertised profiles from the actual ACME directory and inspect the result. Certbot's preferred-profile option permits fallback; required-profile fails when the requested profile cannot be used. Choose fail-closed selection when fallback would violate the design, especially where the identifier/purpose requires a particular profile.

Let’s Encrypt no longer issues new clientAuth certificates through any profile after 2026-07-08. Do not plan workload/client mTLS credentials around its old dual-EKU behavior. A private or other explicitly suitable client-identity CA is the appropriate separate decision.

## Operational implications

IP certificates are not restricted to DNS-name issuance anymore, but they require the short-lived profile and a supported validation method/client. A certificate for a private RFC1918 address is not implied by public IP support. Verify exact plugin capabilities; support for issuance does not imply automatic server installation.

The default lifetime changes announced for 2027 and 2028 are future events at this snapshot. Use the [policy calendar](../public-pki/policy-calendar.md), not a hardcoded “all Let's Encrypt certificates are 90 days” rule.

## Chain and purpose tests

Treat the certificate response as data to validate: expected public key, SAN set, EKU, lifetime, issuer path and chain completeness. Test it with the least capable supported client before a profile or preferred-chain migration. Use private-PKI test identities when testing client authentication; do not attempt to bypass an absent clientAuth EKU by turning verification off.

## Primary references

- **LE-PROFILES** — [Let’s Encrypt certificate profiles](https://letsencrypt.org/docs/profiles/).
- **LE-IP** — [Six-day and IP certificates generally available](https://letsencrypt.org/2026/01/15/6day-and-ip-general-availability).
- **LE-CERTBOT-IP** — [Certbot support for short-lived and IP certificates](https://letsencrypt.org/2026/03/11/shorter-certs-certbot).
- **LE-CLIENTAUTH** — [End of TLS client-authentication certificate support](https://letsencrypt.org/2025/05/14/ending-tls-client-authentication).
- **LE-64D** — [64-day certificates: announcement on 2026-10-07](https://letsencrypt.org/2026/10/07/64-day-certs).
- **LE-45D** — [Let’s Encrypt planned 45-day default lifetimes](https://letsencrypt.org/2025/12/02/from-90-to-45).
- **LE-CHAINS** — [Let’s Encrypt roots and intermediates](https://letsencrypt.org/certificates/).
- **CERTBOT** — [Certbot user guide](https://eff-certbot.readthedocs.io/en/stable/using.html).

Reference snapshot: **2026-10-10**. For dated policy, distinguish current rules from future effective dates.
