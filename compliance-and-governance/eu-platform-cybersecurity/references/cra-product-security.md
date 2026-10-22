# CRA product security for AI software

## Application and boundaries

The CRA concerns products with digital elements, including separately supplied components and necessary remote data processing. Inspect Articles 2–3, relevant exclusions, economic-operator roles, and the product's technical/commercial reality. Source: SEC-CRA; explanatory support: SEC-CRA-GUIDANCE.

Do not mark every cloud service as a CRA product. Do not mark every cloud service outside the CRA either. A distributed AI desktop agent, mobile app, extension, CLI, on-premises edition, or appliance can make a product review necessary; the backend it needs can be part of that review. Map the components, manufacturer's responsibility, functions, market distribution, and backend dependency. A model file or library needs its own facts; “AI” is not an exemption.

Distinguish manufacturer, importer, distributor, authorized representative, substantial modifier, and open-source software steward. A commercial product can embed open source while its manufacturer remains responsible. Donation-funded/noncommercial development and systematic stewardship need the actual legal tests, not a license-name shortcut. An individual contributor is not automatically a manufacturer or steward.

## Dates to preserve

| Date | Scope |
|---|---|
| 2024-12-10 | Entry into force |
| 2026-06-11 | Chapter IV notification of conformity-assessment bodies |
| 2026-09-11 | Article 14 manufacturer reporting applies |
| 2027-12-11 | Main application date; Article 24(3) steward reporting also becomes applicable |

Source: CRA Article 71; SEC-CRA-TIMELINE, SEC-CRA-SUMMARY, SEC-SRP-FAQ. Do not invent an August 2026 CRA deadline. Distinguish dates for amendments and sector instruments from these dates.

Apply Article 69 transition rules to existing products and substantial modifications. Article 14 reporting is not generally postponed for installed products until 2027. Check the applicable obligation separately from the product's conformity transition; support-period or end-of-sale labels are not automatic reporting exemptions. Record placing-on-market dates and version history.

## Build the product file

Use [product-security-file.md](../assets/product-security-file.md). Maintain:

1. Product identity/version, manufacturer and supply-chain roles, intended/foreseeable use, users, and interfaces.
2. Scope decision and exclusions; functions that depend on remote processing; classification under applicable product categories and current implementing acts.
3. Cybersecurity risk assessment over the expected product lifetime, threat assumptions, requirement mapping, and supporting technical documentation.
4. Security architecture, shipped defaults, access control, data minimization, confidentiality/integrity/availability measures, attack-surface reduction, and secure updates.
5. Vulnerability handling, machine-readable component inventory/SBOM, coordinated disclosure, security contact, fixes and affected-version analysis.
6. Support-period determination, end date disclosed to users, update availability, and end-of-support communication.
7. Conformity-assessment route, evidence and required declarations/markings when applicable; do not apply CE merely because documentation exists.
8. Monitoring, reporting, corrective-action and supply-chain communication records.

Map mandatory requirements to CRA Articles 13, 32 and Annexes I/VII after checking the currently applicable date and product category. Treat the detailed implementation recommendations below as a means to meet risks, not a claim that a particular tool is legally mandatory.

## Support and vulnerability process

Determine the expected period of use from reasonable user expectations, product purpose, components, and relevant law. The general support floor is five years unless expected use is shorter; five years is not a universal maximum or automatically sufficient for a long-lived industrial product. Verify the current Article 13 wording and applicable category guidance before promising a term.

Keep a machine-readable dependency record for shipped artifacts, including compiled libraries, operating-system layers, model-serving components, browser runtimes, and bundled update clients. CRA's SBOM requirement does not itself mean every SBOM must be publicly posted. Decide recipient, sensitivity, format, and update obligations explicitly. Track transitive dependencies operationally even where the statutory minimum is narrower.

Bind each vulnerability to product/version, exploitability, exposure, known exploitation, downstream impact, mitigation, patch and disclosure. Do not equate any CVE with a reportable actively exploited vulnerability. Do not wait for a CVE to exist before evaluating credible exploitation. A high CVSS score and a severe incident are different facts.

Verify signed updates, rollback protection where appropriate, tamper checks, safe failure, compatibility, and restoration. Test a compromised update feed and expired signing key using synthetic fixtures. Keep vulnerability notifications free from unnecessary customer secrets.

## Reporting and standards

Read [incident-clocks.md](incident-clocks.md) for exact awareness and final-report triggers. ENISA's live SRP currently serves mandatory manufacturer reports; do not assume all voluntary/steward functions are available before their stated date. Do not submit a test report to the production service.

Commission guidance C(2026) 5252 was adopted on 2026-07-27; older March consultation drafts are historical. Guidance is nonbinding. A standard gives the relevant presumption only when its version and reference have the required Official Journal status and the requirement is within scope; “ISO compliant” or “OWASP checked” alone is not CRA conformity. Record current harmonized standards, common specifications, category acts, and conformity route when the product decision is made.

## Reassessment triggers

New installable client; redistributed component; branding change; open-source commercialization; material architecture/backend change; change of intended purpose; vulnerability that invalidates a risk assumption; support-policy change; substantial modification; new category act or harmonized standard. A CRA review does not replace AI Act conformity or GDPR duties for the same product.
