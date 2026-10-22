# Scope and country adapters

## Decision sequence

Record the supplier, the person contracting, actual intended use, targeted market, performance and consideration. The same natural person may buy for private purposes today and for their business tomorrow. In Germany use BGB §§ 13 and 14; do not decide from VAT status, company email, plan name or an unsupported checkbox alone. Preserve the minimum evidence needed to support a business-only transaction without collecting unnecessary identity documents.

Classify the promised performance independently of its technology. A hosted AI workspace that processes and stores user inputs is commonly a digital service. A downloadable model, file or generated asset can involve digital content. Human consulting delivered by email does not automatically become a digital service. Bundles need component-level analysis, including whether the components are contractually separable. BGB § 327 implements the digital-product framework and expressly includes certain personal-data-for-service arrangements; the scope exceptions are important. [C1, C2]

## Free offers and personal data

Trace what the operator receives and why it processes it. An email address needed only to deliver the service differs from a requirement that the user provide data for advertising or training. Determine whether the data is processed exclusively to perform the digital service or comply with law, and whether processing exceeds those purposes. Do not call all free accounts unregulated or describe personal data as owned merchandise. Consumer rights and GDPR legality are separate tests; satisfying one does not settle the other.

For a free trial record whether a paid contract already exists, whether the user has explicitly committed to future charges, and which cancellation or withdrawal route governs. For credits, record whether they are payment for a defined service, a voucher, refundable value, or a potentially regulated wallet. Route tax and payment licensing to billing-tax.

## Country adapter

Maintain one adapter per targeted country with:

| Field | Required evidence |
| --- | --- |
| Market targeting | Campaigns, supported delivery/service region, country selector, currency, language and actual customers |
| Contract law | Applicable law analysis; Rome I Article 6 consumer protection where its conditions apply |
| EU implementation | National provisions implementing Consumer Rights, Digital Content and Unfair Terms Directives |
| Local disclosures | Identity, contact, price, complaints, language and sector additions |
| Exit flows | National withdrawal implementation, cancellation and renewal rules |
| Capacity/minors | Contract capacity, guardian requirements and separate privacy age rules |
| Enforcement | Relevant authorities, courts and ADR route; verified addresses |
| Dates | Publication, entry into force, application, transition and contract-cohort cutoffs |

The German adapter is a completed reference baseline for the cited topics, not a default for every EU member. EEA incorporation and UK/Swiss rules require separate verification. Translation does not establish national compliance. [C3]

## Implementation decisions

Model an offer as `seller + market + customer_class + performance_type + consideration + contract_version`. Avoid a single global consumer flag that later changes all historical contracts. A move of residence or upgrade to a business workspace does not rewrite the original purchase facts. Keep invoices, entitlements and accepted terms linked to the original transaction.

Escalate meaningful uncertainty with alternatives: for example, offer a consumer-compliant purchase path while a business classification is checked. Do not deny mandatory rights while merely waiting for a company registration number. Document excluded markets only where the product actually enforces the restriction and the commercial operation matches it.
