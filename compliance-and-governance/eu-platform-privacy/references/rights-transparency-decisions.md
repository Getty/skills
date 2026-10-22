# Rights, transparency, and automated decisions

Sources: P1, P3–P5, P7, P11–P12.

## Connect notices to reality

Maintain a notice-to-processing mapping rather than a single boilerplate policy. Cover the controller/contact/DPO where relevant, purposes and bases, legitimate interests where used, recipients, transfers/safeguards, retention criteria, rights, complaint route, required/optional provision and consequences, and relevant automated-decision information. Give Art 13 information when collecting from the person. For Art 14 indirect collection, check the required timing, normally a reasonable period no later than one month and earlier first communication/disclosure where applicable, plus any narrowly justified exception.

A model provider's notice does not satisfy the platform controller's duties. Explain prompt content, retrieved document passages, feedback, abuse monitoring, support access and training separately where their purposes differ. A generic statement that AI may make mistakes is not an explanation of consequential decision logic or lawful basis.

Prepare an accessible layered notice with accurate local-language detail for intended audiences. Record which notice version was shown at each collection point and re-inform before a relevant new purpose under Arts 13(3)/14(4).

## Rights request workflow

1. Detect requests in all relevant channels, including ordinary support language; do not require a magic subject line.
2. Record receipt, role, requested rights, scope, identity confidence, clock and assigned owner.
3. If a processor receives a customer-controlled-content request, promptly assist/route to the controller under the agreement; do not independently release another tenant's data.
4. Verify identity proportionately where there are reasonable doubts. Avoid unnecessary copies of official identity documents. Do not assume an identity check automatically pauses the statutory clock.
5. Search the data map, including content, identifiers, inferences, moderation records, vendors and derived stores.
6. Apply the correct right, document limited exemptions and third-party protections, and prepare a response in intelligible form.
7. Deliver securely through the authorised process, track completion and preserve only necessary audit evidence.

Under Art 12(3), act without undue delay and normally within **one calendar month**, not an arbitrary 30-day period. Where justified by complexity/number, the extension can be up to two further months; inform the person within the initial month with reasons. Requests are generally free; justify any manifestly unfounded/excessive classification and obtain responsible review. Do not auto-deny frequent requesters or requests involving large datasets.

## Keep rights distinct

| Right | Implementation implications |
| --- | --- |
| Access, Art 15 | Provide the person's data and required contextual information; include applicable inferences and actual processing. Protect others by targeted redaction, not blanket withholding. |
| Rectification, Art 16 | Correct source data, derived records and relevant outputs; track propagation. A hallucinated factual allegation about a person is not excused merely by a model disclaimer. |
| Erasure, Art 17 | Determine grounds and exceptions; delete affected data and derivatives, with defensible handling of restricted backups/legal holds. Do not silently delete records required by law. |
| Restriction, Art 18 | Enforce a processing block distinct from deletion, with applicable exceptions and notification before lifting where required. |
| Recipient notification, Art 19 | Notify relevant recipients of rectification/erasure/restriction unless the legal exception is established; report recipients to the person on request. |
| Portability, Art 20 | Assess consent/contract basis and automated processing; provide covered data in structured commonly used machine-readable form. It is not identical to Art 15 or a right to every proprietary inference. |
| Objection, Art 21 | Review grounds for relevant Art 6(1)(e)/(f) processing; stop direct-marketing processing, including related profiling, when objected to. |

Technical difficulty does not itself create an exemption. If training-data erasure/model correction is unresolved, escalate the actual legal and technical options; do not assert deletion of a source row removes information from model weights. Avoid adding personal data solely to identify people under Art 11 when the controller otherwise cannot identify them, while respecting the person's ability to provide information enabling rights.

## Automated decisions: Art 22

Test whether there is a decision based solely on automated processing, including profiling, with legal or similarly significant effects. Examine the whole decision chain, not just the component your team sells. CJEU SCHUFA confirms that an upstream score can fall within the rule where a downstream party gives it a determining role.

Document any applicable exception: contractual necessity, Union/member-state legal authorisation with safeguards, or explicit consent. Check additional special-category restrictions and mandatory safeguards, including human intervention, the person's viewpoint and contesting the decision where applicable. Do not claim that adding a manual approval button automatically makes the process non-automated.

For meaningful human involvement, ensure the reviewer has time, competence, relevant information, actual authority to change the outcome, and an incentive/record demonstrating real assessment. Monitor override patterns without turning employees into an uncontrolled surveillance dataset.

Provide the legally required meaningful information about logic, significance and envisaged consequences. The CJEU Dun & Bradstreet judgment emphasises explanation of the procedure/principles actually applied in an understandable way. Source-code dumping, a generic model description or a fabricated LLM explanation is inadequate. Validate that the explanation corresponds to the real decision trace. Trade-secret claims require a lawful balancing process, not automatic refusal of all information.

Keep GDPR assessment distinct from AI Act transparency, risk classification and explanation duties; meeting one regime does not waive the other.
