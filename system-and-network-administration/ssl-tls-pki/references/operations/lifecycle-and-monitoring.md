# Certificate inventory, monitoring and operating objectives

**Read when:** making TLS dependable beyond the initial deployment.

## Inventory the deployed credential, not only the issuance record

Track owner, service identity, endpoint/port, environment, issuer, SAN set, purpose, public-key/certificate fingerprint, lifetime, renewal mechanism, deployment mechanism, trust consumers and incident contact. Do not store private keys in the inventory.

Represent one certificate used by several replicas as a shared deployment with per-endpoint observations. A central expiry dashboard can miss a forgotten edge node serving an older generation.

## Monitor the full chain of responsibility

| Signal | What it detects |
|---|---|
| Last successful authorization/issuance | CA/DNS/account failures |
| Candidate validation result | Wrong key, names, purpose or unexpected profile |
| Deployment and reload status | Broken hooks and rejected configuration |
| Live endpoint fingerprint | Stale replicas and incorrect routing |
| Remaining validity of selected path | Leaf and issuer expiration risk |
| Trust-bundle version/convergence | Clients not ready for a root migration |
| Revocation-publication freshness | Stale CRLs/responders where relied upon |
| Unexpected issuance / enrollment volume | Misuse or runaway automation |

Keep low-cardinality service metrics separate from high-cardinality certificate evidence where needed. Logging every connection's full certificate can leak names and create noisy monitoring without improving response.

## Recovery-aware thresholds

Choose alert thresholds from the actual lifetime and required recovery margin. A fixed 30-day warning is meaningless for a 160-hour certificate and can be noisy for a 45-day one. Escalate issuance failures before the remaining window becomes an emergency.

Use independent vantage points when the service has multiple regions, proxies or address families. Monitor with the intended reference identity and trust policy; an insecure expiry-only probe can report a forged endpoint's dates.

## Operational exercises

Rehearse a failed reload, inaccessible DNS API, issuer outage, stale root bundle and single-replica drift. Confirm the alerts reach someone who can perform the relevant recovery. Distinguish “renewal job ran” from “valid credential is live and accepted.”

Tie certificate inventory to service retirement. Remove unused DNS validation grants, client identities and secrets rather than allowing unattended renewal forever. Maintain a change history for profile, issuer and trust migrations.

## Primary references

- **CERTBOT** — [Certbot user guide](https://eff-certbot.readthedocs.io/en/stable/using.html).
- **CM-CERT** — [cert-manager Certificate resources and renewal](https://cert-manager.io/docs/usage/certificate/).
- **RFC9773** — [ACME Renewal Information](https://www.rfc-editor.org/rfc/rfc9773.html).
- **LE-64D** — [64-day certificates: announcement on 2026-10-07](https://letsencrypt.org/2026/10/07/64-day-certs).
- **LE-LIMITS** — [Let’s Encrypt rate limits](https://letsencrypt.org/docs/rate-limits/).
- **OPENBAO-CONSIDER** — [OpenBao PKI design considerations](https://openbao.org/docs/secrets/pki/considerations/).

Reference snapshot: **2026-10-10**. For dated policy, distinguish current rules from future effective dates.
