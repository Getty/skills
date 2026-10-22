# Operating model and evidence ownership

## Accountability

The agent researches, identifies gaps, proposes implementation, executes authorised work and checks evidence. The operating organisation remains responsible for its decisions. Assign named organisational functions rather than pretending the agent is the DPO, conformity body, lawyer or tax adviser.

| Function | Owns | Agent contribution |
| --- | --- | --- |
| Product/service owner | Intended purposes, market scope and risk decisions | Feature inventory, scope diffs, decision options |
| Engineering owner | Implementation and reliable deployment | Code/config changes, tests and rollback design |
| Privacy owner/DPO where applicable | Independent advice, privacy process and applicable oversight | RoPA/DPIA drafts, rights workflows, facts and evidence |
| Security/incident owner | Operational response and risk treatment | Triage, scoped containment, evidence collection and drafts |
| Legal/compliance reviewer | Material legal interpretation and approved commitments | Source packet, alternatives and unresolved questions |
| Finance/tax owner | Tax classification, invoicing and record retention | Billing tests, reconciliation and configuration review |
| Accessibility/content owner | User-facing controls and operating process | Journey testing, moderation records and remediation |

In small organisations one person may perform several functions, subject to conflicts and legal constraints. Record actual responsibilities. Do not invent a mandatory committee for routine low-risk work.

## Records with stable identifiers

Maintain a platform profile; feature inventory; applicability and control registers; source registry; vendor/model register; data flow and retention maps; decision records; release evidence; incidents and rights requests. Link records using stable IDs. Apply least privilege to sensitive assessments, security defects and personal information. Repository metadata should normally contain references to protected evidence, not the evidence itself.

Record evidence against a release/commit, environment and observation time. A screenshot of yesterday's staging branch cannot establish today's production behaviour. A valid hash establishes byte identity, not truth. Keep evidence collection and legal interpretation separately reviewable.

## Review rhythm

Choose an operational cadence according to feature risk and change rate. Suggested engineering defaults are per material change, before launch, after a significant incident, on vendor/model/terms change, and a periodic source/ownership refresh. These are internal policy choices unless tied to a specific legal requirement. Record why the cadence is adequate and reduce unnecessary ceremony for stable, low-risk features.

Do not create a scheduler, subscribe a person, send notifications or set recurring tasks merely because a skill describes a periodic process. Create automation only when requested and authorised. A skill is not an always-running monitoring service.

## Escalation packet

State: decision needed; observed facts; exact source/provision/version; applicability argument; uncertainty; options and consequences; implementation ready for review; owner and required date. Prefer a narrow question such as 'May this support team outside the EEA access these records under the proposed transfer arrangement?' to 'Is our platform legal?'.

Escalate an imminent reporting deadline through the existing authorised incident channel. Prepare draft fields even if information is incomplete. Do not send to a regulator without communication authority, and do not hide the urgency while waiting for perfect facts.

## Completion criteria

Close a finding only when its acceptance criteria are met for the relevant release and an accountable owner accepts any remaining nonblocking limitation. Reopen on a changed assumption, expired evidence, failed test, amended law, changed provider terms or complaint revealing a mismatch. Avoid self-approval loops where the same agent changes the control, deletes the failing evidence and declares success without preserving the history.
