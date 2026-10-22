# International transfers and remote access

Sources: D1–D7. A Chapter V mechanism is additional to lawful processing, minimisation, transparency, security and contractual-role duties.

## Apply the transfer test

Under EDPB Guidelines 05/2021, assess the cumulative elements: an exporter subject to GDPR for the processing; disclosure/transmission or other availability to another controller/processor; and that recipient in a third country or international organisation. A recipient already subject to GDPR can still require Chapter V analysis.

Remote access by a separate non-EEA support company can be a transfer even if servers remain in the EEA. An employee abroad acting as part of the same controller is not automatically a transfer to another entity under this test, but security, accountability and foreign-law risks remain. A separately incorporated group subsidiary is not the same entity merely because it shares a brand.

Map each leg: customer → platform → hosting → embedding/reranking → LLM → moderation/support → onward supplier. Include logs, identifiers, prompts, uploaded files, traces and encrypted data that remain personal. Distinguish an end user's direct submission to a third-country controller from the platform's own onward disclosure.

## Choose the mechanism using exact scope

1. **Adequacy, Art 45:** confirm a currently valid Commission decision covers the recipient, sector, processing and territory. No SCC is automatically required for a transfer fully covered by a valid adequacy decision, but other GDPR duties remain.
2. **Appropriate safeguards, Art 46:** select an eligible instrument and assess actual protection. Options may include applicable SCCs, approved BCRs, or other instruments meeting their conditions; do not fabricate an approval.
3. **Derogation, Art 49:** use only if its specific conditions genuinely apply, with restrictive interpretation. Routine structural cloud/LLM transfers must not be repackaged as occasional explicit-consent exceptions without a sound assessment.

Do not maintain a static code allowlist that treats every country labelled Europe as EEA or treats an old adequacy list as permanent. Keep mechanism and recipient verification separate.

## EU-US Data Privacy Framework

Check the exact recipient legal entity on the official Department of Commerce list, active participation, covered subsidiaries and relevant data scope including HR data where applicable. Save the check date and evidence reference. A logo, group brand, Privacy Shield participation or a supplier assertion is not proof of current DPF coverage.

Confirm that the specific transfer is within the adequacy decision and certification scope. Continue Art 28/role, security, notice and onward-transfer work. Monitor relevant suspension/invalidation or certification lapse; reassess on a real change rather than declaring all US transfers unlawful or all US vendors automatically covered.

Where an alternative SCC route is planned, assess its eligibility, terms and practical effectiveness in advance. A fallback document alone does not guarantee continuity if the conditions cannot be met.

## SCC eligibility and completion

Distinguish transfer SCCs under Decision 2021/914 from controller–processor clauses under Decision 2021/915. Select the appropriate transfer module for the actual exporter/importer roles: controller→controller, controller→processor, processor→processor, or processor→controller. Complete parties, transfer description, competent authority, technical/organisational measures, subprocessors and chosen options.

**Important scope issue:** the 2021/914 instrument is intended for importers whose relevant processing is not already subject to GDPR. The Commission page reviewed for this snapshot states that additional clauses for importers already subject to GDPR are being developed. Check the current instrument and importer situation; obtain a specific legal route instead of mechanically selecting a 2021 module for every importer.

Do not alter approved core clauses in a way that conflicts with their safeguards. Supplemental commercial terms must not contradict them. Keep a valid chain of instructions and upstream authorisation when the platform is a processor.

## Assess laws/practices and safeguards

For a route requiring it, document the transfer impact assessment: countries, recipients, data, purposes, format/access, duration, onward flows, relevant laws/practices, government-access risks, contractual commitments, safeguards, limitations and review triggers. Apply SCC clauses 14–15 where relevant and EDPB supplementary-measures guidance.

Encryption can be effective if the relevant importer/authorities cannot obtain intelligible data and the keys are appropriately controlled. TLS or ordinary at-rest encryption is not a solution to a risk where the importer necessarily receives plaintext and holds the keys. Pseudonymisation must actually prevent attribution by the recipient with reasonably available information. Contractual assurances alone may be insufficient where binding law prevents compliance.

If no effective mechanism/safeguard combination is established, suspend or avoid the affected transfer under the applicable process; use a technically viable alternative while resolving the legal question. An acknowledgement of risk does not itself authorise a prohibited transfer.

## Evidence and review

Store the route map, current mechanism, recipient/scope checks, executed instruments, transfer assessment, security proof, customer authorisation where required, notice mapping and owner. Refresh after recipient/access-country/subprocessor changes, legal developments, incidents, and expiry/lapse. Avoid storing unnecessary personal content in the transfer assessment itself.
