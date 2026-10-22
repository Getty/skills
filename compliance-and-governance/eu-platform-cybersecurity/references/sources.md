# Cybersecurity source register

Research snapshot: 2026-10-22. The sources below were located or read through official publishers. Check the live consolidated law and relevant national implementation before making a fresh operational decision. A source being accessible is not evidence that every legal proposition has been checked.

## Binding legal sources

| ID | Source and sections | Jurisdiction/status | Use |
|---|---|---|---|
| SEC-GDPR | [Regulation (EU) 2016/679](https://eur-lex.europa.eu/eli/reg/2016/679/oj), Articles 5(1)(f), 24–25, 28, 32–34 | EU regulation; applicable | Risk-based personal-data security and personal-data breach duties |
| SEC-NIS2 | [Directive (EU) 2022/2555](https://eur-lex.europa.eu/eli/dir/2022/2555/oj), Articles 2–6, 20–23, 26–27, Annexes I–II | EU directive; national implementation required | Entity/service/size/jurisdiction screening; management and incident duties |
| SEC-NIS-IR | [Implementing Regulation (EU) 2024/2690](https://eur-lex.europa.eu/eli/reg_impl/2024/2690/oj), Articles 2–16 and Annex | EU implementing regulation for the named digital entities | Concrete cybersecurity measures and significant-incident criteria; not a universal threshold for all firms |
| SEC-BSIG-SCOPE | [BSIG §28](https://www.gesetze-im-internet.de/bsig_2025/__28.html), [definitions §2](https://www.gesetze-im-internet.de/bsig_2025/__2.html), [Annex 1](https://www.gesetze-im-internet.de/bsig_2025/anlage_1.html), [Annex 2](https://www.gesetze-im-internet.de/bsig_2025/anlage_2.html) | Germany; enacted national law | Exact categories, thresholds, exclusions, and independent-system group rule |
| SEC-BSIG-CONTROLS | [BSIG §30](https://www.gesetze-im-internet.de/bsig_2025/__30.html), [§38](https://www.gesetze-im-internet.de/bsig_2025/__38.html) | Germany; enacted | Documented risk measures and management implementation/oversight/training |
| SEC-BSIG-REPORT | [BSIG §32](https://www.gesetze-im-internet.de/bsig_2025/__32.html), [§33](https://www.gesetze-im-internet.de/bsig_2025/__33.html), [§34](https://www.gesetze-im-internet.de/bsig_2025/__34.html), [§35](https://www.gesetze-im-internet.de/bsig_2025/__35.html) | Germany; enacted | Reporting, registration, special digital-entity registry, recipient information |
| SEC-CRA | [Regulation (EU) 2024/2847](https://eur-lex.europa.eu/eli/reg/2024/2847/oj), Articles 2–3, 13–16, 24, 32, 69, 71; Annexes I–IV, VII | EU regulation with staged application | Product security, manufacturer reporting, lifecycle and conformity scope |
| SEC-DORA | [Regulation (EU) 2022/2554](https://eur-lex.europa.eu/eli/reg/2022/2554/oj), Articles 2, 28–30, 31 onward | EU regulation; applicable from 2025-01-17 | Financial-sector customer contracts and conditional ICT third-party oversight |

The EUR-Lex reader intermittently returned a bot-check page during this research. Statutory entry links are preserved. Relevant published text/search extracts were cross-checked with the official regulator resources below. Before relying on a detailed provision or an amendment, obtain the authenticated OJ/consolidated text; do not treat a failed fetch as legal confirmation.

## Official guidance and operational sources

| ID | Source | Status and dated anchor |
|---|---|---|
| SEC-BSI-FAQ | [BSI NIS2 general FAQ](https://www.bsi.bund.de/DE/Themen/Regulierte-Wirtschaft/NIS-2-regulierte-Unternehmen/NIS-2-FAQ/NIS-2-FAQ-allgemein/FAQ-zu-NIS-2_node.html) | Regulator guidance; confirms German implementation published 2025-12-05, effective 2025-12-06 |
| SEC-BSI-PORTAL | [BSI NIS2 registration information](https://mip2.bsi.bund.de/info-nis2-registrierung/) | Operational guidance; use current BSI portal and category-specific transition instructions; do not hardcode old MIP routes |
| SEC-BSI-DUTIES | [BSI NIS2 duties](https://www.bsi.bund.de/DE/Themen/Regulierte-Wirtschaft/NIS-2-regulierte-Unternehmen/NIS-2-Pflichten/nis-2-pflichten_node.html) | Regulator interpretation and implementation information |
| SEC-ENISA-NIS | [ENISA NIS2 Technical Implementation Guidance](https://www.enisa.europa.eu/publications/nis2-technical-implementation-guidance) | Nonbinding technical guidance, 2025-06-26; evidence examples and mapping for Regulation 2024/2690 |
| SEC-CRA-TIMELINE | [Commission CRA policy](https://digital-strategy.ec.europa.eu/en/policies/cyber-resilience-act) | Official explanatory page; checked 2026-10-22; reporting from 2026-09-11, main obligations from 2027-12-11 |
| SEC-CRA-GUIDANCE | [Commission adopted CRA implementation guidance](https://digital-strategy.ec.europa.eu/en/library/commission-publishes-new-guidance-support-timely-cyber-resilience-act-implementation) | Nonbinding C(2026) 5252, published 2026-07-27; replace the earlier consultation draft in operational reviews |
| SEC-CRA-SUMMARY | [Commission CRA legal summary](https://digital-strategy.ec.europa.eu/en/policies/cra-summary) | Official explanation; Chapter IV from 2026-06-11; useful scope/reporting overview |
| SEC-SRP | [ENISA Single Reporting Platform](https://www.enisa.europa.eu/topics/product-security/vulnerability-services/eu-incident-response-and-cyber-crisis-management/single-reporting-platform-srp) | Operational guidance; platform updated 2026-10-20; interface details must be refreshed before use |
| SEC-SRP-FAQ | [ENISA SRP FAQ](https://www.enisa.europa.eu/topics/product-security/vulnerability-services/eu-incident-response-and-cyber-crisis-management/single-reporting-platform-srp/frequently-asked-questions) | Official guidance; distinguishes manufacturer Art14 duties from steward Art24 duties beginning 2027-12-11 |
| SEC-BREACH | [EDPB Guidelines 9/2022 v2.0](https://www.edpb.europa.eu/system/files/2023-04/edpb_guidelines_202209_personal_data_breach_notification_v2.0_en.pdf) | Regulatory guidance, 2023; awareness and GDPR notification risk tests |
| SEC-BREACH-SME | [EDPB breach guidance](https://www.edpb.europa.eu/sme/assess-the-risks/data-breaches_en) | Official explanation; controller awareness and phased notification |

## Engineering references, not legislation

- SEC-OWASP: [OWASP GenAI Top 10](https://genai.owasp.org/llm-top-10/), including [prompt injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/) and [excessive agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/). Community-maintained primary security guidance; use versioned attack cases, not a claim that OWASP compliance proves legal compliance.
- The controls and test designs in this skill are engineering implementations of identified risks. Unless a paragraph identifies an exact legal requirement, its particular mechanism, sampling schedule, metric, or numerical acceptance threshold is a project recommendation that the owner must approve.

## Refresh method

For each material conclusion record `source_id`, URL, official publisher, article, legal instrument version, checked date, application date, applicability facts, and remaining uncertainty. Check OJ publication and national gazettes for amendments before adopting a news announcement. Keep legislation, binding individual orders, guidance, standards, proposals, vendor commitments, and internal policy as separate source classes. A proposed common reporting mechanism does not extinguish existing parallel duties before its operative law applies.
