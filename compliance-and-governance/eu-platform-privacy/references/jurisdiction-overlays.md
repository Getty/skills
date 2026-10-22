# EU core and country overlays

Sources: P1, P8; verify national laws and competent-authority material for each actual country. This file supplies a method and a German starting overlay, not 27 completed legal opinions.

## Determine the connecting facts

Record legal entities and establishments, where processing decisions are made, countries of operation/targeting, relevant data-subject relationships, sector, and public/private status. Apply GDPR territorial rules independently of contractual choice of law. Analyse supervisory competence under Arts 55–56; a mailbox or hosting location does not manufacture a main establishment or a lead authority.

For each country create an adapter containing authority/source URLs, reviewed version/date, applicable rules and exceptions, local owners, customer-language requirements and unresolved issues. Identify EU/EEA membership separately from the label Europe. UK GDPR/PECR and Swiss FADP are separate regimes; they are not automatically covered by a German/EU adapter.

## German overlay

| Topic | German starting point | Implementation consequence |
| --- | --- | --- |
| Additional DPO obligations | BDSG §38 | Assess 20-person statutory processing test and independent triggers, including DPIA-required processing; do not count developers alone. |
| Employment data | BDSG §26 with GDPR Art 88 and relevant case law/collective rules | Screen necessity, employee consent, sensitive-data conditions and employee-representation involvement. |
| Child consent | GDPR Art 8 default 16 for its specific consent/ISS context | Separate parental authorisation from contract capacity, age-restricted content and other lawful bases. |
| Supervision | Competent federal/state authority depends on entity/sector/processing | Private businesses often fall under a Land authority; do not designate BfDI automatically. |
| Communications/tracking | TDDDG and applicable communications regime | Use the tracking skill for terminal access and separately screen confidentiality/communications obligations. |
| Professional/secrecy restrictions | Sector and professional law, e.g. relevant protected confidential information | Obtain a specific assessment before allowing healthcare/legal/confidential records into general support or model APIs. |

Do not claim that every German AI platform must appoint a DPO, complete a DPIA, or obtain consent for every processing activity. Record the actual trigger.

## Expansion checklist

Verify national additions for DPO designation, Art 8 age, employment, health/genetic/biometric data, criminal-offence processing, national Art 23 rights restrictions, court/claim retention, communications law, and competent-authority DPIA lists. Check whether a rule depends on establishment, affected relationship or service targeting. Use local official sources, not translated German templates.

Keep the EU core controls shared: lawful purpose/basis, data map, access control, minimisation, rights capability, transfer assessment, security and accountability. Parameterise truly local requirements, such as contacts and national triggers, instead of forking the entire architecture.

If expansion details are missing, implement the shared privacy controls and produce a concrete adapter gap list. Do not mark the new country legally approved or block unrelated reversible development.
