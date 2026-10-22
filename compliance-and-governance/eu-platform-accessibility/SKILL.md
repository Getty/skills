---
name: eu-platform-accessibility
description: "Use when building or changing a consumer-facing UI, checkout, AI chat or agent interface, mobile app or generated document, or writing an accessibility statement or exemption — European Accessibility Act, BFSG/BFSGV, EN 301 549, WCAG, screen reader, keyboard."
---

# EU Platform Accessibility

## Operating rule

Establish legal scope and user impact before choosing a test target.
Treat automated scanning, manual evaluation, user testing and legal review as complementary evidence.
Do not declare compliance from an overlay, a vendor badge or a zero-violation scanner result.
Research baseline: 2026-10-22. Verify current laws and Official Journal standard citations at release time.
Distinguish EU directives, national implementation, published standards and contractual targets.

## Determine scope

1. Identify the legal entity, target member states, consumer/business/public customer classes and offered services.
2. Map the actual service to the EAA categories and the relevant national implementing law.
3. For Germany, assess BFSG § 1, including ecommerce services, and the applicable BFSGV requirements.
4. Evaluate microenterprise service exemptions using actual workforce and financial facts.
5. Assess products separately; do not extend the service exemption automatically to products.
6. Record any transition, fundamental alteration or disproportionate-burden claim with evidence and approval.
7. Screen public-sector and procurement obligations separately from private B2C rules.
8. Fill `assets/accessibility-scope.json`; keep uncertainty distinct from exemption.

## Choose and version the evaluation target

- Record the exact law, functional requirement, standard edition, level and applicable clauses.
- Record whether an edition is merely published or cited in the Official Journal for the relevant legal instrument.
- EN 301 549 V4.1.1 was published in September 2026 and incorporates WCAG 2.2.
- Its publication does not itself establish a legal presumption of conformity.
- Recheck OJ citation and transition status; do not infer EAA status from a WAD citation.
- Use WCAG 2.2 AA as a practical forward-looking engineering target where suitable, with explicit scope and legal mapping.
- Include applicable non-web/document/software/support requirements beyond a WCAG-only checklist.

## Inventory complete journeys

Include discovery, registration, consent, authentication, account recovery, pricing, checkout, withdrawal and cancellation.
Include chat, streaming, tool confirmations, uploads, files, tables, code blocks, voice, image outputs and exports.
Include errors, empty states, timeouts, dialogs, restrictions and customer support.
Include third-party components, PSP pages, identity providers and embedded widgets.
Include all supported languages and mobile layouts.
Choose representative templates and states; do not assess only the landing page.

## Build accessible controls

1. Prefer semantic elements with meaningful names, roles, states and keyboard behavior.
2. Preserve logical focus and navigation across asynchronous operations and dialogs.
3. Expose errors and required actions programmatically and in plain language.
4. Make streaming announcements controllable and avoid reading every token repeatedly.
5. Provide usable alternatives to voice-only, image-only, drag-only or color-only interaction.
6. Ensure authentication and payment remain usable with assistive technology.
7. Respect zoom, reflow, reduced motion, contrast and relevant user preferences.
8. Provide accessible documents and support material, with honest limits for generated content.
9. Review agent approval dialogs for clear action, target, consequence, cancellation and timeout behavior.

## Verify behavior

Run suitable automated checks and inspect their coverage limits.
Perform keyboard-only and screen-reader journeys on representative desktop and mobile combinations.
Test zoom/reflow, contrast, input alternatives, focus visibility, errors, timing and dynamic status.
Use synthetic accounts and content; do not expose private user material in shared evidence.
Retest defects in the actual UI after repair.
Mark untested combinations explicitly and select them based on real user impact.
Use `assets/manual-journey-record.md` and `assets/accessibility-test-vectors.json`.

## Handle nonconformity

Record user task, barrier, legal/technical criterion, reproduction, severity and affected scope.
Fix the underlying component and verify every affected journey.
Provide an accessible interim route where appropriate, without treating it as automatic legal compliance.
Assess statutory information and authority-notification duties with the accountable owner.
Do not silently publish a statement claiming full conformance while known material barriers remain.
For German service obligations, review BFSG § 14 and Annex 3 specifically.

## Gate changes

Reassess after a new design system, model UI, checkout, identity provider, voice feature, file exporter or localization.
Reassess exemption assumptions when workforce, finances, service category or countries change.
Reassess legal mapping when a standard is newly cited, amended or withdrawn.
Keep technical remediation separate from a disputed exemption decision.
For a known material barrier on an essential in-scope journey, make the release decision explicit and accountable.

## Required output

Produce scope rationale, applicable legal/technical target, journey inventory, test evidence, findings and remediation owners.
Include tested versions, assistive technology, browser/OS, locale and dates.
State limits and unresolved standards or national-law questions.
Prepare the required service information or statement from observed facts.
Do not call a partial review a full audit.

## Action boundaries

Inspect and fix authorized components and staging tests autonomously.
Use existing authority for routine product updates.
Prepare exact public statements, authority notices or exemption assessments for the responsible approval when needed.
Do not send regulator communications or make unsupported legal declarations.

## Load references selectively

| Task | Reference |
| --- | --- |
| EAA/BFSG scope, exemptions and national adapters | [scope-and-exemptions.md](references/scope-and-exemptions.md) |
| Standards, publication and OJ citation | [standards-and-legal-mapping.md](references/standards-and-legal-mapping.md) |
| AI interface and document implementation | [ai-interface-engineering.md](references/ai-interface-engineering.md) |
| Automated, manual and user evaluation | [evaluation-and-release.md](references/evaluation-and-release.md) |
| Service information, barriers and authority duties | [information-and-remediation.md](references/information-and-remediation.md) |
| Procurement, vendors and localization | [procurement-and-localization.md](references/procurement-and-localization.md) |
| Primary authorities | [sources.md](references/sources.md) |
