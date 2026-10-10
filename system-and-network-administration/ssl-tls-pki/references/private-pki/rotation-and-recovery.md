# Leaf, issuer and root rotation; disaster recovery

**Read when:** planning renewal, CA replacement or recovery after compromise.

## Three different changes

**Leaf renewal** replaces one credential and its deployment generation. **Intermediate rotation** changes an online issuer and possibly the chain served by many endpoints. **Root rotation** changes the relying parties' trust inputs and often takes much longer than issuance.

Do not combine all three into one untested cutover. Assign separate observability and rollback criteria.

## Planned root migration

A proposed sequence is: inventory relying parties; create and approve the new hierarchy; distribute a bundle that trusts both intended roots; verify new-root acceptance and out-of-scope rejection; start new issuance; replace old leaves and chains; observe convergence; remove the old anchor after dependencies are retired.

Overlap is a deliberate transition, not permission to retain obsolete roots indefinitely. Offline devices, pinned applications, firmware images and disaster-recovery tooling can be the long tail. Cross-signing can help selected clients but creates more paths to test and is not a substitute for a trust-distribution plan.

## Recovery matrix

| Event | Immediate concern | Wider work |
|---|---|---|
| Leaf key exposed | Stop impersonation using that key | Revoke where enforceable, replace key/cert, investigate exposure |
| ACME/DNS credential exposed | Unauthorized future issuance | Remove authority, inspect issuance, rotate affected identities |
| Intermediate compromised | Many identities can be forged | Disable issuance, replace hierarchy segment, update trust/constraints |
| Root compromised | Anchor authority is untrustworthy | Authenticated trust replacement across all relying parties |
| Issuer unavailable | Renewal cannot complete | Restore/fail over before the recovery margin is consumed |
| Serving certificate expired | Administrative or data-plane lockout | Use predesigned authenticated recovery path, not disabled verification |

Revocation alone may not terminate existing sessions. Review session tickets, connection draining and application authorization caches. Revoke enrollment grants too; otherwise replacement credentials may be issued back to the compromised principal.

## Restore drills

Use an isolated environment to restore issuer state and validate that policies, revocation data and audit behavior survived. Check whether the restored issuer certificate is still valid and whether the recovery tooling can authenticate without the failed infrastructure.

Define RTO/RPO for signing state, trust distribution and credential deployment separately. A restored database is not sufficient evidence of a restored PKI service. Document manual decisions requiring two-person review and retain a clean, authenticated copy of the recovery procedure.

For a planned migration, rollback can return to a still-trusted uncompromised hierarchy. For a compromise, that same rollback may be prohibited. Make this distinction explicit in the change plan.

## Primary references

- **RFC5280** — [X.509 certificates and CRLs / PKIX](https://www.rfc-editor.org/rfc/rfc5280.html).
- **OPENBAO-CONSIDER** — [OpenBao PKI design considerations](https://openbao.org/docs/secrets/pki/considerations/).
- **LE-CHAINS** — [Let’s Encrypt roots and intermediates](https://letsencrypt.org/certificates/).
- **CM-TRUST** — [cert-manager trust-manager](https://cert-manager.io/docs/trust/trust-manager/).
- **RFC9846** — [TLS 1.3 — July 2026 revision](https://datatracker.ietf.org/doc/html/rfc9846).

Reference snapshot: **2026-10-10**. For dated policy, distinguish current rules from future effective dates.
