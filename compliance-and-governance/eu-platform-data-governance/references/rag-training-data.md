# RAG, training, evaluation, and anonymity

Sources: D1, D8–D12. Distinguish legal requirements from suggested implementation methods.

## Separate the operations

| Operation | Key review |
| --- | --- |
| Ingestion and OCR/transcription | Source rights, third-party personal data, external processors, minimisation and provenance |
| Embedding and indexing | Provider disclosure, identifiable vectors/metadata, tenant isolation, update/delete lineage |
| Retrieval and reranking | Current user authority, permitted purpose, minimal context, tool/vendor recipients |
| Inference | Actual payload, session state, retention, provider use, output handling |
| Fine-tuning/training | Distinct purpose/basis, provenance, sensitive data, extraction risk, rights feasibility |
| Evaluation/red teaming | Test-data authority, access, purpose, retention, synthetic alternatives |
| Feedback/service improvement | Separate optional/necessary uses, actual reuse controls, notice and withdrawal/objection |

RAG does not rewrite or legalise a base model's training history. Retrieval can improve traceability and correction of the external knowledge source, but does not remove false outputs or model memorisation. An embedding endpoint is a real recipient even when the final LLM is local.

## Preserve lineage and authority

Store source document ID/version, content hash, tenant, classification, applicable ACL version, purpose, licence/provenance reference, ingest time, retention rule and derivative IDs. Keep originals separate from transformed representations. Avoid using a visible document title containing personal information as a global telemetry label.

Enforce source access at retrieval time, including changes after indexing. Prevent a stale embedding/summary from bypassing a revoked ACL. Apply restrictions before sending candidates to a reranker or model; output filtering does not undo a disclosure that already occurred. Partition caches by the relevant authorisation context and invalidate them when access or content changes.

Evaluate indirect disclosure through nearest-neighbour results, citations, metadata, autocomplete, error messages, batch exports and tool calls. Include adversarial synthetic queries, with named canaries, to test leakage across tenants and roles.

## Authorise each reuse

Document the service use and any training/evaluation reuse independently. A customer instruction to answer questions is not an instruction to improve a general platform model. Public availability is not a universal lawful basis or copyright licence. A platform-wide terms change does not by itself cure incompatible processing or absent Art 9 conditions.

Record the dataset sources, collection dates, licences, purposes/bases, restrictions, data subjects, sensitive-data screening, quality filters, transformations, provenance and retention. Quarantine uncertain sources before training. Keep customer-controlled data out of general training unless the relevant authorisation and lawfulness have been established.

For sensitive data used to detect/correct bias, assess amended AI Act Art 4a specifically, including strict necessity, alternatives, no other-party access/transmission, safeguards and early deletion. Do not treat it as permission for general model training or sending such data to a vendor.

## Assess anonymity with evidence

EDPB Opinion 28/2024 requires a case-specific assessment of whether personal data can reasonably be extracted from a model or obtained through interactions. Removing direct identifiers, hashing an email, producing a vector or calling data synthetic is insufficient proof of anonymity.

Record the recipient/threat context, reasonably likely means, auxiliary information, singling-out/linkage/inference risks, extraction/memorisation evaluation, mitigations and residual risk. A bounded test that finds no leak is not proof of zero risk. Reassess when model capabilities, public auxiliary data, recipients or access change. Treat the July 2026 anonymisation guidelines as consultation-draft material until a verified final version supersedes them.

Use reversible pseudonymisation with key separation where accountability/rights require linkage; describe it honestly. If relying on true anonymisation to leave GDPR scope, obtain a defensible assessment and avoid retaining practical reidentification capabilities.

## Rights and model changes

Deleting a training source does not establish deletion from weights. Output suppression, unlearning, retraining, quarantining a checkpoint or withdrawing a model are different measures with different residual risks. Determine the applicable right, technical effectiveness and proportionate legal response with the accountable owner; do not invent a general technical-impossibility exemption.

Prefer architectures with separate, updateable retrieval knowledge where that meets the product need and reduces rights complexity. This is an engineering tradeoff, not a legal requirement to use RAG. Preserve model/dataset versions so a corrected deployment can be related to the assessment and complaints that led to it.
