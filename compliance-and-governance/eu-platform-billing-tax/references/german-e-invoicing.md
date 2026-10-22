# German structured e-invoicing

## Scope before dates

UStG § 14 distinguishes structured electronic invoices from other electronic or paper invoices. The domestic B2B requirement depends on the supplier and recipient's statutory establishment and the transaction. Certain exempt supplies and specific invoice exceptions require separate analysis. A plain PDF is an “other invoice,” even if emailed or signed. [T6]

## Transition matrix

| Period | General baseline for qualifying domestic B2B transactions |
| --- | --- |
| From 2025-01-01 | Receiving structured e-invoices must be supported for relevant businesses; issuing transitions are separate |
| Through 2026-12-31 | § 27(38) no. 1 permits specified paper/other-format invoicing; electronic other formats require recipient consent |
| 2027 | The extension for issuers with previous-year turnover no more than EUR 800,000 must be assessed; the specific EDI branch has its own conditions |
| From 2028-01-01 | These general issuing transitions end; genuine scope exclusions and statutory exceptions still need separate review |

Use supply dates and the exact transition wording. Current § 27(38) references turnover under § 19(2), not older renumbered definitions. Do not phrase the rule as “all companies always need XML from 2028” without the domestic transaction and exception tests. [T7]

Assess small-amount invoices under § 33 UStDV, travel tickets under § 34 and small-business invoices under § 34a. Being exempt from issuing in a particular case does not automatically eliminate receiving capability or recordkeeping. Re-open current texts and BMF guidance for edge cases. [T8]

## Format and validation

Choose an appropriate compliant profile, such as XRechnung or a qualifying ZUGFeRD/Factur-X profile, based on the actual statutory and contractual requirements. Pin the current specification and validator versions from their official publishers. Do not accept every file using a familiar extension or product name. B2G may add routing identifiers, portal and procurement requirements independent of B2B VAT law. [T9]

Validate syntax, business rules, mandatory fields, code lists, calculations and invoice-type semantics. Render the structured invoice for human review and compare it with any embedded PDF. For a hybrid invoice, preserve the authoritative structured data and resolve inconsistent representations under the applicable guidance. A green XML-schema result does not prove the tax rate or seller identity is correct.

## Receiving pipeline

Accept the agreed transport, malware-scan safely, disable unsafe XML entity/network resolution, identify profile/version, validate, quarantine exceptions, route for approval and archive original bytes with metadata. Do not run executable content in attachments. Keep rejection and correction workflows accountable so a format error does not become an unnoticed overdue payable.

## Issuing pipeline

Generate from the approved accounting model, not separately from a presentation PDF. Ensure invoice number, periods, parties, tax and totals agree across systems. Preserve sent bytes and transmission evidence. Reissue through a controlled correction workflow. Test foreign-character names, long addresses, discounts, multiple tax categories, negative corrections and rounding.

## Research caveat

The statutory transition text was inspected. The BMF FAQ endpoint returned an availability error during research; retrieve its current version before resolving implementation-specific interpretation. Do not cite a secondary FAQ as though it were the tax authority's current ruling.
