# ISIN, CFI, and FISN

## Identify an instrument with ISIN

ISO 6166 defines the ISIN framework for financial and referential instruments. Its familiar 12-character structure consists of a two-letter prefix, a nine-character national securities identifying component, and a final check digit. The prefix follows assignment rules; it is not a dependable substitute for issuer domicile, trading venue, settlement location, or currency. Consult [ISO 6166](https://www.iso.org/standard/78502.html) and the responsible numbering agency.

Allocation depends on instrument type and fungibility. The [ANNA ISIN Guidelines](https://anna-web.org/additional-resources/) address cases including multiple marketplaces, share classes, tranches, corporate actions, and referential instruments. Instruments that are economically similar are not necessarily fungible. A depositary receipt and its underlying shares require a documented relationship, not an automatic identity merge. OTC derivatives have specialized allocation guidance through the Derivatives Service Bureau.

For an assignment question, identify the instrument's legal form and terms, responsible agency, governing guidance, and existing assignments. Do not calculate a plausible ISIN and present it as official. The [ANNA identifiers page](https://anna-web.org/identifiers/) explains official numbering-agency assignment and the accompanying CFI and FISN ecosystem.

## Compare records using terms

When matching a bond, compare issuer, currency, maturity, coupon structure, seniority, guarantees, and issue or tranche details as available. For equity or funds, compare share class, rights, distribution policy, currency class, and vehicle structure. Use names as search aids, then verify the actual instrument.

Record the limits of each comparison. If two sources describe different levels of a fund structure, the same commercial name is insufficient to join them. If a corporate action changes rights or creates a successor instrument, preserve the old record and the documented transition. An identifier replacement is not proof that old and new instruments were identical at every date.

## Classify with CFI

CFI codes follow ISO 10962. They use six alphabetic characters: category and group, followed by attributes whose meanings depend on that group. Decode with the applicable official code tables; the same position does not have one universal meaning across all categories. CFI classifies many instruments into the same category and is not a unique instrument key. The [ISO 10962 overview](https://www.iso.org/standard/81140.html) also notes that some lifecycle changes can lead to a changed CFI for an instrument.

Do not infer full legal or economic terms from six letters. Preserve detailed source terms and the classification source date. For unfamiliar or unknown codes, report the unresolved positions instead of fabricating a classification. Verify whether the source uses the current edition or a historical classification table.

## Describe with FISN

FISN is a standardized short name intended for human interpretation. The edition is [ISO 18774:2024](https://www.iso.org/standard/84851.html), superseding the 2015 edition. It complements instrument identifiers and classification.

The [ANNA FISN Guidelines](https://anna-web.org/additional-resources/) specify a maximum of 35 characters including the separating slash. The familiar issuer portion of up to 15 characters and remaining instrument-description portion has exceptions, including particular collective-investment and OTC-derivative cases. Use the official abbreviations and category rules rather than a universal truncation algorithm.

Preserve an officially assigned FISN as supplied. A generated display label should be identified as local until checked against the standard and authoritative data. Do not reverse-engineer identity from a short name: abbreviations, truncation, and updates can make superficially similar names ambiguous.

## Use the three together

Store ISIN, CFI, and FISN as complementary attributes with source and effective date. An ISIN can identify a record, CFI can support classification, and FISN can make review easier. Agreement among them is useful corroboration; disagreement is a reason to investigate freshness, taxonomy edition, misassignment, or a mistaken join. Never resolve a conflict solely by choosing the longest or most familiar label.
