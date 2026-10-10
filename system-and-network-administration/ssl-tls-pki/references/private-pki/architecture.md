# Designing private CA infrastructure and trust domains

**Read when:** building an internal SSL infrastructure rather than obtaining one certificate.

## Start with relying parties and authority

Inventory service identities, human/device/workload clients, network boundaries and owners. Define which issuer may assert which identity for which purpose. Separate production from development and distinguish server authentication from client/workload identity when their risk and administration differ.

A practical proposed baseline is an offline root with protected recovery material, an online issuing intermediate per appropriate trust boundary, an authenticated enrollment service, separately available revocation publication, and managed trust distribution. This is a design recommendation, not a claim that every small system needs multiple CA products.

```text
Offline root / ceremony and recovery
  ├─ Production server issuer → DNS/IP server profiles
  └─ Production client issuer → constrained workload/client identities

Bootstrap/attestation → enrollment policy → signing service → credential delivery
Root bundle distribution ───────────────────────────────→ relying clients/servers
Inventory + renewal + deployment probes + revocation ──→ operational control
```

Consider a different root, not merely another intermediate, when environments must not trust one another. Putting every issuer under an unconstrained shared anchor can create a broader trust domain than the organizational diagram suggests.

## Separate planes

The **issuance plane** authenticates requesters, authorizes identities and signs certificates. The **trust plane** distributes anchors and constraints. The **data plane** performs TLS handshakes and application authorization. The **operations plane** manages policy, audits, publication, renewal and recovery. A healthy signing API does not imply healthy trust distribution or successful application reloads.

## Avoid bootstrap cycles

Draw startup dependencies. A CA may need storage, authentication, DNS and a serving certificate. Recovery must remain possible when normal identity services or its own serving certificate are unavailable. Design a restricted, authenticated administrative recovery path and root/trust bootstrap mechanism before deployment.

For example, do not make restoration of the only issuer depend on downloading an image from a registry whose expired certificate can only be renewed by that issuer. Keep authenticated recovery artifacts and credentials available through an independently recoverable path.

## Choose certificate boundaries

Use public Web PKI for public-facing endpoints whose clients you cannot provision. Use private issuance for controlled service identities and mTLS clients. The edge may present a public certificate while independently validating an internal server certificate. Never use the entire public root store as a blanket authority for privileged client identities.

## Required design deliverables

Produce a trust graph, identity/profile table, enrollment policy, root custody procedure, distribution inventory, issuance/renewal SLO, compromise containment plan and root-rotation schedule. Assign an owner to each—not just a VM name. The [architecture decision template](../../examples/architecture-decision-template.md) provides a starting point.

## Primary references

- **RFC5280** — [X.509 certificates and CRLs / PKIX](https://www.rfc-editor.org/rfc/rfc5280.html).
- **OPENBAO-CONSIDER** — [OpenBao PKI design considerations](https://openbao.org/docs/secrets/pki/considerations/).
- **STEP-CA** — [Smallstep step-ca open-source overview](https://smallstep.com/docs/step-ca/).
- **SPIFFE** — [SPIFFE concepts, identities and workload API](https://spiffe.io/docs/latest/spiffe-about/spiffe-concepts/).
- **CM-TRUST** — [cert-manager trust-manager](https://cert-manager.io/docs/trust/trust-manager/).
- **NGINX-PROXY** — [NGINX HTTP proxy module](https://nginx.org/en/docs/http/ngx_http_proxy_module.html).

Reference snapshot: **2026-10-10**. For dated policy, distinguish current rules from future effective dates.
