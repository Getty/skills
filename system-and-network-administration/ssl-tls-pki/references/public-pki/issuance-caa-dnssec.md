# Issuance authorization, CAA, DNSSEC and network perspectives

**Read when:** hardening domain validation or debugging an issuance failure that looks like DNS.

## Split three questions

**Who controls the requested identifier?** Domain/IP validation answers this using an allowed method. **Which CA is authorized to issue?** CAA constrains issuance for DNS names. **Can the DNS answer be authenticated?** DNSSEC provides validation of signed DNS data, not encryption or an automatic TLS trust anchor.

CAA is evaluated during issuance, not as a normal replacement for certificate verification during a browser connection. Changing CAA does not retroactively revoke existing certificates. An `issuewild` policy can differ from the ordinary `issue` policy; do not assume apex and wildcard handling are identical.

Illustrative DNS owner-controlled policy:

```dns
example.com.  IN CAA 0 issue "letsencrypt.org"
example.com.  IN CAA 0 issuewild ";"
```

This permits the named CA for ordinary issuance while denying wildcard issuance under the relevant CAA policy. Deploy only after inventorying every legitimate CA, including CDN and managed-hosting issuers. Account/method binding can reduce unwanted issuance paths where supported; copy the correct production account URI, not a staging account identifier.

## Authoritative DNS is the evidence

Inspect delegation from the parent, authoritative nameservers, CNAME chains, relevant CAA records and the exact TXT owner. Query each authoritative server. A successful response from a corporate recursive resolver is insufficient evidence of global reachability or consistency.

For signed zones, diagnose DS/DNSKEY alignment and signature validity; a broken DNSSEC chain can produce SERVFAIL even when an unchecked query displays the record. Do not repair issuance by removing validation from the CA or resolver. A signed parent with an unsigned child is not the same condition as a bogus signed delegation.

## Current policy boundary

The current Baseline Requirements contain effective-date rules for primary-perspective DNSSEC validation and prohibit treating validation errors as authorization to issue. Multiperspective validation adds independent network observations to reduce some routing/DNS manipulation risks. It is not a proof that all observers or routing paths are uncompromised, and it makes geographically inconsistent DNS harder to ignore.

## Operational controls

Maintain an inventory of DNS administrators, registrar access, API tokens and delegated challenge zones. DNS credentials capable of changing broad zones may effectively authorize certificate issuance for many services. Prefer a constrained validation zone and minimum-privilege credentials, with explicit offboarding.

Before changing a CDN, DNS provider or CAA policy, exercise issuance in staging and inspect production account policy separately. Preserve retry state and avoid repeatedly creating failed orders while DNS is still converging. Record the CA's observed error and perspective where exposed rather than replacing evidence with “DNS propagation takes time.”

## Primary references

- **RFC8659** — [DNS Certification Authority Authorization](https://www.rfc-editor.org/rfc/rfc8659.html).
- **RFC8657** — [CAA account and validation-method binding](https://www.rfc-editor.org/rfc/rfc8657.html).
- **CABF-BR** — [CA/Browser Forum TLS Baseline Requirements — current HTML](https://cabforum.org/working-groups/server/baseline-requirements/requirements/).
- **LE-CAA** — [Let’s Encrypt CAA processing](https://letsencrypt.org/docs/caa/).
- **LE-CHALLENGES** — [Let’s Encrypt challenge types](https://letsencrypt.org/docs/challenge-types/).
- **CM-DNS** — [cert-manager DNS01 and delegation](https://cert-manager.io/docs/configuration/acme/dns01/).

Reference snapshot: **2026-10-10**. For dated policy, distinguish current rules from future effective dates.
