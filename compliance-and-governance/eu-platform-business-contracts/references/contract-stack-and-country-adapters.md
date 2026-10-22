# Contract stack and country adapters

## Identify the actual agreement

Gather the order form, master agreement, linked terms, product description, DPA/AVV, security schedule, support/SLA, acceptable-use rules and pricing/exit schedules. Save the exact versions incorporated at signing. Identify priority if two documents conflict. Review whether future online changes are incorporated validly; a supplier changing a web page is not proof that all existing customer contracts changed.

Classify SaaS access, licenses, hosting, implementation work, advisory services and resale separately. German rental, service, work and mixed-contract classifications depend on obligations and facts. Do not select one contract type merely from the label “subscription” or an English template. Examine who owes a defined result, who controls acceptance, and how defects are remedied. [B1]

Determine who can bind the company and who may configure delegated technical authority. Buying admin access should not silently authorize an employee to amend the corporate DPA or consent to model training. Store signatory and admin authority separately. Electronic signatures and click acceptance require analysis of the applicable form requirement and evidence; do not assert that every SaaS agreement needs a qualified electronic signature. [B2]

## National adapter

Record governing law, jurisdiction, contracting entities, service locations and mandatory local overlays. For Germany, standard terms remain subject to BGB § 307, with § 310 governing B2B modifications. §§ 308 and 309 do not simply operate identically to consumer contracts, but their exclusion from direct application does not validate every restriction. Terms described as “negotiated” need factual support. [B3]

Other-country adapters must identify incorporation, interpretation, remedies, limitation periods, liability restrictions, late-payment rules, electronic form and local public-policy limits. For EU public customers, distinguish procurement eligibility from contract performance. A German forum clause may not answer every question involving cross-border data or regulated services.

## Contract schema

Maintain:

- `agreement_id`, parties, authority, effective date, term and renewal.
- Document IDs, versions, hashes and priority.
- `service_description`: intended use, exclusions, regions, model choices and usage units.
- Roles per processing purpose and per AI system.
- Promises tied to controls, owners and dependencies.
- Customer-specific deviations and expiry dates.
- Change process, notice channels and permitted unilateral changes.
- Suspension, termination, export, retrieval and erasure states.

Do not use a customer success spreadsheet as the only executable policy. Customer-specific no-training, residency and retention restrictions must reach the routing and job layers. Keep a signed-agreement source of truth and a machine-readable policy derived through review; detect drift between them.

## Output discipline

Report a concrete mismatch: “Order form requires EU-only support access; support vendor has global access under its current role.” State whether the remedy is a config change, a contract amendment, a vendor replacement or a limited offering. Provide negotiated alternatives with their technical cost. Do not invent agreement to the most convenient alternative.
