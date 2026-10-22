# Verification, operations and moderation evidence

## Test the actual service

Tie tests to service classification, applicable articles, policy version, environment and release. Treat a document review, local test and production observation as distinct evidence. Use safe synthetic fixtures and mock authority channels; do not generate illegal child-abuse material or expose genuine victims' content in a test set.

| Scenario | Expected invariant | Evidence |
|---|---|---|
| New private chat | No public indexing/sharing without actual permission | Configuration and tenant visibility test |
| Public share link | Classification revisited; source access and revocation work | Public/private mapping and link-expiry tests |
| Ordinary illegal-content notice | Usable intake, precise location, acknowledgement and decision route | Case events and user communication |
| Child-safety report | No demand to upload unlawful copies; urgent route works | Synthetic form and triage outcome |
| Legitimate educational context | Context review and proportionate outcome | Reviewer rationale and false-positive record |
| Policy restriction | Specific reason and applicable redress | Delivered notice and appeal link |
| Successful appeal | Reinstatement affects derived caches/search/monetization | State reconciliation and event trail |
| Small-enterprise status | Exempt clauses scoped, hosting duties retained | Current group-size evidence and matrix |
| Trusted flagger notice | Verified status/scope and priority, independent merits review | Queue trace and decision basis |
| Minor user | Age-appropriate defaults and access paths | UI/API/attachment/share tests |
| Forged authority demand | No data leak, independent verification | Mock case and rejected transmission |
| Valid urgent order | Correct clock, accountable person, narrow authorized action | Tabletop receipt/approval/effect record |
| Transparency publication | Accurate aggregation without personal data | Reconciliation and redaction review |

These are engineering acceptance examples, not universal statutory test cases. Sources for obligations: CON-DSA, CON-MINORS, CON-TCO, CON-EEVIDENCE and applicable national sources.

## Operating ownership

Assign someone who can make a policy decision, someone who can implement it, and an available escalation route for high-impact legal/safety issues. Document training for reviewers, language competence, access limits, conflicts and staff wellbeing. Protect moderators from unnecessary repeated exposure to harmful content with minimized previews, controlled access, appropriate specialist procedures and support.

A moderation classifier can triage and produce evidence but must not silently become the sole final appeal decision-maker where qualified human supervision is required. Preserve model/version, evaluated language/domain, relevant limitations, confidence and reviewer outcome. Track disparate error patterns without collecting unnecessary sensitive attributes.

## Case evidence and retention

Retain the case ID, item location, submitted allegation, jurisdiction, facts, legal/policy basis, restriction scope, automation, reviewer, communications, appeal and final state. Use restricted references to sensitive evidence instead of putting it into public issue trackers or generic model prompts. Record lawful basis, retention purpose, review and deletion schedule for case files.

Separate short-lived triage data, legal holds, TCO preservation, contractual records and public transparency aggregates. Retention for one purpose does not authorize unlimited reuse for model training. Preserve errors and reversals so metrics do not hide bad outcomes. Do not overwrite the original decision with the appeal result; link the two.

## Metrics

Useful internal metrics include time to acknowledgement/triage/decision, urgent missed deadlines, backlog age, notice validity, restrictions by basis and type, appeal uptake, reversal, reinstatement time, recurrent abuse, language-specific errors and manual escalation. Adopt thresholds through the owner's policy and risk assessment rather than presenting them as legal deadlines.

Align the instrumentation with applicable DSA reports/database fields and current templates. Reconcile actions across platform, customer-controlled moderation and third-party providers. If customer administrators make decisions, explain who is acting and which obligations remain with the service provider; outsourcing moderation is not an automatic transfer of legal responsibility.

## Release gate and change monitoring

Reopen the review for public sharing, user stores, new audience/country, image/audio/video generation, recommender changes, profiling ads, default settings, identity/age vendor, corporate size/designation, legal amendment and a material pattern of mistakes. Do not start an ongoing job without authorization.

Block only the affected feature where feasible when mandatory reports/appeals/contact routes are missing, unlawfully public data remains accessible, minors face an uncontrolled material risk, or an urgent required action cannot be performed. State the remedy and what evidence will permit release. A user-visible disclaimer does not close a failed control.

Use the shared assurance skill for the final evidence ledger. Return applicability, findings, evidence, action owner, deadlines, current status and uncertainty; never mark an entire platform “legally safe” because a form renders correctly.
