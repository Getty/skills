<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# Results, protocol, and provenance

Evidence: official RUML 1.0.0 (2026-11-15), commit `d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4`. File `$specVersion` is `"1.0"`.
Normative requirements below come from the pinned specification/schema. **Implementation recommendation** and **Snapshot gap** identify additional engineering decisions or limits.

## Contents

- [Separate result document](#separate-result-document)
- [Binding a result to its rulemap](#binding-a-result-to-its-rulemap)
- [Node instance paths](#node-instance-paths)
- [Statuses and reasons](#statuses-and-reasons)
- [Capability result payloads](#capability-result-payloads)
- [Evaluation protocol](#evaluation-protocol)
- [Source anchoring and provenance](#source-anchoring-and-provenance)
- [Reproducibility and authenticity](#reproducibility-and-authenticity)
- [Review procedure](#review-procedure)
- [Evidence and coverage](#evidence-and-coverage)

## Separate result document

Persisted results belong in a `.ruml-result` document, never embedded into the `.ruml` structure. The discriminator is exactly `RUML-Result`, including case. The closed root requires `$format`, `$specVersion`, `rumlReference`, and `evaluation`. [R1][R3]

| Object | Required fields | Optional fields |
| --- | --- | --- |
| `rumlReference` | `id` | `hash` |
| `evaluation` | `id`, `timestamp`, `mode`, `results` | `caseId`, `userId`, `toolId`, `toolVersion`, `startTimestamp`, `capabilities` |
| Node result | `lexId`, `status`, `reason` | `evaluatedAt`, `capabilities` |

`evaluation.id` identifies the evaluation; `rumlReference.id` identifies the referenced RUML file. Both use lowercase UUID v4 in the published schema. `timestamp` is completion time; `startTimestamp` is separate. `mode` is `optimized` or `complete`. [R1][R3]

There is no standard result-root `ruleset`, `rulesetId`, `inputData`, `provenance`, or `signature` field. Do not extend the closed envelope with convenient runtime fields. Capability payloads and external runtime records are the available implementation mechanisms where the standard permits them. [R3]

The optional evaluation capability list has entries `{id,payload?}` and no meaningful order. Node capability results use ordered entries with the same envelope. These result entries do not carry the authoring fields `required` or `role`. [R1][R3]

## Binding a result to its rulemap

`rumlReference.id` refers to the source document's `metadata.id`. The optional `hash` identifies its exact canonical content. Its shape is a string matching `^(?:sha3-256|sha256|blake3):[0-9a-f]{64}$`, not a manifest hash object. [R1][R3]

When loading a result, locate the referenced RUML file and verify the hash if present. If it matches, the file can be used to reconstruct the rule structure. A missing source file or a mismatching hash requires a warning that reconstruction cannot be established. If the hash is absent, use of the located file is allowed, but a warning about unverifiable integrity is recommended. [R1]

This differs from sidecar merging: an EXT base mismatch must abort its merge, whereas §5.1 specifies warning behavior for reconstruction of an existing result. Do not discard the result's historical evidence merely because its corresponding rulemap is unavailable, and do not present a mismatching rulemap as the verified original. [R1][R8]

An ID and a human-readable `metadata.version` are not substitutes for the content digest. A title, filename, or folder named after a version is weaker evidence still. Preserve the actual source artifact and any applied sidecars in an audit bundle where reconstruction matters.

**Snapshot gap:** `rumlReference` names the base document, not a complete standard execution-environment fingerprint. It does not enumerate merged sidecar digests, model resolution, external input snapshots, or every included file version. Record these through permitted capability/runtime evidence rather than adding undocumented fields to the reference object.

## Node instance paths

`evaluation.results` is keyed by instance path. Start with `1` for the root; append the **one-based position** in each successive `children` array. For example, `1.2.1` means the first child of the root's second child. The stored `lexId` separately identifies the node definition. [R1]

| Identifier | Identifies | Suitable result key? |
| --- | --- | --- |
| File `metadata.id` | RUML document | No |
| Node `id` | Node UUID | No |
| LexID (node-map key) | Definition within a file | No; modular uses can repeat |
| Result path | Traversal instance | Yes |

Two paths may legitimately contain the same `lexId` and different results. A result map keyed by LexID or UUID would overwrite one modular instance. The key's numerical components are positions, not the textual LexIDs of the nodes on the route. [R1]

The schema's path regex is `^[1-9][0-9]*(\.[1-9][0-9]*)*$`; semantic checking must still ensure the actual route begins at the root, selects existing child positions, and resolves to the recorded `lexId`. A regex cannot verify that relationship. [R3]

**Implementation recommendation:** validate paths against the exact hash-bound rulemap. Never replay an old result against reordered children merely because the UUIDs still exist. Internal occurrence identity should distinguish repeated node definitions and recursion depth.

**Snapshot gap:** this version does not standardize every detail of embedding foreign-file subtree results under a `ruml:tree-include` result. Do not invent a globally standardized foreign path prefix or flatten other files' LexIDs into the base namespace.

## Statuses and reasons

Statuses in stored results are strings. `pending` is not a serializable status; absence means there is no recorded evaluation/ignore event for that node. Include one result per evaluated instance and per directly ignored node; do not populate descendants of an ignored subtree. [R1][R2]

| Status | Meaning | Required `reason` |
| --- | --- | --- |
| `"true"` | Evaluated as fulfilled | Human-readable string |
| `"false"` | Evaluated as unfulfilled | Human-readable string |
| `"undefined"` | Evaluation occurred but produced no definitive decision | Object with exactly `type`, `message` |
| `"ignored"` | Deliberately not evaluated | Object with exactly `type`, `trigger`, `operator`, `mode` |

For `undefined`, `reason.type` is `error` for technical failure, or `default` for other causes such as missing input. `message` must be a nonempty string. Do not use a free-form reason string, `null`, or `pending` to represent an undecidable result. [R2][R3]

For `ignored`, `reason.type` is `shortCircuit`, `manualSkip`, or `conditionalDeactivation`; `trigger` is a nonempty identifier of the responsible node/sibling; `operator` records the parent operator; `mode` records the evaluation mode. The object permits no extra fields. [R2]

For `shortCircuit`, permitted operators are `AND`, `XOR`, `NOT_AND`, `NOT_XOR`, or the string `undefined`. `OR`, `NOT_OR`, and `DELEGATED` do not short-circuit in RUML. Short-circuit reasons must also agree with the actual optimized traversal, not merely pass enum validation. [R2][R3]

The schema only constrains `trigger` to a nonempty string. The official example uses an instance path such as `1.4`; using paths makes a trigger unambiguous for modular occurrences. Do not claim the schema mandates a LexID or UUID here. [R2][R9]

An ignored node is excluded from the parent's operator calculation. A technical failure is not a manual skip, and an unreached node after an abort is not automatically an evaluated undefined node. Model these states separately in storage and UI. [R2]

**Implementation recommendation:** supply meaningful reasons even where the true/false string schema would accept an empty string. Record missing input explicitly, explain the relevant operator outcome, and distinguish expected authored examples from observations produced by a running evaluator.

## Capability result payloads

Node capability result arrays preserve order, allowing repeated uses of the same identifier. Every recorded identifier should correspond to a capability actually active in that evaluation. The optional evaluation list provides a place to record global implementation/model configuration. [R1]

| Capability | Required payload fields | Important details |
| --- | --- | --- |
| `ruml:query` | `expression`, `inputs`, `result` | Expression nonempty; inputs keyed by DataPoint ID; result is a status string |
| `ruml:expression` | `expression`, `inputs`, `children`, `result` | Children ordered, each exactly `{lexId,status}`; child status is `"true"` or `"false"` |
| `ruml:protocol` | `events` | Evaluation-level payload; optional schema field `level` |

Query and expression payloads prohibit additional fields. Their `result` is one of `"true"`, `"false"`, and `"undefined"`; the boolean returned inside JSONata is serialized into this string vocabulary. [R1][R3]

Record the resolved DataPoint values that the expression read. An expression reading no DataPoints records `inputs: {}`. For a combiner, recording only child decisions is insufficient if a DataPoint also influenced the result. [R1][R5]

A `DELEGATED` parent whose child is undefined does not run its expression and must not carry an expression execution payload. Do not invent observed child inputs or an execution timestamp for an expression that never ran. [R1][R5]

The result schema does not define closed AI-query/action output payloads comparable to the query/combiner payloads. Provider request IDs, selected model versions, response validation, action receipts, and review annotations therefore need documented implementation-specific conventions. A permissive payload is not a standardized meaning. [R3]

## Evaluation protocol

`ruml:protocol` requests the chronological execution record. It is declared only at root and may configure `payload.config.level` as `standard` or `verbose`. If required, an engine unable to produce the protocol must not evaluate; optional declaration recommends protocol production. Engines may produce one without a declaration. [R4]

The protocol lives at `evaluation.capabilities[{id:"ruml:protocol"}].payload.events`. It is a JSON array using the CloudEvents 1.0 JSON Batch Format and RUML's additional profile. It is not a node capability or a free-form text log. [R4]

| Event attribute | RUML profile |
| --- | --- |
| `specversion` | Exactly `"1.0"` |
| `id` | Unique within this protocol |
| `source` | URI-reference identifying the evaluating engine; version and absolute URI recommended |
| `type` | Registered `ruml.*` event or an implementation event outside that reserved prefix |
| `time` | Required RFC 3339 timestamp |
| `subject` | When applicable, node path or DataPoint ID |
| `data` | Optional direct JSON event payload |

Array order is normative occurrence order. Do not sort by timestamp: equal timestamps are possible. The `source` engine identifier is not the normative source text, an authenticated publisher certificate, or a substitute for file binding. [R4]

The event vocabulary is:

| Standard level | Verbose-only additions |
| --- | --- |
| `ruml.evaluation.started`, `ruml.evaluation.completed`, `ruml.evaluation.aborted` | `ruml.node.skipped` |
| `ruml.node.evaluated`, `ruml.action.triggered` | `ruml.datapoint.resolved` |
| `ruml.warning`, `ruml.error` | — |

Applicable standard events must be emitted at either level; verbose events must not occur in a standard-level protocol. Event data includes such fields as evaluation mode, node LexID/status, skip cause, resolved binding, operation/trigger/status, or warning/error message according to the event. [R4]

Sensitive DataPoint values must not appear anywhere in the protocol, including `data.value` and prose messages. Omitting `value` is possible; there is no authorization to leak it into a warning or custom event. Broader result input snapshots need a separate runtime privacy policy. [R4]

**Snapshot gap:** the result schema requires `events` inside a protocol payload but does not require `level`, and it cannot prove event uniqueness, actual chronology, sensitive-value absence, or truthful execution. Emit an explicit level and validate the profile semantically; do not equate schema acceptance with a trustworthy audit trail. [R3][R4]

## Source anchoring and provenance

| Mechanism | What it expresses | What it does not establish |
| --- | --- | --- |
| Text anchor | Which local text/element a rule represents or relies on | Authorship, factual accuracy, or validity of the legal interpretation |
| Text/context `source` | Declared origin and related source metadata | Cryptographic proof of that origin |
| Result `rumlReference` | Which RUML structure the result refers to | Complete input/environment reconstruction |
| Protocol | Recorded sequence of engine events | Independent proof the events happened |
| Verified digest | Equality to the expected canonical content | Identity or authority of whoever supplied the expected digest |
| Verified trusted signature | Binding to a verified signer under a trust policy | Correctness of the rule or every asserted fact |

`ruml:text-reference` anchors use local text ID, optional element `GUID`, and required relationship `type` (`represents` or `refers-to`). At most one anchor per node may be `represents`; anchors must resolve locally and be unique. They cannot contain an external-file URI or character-range selector. [R6]

An element anchor needs structured RUML Text `content` containing that GUID; plain-text entries can only be anchored as a whole. Stable GUIDs preserve element identity across renumbering, while `eId` is its current textual designation. Source identity and a rule's interpretation remain separate assertions. [R6]

Structured text `source` should record the imported document URI, optionally the archived-source digest and source reuse terms. Context `source` is more open. These differ from a node's normative `represents` relationship and from the execution protocol. [R6]

## Reproducibility and authenticity

An expression snapshot is useful for replay only when the expression and inputs determine the outcome. RUML permits nondeterministic JSONata functions such as `$now` and `$random`; their returned values are not automatically captured in expression results. A reproducibility claim must account for them. [R5]

AI decisions also depend on the resolved model, prompt/template, source material, settings, and service behavior. External inputs and actions introduce further environment dependencies. **Implementation recommendation:** maintain an immutable evidence bundle with explicit versions and document what can and cannot be replayed.

A bare result has no embedded signature. Container layers provide result integrity and authenticity controls; use the exact canonicalization/hash/signature rules in [containers-and-integrity.md](containers-and-integrity.md). A self-asserted `userId`, `toolId`, or `source` does not authenticate itself. [R7]

The specification requires result integrity for legally relevant proceedings. This does not determine whether a particular signature satisfies a jurisdiction's legal requirements or whether the modeled rules are correct; those need the application's actual trust and domain review.

## Review procedure

1. Validate the discriminator, version, closed envelopes, UUIDs, status vocabulary, and status-dependent reason shape.
2. Locate the source and verify its optional reference hash; report missing/mismatching binding accurately.
3. Resolve every instance path and verify its recorded LexID against the source graph.
4. Check evaluated/ignored coverage, absence of pending entries, and absence of descendants under ignored nodes.
5. Reconcile query/combiner inputs and outputs with the actual executed decisions; do not fabricate skipped payloads.
6. Validate protocol profile, occurrence ordering, event IDs, event levels, and sensitive-value handling.
7. Distinguish a schema-valid artifact, a semantically coherent artifact, a reproducible run, and an authenticated run in the report.

Steps above are an implementation review procedure assembled from the distinct obligations; they are not a claim that the JSON Schema alone performs each check.

## Evidence and coverage

The repository contains a result schema and published examples for statuses, modular paths, queries, expressions, and protocol. It has no dedicated `tests/05-result-format` suite at this pin. Treat example parsing/schema checks as limited evidence, not proof of traversal, provider, or cryptographic correctness. [R3][R9]

[R1]: https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/05-result-format/5-1-result-model.md
[R2]: https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/05-result-format/5-0-status-types.md
[R3]: https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/schemas/ruml-result.schema.json
[R4]: https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/04-capabilities/4-13-ruml-protocol.md
[R5]: https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/04-capabilities/4-14-ruml-expression.md
[R6]: https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/04-capabilities/4-12-ruml-text-reference.md
[R7]: https://github.com/Law-as-Code-Institute/ruml/tree/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/07-container
[R8]: https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/04-capabilities/4-5-ruml-ext.md
[R9]: https://github.com/Law-as-Code-Institute/ruml/tree/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/05-result-format
