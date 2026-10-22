# Scope, functional roles, and lawful bases

Sources: P1–P5, P8–P9, P15 in `sources.md`.

## Start from operations, not the product label

Map personal data through signup, billing, corporate directories, prompts, uploads, retrieval, embeddings, inference, agent tools, outputs, feedback, observability, moderation, support, and training. An email address belonging to a business contact can be personal data. Information inferred about a person can be personal data even if wrong. Pseudonymisation reduces risk but normally does not remove the GDPR where identification remains reasonably possible.

Check material and territorial scope under Arts 2–3. Record establishments, targeting/monitoring of people in the Union, and which entity determines purposes. Do not use customer nationality alone. Review Art 27 representation for an in-scope non-EU controller/processor, including exceptions, and identify competent authorities rather than assuming the hosting country decides jurisdiction.

## Role matrix

| Operation | Candidate allocation | Evidence needed |
| --- | --- | --- |
| Platform accounts, own billing, own fraud controls | Platform often controller | Actual purposes, decisions, recipients, legal duties |
| Enterprise employee documents processed only on instructions | Customer controller; platform processor | Instructions, scope, access decisions, contract and runtime settings |
| Independent training from customer prompts | Potential separate platform/vendor controller purpose | Specific authorisation, legal basis, notice, role reassessment; Art 28(10) implications |
| Parties jointly determine collection and intended uses | Potential joint controllers for that operation | Joint influence, Art 26 allocation and essence made available |
| Infrastructure/AI vendor on documented instructions | Processor/subprocessor candidate | Product terms, technical practices, support, retention and reuse |
| User tool sends data to another service | Separate recipient/processing operation | Principal, authorisation, purpose, role, recipients, transfer |

A company may hold different roles simultaneously. Contract headings do not decide the role. A supplier's own legal/security duties require a precise analysis; do not classify every incidental security operation automatically as separate controllership or processing.

## Build a purpose–basis table

For each purpose, specify the data, subject, necessity, basis, recipients, duration, notice and rights. Keep an additional Art 9 condition and Art 10 authority separate from the Art 6 basis.

- **Contract, Art 6(1)(b):** show objective necessity to perform a contract with the data subject or requested pre-contractual steps. Do not extend a corporate customer's contract to all its employees or third parties. Optional behavioural advertising and generic future model improvement are not made necessary by inserting them into terms.
- **Legal obligation, Art 6(1)(c):** identify the concrete Union/member-state obligation. A customer contract or a vague reference to compliance is not enough. Keep only the records that duty requires.
- **Legitimate interests, Art 6(1)(f):** document the specific legitimate interest, necessity including less intrusive options, and balancing with reasonable expectations and impacts. Evaluate children and vulnerable groups explicitly. Implement the safeguards and objection route used in the balancing. Do not assume a right to scrape all public data.
- **Consent, Art 6(1)(a):** document choice, purpose specificity, clear information, positive action, and proof. Make withdrawal practical and as easy as giving consent. Assess power imbalance and detriment before bundling consent with access. Withdrawal does not retrospectively invalidate prior lawful processing but ends future consent-dependent use.
- **Public task/vital interests:** use only where the actual legal conditions fit; ordinary commercial SaaS should not invent public-interest authority.

For further processing, test purpose compatibility where applicable under Art 6(4); assess the applicable basis and safeguards. A processor cannot independently use the customer's instruction as permission for a new controller purpose.

## Sensitive and criminal-offence data

Identify Art 9 categories and inferences rather than matching only obvious column names. A photograph or voice recording is not automatically special-category biometric data; the technical processing and purpose of unique identification matter. Health or political information can be present in ordinary chat text and documents.

For Art 9 processing identify a valid exception and its conditions. Ordinary legitimate interests alone do not overcome Art 9. For Art 10 data verify the required official authority or authorisation in Union/member-state law and safeguards. Do not collapse Art 9 and Art 10 into a single checkbox.

**AI bias exception:** the amended AI Act's Art 4a must be assessed specifically. It is not a blanket training basis. Apply strict necessity, inadequate alternatives including synthetic/anonymised data, technical reuse limits, state-of-the-art protection, documented authorised access, the restriction on access/transmission to other parties, early deletion, and necessity records. Paragraph 2 additionally ties other providers/deployers to relevant likely harms/discrimination and does not create a general duty to process sensitive data. Route the exact applicability and effective-law decision to the AI Act workflow and a responsible specialist; do not assume a third-party LLM API can receive such data under this exception.

## Children, employees, and non-user data

Art 8 applies to consent-based information-society services offered directly to a child; it is not a universal age limit for all processing or contractual capacity. Verify the member-state age within the GDPR range and reasonable efforts for parental authorisation where needed. In Germany the GDPR's 16-year default applies unless a relevant specific rule changes the analysis. Avoid collecting full identity documents merely to avoid making an age-assurance design decision.

Employee monitoring and recruitment require the national employment overlay and works-council/collective rights where applicable. German BDSG §26 is a specific legal route requiring necessity and attention to EU-law constraints; it is not a broad permission to rank workers. Employee consent requires a real voluntariness assessment.

When users upload information about other people, record the customer's/platform's role, indirect-collection notice obligations, likely harms and permitted use. A checkbox that the uploader has all permissions does not replace the platform's own duties.

## Decision checks

Stop the affected new processing where no viable basis is identified. Continue synthetic implementation, data-flow mapping, and deletion/minimisation work. Resolve uncertain sensitive-data use, incompatible purposes, role disputes or large-scale reuse with the accountable privacy owner before enabling it. Record assumptions and recheck them when the data actually processed differs from the design.
