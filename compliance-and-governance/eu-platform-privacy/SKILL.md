---
name: eu-platform-privacy
description: "Use when a feature processes personal data in the EU — controller or processor role, lawful basis, consent or legitimate interest, RoPA, DPIA, DPO, privacy notice, access or erasure request, profiling and automated decisions, a personal-data breach. GDPR, BDSG."
---

# EU Platform Privacy

Turn a concrete processing operation into an evidenced decision, implementation requirements, and checks.
Use the EU GDPR core for EU/EEA operations and a verified country overlay for each relevant establishment and market.
Treat the UK, Switzerland, and other European non-EEA countries as separate legal scopes.
Use English working documents; preserve exact national legal terms and localise customer information appropriately.

## Establish the decision before reviewing code

1. Identify the legal entity, establishments, product, feature, environment, intended launch date, and data subjects.
2. Map collection, inference, storage, disclosure, support access, model calls, and deletion.
3. Classify the parties **for each purpose** as controller, joint controller, processor, or subprocessor.
4. Distinguish the platform's customer-account processing from customer-controlled workspace content.
5. Identify personal data, special categories, criminal-offence data, children, employees, and vulnerable groups.
6. Record what is known, what is assumed, and what evidence is missing.
7. Load the relevant references below rather than the entire collection.

Do not treat business customers, public-web data, pseudonyms, hashes, or vectors as outside the GDPR by default.
Do not infer a legal basis from a privacy notice, a vendor's marketing, or a contract label.
Do not upload production content to another AI tool to perform this assessment without an approved processing path.

## Source and date discipline

- Start with [sources.md](references/sources.md); record the assessment date and governing law version.
- Distinguish enacted law, applicable provisions, judgments, adopted guidance, consultation drafts, and proposals.
- Recheck amendments and territorial rules before a release decision or a numerical threshold calculation.
- If a primary source is unavailable, record the retrieval limitation and the unresolved proposition.
- Treat an unknown as `needs-evidence` or `needs-review`, never as `not-applicable`.
- Use a statutory article plus a source URL for a legal obligation; label engineering choices separately.
- Do not turn an engineering pass into a legal certification or a claim that all processing is lawful.

## Execute the review

### 1. Scope, roles, and lawful bases

Read [scope-roles-lawful-bases.md](references/scope-roles-lawful-bases.md).
Create one processing record per purpose with [processing-record.yaml](assets/processing-record.yaml).
Specify the Article 6 basis, additional Article 9/10 condition where needed, necessity, recipients, and safeguards.
Record a legitimate-interest assessment where relied on; do not use consent as a universal fallback.
For an Article 28 arrangement, verify actual instructions and vendor behaviour.
For training or evaluation reuse, assess the new purpose separately from providing the original service.

### 2. Risk, DPIA, and organisational responsibilities

Read [risk-dpia-dpo.md](references/risk-dpia-dpo.md).
Screen Article 35 and the relevant authority's mandatory DPIA list before implementing high-risk processing.
Assess Article 37 and applicable national DPO rules independently of the DPIA result.
Use [dpia-and-decision.md](assets/dpia-and-decision.md) to record alternatives, residual risk, and ownership.
Do not start processing that requires unresolved prior consultation under Article 36.
Keep DPO advice and management accountability distinct; the agent supports these roles.

### 3. Rights, notices, and significant decisions

Read [rights-transparency-decisions.md](references/rights-transparency-decisions.md).
Connect each collection point to accurate information and each data store to rights fulfilment.
Distinguish access, portability, rectification, erasure, restriction, and objection.
Screen consequential automated decisions even if the platform only supplies a decisive score to a customer.
Require meaningful human involvement where that is the asserted safeguard; record actual authority and practice.

### 4. Implement and verify

Read [privacy-engineering.md](references/privacy-engineering.md).
Specify bounded tests using synthetic data, isolated tenants, and controlled vendor settings.
Review database schemas, access controls, RAG filters, telemetry, prompts, queues, backups, and export paths.
Record the tested commit, configuration, environment, scope, result, and evidence location.
Route lifecycle/transfer implementation to `eu-platform-data-governance` when installed.
Route terminal access and campaigns to `eu-platform-tracking-marketing` when installed.
Keep their underlying obligations in scope if those companion skills are unavailable.

### 5. Operate and respond

Read [incidents.md](references/incidents.md) for a suspected personal-data breach.
Use the organisation's authorised incident process and preserve the legal decision clock.
Draft notices and authority reports for the authorised owner; do not send them without authorisation.
Do not silently delay a statutory deadline while waiting for a perfect root-cause analysis.

## National overlays

Read [jurisdiction-overlays.md](references/jurisdiction-overlays.md) for Germany and expansion work.
Determine the applicable national law, authority, child-consent age, employment rules, and local restrictions.
Do not copy Germany's DPO threshold, retention periods, or BDSG employment provisions into an EU-wide policy.
Screen sector rules separately for health, employment, credit, education, communications, and public services.

## Change triggers

Reopen the affected records after a new model, prompt-logging change, provider, region, support location,
subprocessor, dataset, new purpose, sharing feature, identity join, inference, or retention setting.
Also reopen after an incident, rights failure, regulator update, material judgment, or changed customer role.
Limit the review to affected processing and its dependencies; retain prior decisions with version links.
Use [privacy-change-review.md](assets/privacy-change-review.md) as the review packet.

## Return a decision-ready result

Return a scope statement and a table with:

| Field | Required content |
| --- | --- |
| Processing/feature | Exact feature, purpose, subjects, entity, country, environment |
| Obligation | Legal source, article, applicability reasoning, national overlay |
| Status | `satisfied`, `gap`, `needs-evidence`, `needs-review`, or reasoned `not-applicable` |
| Implementation | Required behaviour and concrete code/configuration location |
| Evidence | Test/record identifier, date, version, owner, retention/access restriction |
| Decision | Action, accountable owner, due date, release consequence, residual uncertainty |

Separate statutory requirements from regulator interpretation and recommended controls.
Explain the decisive unresolved issue rather than attaching a generic legal disclaimer.
Escalate consequential basis/role disputes, Article 9/10 uncertainty, residual high DPIA risk,
rights refusals, incompatible new purposes, and authority communications to the designated owner.
Continue authorised reversible inspection and remediation while those decisions are pending.
Never accept a blanket waiver that purports to override a statutory prohibition.
