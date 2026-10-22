# Regulated customer and activity screening

## Distinguish three reasons for extra controls

1. The platform operator itself conducts regulated activity or is expressly designated.
2. A customer is regulated and must impose controls on its suppliers.
3. A buyer voluntarily requires a standard in procurement or contract.

Record which reason applies. Neither a customer's sector nor a contract turns every supplier into the same regulated entity. Conversely, outsourcing does not relieve the regulated customer of its duties. This reference is a routing screen; it does not supply full sector authorization advice.

## Routing table

| Feature/customer | Next review | Engineering evidence to collect |
|---|---|---|
| EU financial institution | DORA Articles 28–30 contracts; actual critical ICT designation separately | Service dependency, locations, subcontractors, incident assistance, audit/access, exit feasibility |
| Healthcare/medical use | GDPR special categories, secrecy, medical-device qualification, sector IT and national health rules | Intended purpose, claims, clinical decision role, health-data flows, availability and validation |
| Recruitment/workplace monitoring | AI Act classification/prohibitions, GDPR/employee law, works council | Human decision role, purpose, access, monitoring scope, bias/error evidence |
| Critical infrastructure/public administration | National NIS2/critical-entity and procurement requirements | Entity designation, service criticality, recovery, assurance, clearance/access, sovereign constraints |
| Payment, stored-value wallet, credit or investment decisions | Payments/financial licensing and consumer/AI rules | Money flow, account ownership, custody, decision effect, outsourcing model |
| School/children's institution | Minors, national education/public-sector law, child-safe design | Age groups, authority of customer, parent/student notices, unnecessary monitoring, human support |
| Telecom or interpersonal communications | Sector privacy/security and communications obligations | Service function, confidentiality, metadata, lawful-request route |
| Industrial control/device agent | CRA, product safety, relevant sector product law and AI Act | Physical effects, fail-safe behavior, control authority, update lifecycle |

Source for DORA: SEC-DORA. For other sectors, this table identifies research triggers, not a complete statement of obligations. Retrieve the actual national and EU primary instruments before a substantive conclusion. Route to `eu-ai-act`, privacy, content safety, business contracts and the relevant specialist.

## Financial-customer precision

An AI supplier should inspect whether its ICT service supports a critical or important function and which DORA contractual clauses apply to that relationship. Distinguish ordinary ICT supplier obligations accepted by contract from the oversight framework for critical ICT third-party providers designated under Article 31. DORA applies from 2025-01-17; a bank's request for a DORA annex is not proof of supplier designation.

Prepare accurate service and subcontracting facts, incident-assistance capability, access/audit arrangements, data return, termination/exit, and recovery tests. Do not sign a promise to permit a customer audit or regulator access that conflicts with the underlying provider contract without resolving it.

## Specialist handoff

Provide intended purpose, marketing claims, users/countries, data categories, decision/action consequences, customer role, contract, deployment topology, source version, disputed issue, and proposed limited rollout. Ask the reviewer to resolve the specific qualification. Continue general security engineering and safe prototypes while the specialized legal route is assessed.

Use the narrowest real product boundary. Disabling a medical-diagnosis feature can allow a generic drafting feature to proceed only if the claims, interface, permissions and foreseeable use support that separation; a disclaimer alone does not change what the system actually does.
