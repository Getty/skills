---
name: eu-platform-data-governance
description: "Use when defining data retention, deletion or backups, tracing RAG, vector or training data, anonymising, onboarding a processor or subprocessor, or moving personal data outside the EU — SCCs, transfer impact assessment, adequacy, EU-US Data Privacy Framework."
---

# EU Platform Data Governance

Connect each data use to its origin, permitted purpose, recipients, derivatives, lifetime, and evidence.
Cover customer content and operational data across the whole service, including external AI and agent tools.
Use this skill independently; ask the privacy owner for disputed legal-basis/role decisions.
If installed, use `eu-platform-privacy` for the broader GDPR assessment and rights process.

## Identify the work packet

1. Record the legal entities, countries, processing purposes, system/environment and proposed change.
2. Identify actual data classes and people affected, including third parties within customer content.
3. Map collection, ingestion, transformation, inference, logging, disclosure, backup and disposal.
4. Resolve controller/processor roles for each purpose; do not classify only the supplier company.
5. Mark unknown data paths, locations, retention settings and reuse rights as unresolved evidence gaps.
6. Select the relevant references and assets below.

Use synthetic fixtures for discovery/tests where possible.
Do not use live secrets or customer files as prompts to an unapproved review model.
Do not confuse data residency, corporate ownership, contractual location and remote access.

## Legal-source discipline

Read [sources.md](references/sources.md) before relying on transfer mechanisms or legal exemptions.
Record source version, legal status, operative date and assessment date separately.
Recheck adequacy decisions and the exact recipient's certification at the time of a transfer decision.
Distinguish adopted regulator guidance from drafts and legislative proposals.
Do not treat an encrypted or pseudonymised payload as outside the GDPR without a reasoned assessment.
Never invent retention periods, legal holds, certifications, deletion results or vendor assurances.

## Workflows

### Map and minimise

Read [inventory-retention-erasure.md](references/inventory-retention-erasure.md).
Use [data-register.yaml](assets/data-register.yaml) for each data class and its derivatives.
Include queues, exports, support tickets, external embeddings, traces and crash reports.
Link retention to purposes and exact legal/contractual requirements; mark examples as policy choices.
Choose a reversible data minimisation change where it resolves an issue without requiring a legal decision.

### Implement deletion and restriction

Use [erasure-runbook.md](assets/erasure-runbook.md) for a bounded plan and completion evidence.
Separate account closure, erasure, contract exit/export, restriction and a specific legal hold.
Verify all derived data, provider copies, and restore behaviour, not only the primary database row.
Do not claim completion until the actual scope and any lawful retained residue are recorded.
Escalate disputed exceptions, destructive shared-key actions, and model-level deletion uncertainty.

### Govern RAG, training, and evaluation

Read [rag-training-data.md](references/rag-training-data.md).
Keep retrieval, fine-tuning, training, evaluation, safety monitoring and service improvement as separate uses.
Trace source document/version/ACL to chunks, embeddings, summaries, prompts, outputs and cached results.
Require a documented assessment for anonymity and training reuse; hashes and vectors are not a shortcut.
Route copyright/licensing and AI Act duties to their relevant workflows as additional obligations.

### Review suppliers and provider changes

Read [processors-vendors.md](references/processors-vendors.md).
Use [vendor-transfer-review.md](assets/vendor-transfer-review.md) for the exact product/SKU and contract.
Reconcile paper commitments with API settings, observed request routes and actual support access.
Verify subprocessor authorisation/change handling and an operational exit/deletion path.
Treat a fallback provider or diagnostic endpoint as a real recipient.

### Assess international transfers

Read [transfers.md](references/transfers.md).
Identify exporter, recipient, countries, remote access, data and each onward hop.
Apply the Chapter V transfer test before selecting a mechanism.
Check the scope of adequacy or the applicable safeguard/instrument, including its eligibility limits.
Do not treat a signed SCC or an EU data centre as the complete assessment.
When no valid route is established, keep the affected new route disabled and escalate the concrete gap.

### Operate and prove the controls

Read [operational-evidence.md](references/operational-evidence.md).
Link tests to system versions and actual data paths; record limitations and failed/partial jobs.
Protect evidence that itself contains personal data or secrets.
Set operational review frequencies based on change/risk; label them as policy rather than statutory periods.

## Jurisdiction and sector overlays

Read [jurisdiction-overlays.md](references/jurisdiction-overlays.md).
Apply local tax/accounting, limitation/claims, employment and professional-secrecy requirements only where relevant.
Do not translate a German retention schedule into an EU-wide schedule.
Do not treat the UK or Switzerland as inside the EEA; verify applicable transfers and local laws separately.
Screen Data Act portability/switching and sector contracts in addition to GDPR rights when appropriate.

## Reopen on changes

Trigger review for a new provider, subprocessor, service tier, model endpoint, fallback, region,
support country, retention flag, dataset, training opt-in, shared cache, connector, or backup design.
Trigger review after a legal mechanism changes, certification lapses, deletion fails, or a supplier incident occurs.
Record which prior decisions are invalidated and which remain supported.
Do not restart every control review for an unrelated cosmetic change.

## Required output

Return the affected data/recipient map plus:

| Item | Required record |
| --- | --- |
| Applicability | Entity, country, purpose, role, source/article and reasoning |
| Data lifecycle | Origin, permitted uses, derivatives, locations, access, retention, disposal |
| Supplier/transfer | Exact entity/product, contracts, mechanism/scope, safeguards, review date |
| Status | `satisfied`, `gap`, `needs-evidence`, `needs-review`, or justified `not-applicable` |
| Evidence | Actual test/configuration/contract record, date, version, owner and restricted location |
| Action | Concrete change, owner, due date, affected release consequence and residual uncertainty |

Separate a capability demonstrated with synthetic data from confirmation of a specific production deletion.
Complete authorised implementation and evidence collection; reserve disputed legal determinations for the owner.
Do not send vendor/customer/legal messages without an established mandate or explicit authorisation.
