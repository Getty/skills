# Roles and classification

## Identify the object and actor

Use AI Act Articles 2 and 3. Record whether the object is a model, a general-purpose model, an AI system using that model, or an integrated product. Determine who develops or has it developed and places it on the market/puts it into service under their name, and who uses it under their authority. An upstream model can have a different provider from a customer-facing application.

| Scenario | Analysis required |
| --- | --- |
| Branded chat application calling a third-party API | Assess provider status for the downstream system and the vendor's model role; do not automatically assign GPAI-model-provider duties to the wrapper |
| Company uses an off-the-shelf assistant internally | Assess deployer role and actual purpose; distinguish nonprofessional personal use |
| Platform fine-tunes an open model and publishes weights | Assess model and system provider roles, modification scope, market placement, licence and GPAI guidance |
| Customer converts a general assistant into applicant screening | Reassess intended purpose, high-risk status and Article 25 responsibility along the value chain |
| Reseller rebrands an existing high-risk system | Examine Article 25 and the contractual/cooperation consequences; commercial labels alone do not decide responsibility |
| Customer runs a local model with private RAG | Self-hosting changes data flows, not automatically all statutory roles or risk classification |

Assess AI Act roles separately from GDPR roles, copyright rights and product cybersecurity roles.

## Risk classification

Apply Article 5 first. Next consider Article 6(1): the exact product/safety-component conditions and applicable third-party conformity assessment under a currently listed Annex I act. The 2026 amendment added Article 6(1a)-(1c) clarifications and changed Annex I, including removing its previous machinery entry. Do not carry over a stale 'all machinery AI' mapping. Sector legislation can still regulate the product.

For Article 6(2), inspect the exact Annex III use cases: biometrics, critical infrastructure, education, employment, access to essential services, law enforcement, migration/borders and justice/democratic processes. A sector keyword is not enough; match the feature's intended purpose to the provision.

Article 6(3) contains a conditional exclusion for some Annex III systems that do not pose significant harm, including not materially influencing decision outcomes, and meet listed task conditions. An Annex III system profiling natural persons remains high-risk under that rule. Document the reasoning before reliance. Inspect the current Articles 6(4), 49 and 71 together for documentation/registration consequences; do not reuse an old checklist where the 2026 amendments changed the procedure.

## Evidence and changes

Capture intended-use statements, product UI and marketing, customer instructions, system architecture, input/output and actions, affected groups, model/version, distribution channel and launch date. Test how the product actually influences the decision. A human who routinely rubber-stamps a score is not meaningful evidence that the model has no material influence.

Reclassify when changing targets, purpose, autonomy, affected population, biometric inference, training, available tools, model or distribution. Distinguish a small software change from a legal substantial modification; record the analysis rather than relying only on a semantic version number.

Sources: AI Act Articles 2, 3, 6 and 25; current Annexes I and III. Official article links are in sources.md. Commission high-risk classification guidance found during research remained labelled draft on the accessible July 2026 page; verify final status before giving it additional authority.
