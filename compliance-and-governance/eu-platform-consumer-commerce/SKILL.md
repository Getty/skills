---
name: eu-platform-consumer-commerce
description: "Use when building B2C signup, checkout, pricing, subscriptions, trials, renewals, withdrawal (Widerruf), the cancellation button (Kündigungsbutton) or consumer terms, or when a model or quota change affects paying consumers — EU consumer law, BGB §§ 312 ff. and 327 ff., PAngV."
---

# EU Platform Consumer Commerce

## Operating rule

Treat each offer, purchase journey and contract version as a separate reviewable object.
Start from the actual customer, service and country; a business email or checkbox does not settle consumer status.
Use this skill to build controls and identify legal decisions, not to issue a blanket compliance certificate.
Research baseline: 2026-10-22. Reopen current primary sources before relying on a deadline, legal wording or exception.
Keep EU rules, German implementation, other-country requirements and product policy in separate fields.

## Establish the transaction

1. Identify the contracting entity, establishment, target countries, storefront languages and seller of record.
2. Classify the customer as consumer, business, mixed/uncertain or public body using actual transaction purpose.
3. Describe every supplied item: ongoing AI service, downloaded digital content, implementation work, physical device or bundle.
4. Record money, prepaid value, personal data and other consideration separately.
5. Identify subscription duration, trial conversion, minimum term, renewal, metered usage, top-ups and refunds.
6. List web, app, app-store, sales-assisted and API purchase paths; do not assume one UI represents all contracts.
7. Record whether minors are admitted and whether guardian capacity review is needed.
8. Fill `assets/transaction-review.json` before deciding applicability.

## Decide applicability

- Use `applicable`, `not_applicable`, `unknown`, or `conditional`; explain the evidence and trigger for each.
- Distinguish a digital service from digital content for withdrawal and performance rules.
- Assess free services involving personal data under the digital-content framework; security-only or contract-necessary processing has different treatment.
- Map directives to the enacted national law and applicable contract date.
- For Germany, assess BGB §§ 312 ff. and 327 ff., EGBGB information rules, PAngV and VSBG separately.
- For cross-border consumers, assess mandatory consumer protections under Rome I Article 6.
- Do not treat a German choice-of-law clause as eliminating the consumer's mandatory home-country protection.
- Do not infer that a B2B-only policy works if the actual checkout admits consumers without meaningful qualification.

## Build the purchase controls

1. Capture a versioned offer defining functionality, limits, models, availability and paid usage units.
2. Present total consumer prices, billing intervals, taxes, minimum commitment and variable-price calculation before ordering.
3. Separate an immediate purchase from a free trial that later becomes paid; document the paid commitment at the legally relevant step.
4. Provide required pre-contract information and retain a reproducible version.
5. Review the payment-obligation button in the actual language and visual context.
6. Deliver the contract confirmation on a durable medium; retain the sent version and delivery event.
7. Record consent to early performance and acknowledgement of loss of withdrawal rights only when the applicable legal branch permits them.
8. Do not use one global `waived_withdrawal=true` field for all products.
9. Make billing, entitlement and legal state transitions idempotent and auditable.

## Implement separate exit paths

- **Withdrawal / Widerruf:** unwind a qualifying distance contract during the withdrawal period, with the proper refund and performance treatment.
- **Ordinary cancellation / Kündigung:** end an ongoing contract according to the permitted term and notice regime.
- **Extraordinary termination:** process a fact-specific right to end the contract for serious cause.
- **Digital-product remedies:** handle non-supply, defects, required updates and material service changes separately.
- **Account deletion:** route personal-data erasure to privacy/data governance; preserve only justified contractual and accounting records.

For Germany, independently assess the § 356a electronic withdrawal function and § 312k cancellation button.
The § 356a function applies from 2026-06-19; do not confuse it with cancellation or suppress it merely because service access began.
Current § 356 numbering differs from older guides: services are in paragraph 5 and digital content in paragraph 6.
Verify the live statute before implementing an early-extinction branch.

## Gate product changes

Reassess on a new model, lower quota, changed context window, withdrawn feature, price increase, new data use, new country or new payment path.
Treat contract conformity, mandatory security updates and optional functionality changes as separate questions.
Do not silently substitute an advertised model with a materially weaker one merely because an upstream API changed.
Tie notice delivery, effective date and any termination right to the actual consumer cohort and contract version.
Prevent launch of affected transactions when a material legal requirement is known to be unmet.
If facts or legal classification are unresolved, keep the affected path pending review; continue unrelated work.

## Evidence and output

Produce one review with:

1. Transaction facts and missing facts.
2. Country and law matrix with source, provision, effective date and retrieval date.
3. Duties mapped to UI, API, billing logic, documents and owners.
4. Test results with build, locale, device and relevant account state.
5. Contract/notice versions and evidence of communication.
6. Findings classified by severity, legal certainty and affected customer cohorts.
7. Concrete patches or a remediation plan, remaining decisions and review owner.

Distinguish `implemented`, `tested`, `legally_reviewed` and `approved_for_release`.
Do not equate generated text or a passing browser test with legal approval.
Use `assets/consumer-release-review.md` and `assets/consumer-test-vectors.json`.

## Action boundaries

Inspect and repair authorized code, test data, staging flows and draft text autonomously.
Use approved policies for routine refunds and contractual notifications; do not invent authority to send notices or change customer contracts.
Prepare concrete draft wording and an impact assessment before requesting a legal or commercial decision.
Escalate disputed consumer status, uncertain waiver validity, minors' capacity and material rights restrictions to the responsible specialist.

## Load references selectively

| Task | Reference |
| --- | --- |
| Scope, free offers, customer purpose, cross-border markets | [scope-and-country-adapters.md](references/scope-and-country-adapters.md) |
| Prices, purchase state, order button, notices | [checkout-and-pricing.md](references/checkout-and-pricing.md) |
| Withdrawal, new withdrawal function, cancellation | [withdrawal-and-cancellation.md](references/withdrawal-and-cancellation.md) |
| Defects, updates, renewals and model changes | [digital-service-lifecycle.md](references/digital-service-lifecycle.md) |
| Complaints, ADR and contract evidence | [complaints-and-evidence.md](references/complaints-and-evidence.md) |
| Primary authorities and current-law checks | [sources.md](references/sources.md) |

Coordinate with `eu-platform-billing-tax`, `eu-platform-accessibility`, `eu-platform-privacy` and `eu-platform-tracking-marketing` when those domains change.
Retain this skill's transaction review even when another domain reports no findings.
