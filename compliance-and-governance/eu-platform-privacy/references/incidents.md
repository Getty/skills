# Personal-data breach response

Source: GDPR Arts 4(12), 28(3)(f), 32–34 (P1). Apply the current text and any additional national/sector reporting rules. Coordinate with cybersecurity/AI Act response without assuming the clocks or thresholds are identical.

## Triage facts and legal clocks separately

A personal-data breach can concern confidentiality, integrity or availability. Examples include wrong-tenant retrieval, unauthorised support access, exposed model logs, ransomware preventing access, corrupted customer records, or deletion without recoverability. Not every vulnerability or hallucination is a breach; establish what happened to personal data.

Record detection time, evidence, systems/data/people, controller/processor roles, and the time the relevant entity became aware. Use the designated incident owner to assess awareness rather than silently starting or resetting the legal clock when a ticket changes hands. Preserve facts even where the notification conclusion is uncertain.

## Roles and duties

| Role/threshold | Required handling |
| --- | --- |
| Processor becomes aware | Notify the controller without undue delay under Art 33(2); follow stricter contractual assistance windows where agreed. Do not substitute a universal 72-hour processor allowance. |
| Controller; breach not unlikely to risk rights/freedoms | Notify the competent authority without undue delay and, where feasible, within 72 hours after awareness under Art 33(1). Document reasons for delay. |
| Controller; breach unlikely to risk rights/freedoms | A reasoned no-notification decision can apply; still document the breach under Art 33(5). |
| Likely high risk to people | Communicate to affected persons without undue delay under Art 34 unless a specific exception is justified. Do not equate this threshold with the authority-notification threshold. |

Where complete information is unavailable, consider phased notification under Art 33(4). Do not wait for final forensics if the reporting obligation is already triggered. Identify the proper supervisory authority and applicable lead-authority/cooperation rules; a vendor's location does not automatically choose it.

## Execute safely

1. Activate the authorised incident plan and assign a controller decision owner and technical lead.
2. Contain the relevant route using proportionate actions: revoke compromised keys, disable exposed links, isolate the affected connector or stop leakage. Preserve evidence and avoid unnecessary production destruction.
3. Record nature, categories and approximate numbers where known, contact point, likely consequences, and measures taken/proposed.
4. Assess risk to people based on data sensitivity, identifiability, recipients, likelihood of misuse, reversibility and affected groups. Evidence that encryption prevents access must include key exposure facts.
5. Draft authority/customer/person communications, explain uncertainty, and obtain the organisation's authorised decision/send action.
6. Track remediation, updates to previous notifications, customer assistance and post-incident review.

Agent authority to inspect/remediate a repository does not automatically authorise sending legal notifications or making public admissions. Prepare complete reviewable drafts promptly and surface an approaching deadline to the authorised owner. Do not send messages without explicit permission or an already established mandate.

## Record even a negative decision

Retain incident ID, chronology, facts known at each decision time, role allocation, risk analysis, notification/non-notification rationale, authoriser, communications, containment and prevention evidence. Avoid copying full affected datasets into a broad-access ticket. Use restricted evidence references and retention appropriate to the investigation and legal duties.

For customer-controlled content, preserve contractually agreed assistance and information flow; the platform may simultaneously be controller for its own affected account/log data. Make both decisions explicitly. Do not assume one supplier's notice satisfies all customer/controller obligations.
