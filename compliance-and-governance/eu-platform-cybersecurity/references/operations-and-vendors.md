# Operations, recovery, logging, and suppliers

## Operating system of controls

Maintain named owners for identity/access, infrastructure, application security, AI safety integration, incident response, privacy, vendor management, and business continuity. Map shared responsibilities explicitly between the platform, hosting provider, model provider, customer administrators, and managed-service contractors. Use contractual commitments as inputs to control design; do not assume the provider covers what its service contract excludes.

Sources: SEC-GDPR Articles 28/32; SEC-BSIG-CONTROLS; SEC-NIS-IR and SEC-ENISA-NIS where relevant. The concrete patterns below are risk-based implementations, not mandatory product selections.

## Access and support

Use individual identities, appropriate MFA, short-lived privileges, separation of tenant and platform administration, and prompt revocation. Test joins, role changes, departures, break-glass use, and token theft. Record the purpose and scope of support access; require a real audit trail and avoid browsing customer content out of curiosity. Assess international support access with data-governance; EU server location alone is insufficient.

Audit API keys, webhook secrets, recovery codes, service accounts, certificate issuance, database users, cluster administration, and object storage access. Ensure emergency access survives an identity-provider outage without becoming an unmonitored bypass. Rehearse recovery of control-plane credentials and encryption keys.

## Backups and continuity

Set RTO/RPO from the service and customer contract. Identify critical dependencies: DNS, PKI, identity, secrets, database, object store, vector store, queue, GPU/model serving, provider credits, payment processor, registry, and staff. Distinguish redundancy, disaster recovery, backup, and export; each solves a different failure mode.

Test recovery in an isolated environment with sanitized data or appropriate protections. Verify data consistency, tenant permissions, key availability, connection routing, and deletion tombstones after restoration. A successful backup job is not proof of restore capability. Document failure assumptions such as compromised admin account, ransomware affecting online backups, one-region loss, model-provider exit, and exhausted budget.

Retention and deletion must remain coherent. Keep backups inaccessible to normal application queries, expire them under a documented schedule, and reapply valid deletion/suppression records when restoring. Do not retain all content indefinitely because it might help an incident investigation. Route statutory retention and legal holds to data-governance/legal review.

## Logging and detection

Collect enough events to reconstruct security-relevant actions: authentication, authorization failure, privilege change, sensitive object access, export, external tool invocation, admin operation, build/release, key rotation, and incident decision. Store actor/tenant/object/action/result/time and safe correlation identifiers. Avoid default full-content prompt logging and redact secrets before events leave the service.

Protect logs against unauthorized editing and broad support access. Record retention, lawful basis/purpose, regional processing, vendor access, and deletion. Test that audit events cannot be forged by model output or user-supplied IDs. A monitoring agent must not treat logs as trusted instructions or open arbitrary links embedded in an alert.

Use alerts tied to action: abnormal cross-tenant denials, bulk export, unexpected egress, privileged token use, modified policy gates, provider-route changes, expensive recursion, restoration failures, and new actively exploited dependency exposure. Assign severity, owner, response budget, and suppression expiry. “Alerts exist” without staffed ownership is not a response capability.

## Vendor and customer evidence

Collect service description, processing roles, security schedule, incident-notification terms, support locations, subprocessors, audit evidence scope/date, business continuity, exit/data return, and change notice. Review what an ISO/SOC report actually covers and its exceptions; a logo is not evidence for your configuration. Access to a report can be limited; record the reviewed portion without inventing assurance.

For model providers record retention/no-training options, abuse-monitoring exceptions, fallback models, subprocessors, encryption, admin access, regional routing and actual settings. For self-hosting record the same responsibilities now held internally; replacing an API does not remove security work.

Provide customers accurate security statements. Do not promise end-to-end encryption if the service decrypts content for inference, “zero retention” while abuse logs persist, or absolute isolation from a design that has not been tested. Maintain a contract-to-control mapping and alert the account/legal owner before a change breaks a promise.

## Operating reviews

Choose risk-based cadence with the owner. Candidate events include new vulnerabilities, permission changes, failed backups, expiring certificates/keys, subprocessor changes, product releases, new countries and material incidents. Do not create a recurring external automation merely because the skill describes a cadence.

Evidence outputs: dependency map; access review; restore report; incident drill; supplier register; detection coverage; current exceptions; overdue actions; reviewed legal-source versions. Expose freshness and missing evidence rather than presenting a green dashboard from old questionnaires.
