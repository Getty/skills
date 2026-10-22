# Secure AI architecture and tenant boundaries

These are risk-based engineering controls. Map their necessity and chosen implementation to the applicable legal and contractual duties. Sources: SEC-GDPR, SEC-BSIG-CONTROLS, SEC-NIS-IR, SEC-CRA; technical risk catalogue: SEC-OWASP.

## Trust boundaries

Treat user prompts, uploaded files, OCR text, web pages, retrieved chunks, tool responses, plugins, model output, and stored memory as untrusted data. Their natural-language content cannot grant permissions or change the system's authority. Treat model output as a proposal until validated by the application. A prompt telling the model “never leak secrets” does not enforce access control.

For every operation bind `actor -> tenant -> delegated scope -> object -> action -> destination -> current authorization`. Authenticate once at the boundary and recheck authorization at execution, including after delays and retries. Do not authorize by an object identifier provided by the model or by a tenant ID supplied in a request body.

## Retrieval and storage

| Surface | Implementation objective | Evidence |
|---|---|---|
| Document ingestion | Record owner, tenant, ACL, provenance, file type/size; isolate parsers and reject unsafe formats | Ingestion permission tests and sandbox configuration |
| Vector/full-text retrieval | Apply effective user/object ACL before content enters model context; maintain ACL changes and deletions | Cross-tenant and revoked-access tests at each retrieval path |
| Reranking and embedding | Send only authorized/minimized content to approved provider/region | Provider route traces and payload sampling with synthetic data |
| Caches | Partition by relevant tenant/principal/permission/model/context inputs; invalidate on privilege change | Cache collision and access-revocation tests |
| Citations/downloads | Reauthorize original object access; constrain signed URL scope and lifetime | Link-sharing and expired/revoked-token tests |
| Jobs/exports | Preserve initiating principal and current permission checks; prevent path/URL substitution | Delayed-job, replay and role-change tests |
| Memory | Namespace by tenant/user/workspace; provenance and deletion propagation | Poisoned-memory and cross-session leak tests |

Separate shared system knowledge from customer data. An embedding is not automatically anonymous. Do not copy data from private workspaces into shared “optimization” corpora. Security logs should generally store references and minimized diagnostics rather than full prompts, tokens, and documents.

## Tool execution

Keep a tool registry with explicit input schema, allowed operations, principal, credential scope, egress destinations, side effects, rollback, and maximum resource use. Apply least privilege and short-lived credentials. Keep secrets in a broker/secret store instead of prompt text. A model may select a tool, but an application policy engine decides whether this actor may execute this action against this object and destination.

Use independent approval or policy conditions for high-impact actions appropriate to the actual task: sending externally, changing money, destructive operations, privilege elevation, deployment, and disclosure. Honor previously authorized scopes; do not ask again for every routine action. Bind approval to exact parameters, recipient, amount/object, scope, and freshness so a later model step cannot change them unnoticed. Protect against time-of-check/time-of-use changes.

Block arbitrary shell/database access by default in end-user agents. Where the product explicitly supplies code execution, isolate the process, filesystem, credentials, network, CPU/RAM, time, and tenant. A container is one boundary, not a complete tenancy design. Deny cloud metadata endpoints and internal administrative networks unless explicitly required and authorized. Validate URL redirects, DNS resolution, webhook destinations, and artifact paths against SSRF/path traversal.

## Output handling

Encode or sanitize output for its eventual sink: HTML, Markdown, SQL, shell, email, URLs, JSON, and file names have different rules. Do not execute model-generated commands directly or assume JSON schema validation makes business intent authorized. Validate numbers, currency, identifiers, row/column access, allowed operations, and idempotency before side effects.

Prevent model-controlled images or links from exfiltrating hidden context through automatic fetches. Use a restrictive browser policy for rendered output, explicit remote-resource handling, safe attachment scanning, and appropriate content security policy. Do not log secrets exposed during a failed safety test into a wider observability service.

## Model and connector changes

Treat model/provider changes as security changes when tool-calling behavior, context size, prompt format, safety filtering, logging, or data location changes. Record approved versions and fallback routes. A fallback must not silently bypass a no-training commitment, tenant contract, region restriction, or tool boundary. Exercise the fallback path in tests.

Disable a compromised connector independently from the whole platform. Provide kill switches and revocation that work when the model service is unavailable. Apply quotas and circuit breakers to recursive tool use, token generation, file ingestion, and paid APIs; test cancellation and cleanup. Resource limits protect availability and cost, but cannot replace integrity or privacy controls.

## Defensive tests

Run only within the authorized test environment, with synthetic canary secrets and isolated tenants. Test a retrieved document claiming to be an administrator, a tool result requesting an external upload, malformed tool parameters, cross-tenant object IDs, revoked permissions, an agent-generated external image URL, repeated retries after payment, a poisoned persisted memory, and model/provider fallback. Record actual effects and denied side effects; a model's refusal text is not sufficient if a tool ran.

Measure false positives alongside escaped actions and data disclosure. Include legitimate workflows so a brittle guardrail does not silently break the service. Do not claim complete prompt-injection prevention from a finite attack suite. Demonstrate that the attacker cannot cross enforced authority boundaries even if the model follows a malicious instruction.
