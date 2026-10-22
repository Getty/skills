# Bias-related data and evaluations

## New Article 4a

The July 2026 amendment added Article 4a. Its paragraph 1 addresses strictly necessary special-category processing by high-risk providers for the specified bias detection/correction purpose. Paragraph 2 provides a conditional route for other AI systems/models and high-risk deployers where the specified likely harms or unlawful discrimination are involved. It does not itself impose a new obligation on all such actors to conduct bias detection/correction.

Do not present the former Article 10(5) provider-only framing as the complete current law. Do not infer broad permission to collect sensitive attributes for model training, analytics, profiling or unrelated fairness research.

## Require every condition

Before relying on Article 4a, document why other data, including anonymised or synthetic data, cannot effectively fulfil the purpose; technical reuse restrictions and state-of-the-art privacy/security measures; strict authorised access/confidentiality; the restriction against transmission, transfer or access by other parties; deletion after correction or the retention limit, whichever comes first; and the required necessity reasoning in processing records.

Coordinate the exact Article 6/9 GDPR analysis and Article 4a with the privacy owner. A third-party evaluation or remote model call involving these data can conflict with the Article 4a conditions. Do not upload them to a vendor merely because that vendor signed a DPA. Analyse whether another valid legal route exists instead of weakening the condition.

## Evaluation design

Define a real product question: e.g. whether a retrieval feature exposes cross-tenant documents, whether an assistant misleads users about decisions, or whether a classifier's error distribution disadvantages an affected group. Use a documented intended task, population, coverage, labels, sample limits and decision criteria.

Use lawful synthetic tests when they can establish the property. Use appropriate controlled data only when justified. Keep benchmark/test data separated from model training and do not leak production prompts into public evaluation tools. A lawful access basis for serving a customer is not automatically a basis for reusing their content to improve the service.

Measure errors and uncertainty as well as success. Include adversarial prompts, long inputs, language variants, accessibility surfaces, rare conditions, model fallback and version changes. Choose metrics for actual harm and intended use; generic leaderboard scores are not conformity evidence.

## Evidence

Keep test design, data provenance, permitted purpose, model/system version, code/parameters, outputs or redacted summaries, known limits, reviewer and remediation. Minimise individual-level records. Describe what the experiment can and cannot establish. Preserve lawful deletion and access controls for the evaluation evidence itself.

Sources: [Article 4a current text](https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-4a), Articles 9, 10 and 15; GDPR Articles 5, 6, 9, 25, 32 and 35. The experimental workflow is an engineering method, not a statutory universal benchmark specification.
