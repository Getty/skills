# Certificate profiles, enrollment and requester authorization

**Read when:** defining CA roles or deciding who may obtain which identities.

## Make profiles explicit policy objects

For each profile specify: allowed identity namespace, SAN forms, EKU/KU, CA status, algorithm policy, validity/renewal window, issuance authorization, key-generation location, audit fields and revocation behavior. Test rejected requests as carefully as successful issuance.

An issuing intermediate should have appropriate CA constraints and bounded delegation. `pathLenConstraint=0` limits further non-self-issued CA certificates in the path; it is not a count of leaf certificates and does not by itself restrict the DNS names that issuer may sign. Name constraints and enrollment policy solve different parts of that problem.

## Enrollment pipeline

```text
Requester bootstrap identity
  → authenticate requester
  → derive permitted certificate identity from policy
  → validate CSR and key constraints
  → sign bounded profile
  → return leaf/chain, never grant extra authorization implicitly
```

Prefer deriving sensitive names from the authenticated workload context rather than trusting arbitrary CSR fields. Test cross-tenant SAN requests, wildcard escalation, unauthorized URI identities, CA:true requests, excessive lifetime and forbidden dual-purpose EKUs.

## Enrollment protocol choice

ACME is well suited to automated certificate management with supported identifier validation. EST offers enrollment over authenticated TLS in managed-device/enterprise contexts. Device ecosystems may impose other protocols, vendor provisioning or hardware attestation. Select a maintained implementation for the required workflow rather than inventing a signing endpoint that accepts any authenticated CSR.

A bearer token embedded in a base image can enroll every copy as the same principal. Prefer short-lived, scoped bootstrap credentials or workload/device attestation. Document the first-boot trust decision and how an attacker is prevented from replaying it on another machine.

## Key generation and signing

A local CSR flow keeps the private key at the endpoint or its hardware custodian. A central issue flow can generate and return the private key, making transport, logging, persistence and CA-side access part of the key's threat model. Both can be valid designs; they are not equivalent security properties.

Separate permission to request a bounded leaf from permission to create issuers, alter profiles, change publication URLs or export keys. Role names alone do not enforce least privilege; review the actual API paths and constraints.

## Acceptance evidence

Record the authenticated principal, derived identity, profile version, public-key fingerprint, issuer, serial, validity and decision. Do not log private keys or bootstrap secrets. Verify that a denied request leaves no issued certificate and that audit evidence is available even when the request fails.

## Primary references

- **RFC5280** — [X.509 certificates and CRLs / PKIX](https://www.rfc-editor.org/rfc/rfc5280.html).
- **RFC7030** — [Enrollment over Secure Transport](https://datatracker.ietf.org/doc/html/rfc7030).
- **RFC8555** — [Automated Certificate Management Environment](https://www.rfc-editor.org/rfc/rfc8555.html).
- **OPENBAO-PKI** — [OpenBao PKI secrets engine](https://openbao.org/docs/secrets/pki/).
- **OPENBAO-CONSIDER** — [OpenBao PKI design considerations](https://openbao.org/docs/secrets/pki/considerations/).
- **SPIFFE** — [SPIFFE concepts, identities and workload API](https://spiffe.io/docs/latest/spiffe-about/spiffe-concepts/).
- **OPENSSL-REQ** — [OpenSSL 3.5 req](https://docs.openssl.org/3.5/man1/openssl-req/).

Reference snapshot: **2026-10-10**. For dated policy, distinguish current rules from future effective dates.
