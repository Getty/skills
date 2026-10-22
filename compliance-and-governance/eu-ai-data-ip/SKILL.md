---
name: eu-ai-data-ip
description: "Use when onboarding a dataset or model, scraping or crawling for AI, fine-tuning, building RAG over third-party content, reviewing a model or software licence, deciding who owns AI output, or handling a copyright or rights-holder complaint — TDM exception, UrhG, trade secrets."
---

# EU AI Data and IP

Establish the rights needed for each actual use of each asset. Do not infer a licence from public availability, an uploader checkbox, a model card or a vendor's general marketing claim. Work in English and retain precise national terms. Research snapshot: 2026-10-22.

## Rights analysis workflow

1. Identify the asset, source, owner/licensor, collection date/version, intended operations, markets, users and downstream recipients.
2. Decompose operations: acquire, copy, OCR, store, embed, index, retrieve, quote, train, fine-tune, evaluate, distribute, generate and publish. They do not necessarily share one permission.
3. Check copyright/related rights, database rights, software/model licence, contract/access terms, trade secrets, personal data, personality/likeness and trademarks where relevant. A GDPR lawful basis does not clear copyright, and a copyright licence does not clear personal data.
4. For each required right, record explicit licence, valid statutory exception or other grounded justification. Record unverified assumptions. Assess national implementation rather than applying US fair use as a global answer.
5. For text and data mining, inspect DSM Directive Articles 3/4 and national implementation. In Germany examine UrhG §§44b, 60d and 87c. Distinguish commercial/general TDM from eligible scientific research and rights-reservation conditions.
6. Inspect model/API/software terms for hosting, commercial use, redistribution, fine-tuning, distillation, derived models, use restrictions and downstream notices. Use the exact product/version terms.
7. Implement provenance, access boundaries, output safeguards, revocation and incident workflows. Verify negative cases and copied/derived data.
8. Produce a rights decision with source, purpose, permitted/prohibited acts, constraints, uncertainty, owner and renewal/review trigger.

Use [asset-rights-record.json](assets/asset-rights-record.json) and [rights-review.md](assets/rights-review.md). Empty or unknown permissions are not an approval.

## Critical boundaries

- A mining exception is not a general permission to publish the source or output substantial protected expression.
- Research affiliation does not automatically qualify a commercial platform for the scientific TDM exception.
- Open code, open weights, open data and an open-source AI Act exception are different concepts.
- Attribution is not permission. A fixed word/percentage threshold does not determine infringement or lawful quotation.
- A model output is not automatically exclusively owned, protectable, noninfringing or free of third-party rights.
- Removing a source file does not necessarily remove cached chunks, embeddings, evaluations or trained influences. Make the remediation claim match what can actually be demonstrated.

## Engineering controls

Tie every corpus item and model version to a rights/provenance record. Preserve source ACLs at retrieval time, including shared-link and export paths. Store permissions as purpose-specific constraints, not a single `is_public` flag. Separate customer private RAG from global training and cross-tenant retrieval.

For output features, review material reproduction, source attribution where required, database extraction, likeness/voice, marks, confidential facts and legal promises. Use tests with authorised fixtures. Do not retain prohibited content or distribute customer materials merely to create evidence.

## Decisions and escalation

Continue authorised ingestion of clearly permitted assets. Quarantine the specific asset/use with missing rights rather than declaring the whole platform unusable. Obtain targeted specialist review for contested TDM scope, rights reservations, litigation-sensitive datasets, model licence conflicts, substantial reproduction, personality rights and exclusivity promises.

Prepare a rights-holder response or takedown decision for authorised review; do not contact people, concede liability, sign licences or publish statements without the relevant authority. Preserve evidence proportionately and honour legitimate holds without leaving the material broadly available.

## Load references

- [rights-and-provenance.md](references/rights-and-provenance.md): layered rights and data records.
- [tdm-and-web-ingestion.md](references/tdm-and-web-ingestion.md): statutory exceptions, research limits and web access.
- [rag-and-customer-content.md](references/rag-and-customer-content.md): retrieval, snippets and tenant boundaries.
- [model-and-software-licences.md](references/model-and-software-licences.md): supply-chain permissions and distribution.
- [outputs-and-personality.md](references/outputs-and-personality.md): human creativity, reproduction and public claims.
- [rights-incidents.md](references/rights-incidents.md): complaints, withdrawal and downstream remediation.
- [sources.md](references/sources.md): official legal anchors and verification limits.

Route AI Act GPAI copyright-policy/summary duties to `eu-ai-act`, personal data to `eu-platform-privacy`, lifecycle/transfers to `eu-platform-data-governance`, and intermediary notice duties to `eu-platform-content-safety`.
