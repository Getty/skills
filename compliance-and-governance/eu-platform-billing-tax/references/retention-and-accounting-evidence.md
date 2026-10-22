# Retention and accounting evidence

## Classify records

Do not assign a single retention period to the entire customer account. In Germany, UStG § 14b generally specifies eight years for invoices. AO § 147 distinguishes ten-year books/records and specified customs documents, eight-year booking vouchers, and six-year other listed records. Start events, transitions, tax limitation and other laws can extend or alter the result. HGB § 257 supplies the commercial-law branch and retains a ten-year booking-voucher rule for specified regulated financial entities. [T10, T11]

OSS and other special regimes may require longer scheme-specific records, commonly a ten-year OSS record period under the applicable EU rules. Verify the actual record category and scheme rather than deleting because the invoice's eight-year clock expired. Legal holds and open tax matters require scoped review, not indefinite default preservation. [T3]

## Preserve usable originals

Archive the original structured invoice payload, needed attachments, integrity metadata and readable representation. Retaining only a screenshot or printed PDF loses machine-readable evidence. Maintain the ability to retrieve, render and export records throughout retention, including after software migration. Record formats, schemas, encryption-key availability and restoration tests.

German GoBD is administrative guidance explaining accounting and data-access expectations, not a universal software certification. Review the current BMF version, including electronic-invoice changes, and align procedural documentation, internal controls and data availability. Do not claim a vendor's “GoBD compliant” label transfers the operator's organizational duties. [T12]

## Procedural documentation

Document systems, responsibilities, input channels, validation, authorization, posting, correction, archiving, access control, backup, migration and export. Keep the document version matching the actual process. Reconstruct a sample from service/usage event through invoice, payment and ledger to archive; record every transformation and its controls.

## Privacy separation

When an account is deleted, separate accounting records retained under legal obligation from product content, prompts, files, marketing identifiers and support data. Restrict retained financial records to accounting/audit purposes and appropriate staff. A valid invoice retention rule does not authorize retraining models on old conversations. [T13]

Keep minimal transaction identifiers needed for reconciliation and rights requests; avoid retaining entire production objects unnecessarily. Implement a retention registry with category, legal basis, start event, period, jurisdiction, hold, owner, access restrictions and destruction evidence.

## Location and outsourcing

Assess statutory conditions for electronic storage outside Germany or outside the EU, tax-authority access and any notification/authorization requirements, as well as GDPR transfers. UStG § 14b and AO § 146 have their own location/access rules; “EU cloud” does not resolve every requirement. Verify the actual storage, backup and administrator locations before migration. [T10, T14]

## Deletion gate

Calculate eligibility using the approved record policy, check holds and open matters, retain a minimal destruction record and reconcile replicas. Finance/tax owns contested statutory periods; engineering demonstrates that the selected policy is actually executed. Do not mass-delete archived invoices merely to satisfy a generic user-data erasure job.
