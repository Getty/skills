---
name: eu-ai-act
description: "Use when classifying an AI feature, system or model under the EU AI Act — provider or deployer role, prohibited practice, high-risk (Annex I/III), Article 50 transparency, marking AI-generated content, GPAI model duties, fine-tuning, AI literacy, conformity, AI Act deadlines."
---

# EU AI Act Engineering

Assess each feature, legal actor and model/system version separately. Translate applicable duties into architecture, interfaces, controls, records and testable evidence. Use current primary law before relying on a date or exemption. Snapshot: 2026-10-22, incorporating Regulation (EU) 2026/1744, effective 27 July 2026.

## Critical current-law checks

- Read [dates-and-amendments.md](references/dates-and-amendments.md) before a deadline claim. Do not reuse an unamended 2024 timeline.
- Assess Chapter III Sections 1-3 against the amended dates: 2 December 2027 for Article 6(2)/Annex III; 2 August 2028 for Article 6(1)/Annex I. Review other provisions and transitional rules separately.
- Treat Article 50 transparency as generally applicable from 2 August 2026. Article 111(4) grants a specific Article 50(2) transition until 2 December 2026 for covered systems placed on the market before 2 August 2026; it does not postpone every disclosure obligation or cover every new system.
- Apply the amended Article 4: support AI literacy through proportionate measures; do not claim a statutory guarantee of a particular individual competence level or a universal mandatory certificate.
- Assess new Article 4a safeguards for bias-related special-category processing; it is not general permission to train on sensitive data.

## Classification workflow

1. Identify the legal entity, countries, intended purpose, affected persons, autonomous behaviour, model supplier, system integrator and deployment owner. Gather actual implementation, customer promises and version/launch history.
2. Apply Article 2 scope/exclusions and Article 3 definitions. Separate an AI model, a GPAI model, a GPAI system and a downstream application. Do not use marketing terminology as the legal test.
3. Classify roles for this activity: provider, deployer, importer, distributor, product manufacturer, authorised representative. Reassess role changes under Article 25 and the separate GPAI modification guidance.
4. Screen prohibited practices first. If facts indicate a prohibited intended use, contain the affected feature and prepare alternatives; consent, a disclaimer or an account tier is not a general cure.
5. Assess Article 6 and the current Annexes. Document precise categories and exceptions; a 'human review' label alone does not establish that a consequential system is outside scope.
6. Assess Article 50 paragraph by paragraph, regardless of high-risk status. Separately assess GPAI provider duties under Articles 51-55.
7. Apply dates to the correct entity/system/model cohort. Preserve evidence of placing on the market, putting into service and significant/substantial changes.
8. Map each applicable obligation to implementation, owner, evidence and review trigger. Record unknowns, guidance status and interpretations explicitly.

Use [ai-inventory.json](assets/ai-inventory.json) and [classification-record.md](assets/classification-record.md). Do not conclude that all platform functions have one risk level.

## Engineering pass

For ordinary assistants, verify user-facing AI identity, appropriate generated-content handling, lawful data flows, limitations, escalation and tool permissions. These controls may originate in several laws or internal policy; identify the source of each.

For high-risk candidates, prepare the technical documentation, risk management, data governance, evaluations, logging, human oversight, instructions, cybersecurity and quality management required by the applicable role and schedule. Identify conformity/registration/declaration steps; never create a fictitious certificate or treat a generic benchmark as proof of conformity.

For GPAI providers, assess documentation to authorities and downstream providers, copyright policy, training-content summary, representatives and systemic-risk duties. Do not impose model-provider duties on every API customer or assume an open-weight licence removes all duties.

Use targeted synthetic/adversarial evaluations for intended tasks and affected groups. Preserve dataset rights and privacy. Explain uncertainty and measurement limits; do not invent performance thresholds mandated by law.

## Output and escalation

Return: feature/role matrix; risk-classification rationale; applicable-now and future duties; source versions; implementation gaps; evidence and owner; explicit change triggers; narrowly scoped unresolved legal questions.

Seek accountable legal/product review for contested classification, prohibited-use exceptions, product-sector interaction, sensitive bias data, new model-provider status, conformity routes and regulatory submissions. Continue already authorised reversible preparation. Do not contact authorities, sign codes, register a system or issue legal assurances without the relevant authority.

## Reference map

- [roles-and-classification.md](references/roles-and-classification.md): definitions, supply chain and feature examples.
- [prohibited-practices.md](references/prohibited-practices.md): precise screens and safeguards.
- [transparency-and-literacy.md](references/transparency-and-literacy.md): Article 50 surfaces and amended Article 4.
- [high-risk-engineering.md](references/high-risk-engineering.md): controls, conformity, deployer and impact-assessment boundaries.
- [gpai-and-model-changes.md](references/gpai-and-model-changes.md): model-provider responsibilities and fine-tuning.
- [bias-data-and-evaluations.md](references/bias-data-and-evaluations.md): Article 4a, datasets and useful tests.
- [post-market-and-incidents.md](references/post-market-and-incidents.md): monitoring, change control and incident coordination.
- [dates-and-amendments.md](references/dates-and-amendments.md): operative timeline and source conflicts.
- [germany-and-authorities.md](references/germany-and-authorities.md): KI-MIG and authority routing.
- [sources.md](references/sources.md): authoritative links and verification limits.

Coordinate privacy with `eu-platform-privacy`, data/IP with `eu-ai-data-ip`, security with `eu-platform-cybersecurity`, and implementation evidence with `eu-platform-agent-assurance`.
