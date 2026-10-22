# RAG and customer content

## Design a permission-preserving pipeline

Carry source ownership, tenant, ACL, purpose, licence restrictions, provenance and lifecycle state into every derived representation. Enforce current user authorisation before retrieval and before export, not solely when the corpus was ingested. Shared caches, rerankers, logs, evaluation tools and external embeddings are additional disclosure surfaces.

Separate private customer retrieval from shared public knowledge and product improvement datasets. An enterprise DPA does not grant a copyright licence for the platform's own training; a broad content licence does not resolve controller/processor or employee-privacy obligations.

## Review source-to-output operations

| Stage | Review |
| --- | --- |
| Upload/connect | Is the user authorised to connect this source and grant the requested use? |
| OCR/parse/chunk | Are copies/transforms permitted and limited to the service purpose? |
| Embed/index | Which vendor receives data; can derived data leak material or identity? |
| Retrieve/rerank | Does the requester's current permission cover every source, including cross-project and inherited permissions? |
| Answer/snippet | Is reproduction/quotation justified; are attributions accurate where required? |
| Export/public share | Does the recipient/publication have rights beyond the private answer context? |
| Revoke/delete | Are links, cached chunks, embeddings, previews and downstream access revoked as required? |

## Quotation and answer controls

German UrhG §51 is a purpose-bound quotation exception, not a free fixed number of words. Assess the quotation purpose, necessary extent, publication status and source/author attribution requirements, including §63. Other countries' implementation and applicable rights must be checked. Do not invent a universal safe percentage.

Use documented output limits and reproduction detection as risk controls, not as declarations of legal permission. Test extraction attacks over repeated prompts, continuation requests, translated reproductions, cross-document assembly and requests for complete licensed texts. Verify that the user can still perform legitimate permitted uses under the actual contract.

## Customer-facing promises

Describe permitted purposes, vendor access, training choices, confidentiality and deletion truthfully. Do not promise 'never stored' when request bodies exist in logging/error tooling. Do not promise complete removal from already trained weights without a supported process. Coordinate exact contract language with product implementation and the business-contracts skill.

Acceptance cases: unauthorised user cannot retrieve an otherwise valid chunk; revoked document disappears from subsequent answers and shares; public sharing needs distinct permission; cross-tenant cache does not return a matching answer containing another tenant's text; attribution points to the actually used source; output filters do not merely hide a source URL while reproducing the full work.

Sources: UrhG §§16, 19a, 44b, 51, 63, 87a-87c and applicable licences; GDPR and trade-secret law are separate parallel assessments.
