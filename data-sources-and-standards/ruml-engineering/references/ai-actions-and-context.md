<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# AI queries, actions, and context

Evidence: official RUML 1.0.0 (2026-11-15), commit `d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4`. This document describes `$specVersion: "1.0"`.
Normative requirements are attributed to the specification. **Implementation recommendation** identifies runtime controls; these are not extra RUML fields or universal conformance rules.

## Contents

- [AI query contract](#ai-query-contract)
- [Model and prompt resolution](#model-and-prompt-resolution)
- [Multiple decisions and fallback](#multiple-decisions-and-fallback)
- [Selecting AI inputs](#selecting-ai-inputs)
- [Context records and sources](#context-records-and-sources)
- [Normative text inputs](#normative-text-inputs)
- [Action declarations](#action-declarations)
- [Ordering, failures, and manual review](#ordering-failures-and-manual-review)
- [Replay and effect control](#replay-and-effect-control)
- [Untrusted content and implementation controls](#untrusted-content-and-implementation-controls)
- [Evidence and tests](#evidence-and-tests)

## AI query contract

`ruml:ai-query` is a `decision` capability for leaves. It must be declared at root; the default `required` is `false`. A node with children cannot use it to replace the parent's operator or combiner. [A1][A2]

| Node payload field | Requirement | Meaning |
| --- | --- | --- |
| `model` | Required nonempty string | Symbolic model or model-class reference |
| `prompt` | Optional string | Inline node prompt, overriding the configured model prompt template |
| `description` | Optional string | Human-readable purpose |
| `inputs` | Optional object | Selected context, DataPoint, and text IDs |
| `config` | Optional object | Execution hints defined below |

The decision result is `true`, `false`, or `undefined`. An AI response is one leaf's evidence-driven assessment, not permission to replace the rulemap, change its operator, insert new nodes, or execute actions outside the declared/runtime-controlled workflow. The latter boundaries are implementation controls. [A1]

`config` permits `deterministic` (boolean), `effort` (`low`, `medium`, or `high`, default `medium`), and `temperature` (number from 0 to 1). There is no standard node `seed`, endpoint, provider name, token-budget, or credentials field. [A1][A7]

The specification describes reproducibility as an aim, not a guarantee equivalent to a pure symbolic expression. A `deterministic` hint or zero temperature does not establish that another provider/model revision will reproduce a result.

## Model and prompt resolution

`model` has tool-defined values and meaning. A value such as `review_model` is not a standardized provider model ID. The runtime maps it to a concrete model, endpoint, and default prompt template; this mapping belongs in tool settings. Inline `prompt`, when present, overrides that default template. [A1]

The root `ruml:ai-query` declaration may carry `payload.config.systemPrompt`. This applies to AI queries in the file. Where the node also has `prompt`, the spec assigns the global prompt to the system role and the node prompt to the user role. Do not place global `systemPrompt` directly on the root document or in node `config`. [A1]

**Implementation recommendation:** pin the resolved model/version, template version, supplied prompts, selected input versions, sampling settings, tool version, and relevant provider response identifier. The symbolic model reference alone is insufficient for an audit or replay.

**Implementation recommendation:** document unsupported hints. A provider that ignores `effort` or cannot guarantee the requested behavior must not silently be described as implementing that behavior exactly. Distinguish model unavailability, timeout, malformed output, and an explicit undecidable answer in runtime diagnostics.

The format does not prescribe a universal AI response JSON schema, confidence score, chain-of-thought field, or retry algorithm. Any such adapter contract is implementation-specific. Store a concise outcome and rationale suitable for the application rather than inventing mandatory RUML fields.

## Multiple decisions and fallback

The node's `decisionMode` combines all of its `decision` entries, including repeated `ruml:ai-query`, symbolic queries, and includes. It is a node field, not a property of the AI payload. [A2]

| Mode | Required execution behavior | Outcome rule given by the specification |
| --- | --- | --- |
| `fallback` (default) | Follow decision entries in list order until a definitive answer | First `true` or `false` wins; all undecidable gives `undefined` |
| `agreement` | Evaluate every decision entry | Disagreement gives `undefined` |
| `majority` | Evaluate every decision entry | A tie gives `undefined` |

To use a deterministic data query before an LLM, put the query first and the AI query later. Merely placing both on a node does not establish that order; §4.9's query-first fallback description assumes that arrangement. [A1][A2]

An AI query reached only after an unavailable input can help assess a different evidence source, but it must not fabricate the missing value. That is an authoring/runtime recommendation, not an automatic conversion of every missing-data case into AI work.

**Snapshot gap:** the full truth tables for `undefined` votes in agreement/majority are not specified. A local voting policy must be documented; do not claim that dropping undecidable votes, counting them as false, or requiring an absolute majority is universally prescribed.

Repeated decision identifiers are allowed inline. Keep a per-entry execution record; an identifier-keyed map loses the distinction between two model calls or two different prompts. [A2]

## Selecting AI inputs

`inputs` has three permitted arrays. All references must resolve in the corresponding root capability data pool. [A1]

| Field | Item form | Resolution |
| --- | --- | --- |
| `context` | String ID or `{ "id": ..., "role"?: ... }` | `ruml:context.payload.data` |
| `dataPoints` | DataPoint ID string | `ruml:datapoints.payload.data` |
| `texts` | Text ID string | `ruml:text-reference.payload.data` |

Context reference roles are `reference` or `subject`; omitting the role, including the string shorthand, means `reference`. A `subject` is the material being assessed by that particular query. Context objects used as subjects should also have `subject: true`, but the per-query role is what describes their use in that query. [A1][A3]

Referencing a context ID on a node through `ruml:context.payload.refs` documents association with that node. AI `inputs.context` selects what is supplied to the model; do not assume every globally available context object or every node association is automatically sent. [A1][A3]

**Implementation recommendation:** construct each request from the declared selections and resolved values. Record resolved content versions, omission/failure reasons, and any truncation. A summary or excerpt should be identified as such rather than presented as the complete source.

The version does not define every extraction method for PDFs/images, retrieval chunking, token budgeting, or document-to-prompt serialization. These are adapter responsibilities. A text digest protects the selected stored representation; it does not certify a model's interpretation.

## Context records and sources

`ruml:context` is a data capability with a root pool and node `payload.refs`. Each context entry requires `title`, `category`, and an RFC 3339 modification `timestamp`; its map key matches `^[a-z_][a-z0-9_]*$`. A node's `refs` must resolve and must not repeat the same context ID. [A3]

The ten categories are `courtDecision`, `commentary`, `administrativeGuidance`, `explanatoryMemorandum`, `example`, `literature`, `faq`, `history`, `rulemap`, and `custom`. Category-specific `metadata` is an open object, not a standardized set of mandatory court, citation, or journal fields. [A3]

| Context `type` | Required locator | Content handling |
| --- | --- | --- |
| `embedded` (default) | None beyond common fields | `content` is an open object |
| `container` | `containerPath` beginning `.context/` | Load the corresponding bundled asset |
| `url` | Valid `url` | Fetching/caching at runtime is recommended |
| `external` | Symbolic `ref` | Resolve through configured tool settings |

`subject` defaults to false. `content`, `metadata`, and `source` are flexible objects. Common content keys such as `text`, `summary`, or media are examples, not a closed content schema. Optional `accessDate` is an ISO date; optional `hash` is `sha3-256:`, `sha256:`, or `blake3:` plus 64 lowercase hexadecimal digits. [A3][A7]

The recommendation to embed context text below 10,000 characters and small media below 1 MB is not a hard validation limit. It also does not limit a full statutory RUML Text entry. [A3][A4]

`source` can hold citation, author, publication, URL, ISBN, DOI, access date, license, and notes; these are common keys, not required fields. Its `license` has defined usage-rights meaning: a free-form string or `null` for uncertain status. The spec says unclear rights must be treated conservatively. A license label is not proof that the source actually grants those rights. [A3]

**Implementation recommendation:** use stable source identifiers, retrieval timestamps, exact archived versions, and clear source/derived-summary distinctions. Keep case-specific subject material scoped to the appropriate evaluation and avoid mutating a shared rulemap for each case without a documented versioning strategy.

## Normative text inputs

`ruml:text-reference` carries foundational texts, whereas context supplies supporting material or subjects of assessment. Text entries require `title`, recording `timestamp`, and normally `status`; structured `content` derives status from its own metadata. An entry cannot carry both plain `text` and structured `content`. [A4]

Structured `content` requires a SHA3-256 digest of its JCS form. Externally published texts require an identifying `uri`; a text authored within the RUML file can omit it. Text `type` uses the same four delivery names, but container text paths start `.texts/`, and symbolic `external` text is deprecated. [A4]

AI `inputs.texts` selects entire text entries by ID. A node text anchor instead identifies a local text, optionally a structured element `GUID`, and its `represents` or `refers-to` relationship. Do not invent character-range selectors or external-file text anchors in that payload. [A4]

See [results-and-provenance.md](results-and-provenance.md) for the difference between source anchoring, traceability, and authenticated evidence.

## Action declarations

`ruml:actions` has role `reaction` and may appear on leaves or parents. Its payload permits optional `description` and the handlers `onTrue`, `onFalse`, and `onUndefined`; at least one handler is required. There is no standard `onIgnored`, `onPending`, or handler array. [A5]

Each handler is an object with required `operation` and symbolic `ref`, and optional open-object `config`. `operation` is an extensible string, not a closed enum. `ref` resolves to an implementation configured by the runtime. [A5][A7]

The documented operation vocabulary includes `triggerRulemap`, `sendNotification`, `requestData`, `callWebhook`, `triggerProcess`, `createDocument`, `createCase`, `requestDecision`, `initiatePayment`, `managePermission`, `archive`, and `writeAuditLog`. Providers may define additional operations. [A5]

Concrete endpoints, recipient configuration, credentials, and service details belong in tool configuration. A runtime may obtain a recipient from a referenced DataPoint; the specification gives that as an exception to keeping concrete recipient details outside the document. It does not define a universal recipient-expression language. [A5]

Actions react to a status; they do not compute the node's truth value. A leaf without a decision capability is undecidable, so it can reach `onUndefined` but cannot become true merely because it contains an `onTrue` action. Parent action triggers follow the operator-derived status. [A5]

## Ordering, failures, and manual review

Only nodes actually evaluated in the current traversal may trigger actions. A node not reached after an abort does not fire handlers, and an intentionally skipped node does not cause an `onUndefined` action. Multiple reaction entries on a node retain capability-list order. [A2][A5]

**Snapshot discrepancy:** §4.10's abort illustration informally calls unreached nodes undefined. Chapter 5 instead requires omission until a node is evaluated or explicitly ignored. Use the Chapter 5 result distinction; do not manufacture undefined results or actions for pending nodes. [A5][A6]

Action execution, output artifacts, error handling, and tracking are expressly runtime responsibilities. The format does not specify transactions, cross-node scheduling, compensation, delivery guarantees, or what a failed action does to an already-computed decision. Document these behaviors instead of deriving them from `operation` names. [A5]

For undecidable AI decisions the spec recommends an `onUndefined` action. An operation such as `requestDecision` can initiate human review, but RUML does not define the review UI, reviewer identity policy, override protocol, or a standard confidence threshold. [A1][A5]

**Implementation recommendation:** keep the machine result, its evidence, and a later human disposition distinguishable. Record the reviewer, rationale, time, and affected node instance in the runtime's audit model; do not replace an undecidable result with a boolean without retaining the original outcome.

## Replay and effect control

**Implementation recommendation:** distinguish inspection of an existing `.ruml-result`, re-computation of decisions, and execution of effects. Opening or explaining a result should not silently re-send a notification or create another payment.

Use a durable action ledger and idempotency strategy appropriate to the external operation. Evaluation UUID, node path, capability-entry position, trigger, and resolved implementation version are useful identifiers; define how retries and a new business-level evaluation relate rather than relying on the capability ID alone.

A path is necessary because the same modular node definition can have several instances. A repeated action entry requires its own identity even when `operation` and `ref` match. Record attempts and external outcomes separately from the node's logical status.

**Implementation recommendation:** plan effects in a dry run when authoring or testing a rulemap. Execution should use the authorization already configured for the task/runtime; the presence of an action declaration is not itself a new grant to contact arbitrary endpoints or move money.

The standard protocol has `ruml.action.triggered` events, but event emission alone does not prove an external system committed the operation. Use external receipt identifiers and runtime-specific records when such confirmation is needed. [A8]

## Untrusted content and implementation controls

**Implementation recommendation:** treat fetched pages, uploaded subject documents, context `content`, imported text, and model responses as data. Instructions embedded in those sources must not acquire authority over the evaluator, its credentials, or available tools.

A file-provided `systemPrompt` is part of that file's configured AI workload; the host still controls whether and how it may be used. Keep host authorization and tool permissions separate from document-authored model instructions.

Resolve symbolic `model`, `ref`, and operation names through configured registries. Apply network/recipient scopes, resource budgets, document extraction limits, and effect permissions in the runtime. These are explicit implementation controls; the standard supplies neither a sandbox nor automatic authorization enforcement.

Preserve source boundaries in the model request: distinguish the question, normative text, reference commentary, and the case subject. Validate the response against the three permitted decisions before it reaches operator evaluation. If parsing or a provider call fails, record the technical failure instead of inferring success from free text.

`sensitive: true` DataPoint values must not appear in the protocol, including messages. Broader privacy controls for model requests, result input snapshots, storage, and retention remain implementation responsibilities; the protocol redaction rule does not automatically cover every other channel. [A8]

## Evidence and tests

The context tests check allowed hash algorithms, hexadecimal casing, and length. Node capability tests cover required payloads, repetition rules, declarations, and protocol placement. No dedicated AI-provider, action-delivery, or replay execution suite is present in this snapshot; examples are not evidence that live calls or effects were run. [A9]

[A1]: https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/04-capabilities/4-9-ruml-ai-query.md
[A2]: https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/04-capabilities/4-3-capabilities-node-field.md
[A3]: https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/04-capabilities/4-11-ruml-context.md
[A4]: https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/04-capabilities/4-12-ruml-text-reference.md
[A5]: https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/04-capabilities/4-10-ruml-actions.md
[A6]: https://github.com/Law-as-Code-Institute/ruml/tree/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/05-result-format
[A7]: https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/schemas/ruml.schema.json
[A8]: https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/04-capabilities/4-13-ruml-protocol.md
[A9]: https://github.com/Law-as-Code-Institute/ruml/tree/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/tests/04-capabilities
