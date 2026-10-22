# Operations and controls

## Control ownership

Assign finance ownership for price and accounting policy, tax ownership for classification/rates/reporting, engineering ownership for execution, security ownership for sensitive payment handling and customer support ownership for disputed charges. A deterministic rules engine is useful only if its policy is approved and current.

## Daily operational evidence

Reconcile billable usage to invoiced usage, invoices to payment events and ledger postings, refunds to original charges and settled amounts, and issuing/receiving failures to exception queues. Detect duplicate invoice numbers, impossible tax combinations, invalid country evidence, repeated webhook events and contract cancellations still billed. Investigate using identifiers and minimized logs.

## Deadline preparation

Treat the 2027 and 2028 German e-invoice transitions as implementation milestones with verified scope. Build receiving/validation and correction capabilities before relying on an issuing exemption. Track Data Act switching-fee removal separately from ordinary service billing. Configure effective-date transitions with replayable tests rather than a manual production toggle at midnight.

For other EU countries, monitor their actual national e-invoice/reporting mandates and applicable EU reform dates. Do not assume Germany's timetable is European. ViDA was adopted in March 2025 and entered into force on 2025-04-14 with staged application: relevant OSS/IOSS clarifications from 2027, further measures from 2028, cross-border B2B digital reporting from 2030, and domestic-system alignment by 2035. The Commission published revised OSS materials in July 2026. Select the measures relevant to the actual service and date; do not treat the entire package as either a pending proposal or fully applicable today. [T19]

## Change-impact questions

- Does a new model alter the billable unit or price promise?
- Does a reseller become seller of record or merely collect payment?
- Does a customer move country or change the contracting entity?
- Does a new trial or credit system affect taxable timing or refund rights?
- Does a marketplace introduce third-party fund handling or tax reporting?
- Does a retention or cloud change affect archived records and authority access?
- Does an invoice profile/validator update change accepted documents?

## Controlled corrections

When a pricing or tax defect is found, identify affected cohorts using historical policy versions, quantify the discrepancy, preserve the original records and prepare a reviewed correction plan. Do not recompute the entire ledger with current prices or overwrite evidence. Determine customer communication, credit/refund and tax-return implications with responsible owners. Execute under existing authority where available; otherwise request approval for the concrete batch.

## Release evidence

Test a representative domestic B2B invoice, domestic consumer sale, EU B2C electronic service, EU B2B reverse-charge candidate, non-EU purchase, credit redemption, cancellation/refund and late usage event. Include unknown classification and format failure. A happy-path invoice PDF is insufficient assurance.

Keep tests meaningful and risk-based. Use sandbox payments and synthetic data unless live tests are explicitly authorized. Stop expanding test scope when the concrete release risk and required gates are covered.
