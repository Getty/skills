# VAT and country adapters

## Classify before calculating

Identify seller, establishments, customer status, location, supplied performance and service date. AI-assisted consulting, automated SaaS access, downloadable content, licenses and bundles can have different tax treatment. The EU electronically supplied-services concept involves the nature and automation of performance; sending an invoice or attending a human-led meeting online is not sufficient. Use VAT Directive 2006/112/EC, Implementing Regulation 282/2011 and national implementation for the actual facts. [T1]

## EU B2C electronic services

Assess the customer's place of residence/establishment under the applicable rules. The general destination principle for these services is distinct from the limited EUR 10,000 cross-border threshold rule. The threshold combines the relevant intra-EU distance sales and TBE supplies and has conditions, including the supplier's establishment situation and current/previous year amounts; it is not a separate allowance per country or a generic exemption for every service. An opt-in to destination taxation has consequences. [T2]

OSS can simplify reporting of qualifying supplies. It does not make transactions tax-free or mean every foreign supply belongs in OSS. Determine the Union or non-Union scheme, registrations and excluded domestic establishments. A business can have obligations outside OSS. Record the reporting country and period separately from the customer's tax country. [T3]

## B2B and imported services

Verify business use and the relevant receiving establishment. An EU VAT number and validation evidence are useful but do not replace the complete factual assessment. Apply the proper place-of-supply and reverse-charge rules, including invoices and reporting, where their conditions hold. A German platform buying non-German model/API services also needs a purchase-side tax analysis; the supplier charging no VAT does not automatically mean no tax is owed. [T4]

Do not permit arbitrary customer country changes to rewrite issued transactions. A later address correction needs evidence and an accounting/tax correction workflow. Handle inconsistent IP, billing, bank and declared country evidence through a reviewed rule, not a model's guess. Apply the current evidence requirements and permitted exceptions; do not hardcode “one IP address proves location.”

## German small-business overlay

Current § 19 UStG uses EUR 25,000 prior-year and EUR 100,000 current-year thresholds for its specified domestic exemption, with additional definitions and conditions. Cross-border EU SME use has its own requirements and identification process. Do not transplant older EUR 22,000/50,000 guidance. Tax exemption, invoice obligations, reverse-charge liability and e-invoice receiving capability are separate questions. [T5]

## Rule schema

Store country, product tax category, customer tax status, establishment, evidence references, tax basis, rate, exemption/reverse-charge reason, invoice annotation, scheme, currency, effective period and approval. Use versioned data with a named owner and source. Unresolved facts must enter a review queue or a legally approved conservative path; never silently select zero.

For expansion, obtain the national adapter for rates, invoicing, reporting and exemptions. EU VAT harmonization does not make every country's invoice and compliance process identical. Treat UK, Switzerland and other non-EU locations as separate jurisdictions.
