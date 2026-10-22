# Processor, subprocessor, and AI-vendor review

Sources: GDPR Arts 24, 28–29, 32, 44–49 (D1); transfer sources D2–D7. Assess actual facts for each product, purpose and legal entity.

## Scope the exact service

Record contracting entity, service/SKU, region, API endpoints, account tier, optional features, model versions, content categories, support route, fallback providers and intended volume/sensitivity. Consumer chat, enterprise chat and developer API terms may differ. A vendor's generic privacy statement does not establish the terms of the purchased service.

Resolve whether each use is processing on instructions, separate controllership or joint control. Capture actual training, human review, abuse/security processing and legal-request practices. A claim of no model training does not imply no storage, no human access, no secondary metadata use or no international transfer.

## Article 28 contract and operational checklist

Verify the required subject matter, duration, nature/purpose, data types and subject categories; documented instructions including transfers; confidentiality; security; subprocessor authorisation and flow-down; rights assistance; assistance with security/breach/DPIA duties; deletion/return and permitted legal retention; evidence/audit cooperation; and informing the controller if instructions infringe relevant data-protection law.

Assess sufficient guarantees instead of treating the signed agreement as the whole control. Request concrete evidence proportionate to risk: access design, independent assurance scope, deletion/backup policy, incident process, vulnerability management and contractual limitations. A security certificate is useful evidence within its scope; it is not a GDPR approval.

For general subprocessor authorisation, verify how changes are notified and how a real opportunity to object works. Record identity, service, locations, data and transfer route for each relevant subprocessor. Do not promise the customer an objection right that the platform cannot operationalise.

## Reconcile promises with technical settings

| Contract/product claim | Check |
| --- | --- |
| EU region | Content and metadata routes, backups, control plane, support access, subprocessors and disaster recovery |
| No training | Exact data/classes/features covered; feedback opt-in, evaluation, abuse review and customer fine-tuning |
| Zero retention | Eligible endpoints/models, exceptions, caches/files/batch jobs, abuse logs, approval prerequisites |
| Customer-managed keys | Who can access plaintext and keys; in-use processing; recovery/escrow; actual access isolation |
| Delete API | Semantics, completion time, derived stores, backups, vendor confirmation and surviving legal duties |
| Dedicated tenant | Logical/physical isolation scope, support privileges, shared caches and diagnostic channels |

Collect actual configuration exports and synthetic request traces where authorised. Avoid aggressive vendor probing or sensitive test data. Recheck settings after SDK or endpoint migrations.

## Exit and change control

Design a tested export/return, access revocation, deletion, backup-expiry and evidence path before adopting a supplier for critical data. Separate GDPR return/deletion obligations from commercial switching and any Data Act duties. Contract termination must not orphan subject rights or leave uncontrolled training copies.

Reassess a service when pricing tier, contracting entity, terms, training default, endpoint, support region, subprocessor or transfer mechanism changes. Record the affected purpose and whether customer instructions/notice/approval need updating. Do not let automatic model fallback bypass the approved-recipient list.

If a material claim cannot be substantiated, record `needs-evidence` with the concrete request and restricted use scope. Continue safe integration work with synthetic fixtures. Escalate a supplier's incompatible purpose, missing required agreement or unestablished transfer route before real data is enabled.
