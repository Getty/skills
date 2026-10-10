# DNS, reverse DNS, certificates, and migration

Verified on **2026-10-04**. Recheck the current DNS/API integration matrix and certificate behavior before migration; tool support and strict request validation change independently of ordinary DNS resolution.

## Contents

- Current DNS control plane
- RRSet and delegation constraints
- Migration runbook
- TLS choices and readiness
- Reverse DNS and diagnosis

## Current DNS control plane

Use DNS zones in **Hetzner Console** and the Cloud API `/v1/zones` family. DNS became generally available there on **2025-11-10**; creating new zones in the legacy DNS Console stopped then. Treat tutorials for `dns.hetzner.com/api/v1` as historical migration material, not a template for new automation. [API changelog](https://docs.hetzner.cloud/changelog)

Tokens created in the old DNS Console do not work with the Cloud API. DNS zones now belong to projects. To limit a DNS automation token's blast radius, put the appropriate zones in a dedicated project rather than claiming the token has unsupported per-record permissions. [Features and integration migration](https://docs.hetzner.com/networking/dns/migration-to-hetzner-console/features-and-differences/)

Selected documented compatibility floors, not recommendations to install these older versions:

| Integration | New API support / migration detail |
|---|---|
| Official Terraform provider | `hetznercloud/hcloud` 1.54.0+ |
| Official Ansible collection | `hetzner.hcloud` 5.4.0+ |
| lego | 4.27.0+; use `HETZNER_API_TOKEN` |
| acme.sh | New provider name `dns_hetznercloud` |
| Kubernetes | Official external-dns and cert-manager webhooks available |

Verify the exact installed integration, authentication variable, project, provider name, and release notes. A product saying “Hetzner DNS supported” may mean only the legacy API. [Integration matrix](https://docs.hetzner.com/networking/dns/migration-to-hetzner-console/features-and-differences/)

## RRSet and delegation constraints

Manage a zone as record sets grouped by owner name and type. Read the complete RRSet before replacing it so another TXT challenge, MX target, or A address is not lost. Distinguish replacing a set from adding/removing records through action endpoints; check the current request schema and completed action. [Cloud DNS API](https://docs.hetzner.cloud/reference/cloud#zones)

Since **2026-09-30**, `change_ttl` requires an explicit `ttl`: a number for that RRSet, or `null` for the zone default. Omission is no longer accepted. [API changelog](https://docs.hetzner.cloud/changelog)

New zones automatically receive SOA and NS records, not application A/MX records. In zone-file values, a fully qualified CNAME/MX/NS/SRV target normally needs its terminal dot; omitting it can append the current zone unexpectedly. Inspect the resulting name rather than applying one dot rule to every API field. [Record FAQ](https://docs.hetzner.com/networking/dns/faq/records/)

Do not equate creating a zone with registering a domain or activating delegation. Configure the nameservers shown for that zone at its registrar. The current FAQ states that incorrectly delegated zones can be automatically deleted after more than 28 days. Account for this when creating staging zones or planning a long migration. [General DNS FAQ](https://docs.hetzner.com/networking/dns/faq/general/)

Documented boundaries: subzones are unsupported; Hetzner can serve as secondary to an external primary, including TSIG, but the inverse external-secondary setup is unsupported. TSIG authenticates transfers; it does not encrypt them. [Zone FAQ](https://docs.hetzner.com/networking/dns/faq/zones/)

DS record support alone is not evidence of managed DNSSEC signing: the current DS documentation says DNSKEY records are not supported. Verify hosted-zone signing capability and registrar DS handling separately before promising DNSSEC or DANE. [DS record](https://docs.hetzner.com/networking/dns/record-types/ds-record/)

## Migration runbook

1. Export the current zone and inventory every writer: IaC, dynamic DNS, ACME clients, Kubernetes, control panels, scripts, and human operators. Preserve TTLs and multi-value TXT/MX records.
2. Identify whether this is an internal legacy-console migration, an external authoritative-DNS move, or a domain registration transfer. These are different operations.
3. Select the destination project and compatible integration versions. Prepare a new project token in a secret store. Plan which system owns each RRSet.
4. Test read access and a disposable record using the new integration. For certificates, test a renewal or the ACME staging service as appropriate; a currently valid certificate can hide broken renewal automation.
5. For an authoritative nameserver change, lower relevant TTLs in advance, wait out the old TTL, check the target zone directly, and then change delegation. Preserve the source zone through the cache transition.
6. Compare authoritative answers and external recursive resolution for A, AAAA, MX, TXT, CAA, and application-specific records. Check DNSSEC/DS continuity where applicable.
7. Remove old credentials only after all writers and renewal jobs are confirmed on the new API. Record the source export and exact rollback boundary.

Never “fix” a migration by deleting/recreating all zones without reviewing delegation, zone protection, ownership, and certificate dependencies.

## TLS choices and readiness

Choose where TLS terminates:

| Choice | Responsibility |
|---|---|
| Hetzner managed certificate on an HTTPS LB service | Hetzner issues and renews the certificate |
| Uploaded certificate on an HTTPS LB service | Operator obtains, uploads, and renews it |
| TCP LB service forwarding TLS to a reverse proxy | Backend manages TLS and certificate renewal |

Managed certificates require a Hetzner DNS zone. The certificate FAQ also documents external DNS with delegated ACME challenges, so moving the entire public zone is not always necessary. Follow that documented delegation arrangement rather than assuming arbitrary `_acme-challenge` subzones can be created. [Certificate FAQ](https://docs.hetzner.com/networking/certificates/faq/)

A zone's “Share zone with other projects” option enables managed certificate use across projects; the certificate and its Load Balancer still belong to the relevant project. Review the expanded scope before enabling sharing. [DNS project sharing](https://docs.hetzner.com/networking/dns/faq/general/)

Separate certificate issuance from backend readiness. Verify certificate/action state, SNI name, full chain, listener port, target health, readiness path, and private reachability before changing production DNS. Hetzner HTTPS services terminate TLS and use HTTP toward targets; use a TCP service for end-to-end backend TLS. HTTPS health checks are a separate capability. [Load Balancer protocol behavior](https://docs.hetzner.com/networking/load-balancers/faq/)

## Reverse DNS and diagnosis

Set a public IP's PTR through its resource's reverse-DNS operation; adding a PTR inside an unrelated forward zone does not change reverse delegation. Cloud Server/Primary IP, Floating IP, and Load Balancer operations are distinct. Since **2026-09-30**, explicitly include `dns_ptr`; rDNS names must not have a trailing dot. [API changelog](https://docs.hetzner.cloud/changelog) [DNS architecture](https://docs.hetzner.com/networking/dns/technical-concepts/architecture/)

Use nonsecret probes, replacing example values:

```bash
dig +short NS example.com
dig @hydrogen.ns.hetzner.com example.com A
dig example.com AAAA
dig example.com CAA
dig -x 203.0.113.10
curl -I --resolve app.example.com:443:203.0.113.10 https://app.example.com/
```

When resolution fails, distinguish delegation failure, missing record, stale cache, broken DNSSEC, split DNS, IPv6 reachability, and an application/TLS error. Preserve the exact query, authoritative response, resolver, and timestamp so retries answer a specific hypothesis.
