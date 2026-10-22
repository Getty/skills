# Sector and expansion boundaries

The collection provides a horizontal platform framework. Treat the following as specialist triggers, not fully implemented sector compliance. Do useful common engineering work while marking the additional review scope explicitly.

| Capability/customer context | Additional assessment | Engineering implication |
| --- | --- | --- |
| Diagnosis, treatment, clinical decisions | MDR/IVDR device qualification, intended purpose, health-professional duties and national rules | Separate wellness claims from medical intended use; assess clinical evidence, change control and health data before launch |
| Creditworthiness, insurance risk/pricing, trading/investment guidance | AI Act category, GDPR decisions, financial regulation; DORA for regulated entities and relevant ICT arrangements | Preserve decision reasons and human controls; do not assume a bank customer makes the SaaS vendor a financial entity |
| Hiring, allocation of work, performance/termination | AI Act, GDPR/employee privacy, national employment and equality rules | Assess works-council participation where applicable; avoid default employee surveillance dashboards |
| Education admission, grading, exam monitoring | AI Act intended use, minors, education law and accessibility | Separate administrative assistance from decisions about learners |
| Children or intimate companion services | Youth/media rules, consumer vulnerability, GDPR age/basis, AI prohibitions, DSA where applicable | Age-appropriate defaults, reporting and safeguards; do not collect ID universally without necessity |
| Public authorities or public procurement | Administrative law, procurement, accessibility, records, AI Act FRIA conditions | Validate responsible decision maker, explanation/appeal, retention and procurement promises |
| Identity, biometrics, emotion analysis | AI Act prohibitions/high-risk rules, GDPR special data, national restrictions | Review exact inference, context and affected groups; a notice does not cure a prohibited use |
| Payments, transferable credits, wallet, lending | PSD2/national payments law, e-money, credit rules, AML where triggered | Identify who holds funds and who owes the claim; involve regulated provider design before adding a wallet |
| Hosting marketplaces or selling third-party goods | DSA/P2B, marketplace consumer rules, product safety, VAT and seller obligations | Identify sellers and listing responsibility; separate own supplies from intermediation |
| Interpersonal communications or communications infrastructure | EECC/national telecom law, confidentiality and lawful orders | A chat feature needs functional assessment; do not assume all collaboration tools are telecom services |
| Qualified identity/signature or trust service claims | eIDAS and national supervision | Do not market qualified status without the necessary qualification |
| Physical products, autonomous control or robotics | Sector product safety, CRA, AI Act revised Annex I and liability law | Apply product-specific conformity and supply-chain review; software checks alone are insufficient |
| Exported dual-use functions or sanctioned markets | Applicable sanctions/export rules and exact product/end use | Treat country/service exposure as a screening input, not a universal geoblock instruction |

## Germany: workplace example

For an enterprise usage dashboard, determine whether it identifies employees and can monitor behaviour or performance. BDSG §26, GDPR and BetrVG §87(1)(6) may be relevant; employer/customer and platform roles still require separate assessment. Prefer purpose-limited aggregate service metrics by default and validate whether the employer has met applicable participation requirements. A customer administrator's technical permission is not proof of lawful surveillance.

## Sources and boundaries

Use current official texts: [MDR 2017/745](https://eur-lex.europa.eu/eli/reg/2017/745/oj/eng), [DORA 2022/2554](https://eur-lex.europa.eu/eli/reg/2022/2554/oj/eng), [GDPR](https://eur-lex.europa.eu/eli/reg/2016/679/oj/eng), [BetrVG §87](https://www.gesetze-im-internet.de/betrvg/__87.html), [BDSG §26](https://www.gesetze-im-internet.de/bdsg_2018/__26.html), [AGG](https://www.gesetze-im-internet.de/agg/), [eIDAS](https://eur-lex.europa.eu/eli/reg/2014/910/oj/eng). These are legal anchors to re-open for the actual product, not a claim that each sector was exhaustively reviewed on the snapshot date.

Do not certify a medical, financial or regulated public-sector deployment using this horizontal collection. Produce a concrete sector handoff with facts, architecture, intended use, data, vendor responsibilities and the unresolved specialised questions.
