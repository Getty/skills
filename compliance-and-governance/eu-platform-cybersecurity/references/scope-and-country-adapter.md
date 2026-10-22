# Security applicability and country adapter

## Minimum facts

Record each legal entity and each service line separately: AI chatbot, hosted model API, customer document storage, managed deployment, MSP/MSSP, marketplace, downloadable client, mobile app, appliance, SDK, and consultancy. Record actual activities rather than SIC/NACE labels alone. Document establishments, management location, EU customer targeting, group ownership, staffing and financial measures, regulated customers, product branding, and distributor/importer relationships.

## Apply the layers independently

| Layer | Test | Result to preserve |
|---|---|---|
| GDPR security | Personal data processed as controller or processor | Articles 28/32 security allocation plus personal-data scope; not a size-based exemption |
| NIS2 | Defined entity/service, Annex I/II, size or special inclusion, territorial jurisdiction | National law and regulator; category and class; calculation; exclusions |
| CRA | Product with digital elements made available in commercial activity with relevant connection, plus necessary remote processing | Product boundary, economic-operator role, exclusions, dates, conformity class |
| Sector rules | Actual regulated activity or designated entity | Specialist regime and competent reviewer; distinguish direct obligation from customer flow-down |
| Contract | Signed security schedule, SLA, AVV/DPA, procurement conditions | Exact commitment, owner, test, deadline; stricter contracts do not rewrite legislation |

Sources: SEC-GDPR, SEC-NIS2, SEC-CRA, SEC-DORA in [sources.md](sources.md).

## NIS2 assessment sequence

1. Match the real service to definitions in Article 6 and Annexes I/II. Being a cloud customer does not make the organization a cloud provider. A provider of managed customer systems needs a genuine MSP/MSSP review. SaaS can fall within the cloud definition depending on the actual service.
2. Calculate entity size using the applicable SME rules, including linked and partner enterprises, then apply national implementation. Separate `employees >= threshold` from `turnover AND balance sheet > threshold`; one financial value alone may not satisfy the statutory alternative.
3. Check special categories independent of ordinary size rules, designation, critical-entity status, and relevant sector exceptions. A small enterprise is not automatically outside all NIS2 duties.
4. Establish jurisdiction. For named cross-border digital providers, Article 26 contains special main-establishment rules. Where cybersecurity risk-management decisions are mainly taken can matter; the marketing country or cloud region is not a substitute.
5. Map registration, governance, controls, notification, and supervision. Apply Regulation 2024/2690 only to its named entities; preserve national/sector alternatives where applicable.
6. Reassess on acquisition, group integration, new service line, moved security decision-making, or threshold crossing.

## CRA assessment sequence

Treat a desktop agent, browser extension, mobile app, on-premises image, and separately distributed software component as product candidates. Identify whether the operator develops or has the product developed and markets it under its name. A product supplied without a price can still be part of commercial activity. Free/open-source software needs the specific noncommercial and steward rules; an open-source license is not a blanket business exemption.

For a backend, apply the remote-processing definition: identify processing designed/developed by or under the manufacturer's responsibility without which the product could not perform a function. Separate this from a pure standalone hosted service. Record the interpretation and product dependency, not merely `backend = out` or `internet = in`. Check sector exclusions, substantial modifications, and placing-on-market timing. Use the adopted Commission guidance for difficult boundaries.

## Adapt beyond Germany

Create one country record per relevant jurisdiction:

`country | establishment/targeting fact | national NIS2 law/version | regulator/CSIRT | entity criteria | registration route | incident route | sector exception | language | verified_on | reviewer`

Use EUR-Lex for EU law and the national gazette/regulator for implementation. Do not copy German BSIG sections, registration dates, critical-infrastructure thresholds, portal names, or management-liability language into another country's conclusion. EU membership, EEA incorporation, UK law, and Swiss law are distinct checks. Do not label the entire European continent as an EU legal territory.

## Examples

- A six-person German B2B chatbot using a hyperscaler's API still needs GDPR and contractual security. NIS2 is a separate activity/size/special-category test; the API provider's coverage does not transfer automatically to the startup.
- A larger managed AI hosting company operating customer systems may fit cloud/MSP categories and require a group-size and jurisdiction review.
- A browser-only service with an added local file-sync agent needs a fresh CRA product review for the agent and necessary backend, even if the billing SKU remains “SaaS”.
- A supplier to a bank is not automatically a DORA-regulated financial entity or a designated critical ICT provider. The customer may nevertheless need contractual rights under DORA.

When facts are missing, state a provisional applicability result and collect the missing fact. Continue generally required security work; hold only decisions whose legal or technical basis remains unresolved.
