# Secure development and software supply chain

## Map obligations to the delivery path

Use risk-based secure development under GDPR Article 32 and, where applicable, BSIG §30, Regulation 2024/2690 and CRA Annex I. Exact tooling choices below are engineering recommendations. Sources: SEC-GDPR, SEC-BSIG-CONTROLS, SEC-NIS-IR, SEC-CRA.

Map source repository, pull requests, CI workers, package/model registries, artifact signing, container registry, configuration delivery, secrets, infrastructure state, and deployment identities. Identify which actor can alter code, tests, dependencies, approval rules, build environment, and release artifacts. An agent able to edit both the implementation and the compliance gate must not silently mark its own exception as approved.

## Development controls

- Require review for materially privileged, data-processing, billing, tenancy, identity, and safety changes according to the established release policy.
- Use branch and environment protections where appropriate; separate contribution credentials from deployment credentials.
- Pin dependencies and model artifacts with verifiable versions/hashes; review lockfile and registry changes.
- Avoid privileged execution of untrusted pull requests, package scripts, model loaders, and generated code.
- Keep development/test data synthetic or lawfully minimized. Production-data access needs its own purpose and authorization.
- Use secrets scanning, dependency and container analysis, static/dynamic checks and targeted manual review for the actual risks; document what a tool cannot test.
- Treat infrastructure, consent routing, provider configuration, agent permissions and feature flags as reviewable code where practical.

## AI-specific supply-chain objects

Inventory model weights, adapters, tokenizers, prompt templates, tool specifications, retrieval parsers, embeddings, safety classifiers, inference engines, CUDA/container runtimes, and customer-provided plugins. Record origin, version, integrity mechanism, license/terms, update channel, execution behavior, and approval. Route licensing/training-data rights to the IP skill and supplier data handling to data-governance.

Untrusted serialization formats, remote code loaders, install hooks and conversion tools can execute code before inference starts. Evaluate and sandbox those steps. A download from a familiar model hub is not a provenance or safety guarantee. Preserve artifact hashes and an approved build manifest; do not log private repository credentials.

## Release evidence

For each release preserve a compact evidence bundle: commit/version, reproducible build identifiers where feasible, dependency/SBOM record, threat-model deltas, relevant test results, vulnerability decisions, configuration fingerprint, rollout/rollback plan, owner approval, and deployment observation. Sign or protect artifacts where proportionate and prevent an unreviewed artifact from replacing the reviewed one.

The evidence must distinguish `planned`, `implemented`, `tested`, and `observed in deployment`. A passing development test does not establish the production reverse proxy, IAM role, or provider setting is identical. Verify the material configuration after rollout without copying customer secrets into the evidence.

## Vulnerability triage

Map each advisory to affected artifacts and deployed products. Assess reachability, privilege, exploitability, active exploitation, tenant/customer exposure, compensating controls, fix feasibility, and reporting thresholds. Set severity and remediation due date using the owner's approved policy; there is no universal statutory “patch all critical CVEs within 24h” rule in this skill.

Preserve decisions not to patch immediately, including the reason and review date. A risk acceptance cannot excuse violating a binding requirement. Avoid dismissing a dependency because it is “only in the base image” or “not directly called” without evidence. Supply-chain compromise and an actively exploited vulnerability require incident assessment before an ordinary maintenance queue.

## Update pipeline and end of support

Test integrity validation, rollback/failure behavior, version compatibility, credential revocation, and rollback of both database and application changes. Never use customers as unannounced adversarial test subjects. For CRA products verify the support-period and user-information requirements under the applicable date and product class. End-of-support does not authorize deletion of required evidence or automatically end all reporting responsibilities.

## Release decision examples

- A new GitHub Action requests a write token for all repositories: review and narrow permissions before release.
- An agent disables failing tenancy tests: investigate the failure; do not count the now-green pipeline as evidence.
- A model update changes tool parameter interpretation: rerun permission and side-effect cases, not only answer-quality benchmarks.
- An SDK vulnerability exists but the impacted module is excluded from the shipped build: preserve the build evidence and reassess on dependency changes.
