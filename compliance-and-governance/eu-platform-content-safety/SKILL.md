---
name: eu-platform-content-safety
description: "Use when users can publish, share or report content, a marketplace or agent store is added, minors may use the service, or a takedown notice, appeal or government or e-evidence order arrives — DSA, notice and action, statement of reasons, DDG, JMStV, JuSchG, age assurance."
---

# EU Platform Content Safety

Build service-specific safeguards and evidence for the content the platform generates, stores, distributes or intermediates.
Use the EU layer first and load the relevant national adapter.
Treat 2026-10-22 as the research snapshot and refresh changing law before consequential decisions.

## Classify before implementing

Read [service-classification.md](references/service-classification.md) and [sources.md](references/sources.md).
Separate private AI interaction, private document hosting, public share links, searchable galleries, community channels, external search, and marketplaces.
For each feature record who supplies the content, whether it is stored on request, who can receive it, whether access is individually selected, and who has editorial control.
Do not infer DSA “online platform” status from the product's marketing name.
Do not infer absence of hosting duties merely because the feature is not public.

Record legal entity, establishment, targeted countries, EU recipients, enterprise size/group, designation, minors' access, and other relevant services.
Use `applicable`, `not_applicable`, `unknown`, or `future` with reasons and evidence.
Use [service-classification.json](assets/service-classification.json) as a fact record.

## Route only the relevant references

| Topic | Reference |
|---|---|
| DSA role, mixed services, public/private boundary | [service-classification.md](references/service-classification.md) |
| Conditional obligations and exemptions | [dsa-obligations.md](references/dsa-obligations.md) |
| Reports, decisions, reasons and redress | [notice-action-appeals.md](references/notice-action-appeals.md) |
| Child-safe product/age assurance | [minors-eu.md](references/minors-eu.md) |
| German youth/content law and exclusions | [german-youth-overlay.md](references/german-youth-overlay.md) |
| Orders, e-evidence, terrorist content | [government-orders.md](references/government-orders.md) |
| Third-party sellers, app/agent store, ranking | [marketplaces-and-business-users.md](references/marketplaces-and-business-users.md) |
| Imprint, policies, AI outputs and transparency | [notices-moderation-ai.md](references/notices-moderation-ai.md) |
| Tests, operations and evidence | [verification-and-operations.md](references/verification-and-operations.md) |
| Additional countries, sectors and workforces | [country-sector-routing.md](references/country-sector-routing.md) |

## Core workflow

### 1. Build an applicability record

Classify each service and each material content flow.
Identify applicable DSA tiers and precise SME exemptions; do not call small firms wholly exempt.
Distinguish the EU regulation from national substantive content rules and national implementation.
Check current amendments, entry/application dates, designations and official guidance.
Record uncertainty as an unresolved scoped decision with an owner.

### 2. Define policy and responsibility

Distinguish illegal content, harmful-but-lawful content, contractual policy breaches, privacy complaints, intellectual-property complaints, and safety incidents.
For each restriction record its legal or contractual basis and intended proportionality.
Assign policy owner, moderation operator, trained human escalation, privacy reviewer, legal reviewer and out-of-hours contact.
Treat model-generated classifications as evidence to review; do not treat a model's confidence as a legal finding.

### 3. Build product controls

Implement discoverable contact/report paths, accessible forms, acknowledgements, decision records, applicable reasons/redress, and privacy-safe evidence.
Add age-appropriate defaults and safeguards where justified by the applicable scope/risk assessment.
Apply restrictions at API, sharing, search, export and cached delivery paths, not only at the main UI.
Keep policy versions and effective dates aligned with actual behavior.
Use [public-notices-and-policy.md](assets/public-notices-and-policy.md) as a structured drafting brief.

### 4. Verify decisions and rights

Use [moderation-case.json](assets/moderation-case.json) to preserve the evidence, basis, action, automation, communication and appeal.
Test legitimate expression as well as unlawful-content scenarios with synthetic or sanitized material.
Test mistaken decisions, successful appeals, reinstatement, translations, accessibility, and abusive reporting.
Do not download or redistribute illegal material to create a test set; use safe surrogates and controlled specialist procedures.
Preserve applicable evidence and legal holds without retaining all customer content indefinitely.

### 5. Handle urgent matters

For a credible threat, mandatory report or official order, open [government-order-case.json](assets/government-order-case.json) and read [government-orders.md](references/government-orders.md).
Validate authority, authenticity, jurisdiction, scope, exact receipt time, legal route and deadline.
Page the authorized responsible person immediately; preserve the deadline while validity is assessed.
Prepare necessary records and drafts; submit, disclose, or contact authorities only under actual user/organizational authorization.
Do not turn a request for a compliance review into private-message surveillance or an unsolicited external report.
Escalate a missing authority to act explicitly when a deadline is approaching.

## Operating and release rules

- Reassess whenever private data becomes publicly shareable, public groups are added, a marketplace opens, ranking/ads change, a new age group is targeted, or the business enters another country.
- Reassess size/designation exemptions and each amendment's exact application date.
- Separate the DSA platform role, GDPR controller role, AI Act provider/deployer role and CRA manufacturer role. None is inferred from another.
- Block the affected feature when a mandatory prerequisite or a serious uncontrolled harm remains; identify the narrow release condition and continue unrelated authorized work.
- Do not let a generic disclaimer substitute for actual safeguards, user rights or a regulated-service qualification.
- Use monitoring cadence only under the user's authorization; this skill itself creates no scheduled job and performs no filings.

## Required output

Return the proposed feature/action and decision, followed by:

`finding_id | service | regime/source/article | applicability | facts | control/evidence | action/owner | deadline | residual uncertainty`

For an incident, include exact receipt/awareness times and next required action.
For an implementation, include changes, tests and remaining limitations.
Distinguish a draft, a tested local flow, and a live production observation.

## Coordinate with related skills

Use `eu-ai-act` for AI prohibited practices, Article 50 and risk classification; `eu-platform-privacy` for data processing/children/automated decisions; `eu-ai-data-ip` for content rights; `eu-platform-consumer-commerce` and `eu-platform-business-contracts` for contracts; and `eu-platform-cybersecurity` for security incidents.
If a sibling is absent, complete this skill's scope and identify the missing review explicitly.
