---
name: eu-platform-cybersecurity
description: "Use when designing or reviewing security of an EU AI platform — tenant isolation, agent tools, RAG, supply chain, vulnerability handling, shipping a desktop app, client, agent or self-hosted edition (CRA), NIS2/BSIG scope, or a security incident with a reporting deadline."
---

# EU Platform Cybersecurity

Translate applicable security duties into engineering controls and verifiable operational evidence.
Use EU rules as the common layer and select the law of the relevant Member State for national duties.
Treat 2026-10-22 as this package's research snapshot, not as a permanent statement of current law.

## Start with scope

1. Identify the operating legal entity, service lines, establishments, target countries, customers, headcount, group structure, revenue, and balance sheet.
2. Identify downloadable software, apps, browser extensions, CLI clients, on-premises packages, appliances, and their necessary remote processing.
3. Identify the actual data-controller/processor roles for each flow and the scope of the authorized security review.
4. Read [scope-and-country-adapter.md](references/scope-and-country-adapter.md), then [sources.md](references/sources.md).
5. Record applicability as `applicable`, `not_applicable`, `unknown`, or `future`. Give reasons and evidence. Do not convert an unknown into an exemption.

Never infer NIS2 coverage merely from using cloud infrastructure or offering AI.
Never infer CRA exclusion merely from the commercial label “SaaS”.
Do not treat a certification, vendor questionnaire, or successful scan as proof that all statutory duties are satisfied.

## Route the work

| Task | Read |
|---|---|
| New market, company size, cloud/MSP role | [scope-and-country-adapter.md](references/scope-and-country-adapter.md) |
| German NIS2 scope, registration, management duties | [nis2-german-overlay.md](references/nis2-german-overlay.md) |
| Distributed app, agent, extension, appliance, self-hosted edition | [cra-product-security.md](references/cra-product-security.md) |
| Breach, exploited vulnerability, availability incident | [incident-clocks.md](references/incident-clocks.md) immediately |
| Agent tools, model gateway, RAG, cross-tenant access | [secure-ai-architecture.md](references/secure-ai-architecture.md) |
| Dependencies, build chain, updates, release | [development-supply-chain.md](references/development-supply-chain.md) |
| Production, backup, logging, support, suppliers | [operations-and-vendors.md](references/operations-and-vendors.md) |
| Test design, evidence, release decision | [security-verification.md](references/security-verification.md) |
| Financial, healthcare, public-sector, critical customers | [regulated-customer-screening.md](references/regulated-customer-screening.md) |

## Work from facts to a control decision

### 1. Establish the boundary

Draw the paths from user input to model, retrieval, tools, memory, logs, exports, support access, and subprocessors.
Record the authenticated principal and tenant at every boundary.
Distinguish platform administration from customer administration and user-delegated actions.
List entry points that bypass the main UI: API, webhooks, jobs, mobile, SDK, support tooling, and backups.

### 2. Determine obligations

Map each requirement to its legal basis, applicability facts, application date, and owner.
Separate legal requirements, contractual promises, voluntary standards, and engineering recommendations.
Refresh live sources before a launch decision, regulator notification, new classification, or time-critical change.
Use the German overlay only where Germany is the appropriate jurisdiction.
Keep proposed amendments separate from law already published and applicable.

### 3. Implement proportionate controls

Create a threat model and control register using [security-control-register.json](assets/security-control-register.json).
Prioritize unauthorized access, cross-tenant disclosure, uncontrolled tool actions, compromised builds, unavailable recovery, and missing incident escalation.
Make authorization decisions in deterministic application controls outside the model.
Use synthetic data and an isolated environment for destructive or adversarial tests.
Implement already-authorized reversible fixes; do not silently broaden an authorized test into third-party testing or production disruption.

### 4. Gather evidence

Attach code/configuration locations, environment and artifact versions, test results, review date, owner, and residual risk.
Mark evidence `verified`, `missing`, `stale`, or `not_tested` independently of legal applicability.
Retain failed tests and remediation history; do not replace failure evidence with a narrative assertion.
Use [security-review.md](assets/security-review.md) for a release review.
Use [product-security-file.md](assets/product-security-file.md) for a CRA product file.

### 5. Handle incidents separately

Start [incident-record.json](assets/incident-record.json) on credible detection.
Record detection time and the separate legal awareness/receipt times; preserve uncertainty without resetting clocks.
Assess GDPR, NIS2/BSIG, CRA, sector, and contractual duties independently.
Page the designated incident lead immediately when a reporting threshold or deadline may apply.
Prepare accurate staged notices; an investigation need not be complete before an initial notice is due.
Submit messages, disclose customer data, or contact authorities only under the user's actual authorization and the organization's delegated incident procedure.
Do not let a missing authorization disappear into a backlog: expose the next deadline and the specific action required now.

## Release and monitoring rules

- Reassess on a new tool permission, data source, tenant model, model/provider, region, remote support route, downloadable component, or supplier.
- Reassess NIS2 on service-line and group-size changes; reassess CRA on product changes, branding, distribution, and substantial modifications.
- Block the affected release when a demonstrated severe exposure remains uncontrolled, an applicable mandatory prerequisite is absent, or evidence needed for a high-impact decision is unavailable.
- Limit a block to the affected feature or deployment where isolation is technically sound. State the dependency and release condition.
- Let the accountable owner decide residual business risk; do not describe a risk acceptance as a waiver of law.
- Configure recurring checks only when requested or already authorized. Writing this skill does not start monitoring.

## Required output

Return a concise decision followed by a table containing:

`finding_id | service/asset | requirement and source | applicability | observed evidence | severity | action | owner | deadline | verification`

Include the assessed version and environment, facts still missing, relevant legal dates, and the next smallest safe implementation step.
State whether a result is a local test, a document review, or a production observation.
Use measured findings; do not claim the platform is “GDPR/NIS2/CRA certified” from this workflow.

## Coordinate with the suite

Use `eu-platform-privacy` for personal-data roles and rights, `eu-platform-data-governance` for deletion/transfers, `eu-ai-act` for AI-system duties, and `eu-platform-agent-assurance` for the shared release evidence process.
Use `eu-platform-content-safety` for government orders and unlawful-content procedures.
If a sibling skill is absent, continue the controls covered here and flag the missing specialist review explicitly.
