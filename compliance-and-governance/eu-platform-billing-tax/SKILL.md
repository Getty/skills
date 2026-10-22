---
name: eu-platform-billing-tax
description: "Use when building usage metering, token or subscription billing, invoices and credit notes, VAT, OSS or reverse charge, German e-invoicing (XRechnung, ZUGFeRD), accounting exports or retention (GoBD), PSP integration, prepaid credits, wallets or marketplace payouts."
---

# EU Platform Billing and Tax

## Operating rule

Separate usage measurement, contract charges, tax classification, invoice generation and payment settlement.
Implement approved tax policy deterministically; do not let an LLM improvise rates or exemptions per transaction.
Use this skill to prepare evidence, rules and code for finance/tax review.
Research baseline: 2026-10-22; verify effective dates and national rules before release or filing.
Keep EU VAT principles separate from German invoicing and accounting implementation.

## Establish the commercial facts

1. Identify legal seller, merchant of record, establishments and relevant tax registrations.
2. Classify each supplied performance and the degree of human intervention.
3. Identify B2B/B2C status for tax purposes, customer location and evidence.
4. Identify subscription, metered service, prepaid credit, voucher, refund and third-party payout models.
5. List currencies, taxes, fees, trials, promotions, upgrades and supported countries.
6. Document PSP and reseller responsibilities; verify actual contracts rather than marketing labels.
7. Determine who invoices whom and whether self-billing or marketplace rules apply.
8. Complete `assets/billing-policy.json` with unknowns visible.

## Build the tax decision

- Determine place of supply before selecting a rate.
- Assess electronically supplied services from the actual service, not simply because it uses the internet.
- For EU B2C electronic services, assess destination taxation and the limited EUR 10,000 rule where its conditions apply.
- Treat OSS as a reporting mechanism, not a separate tax exemption or universal mandatory scheme.
- For cross-border B2B, verify customer status, relevant establishment and reverse-charge conditions.
- Do not equate a missing VAT ID with a definitive consumer classification in every case.
- Check German small-business rules and EU cross-border SME conditions separately.
- Store legal basis, policy version, evidence and effective date with the tax decision.
- Route unresolved classification to finance/tax; do not silently assume zero VAT.

## Meter and invoice reliably

1. Define billable events and units for each model, cache, tool, retry and failed request.
2. Deduplicate events and preserve the original service period.
3. Use exact decimal/integer arithmetic and documented rounding.
4. Link usage to contract and price versions; do not recalculate old invoices from today's price table.
5. Generate invoice fields and tax annotations from the approved jurisdiction-specific policy.
6. Preserve issued records and create linked corrections rather than silently replacing them.
7. Reconcile usage, invoice, PSP payment, refund and ledger entries.
8. Provide interpretable customer explanations without exposing prompts or confidential payloads.

## German e-invoice gate

Assess domestic in-scope B2B invoicing under UStG § 14 and transitions under § 27(38).
Do not call a plain PDF an e-invoice under the structured statutory definition.
Distinguish receiving capability since 2025 from phased issuing requirements.
For 2027, assess the previous-year EUR 800,000 turnover threshold and the separate EDI transition.
For 2028, assess the end of these transitions while retaining genuine statutory exceptions.
Check small-amount, small-business and other exceptions explicitly.
Validate actual structured data and preserve it; a readable PDF preview is insufficient.
Keep B2G procurement formats and portals as a separate branch.

## Retention and deletion

Classify accounting documents and customer-service data separately.
For Germany, invoices and booking vouchers generally have eight-year rules; books and other record classes differ.
Evaluate tax limitation, legal holds, OSS records and special regimes before deletion.
Do not use accounting retention to keep all prompts, files or profiling data indefinitely.
Retain original structured invoice data, integrity evidence and the ability to render and export it.
Coordinate account erasure with privacy and data governance.

## Payments and financial perimeter

Map the actual flow of funds, custody, acceptance and payouts.
Screen third-party wallets, transferable credits, marketplace collections, remittances and credit features.
Do not infer that naming value “tokens” removes payment or e-money regulation.
Do not infer that every closed-loop service credit is regulated e-money.
Obtain specialist classification before implementing an unresolved regulated activity.
Prefer an authorized PSP structure where appropriate, but verify what responsibility it actually assumes.

## Required output

Produce transaction classification, country tax matrix, rate/policy versions, invoice profile and billing reconciliation evidence.
Include applicability reasons, sources, effective dates, unresolved facts and responsible finance/tax owner.
Provide tested failure cases and a migration plan for deadline-driven changes.
Separate technical validation, accounting acceptance, tax review and authority to file.
Use `assets/billing-release-review.md` and `assets/billing-test-vectors.json`.

## Action boundaries

Inspect, simulate, draft and fix authorized billing code and staging records autonomously.
Use existing approved policies for routine billing operations.
Do not file returns, move funds, issue live invoices, change bank details or initiate bulk refunds without authorization.
Prepare exact amounts, affected transactions and evidence before seeking a financial decision.
Never log card secrets or full payment credentials in debugging output.

## Load references selectively

| Task | Reference |
| --- | --- |
| VAT, customer status, destination and OSS | [vat-and-country-adapters.md](references/vat-and-country-adapters.md) |
| AI usage, invoice fields and corrections | [metering-and-invoices.md](references/metering-and-invoices.md) |
| German structured invoices and transitions | [german-e-invoicing.md](references/german-e-invoicing.md) |
| Archiving, GoBD and privacy separation | [retention-and-accounting-evidence.md](references/retention-and-accounting-evidence.md) |
| PSP, credits, vouchers and licensing | [payments-and-credits.md](references/payments-and-credits.md) |
| Reconciliation, deadlines and change review | [operations-and-controls.md](references/operations-and-controls.md) |
| Primary authorities and refresh | [sources.md](references/sources.md) |
