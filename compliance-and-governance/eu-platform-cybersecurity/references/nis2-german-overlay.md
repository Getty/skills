# NIS2: German BSIG overlay

## Legal status

The BSI confirms the German NIS2 implementation was promulgated on 2025-12-05 and entered into force on 2025-12-06. Use the current `bsig_2025` text rather than the old BSIG or a 2024 draft. Recheck amendments, including changed critical-facility registration references. Sources: SEC-BSI-FAQ and SEC-BSIG-SCOPE.

## Classify the entity correctly

Read BSIG §28 together with §2 and both annexes. For the ordinary remunerated Annex 1 entity route, the particularly important category uses at least 250 employees OR annual turnover over EUR50 million AND annual balance sheet over EUR43 million. The ordinary important route for Annex 1/2 entities uses at least 50 employees OR both turnover and balance sheet over EUR10 million. Preserve strict `over` versus `at least` and the Boolean grouping.

These are not complete universal tests. §28 also addresses critical facilities, trust services, DNS/TLD registries, telecommunications, public entities, sector-specific exclusions, and relationship to DORA/energy/health infrastructure. Map each relevant paragraph instead of applying the ordinary table universally. §28(3) allows consideration of negligible business activities in classification; do not invent a revenue percentage as a safe harbor.

For size, §28(4) refers to Recommendation 2003/361/EC with a specified exception. Partner/linked enterprise figures have a particular German carve-out when the undertaking is independent regarding the relevant IT systems considering the legal, economic, and factual circumstances. Record architecture and governance evidence before relying on this; a separate company registration alone does not establish independence. Source: SEC-BSIG-SCOPE.

## Required operational records

| Area | Legal anchor | Evidence |
|---|---|---|
| Scope | §§2, 28, Annexes 1/2 | Entity/service decision, organizational figures, group assessment, country decision |
| Risk management | §30 | Threat/risk register, proportionate controls, effectiveness reviews, exceptions with rationale |
| Incidents | §§2(11), 32, 35 | Threshold assessment, independent clocks, staged reports and delivery evidence, customer notices |
| Registration | §§33–34 | First/repeat qualification date, submission, current contacts and service details, special digital-provider record |
| Leadership | §38 | Named management owner, approved plan, oversight minutes, regular management training |
| Critical facilities | §§31, 39 and current cross-references | Separate critical-facility determination and evidence timetable |

Source: SEC-BSIG-CONTROLS and SEC-BSIG-REPORT.

## Implement the §30 risk management system

Cover risk analysis, incident handling, continuity and backup restoration, supplier security, secure acquisition/development/maintenance, vulnerability handling/disclosure, effectiveness assessment, security hygiene/training, cryptography, personnel/access/asset management, and appropriate MFA or continuous authentication/secure communications. An AI application's model gateway, RAG indexes, identity provider, tool workers, GPU services, payment hooks, and monitoring suppliers belong in the same asset/dependency view.

For each control connect the threat to implementation and proof: `risk -> objective -> system/configuration -> test -> owner -> review`. Explain proportionality against exposure, size, costs, likelihood, severity, and social/economic impact. “We use a certified cloud” does not document the customer's tenant permissions, secrets, model integrations, recovery, or incident decisions.

For the digital entities named in Regulation 2024/2690, use its binding Annex and criteria. ENISA's June 2025 implementation guidance supplies useful evidence examples but does not create a separate certification or remove national duties. Source: SEC-NIS-IR, SEC-ENISA-NIS.

## Registration and notifications

§33 generally requires registration no later than three months after first or renewed qualification. Calculate the entity-specific date. Do not present 2026-03-06 as the only possible deadline; that date follows only for entities already qualifying at commencement. Do not treat informal enforcement tolerance as an amendment to the statutory deadline. Check special registration under §34 and current BSI instructions.

Use the currently published BSI portal and migration guidance; historical MIP links are not interchangeable. A reporting channel's operational availability and §32's rule concerning the established channel must be recorded. The current BSI information says affected companies use the BSI portal; some critical facilities/federal bodies have transition arrangements. Do not submit duplicate reports merely to feel safe. Sources: SEC-BSIG-REPORT, SEC-BSI-PORTAL.

For significant incidents, use the 24-hour early notification, 72-hour notification, and one-month final-report sequence, plus updates on request. The one-month clock runs from submission of the 72-hour notification. Ongoing incidents use the statutory progress/final handling. Consult [incident-clocks.md](incident-clocks.md) for simultaneous GDPR/CRA duties. The organization cannot defer awareness until its next board meeting.

## Verification and fail conditions

Test an out-of-hours incident, an absent primary contact, and a provider outage. Evidence must show a reachable decision-maker and a prepared submission path; do not create a fake report on a live regulator portal. Tabletop with a synthetic report and route validation is sufficient for the drill.

Flag a release risk when a covered entity cannot identify its management owner, register/report through the correct route, restore critical service, or show measures for a material threat. Escalate disputed statutory classification or liability to counsel and management with the exact disputed facts. Continue feasible security fixes while that review occurs.
