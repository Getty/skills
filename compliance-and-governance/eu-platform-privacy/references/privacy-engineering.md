# Privacy engineering and verification

Sources: GDPR Arts 5, 24–25, 28 and 32 (P1); DSK lifecycle controls (P10). The concrete tests below are engineering methods, not a statutory certification checklist.

## Translate principles into verifiable invariants

| Principle/control | Implementation invariant | Useful evidence |
| --- | --- | --- |
| Purpose limitation | Content approved for customer inference cannot enter a general training/evaluation job without a separately approved purpose | Pipeline provenance, service identities, policy tests |
| Data minimisation | Send only necessary fields/chunks; exclude secrets and unrelated tenant data | Captured synthetic provider request, schema allowlist |
| Privacy by default | New accounts have conservative sharing/logging settings; public links require an explicit action | Fresh-account test and configuration diff |
| Confidentiality | Identity, tenant, document ACL and purpose constraints survive retrieval, reranking, tools and output caches | Cross-tenant and revoked-access tests |
| Accuracy | Record source/version and distinguish model inference from verified facts about people | Provenance metadata, correction workflow |
| Storage limitation | Every class has a purposeful schedule and deletion owner; retention is enforced | Expiry tests, deletion job outcomes |
| Accountability | Link the release to processing decisions and bounded evidence | Review packet tied to commit/configuration |

## Inspect the complete AI request path

Review browser/mobile SDKs, API gateway, authentication, input processing, object stores, OCR/transcription, embedding service, vector/keyword indexes, reranker, LLM, agent tool calls, outputs, feedback, tracing and support systems. A local LLM does not imply local OCR, embeddings, error telemetry or support.

Keep tenant/security filters outside the prompt as authoritative enforcement. A system instruction telling the model not to reveal other users' records is not access control. Apply ACLs before disclosure to rerankers or model vendors, not only after generation. Avoid globally shared semantic caches that reveal another tenant's content.

Treat externally retrieved material as untrusted. Test whether prompt injection can cause exfiltration to tools, logs, webhooks or third-party endpoints. Apply scoped credentials, permitted destinations, independent action checks and purpose-aware redaction. Keep the security rationale distinct from the lawful-basis decision.

## Observability without uncontrolled reuse

Default to metadata sufficient for reliability/cost/security rather than full prompt bodies. Separate security logging, debugging, quality evaluation and product analytics; they have different purposes and retention needs. Avoid secrets and sensitive data in exception messages, URL query strings, labels, tracing baggage, screenshots and session replays.

Where temporary content capture is necessary, specify authorised people, tenant/data scope, trigger, end time, retention, legal basis, notice implications and redaction. A debug flag that remains on after the incident is a material privacy change.

Use approved synthetic or appropriately de-identified fixtures in CI and evaluation. Replacing names with IDs is usually pseudonymisation, not proof that test data is anonymous. Keep real production data out of third-party coding agents unless that path has been assessed and authorised.

## Meaningful test set

1. Create two synthetic tenants with distinct canary records. Attempt direct IDs, semantic queries, shared links, search, export and tool actions across the boundary.
2. Revoke document access and retest retrieval, caches, conversations and generated summaries; determine which already-disclosed copies cannot be recalled.
3. Delete a synthetic subject's data and verify source, derived stores, queues and vendor requests, including a controlled restore scenario.
4. Request access/rectification/restriction through ordinary support and verify routing, scope and clock handling.
5. Toggle vendor model/region/logging controls and inspect actual synthetic requests and effective configuration.
6. Exercise an adverse consequential decision and demonstrate meaningful explanation, contestation and authorised human intervention.

Do not scan live customer data just to generate proof. Limit tests to the affected feature and concrete remaining risks. A passing test establishes tested behaviour under stated conditions, not the absence of all privacy risk.

## Release and operation

Distinguish a control gap from an uncertain legal determination. For a confirmed cross-tenant disclosure or unapproved new data use, contain the affected path using the authorised incident/release process. For a missing document, obtain actual evidence rather than synthesising a record that claims a test happened.

Record remediation, test evidence, residual risk, decision owner and review trigger. Recheck controls after model/provider updates, access-policy changes, new connectors, logging changes and restore/migration operations. Monitor failed erasure jobs, access denials, unusual export volumes, rights deadlines and retention overruns using proportionate metadata.
