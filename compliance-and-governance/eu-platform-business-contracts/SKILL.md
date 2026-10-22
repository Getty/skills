---
name: eu-platform-business-contracts
description: "Use when reviewing B2B contracts of an AI or SaaS platform — enterprise terms, DPA/AVV, SLA, security schedule, customer questionnaire or audit, model-provider or vendor terms, acceptable use, subprocessors, Data Act switching and exit, banks, health or public-sector customers."
---

# EU Platform Business Contracts

## Operating rule

Review both directions of the supply chain: what the platform buys and what it promises customers.
Translate every material promise into an owner, control and verifiable record.
Treat legal, commercial and technical approval as different decisions.
Research baseline: 2026-10-22; verify current law and actual contract versions before concluding.
Use the EU core plus an explicit national adapter; German AGB rules do not represent all member states.

## Establish the deal

1. Identify parties, signing authority, seller/merchant role, customer country and transaction purpose.
2. Identify the platform's role for each AI system, data operation and subcontracted service.
3. List supplied performance, deployment model, seats, usage, support and implementation work.
4. Classify business-only, mixed consumer/business or public/regulated procurement.
5. Obtain the actual order form, master terms, DPA, security annex, SLA, license and acceptable-use policy.
6. Record document precedence, incorporation method, dates, versions and renewal/change mechanisms.
7. Inventory upstream commitments and exclusions that can conflict with downstream promises.
8. Complete `assets/contract-control-register.json` with unknowns visible.

## Review the contract stack

- State what service is supplied and which outcomes are only best efforts.
- Describe AI limitations without using them to disclaim every contractual obligation.
- Separate customer data, personal data, inputs, generated outputs, fine-tuned weights, metadata and platform IP.
- Specify permitted processing, training use, retention, access, locations and subprocessors consistently.
- Verify authority to grant any claimed license or exclusivity.
- Define suspension triggers, notice, containment, review and restoration.
- Define support, service availability, incident communication, recovery and exit in measurable terms.
- Review liability, indemnity, warranty and remedy allocation under applicable law.
- Avoid assuming that B2B standard terms are exempt from unfair-terms review.
- Escalate contested classifications with the concrete clause and operational impact.

## Convert promises into controls

1. Link each clause to code, configuration, runbook or human process.
2. Add evidence, owner and renewal date for each control.
3. Compare the promise to the actual model-provider and cloud configurations.
4. Check tenant isolation and whether customer-specific restrictions follow background jobs, support access and fallback routes.
5. Test claimed export, deletion, retention, security and availability behavior on representative data.
6. Document partial coverage and dependencies; do not call a supplier certificate platform-wide assurance.
7. Make deviations explicit before signature or renewal.

## Assess Data Act switching separately

Assess Regulation (EU) 2023/2854 Chapter VI for the actual data processing service.
Do not limit the assessment to IaaS or assume all bespoke work is exempt.
Distinguish customer-data export, service migration and GDPR data-subject portability.
Check notice, transition, retrieval, deletion, assistance, continuity, interfaces and charges.
Plan for the general switching-charge prohibition from 2027-01-12, subject to the actual statutory scope and exceptions.
Review the current consolidated law for amendments before relying on a timing or exemption.
Keep the proposal/adoption/application status of Digital Omnibus changes explicit.
Use [data-act-switching.md](references/data-act-switching.md) for the detailed workflow.

## Procurement and regulated customers

Evaluate vendors before signing and before material changes to processing, routing or ownership.
For a financial, health, legal, public-sector or critical-infrastructure customer, obtain its actual mandatory requirements.
Assess flow-down duties and direct statutory status independently.
Do not label every ICT vendor a directly regulated financial entity merely because a bank buys the service.
Route AI Act roles, privacy, cybersecurity, secrecy and accessibility questions to their specialist skills.
Do not promise sector compliance based only on a generic enterprise plan.

## Release and renewal gates

Reassess whenever a model or cloud provider changes, a new region is used, telemetry is added, an SLA changes, or a contract is renewed.
Reject unsupported promises before they enter sales material or the signed schedule.
Treat a signed deviation as an obligation to implement, not as evidence that implementation already happened.
Block an affected release when a known material contractual or statutory requirement is unmet.
Keep unresolved legal interpretation pending; continue unrelated authorized engineering.
Do not silently weaken a customer's agreed control to restore a failing build.

## Required output

Produce:

1. Deal facts and applicability matrix.
2. Annotated contract issues and precedence map.
3. Upstream/downstream gap analysis.
4. Clause-to-control register with owners and evidence.
5. Tested exit and incident procedures.
6. Negotiation options with operational costs and risks.
7. A concrete signature/release recommendation and unresolved decisions.

Separate legal risk, service reliability, commercial concessions and missing evidence.
Label an unreviewed draft as a draft.
Use `assets/contract-review.md` and `assets/business-test-vectors.json`.

## Action boundaries

Inspect, compare, draft and implement authorized controls autonomously.
Preserve existing authority for routine contract operations under approved policy.
Do not sign, accept changed vendor terms, send negotiation messages or grant concessions without authorization.
Prepare the exact clause and impact before asking the accountable person for a decision.
Do not allow an agent's generated summary to replace the signed agreement.

## Load references selectively

| Task | Reference |
| --- | --- |
| Deal classification and document hierarchy | [contract-stack-and-country-adapters.md](references/contract-stack-and-country-adapters.md) |
| Liability, IP, confidentiality, AI promises | [clauses-and-risk-allocation.md](references/clauses-and-risk-allocation.md) |
| Vendor and subprocessor review | [vendor-procurement.md](references/vendor-procurement.md) |
| Switching, migration, export and fees | [data-act-switching.md](references/data-act-switching.md) |
| SLA, incidents, continuity and evidence | [service-operations-and-evidence.md](references/service-operations-and-evidence.md) |
| Banks, healthcare, professionals and public bodies | [regulated-customers.md](references/regulated-customers.md) |
| Sources and law refresh | [sources.md](references/sources.md) |
