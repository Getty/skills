# Implementation patterns: OpenBao, step-ca and SPIFFE/SPIRE

**Read when:** selecting a private-PKI implementation without confusing product roles.

## Choose by responsibility

| Pattern | Strong fit | Questions to resolve |
|---|---|---|
| OpenBao PKI | Policy-controlled issuance integrated with secret/auth workflows | Issuer/key storage, role constraints, HA, publication and recovery |
| step-ca | A focused online CA and automated enrollment | Provisioners, supported protocols, trust bootstrap and edition/version boundaries |
| SPIFFE/SPIRE | Attested workload identities and automated short-lived SVIDs | Attestation, trust domains, workload API, federation and authorization |

These are not interchangeable services. A secrets engine is not automatically a complete device-management system; a CA is not automatically a workload attestor; workload identity does not automatically supply application authorization.

## OpenBao design route

Prefer an online intermediate under an independently protected root when that matches the risk model. Use bounded roles for names, purposes and lifetimes, and narrowly scoped API permissions. Decide whether endpoints submit CSRs or receive centrally generated keys. Configure distribution URLs and issuer chains deliberately.

Separate the TLS certificate protecting OpenBao's API from the certificates its PKI engine issues. Map the authentication path that lets a workload request a credential, including initial bootstrap and recovery. Review actual OpenBao documentation for the deployed version; do not assume every Vault-specific enterprise capability or configuration example applies.

## step-ca route

Inventory supported provisioners/enrollment flows, key custody, certificate templates, policy enforcement, revocation/publication and HA requirements. Distinguish the open-source CA's capabilities from managed/commercial offerings. Verify feature support against the chosen release rather than promoting a vendor overview into a universal guarantee.

Test both issuance and client trust bootstrap. A convenient root download command still needs an authenticated fingerprint or another reliable trust source.

## SPIFFE/SPIRE route

Use a deliberate trust-domain name, node/workload attestation policy and registration model. Obtain identities through the supported workload API and use a compatible TLS/SVID verification library. Authorization should be based on intended workload identities, not merely any member of a trusted domain.

Federation expands the set of authorities whose assertions may be accepted. Inventory that expansion and test foreign-domain identities that must be rejected. Do not convert every accepted federation bundle into broad authorization.

## Proof before selection

Build a small non-production proof: issue an authorized identity, reject a cross-tenant request, rotate a leaf without outage, rotate an issuer, revoke/offboard a principal, and restore from backup. Measure the operational work and failure behavior rather than choosing only by the shortest quick-start guide.

## Primary references

- **OPENBAO-PKI** — [OpenBao PKI secrets engine](https://openbao.org/docs/secrets/pki/).
- **OPENBAO-CONSIDER** — [OpenBao PKI design considerations](https://openbao.org/docs/secrets/pki/considerations/).
- **STEP-CA** — [Smallstep step-ca open-source overview](https://smallstep.com/docs/step-ca/).
- **SPIFFE** — [SPIFFE concepts, identities and workload API](https://spiffe.io/docs/latest/spiffe-about/spiffe-concepts/).
- **CM-TRUST** — [cert-manager trust-manager](https://cert-manager.io/docs/trust/trust-manager/).

Reference snapshot: **2026-10-10**. For dated policy, distinguish current rules from future effective dates.
