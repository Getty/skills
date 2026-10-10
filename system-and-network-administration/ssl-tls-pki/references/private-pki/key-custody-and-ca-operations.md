# CA key custody, ceremonies and dependable operation

**Read when:** taking a CA from a demo to a recoverable service.

## Protect authority, not just a PEM file

A CA key represents permission to assert identities across its scope. Protect it with administrative separation, limited signing interfaces, audited access and tested recovery. Keeping a root offline reduces routine exposure but does not protect a poorly controlled backup or signing ceremony.

For a proposed offline-root/online-intermediate design, define who can authorize a ceremony, who can operate the key, how the input CSR is authenticated, how constraints and fingerprints are independently checked, and where the signed output and audit record are stored. Avoid a single person's laptop becoming the undocumented root of the company.

## HSM, TPM and KMS choices

Hardware protection can reduce key extraction risk. It does not automatically prevent an authorized compromised service from requesting malicious signatures. Evaluate supported algorithms, APIs, throughput, latency, availability, audit integration, backup/replication and disaster recovery. Confirm that the chosen CA/TLS server supports the actual provider or key interface.

Compliance claims must refer to the exact validated module and operating conditions. A “FIPS” configuration flag is not sufficient evidence that a whole deployment is certified. Private-PKI requirements depend on the organization's risk and obligations; public-CA hardware rules are not automatically the same legal requirement for every private CA.

## Operational state

Back up keys or hardware recovery material according to their custody model, CA configuration, issuers, serial/revocation state, role policies, audit configuration and publication metadata. Document what cannot be exported. Verify restores into an isolated environment without accidentally creating a second unauthorized active issuer.

For online CA high availability, determine which state must be consistent and what happens during partition or failover. Do not invent a generic “copy the CA directory to two servers” design. A functioning API after failover does not establish consistent revocation state or safe signing authority.

## Publication and observability

Keep CRL/OCSP distribution, when used, available independently of the administrative signing path. Monitor signing failures, denied enrollment, unusual identity volume, issuer lifetime, publication freshness, storage health and audit-sink failures. Expiration of an intermediate can disable many otherwise unexpired leaves.

Patch the CA and crypto dependencies with a staged compatibility test. Preserve a minimal emergency procedure that does not require an unavailable normal identity provider. Restrict this recovery path, test it periodically, and ensure its use is visible and reviewed.

## Primary references

- **OPENBAO-CONSIDER** — [OpenBao PKI design considerations](https://openbao.org/docs/secrets/pki/considerations/).
- **STEP-CA** — [Smallstep step-ca open-source overview](https://smallstep.com/docs/step-ca/).
- **CABF-BR** — [CA/Browser Forum TLS Baseline Requirements — current HTML](https://cabforum.org/working-groups/server/baseline-requirements/requirements/).
- **OPENSSL-MIGRATION** — [OpenSSL 3.5 migration guide](https://docs.openssl.org/3.5/man7/ossl-guide-migration/).
- **RFC5280** — [X.509 certificates and CRLs / PKIX](https://www.rfc-editor.org/rfc/rfc5280.html).

Reference snapshot: **2026-10-10**. For dated policy, distinguish current rules from future effective dates.
