# Filing profiles, packages, and current rules

## Separate standards from program requirements

XBRL International specifies the reporting technology. A regulator, exchange, statistical authority, or other recipient selects accepted formats, taxonomies, packages, validation rules, identifiers, and deadlines. Accounting standards determine substantive reporting meanings through their own governance. These layers interact but are not identical.

Before preparing or assessing a filing, establish jurisdiction, recipient, form or report type, entity category, financial period, accounting framework, language, and submission date. Ask only for missing details that materially change the answer. For a general explanation, describe the architecture without inventing a filing obligation.

## Build a version and applicability manifest

Record the recipient's current technical guide and effective version; accepted taxonomy releases and entry points; extension and anchoring rules; transformation registry; package format; calculation and formula expectations; conformance-suite version; and submission-channel requirements. Distinguish optional adoption, transition dates, and mandatory effective dates.

A published international specification may be newer than a filing program's accepted implementation. A draft taxonomy is not necessarily accepted. A taxonomic concept can exist before the accounting rule using it applies to a particular filer. Verify each dependency rather than assuming all “latest” components belong together.

## Apply SEC guidance specifically

Use the [SEC structured-data taxonomy pages](https://www.sec.gov/data-research/structured-data/taxonomies-schemas), [EDGAR Filer Manual](https://www.sec.gov/submit-filings/edgar-filer-manual), and [technical specifications](https://www.sec.gov/submit-filings/technical-specifications) for the current filing context. Select the relevant form and accepted taxonomy set rather than treating all EDGAR submissions as the same XBRL profile.

The SEC moved detailed XBRL technical material from Chapter 6 of the Filer Manual into the **EDGAR XBRL Guide**. The technical-specifications page lists the guide for each EDGAR release; read the one in force there before a live filing; do not rely solely on historical Chapter 6 references.

For a specific question, identify the applicable technical rule and the submission behavior it governs. Explain whether a finding is a rejection condition, warning, accounting concern, or a limitation of the review. Do not promise acceptance based on local validation alone.

## Apply ESEF guidance specifically

Use [ESMA's electronic-reporting hub](https://www.esma.europa.eu/issuer-disclosure/electronic-reporting) to locate the applicable regulatory technical standards, taxonomy, reporting manual, and conformance suite. ESEF uses XHTML and Inline XBRL within its scope, including tagging requirements for relevant IFRS consolidated financial statements. Determine the actual issuer and reporting-period applicability before stating obligations.

The [ESEF Reporting Manual](https://www.esma.europa.eu/sites/default/files/library/esma32-60-254_esef_reporting_manual.pdf) provides technical guidance, including taxonomy and extension considerations. Read its status and effective-date language; the manual is not itself a substitute for the governing legal requirements. The version located during this check was the 2025 update. Do not extrapolate its discussion of proposed or future accounting changes into a claim that every issuer must already use them.

For tagging, distinguish detailed facts from block tagging and assess required anchoring in the correct context. Check the accepted taxonomy entry point and the issuer's accounting basis. Review the rendered XHTML and extracted data together, including text continuations and language.

## Choose package formats deliberately

[Report Packages](https://specifications.xbrl.org/spec-group-index-taxonomy-packages.html) assemble reports and supporting artifacts; Taxonomy Packages describe reusable taxonomy material and remappings. They serve different roles. Do not assume every ZIP archive is a conforming package, or that every recipient accepts every package convention.

The international index lists every specification with its status — Recommendation, Candidate Recommendation or draft. Preserve these status distinctions. For a deliverable, select the version accepted by its recipient and document any prospective feature separately.
