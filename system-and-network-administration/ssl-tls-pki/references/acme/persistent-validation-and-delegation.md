# Persistent validation, delegation and automation privileges

**Read when:** considering delegated DNS solvers, managed issuance or DNS-PERSIST-01.

## Delegation is an authorization decision

Giving a component permission to write challenge DNS can allow it to obtain certificates for the delegated names. That can be substantially more powerful than permission to restart a web server. Document the authorized names, account, CA, challenge method, credential custodian and revocation/offboarding process.

Prefer narrowly scoped update permissions and a dedicated validation zone when practical. Protect registrar and parent-zone administration separately from routine solver credentials. A compromised DNS parent can invalidate carefully scoped child-zone controls.

## Persistent DNS authorization

DNS-PERSIST-01 was announced by Let's Encrypt as a new model using a persistent DNS authorization record tied to a CA/account context. It changes the operational tradeoff: fewer recurring DNS writes, but a long-lived issuance grant that needs deliberate lifecycle management.

At this package's snapshot, the reviewed sources describe implementation and standardization work, not sufficient evidence to assert general production availability. Check the current draft, CA documentation, advertised capabilities and client implementation before selecting it. Do not substitute an invented configuration flag for that verification.

## Threat-model comparison

| Model | Recurring dependency | Sensitive authority to control |
|---|---|---|
| HTTP/TLS challenge solver | Correct public challenge routing | Ability to answer for the service |
| Dynamic DNS-01 | DNS API and propagation | Permission to alter validation records |
| Delegated DNS zone | Delegation and solver service | Subzone update/admin authority |
| Persistent account-bound grant | Continued grant and account security | Account key plus durable authorization |

A persistent grant does not mean an eternal certificate. Certificate renewal, deployment and key protection remain necessary. A tenant's departure or domain transfer must revoke both credentials and the DNS authorization/delegation, not just delete one leaf certificate.

## Acceptance procedure

First enumerate who can issue without changing the main application. Then test removal of each grant in staging: solver token revoked, account disabled, delegation removed, tenant offboarded. Determine whether previously valid authorizations remain reusable under CA policy. Maintain an audit trail that explains why each continuing grant exists.

## Primary references

- **LE-PERSIST** — [DNS-PERSIST-01 announcement](https://letsencrypt.org/2026/02/18/dns-persist-01).
- **RFC8657** — [CAA account and validation-method binding](https://www.rfc-editor.org/rfc/rfc8657.html).
- **RFC8555** — [Automated Certificate Management Environment](https://www.rfc-editor.org/rfc/rfc8555.html).
- **CM-DNS** — [cert-manager DNS01 and delegation](https://cert-manager.io/docs/configuration/acme/dns01/).
- **LE-45D** — [Let’s Encrypt planned 45-day default lifetimes](https://letsencrypt.org/2025/12/02/from-90-to-45).

Reference snapshot: **2026-10-10**. For dated policy, distinguish current rules from future effective dates.
