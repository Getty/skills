# Incident qualification and parallel clocks

## Preserve multiple legal events

Record initial detection, confidence changes, controller awareness, processor awareness, significant-incident awareness, CRA exploited-vulnerability/severe-incident awareness, notification submission, fix availability, and authority-order receipt separately in UTC with the original local timezone. A legal awareness assessment must explain when sufficient facts existed. Do not reset the start to the time counsel, the CEO, or an agent reads the ticket.

Clocks are maximum windows or statutory timings, not permission to wait. “Without undue delay” can require action earlier. Record a deadline even when investigation remains incomplete; stage information rather than invent facts.

## Main notification table

| Regime/actor | Trigger | Timing | Audience and notes |
|---|---|---|---|
| GDPR controller, Art33 | Personal-data breach, unless unlikely to risk natural persons' rights/freedoms | Without undue delay; where feasible within 72h of awareness; explain delay | Competent supervisory authority; permit phased information under Art33(4); document all breaches under Art33(5) |
| GDPR processor, Art33(2) | Awareness of personal-data breach | Without undue delay | Controller; no general statutory “processor may wait 72h” rule; contract can add a shorter operational time |
| GDPR controller, Art34 | Likely high risk to affected people, subject to statutory exceptions | Without undue delay | Affected people in clear language; separate from authority notification |
| NIS2 covered entity, Art23 | Significant incident under applicable law and criteria | Early warning <=24h; incident notification <=72h from awareness; requested updates; final <=1 month after the incident-notification submission | CSIRT/competent authority; trust-service providers have a specific 24h incident-notification provision; national implementation must be checked |
| German BSIG covered entity, §32 | Significant incident under §2(11) and applicable implementing criteria | Without delay, <=24h early; <=72h fuller notice; requested updates; final <=1 month from fuller notice | Current BSI-designated route; ongoing-incident progress/final provision in §32(2) |
| CRA manufacturer, Art14(1)–(2) | Awareness of an actively exploited vulnerability contained in an in-scope product | Without undue delay, <=24h early; <=72h vulnerability notification; final <=14 days after corrective/mitigating measure becomes available | Coordinating CSIRT and ENISA through SRP, subject to statutory arrangements |
| CRA manufacturer, Art14(3)–(4) | Awareness of severe incident affecting security of an in-scope product | Without undue delay, <=24h early; <=72h incident notification; final within 1 month after that notification | Separate from vulnerability reporting; Art14 criteria and interim/final handling matter |
| Customer contract | Defined security event / personal-data incident / outage | Exact signed term | Contractual recipient, secure channel, information schedule; do not infer it from GDPR |

Sources: SEC-GDPR, SEC-BREACH, SEC-BREACH-SME, SEC-NIS2, SEC-BSIG-REPORT, SEC-CRA, SEC-SRP-FAQ. Open-source steward reporting under CRA Article 24(3) has its own scope and applies from 2027-12-11; do not backdate it to the manufacturer deadline.

Other regimes, including financial-sector DORA, health, telecom, critical facilities, and AI Act serious-incident obligations, require their own qualification and clocks. Route them to the designated sector/AI reviewer. Never reuse the GDPR 72h rule as a universal incident SLA.

## Qualify without over-reporting or hiding

**Personal-data breach:** assess loss of confidentiality, integrity, or availability, including accidental wrong-recipient disclosure, unauthorized tenant access, deleted essential records, unavailable data, and key compromise. Risk to people is distinct from the provider's financial damage. A log finding may be enough for awareness; complete attribution is unnecessary. Encryption may reduce risk if the relevant keys remained protected, but an encrypted backup being the sole unavailable copy creates a different availability risk.

**NIS2 significance:** review serious operational disruption/financial loss and considerable harm to others, including potential harm. For named digital entities, Regulation 2024/2690 has cross-cutting and service-specific criteria; a complete cloud-service unavailability exceeding 30 minutes is one criterion, not a universal threshold for every business or the only cloud criterion. Review aggregation of recurring incidents and excluded scheduled interruptions under the actual text. Preserve service scope, EU users affected, duration, compromise, malicious access, and evidence supporting the decision.

**CRA vulnerability:** distinguish a weakness, exploit available in theory, and reliable evidence of malicious exploitation. Map the exploit to the actual product/components; third-party notification can trigger awareness. **CRA incident:** assess severe impact on product security using Article 14, not merely uptime or the presence of personal data. Both CRA branches may need assessment for the same event.

## First-hour operational sequence

1. Open the incident record and appoint incident lead, security operator, privacy reviewer, legal reviewer, and communications owner. Record backups for absent staff.
2. Contain within actual authority: revoke a demonstrably compromised token, disable an affected connector or narrow access under the existing runbook, preserve relevant evidence, and keep necessary service available where safe.
3. Record affected tenants, data categories, people, regions, systems/products/versions, supplier involvement, observed facts, uncertainties, and mitigation already done.
4. Start independent deadline entries with owner and reminder/escalation under the organization's authorized incident procedure. Account for weekends, timezones, and calendar months; do not replace “one month” with a fixed 30 days.
5. Validate each recipient, portal, controller/processor responsibility, required fields, and disclosure minimization. Prepare a draft initial report with clearly marked unknowns and the planned next update.
6. Seek the authorized decision where necessary, explicitly showing deadline and consequence of delay. The agent must not quietly send reports, admit liability, or disclose customer content without the user's authorization.

## Evidence and communication controls

Store hashes, original timestamps, access history, and minimal relevant forensic artifacts in a restricted evidence location. Separate production recovery from evidence copies; do not preserve all customer data indefinitely. Define legal hold scope and review/expiry. Use secure recipients/channels and verify requests independently. A malicious “incident reporter” can attempt to extract sensitive information.

Keep fact statements, legal assessments, decisions, reports actually sent, acknowledgement receipts, and update schedule distinct. Do not say “reported” when a draft exists or a submission failed. Record a decision not to notify with rationale and conditions that reopen it.

Avoid public disclosure of exploit details while protection and coordinated response are pending. Do not suppress relevant facts from a required notice. Let counsel assess privileges, cross-border obligations, notification exceptions, or disputed thresholds; preserve technical truth and clocks.

## Tabletop scenarios

- Tenant A can read one document belonging to Tenant B through a signed URL. Assess personal-data breach independently of whether anyone exploited it; inspect access evidence and risk to people.
- A covered cloud API is completely unavailable for 40 minutes. Apply the relevant digital-entity criterion even if no data was leaked.
- A shipped extension contains an actively exploited dependency. Assess CRA manufacturer reporting now even if its full conformity transition is 2027.
- A patch becomes available after the initial CRA notice. Set the vulnerability final-report date from patch/mitigation availability, not from incident discovery.
- An upstream processor says “our legal team will confirm next week”. Assess the known facts and contractual/controller notices; the upstream response does not suspend your clock.
