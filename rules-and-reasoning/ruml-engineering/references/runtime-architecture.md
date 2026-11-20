<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# Runtime architecture

Baseline: RUML 1.0.0, specification commit `d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4`. This reference separates required RUML behavior from recommended implementation boundaries. It is language-neutral; a parser library is not an evaluation engine.

## Contents

- [Architecture and execution boundary](#architecture-and-execution-boundary)
- [Execution sequence](#execution-sequence)
- [Operator and decision semantics](#operator-and-decision-semantics)
- [Profiles without inventing conformance levels](#profiles-without-inventing-conformance-levels)
- [Effect adapters](#effect-adapters)
- [Errors and result states](#errors-and-result-states)
- [Replay and reproducibility](#replay-and-reproducibility)
- [Conformance goals](#conformance-goals)
- [Sources](#sources)

## Architecture and execution boundary

Keep the immutable rule definition separate from per-run inputs, node-instance state, provider responses, and effect receipts. RUML stores rules in `.ruml`; evaluation output belongs in `.ruml-result`. Never write case-specific statuses into `rulemap.nodes`. [§5.1][results]

Recommended components:

| Component | Responsibility | Output |
| --- | --- | --- |
| Artifact loader | Bytes, container layers, exact source identity | Verified artifacts or explicit unreadability |
| Validator/resolver | Version, structure, semantic references, capability support, sidecars | Validated static representation plus findings |
| Traversal engine | Ordered child visits, per-path state, recursion, operators | Node-instance results |
| Capability registry | Declared role, accepted payload, parser/evaluator implementation | Typed capability dispatch |
| Data/provider adapters | Input, computed values, external data, AI and included trees | Values and evidence for this invocation |
| Reaction dispatcher | Status-triggered actions with authorization and deduplication | Effect events and actual receipts |
| Result writer | Versioned references, reasons, capabilities, timestamps | Validated `.ruml-result` |

These component boundaries are advice. The exact call graph and persistence model are not prescribed by RUML. An implementation may combine components while preserving their responsibilities and observed behavior.

## Execution sequence

1. **Establish artifact identity.** Preserve input bytes. For a container, follow manifest processing: verify its signature when present; per file decrypt, verify the signature, then verify the hash. A failed hash/signature is an error, not an ordinary undecidable leaf. [§7.6][container]
2. **Read the header and capability declarations.** Check `$format` and supported `$specVersion`; read root `capabilities` before processing `rulemap`. Reject unsupported `required: true` capabilities without partially processing the file (`CAP-01`). [§4.6][parser-obligations]
3. **Validate and resolve.** Check schema and semantic invariants. Build indexes for LexIDs and UUIDs without changing their meanings. Retain array order. Check sidecar `$base.id`, `$base.hash`, UUID membership and capability collisions before merging (`CAP-24`–`CAP-27`). [Chapter 8][rules]
4. **Resolve static dependencies.** Pin included/referenced RUML versions; validate target existence and inclusion cycles (`TREE-04`, `TREE-06`, `TREE-09`). Reference cycles and inclusion cycles have different rules: references may cycle; inclusions may not. [§4.15][tree-reference] [§4.16][tree-include]
5. **Create the run context.** Fix evaluation ID, mode, clock abstraction, input snapshot, runtime/capability versions, recursion limit, model/provider bindings, and action policy. This context belongs to the application, not arbitrary extra RUML root fields.
6. **Resolve values for the current instance.** Input values use DataPoint IDs. A missing value is absent from the JSONata input object. Resolve external values and computed dependencies through explicit adapters; validate declared value constraints. Reject computed dependency cycles as document errors (`DP-12`). [§4.7][datapoints] [§4.8][query]
7. **Visit the root at path `1`.** A child at zero-based array position `i` receives path `parentPath + "." + (i + 1)`. Its `lexId` remains the referenced key, not the child position. Do not cache context-dependent results solely by LexID or UUID. [§5.1][results] [§6.3][modular]
8. **Determine each reached node's status.** Leaves use decision capabilities; parent nodes use their operator or combiner. Preserve decision-capability order and the distinctions below. Apply the recursion limit to instance self-reference depth. [§3.6][operators] [§4.3][node-capabilities] [§6.4][recursion]
9. **Process reactions at the defined runtime event.** Only nodes actually evaluated during this traversal can trigger actions. Match `onTrue`, `onFalse`, or `onUndefined`; unreached/ignored nodes must not trigger actions. Preserve repeated reaction-entry order. [§4.10][actions] [§4.3][node-capabilities]
10. **Write and verify the result.** Record reached results and explicitly ignored direct children, omit descendants of ignored nodes, preserve each path's LexID, and validate the result schema plus references. Result `$specVersion` is the highest input version among the base and sidecars, not the engine's own version. [§5.1][results] [§2.3][versioning]

Do not turn a resolver's inability to load an included tree into `false`. A `ruml:tree-include` that cannot be evaluated yields `undefined`; distinguish that runtime inability from a known invalid anchor or forbidden inclusion cycle discovered in validation. [§4.16][tree-include]

## Operator and decision semantics

Use explicit status values; never apply host-language truthiness to the strings `"false"` or `"undefined"`.

| Operator | `optimized` | `complete` |
| --- | --- | --- |
| `AND` | Visit in order; first `false` or `undefined` stops traversal and determines the result | Evaluate all; `false` takes priority over `undefined`, otherwise `true` |
| `OR` | Evaluate all; `true` takes priority over `undefined`, otherwise `false` | Same |
| `XOR` | Visit in order; first `true` or `undefined` stops traversal and determines the result | Evaluate all; `true` takes priority over `undefined`, otherwise `false` |
| `NOT_AND`, `NOT_OR`, `NOT_XOR` | Underlying operator's traversal; invert only definitive `true`/`false` | Same inversion rule |
| `DELEGATED` | Evaluate all children; any `undefined` prevents running the combiner | Same |

`XOR` is RUML's ordered legal disjunction, not parity or “exactly one true.” `OR` does not short-circuit. Changing mode may change the final status: `AND(undefined, false)` is `undefined` in optimized mode and `false` in complete mode. These are specified semantics, not performance-equivalent implementation choices. [§3.6][operators]

For a short-circuit, create `ignored` results for remaining direct children with the required reason object; do not descend into those children. Already evaluated siblings keep their actual results. An ignored result is excluded from parent aggregation. [§5.0][statuses] [§5.1][results]

Leaf decisions follow `decisionMode`, defaulting to `fallback`: the first definitive decision in list order wins. `agreement` evaluates all and requires agreement; `majority` evaluates all and returns `undefined` on a tie. Parent nodes ignore `decisionMode`. Preserve the distinction between multiple decision entries and one custom combiner. [§4.3][node-capabilities]

The prose does not fully spell out every mixed `undefined` voting case. Resolve such gaps using applicable fixtures and a documented implementation policy; do not quietly assume `undefined` is a `false` vote. A leaf with no decision capability remains `undefined`. [§4.3][node-capabilities] [§4.10][actions]

`ruml:query` evaluates JSONata against the DataPoint object. Only native Boolean results become definitive statuses; numbers, strings, structures and no result become `undefined`. `ruml:expression` follows the combiner contract and receives direct child records as `$children` in child order. A combiner must have a prose `description`, and arbitrary non-Boolean outputs do not constitute valid node decisions. [§4.8][query] [§3.6][operators]

`operator: "undefined"` is permitted only in a draft; on draft leaves any operator is ignored. Do not invent a normal Boolean operator for an unfinished parent or claim that a draft is executable merely because its structure validates. [§3.6.5][operators]

For recursive modular nodes, the first instance is depth 0; each self-reference increases depth by one. The specified default maximum is 500; an instance at maximum + 1 becomes `undefined` with reason type `error`. Depth is not the number of dots in the path. The exit-condition rationale for `XOR` applies to short-circuit execution; `complete` mode still evaluates children and therefore needs the depth limit. [§6.4][recursion]

## Profiles without inventing conformance levels

RUML defines no conformance levels. The following are suggested **deployment policies**, which must be named as application choices rather than “RUML Basic/Advanced” certifications. [§1.4][conformance]

| Deployment policy | Concrete configuration | Honest claim |
| --- | --- | --- |
| Inspection | No evaluation, adapters or actions; static findings only | Inspected the stated checks |
| Reproducible simulation | Recorded inputs/provider responses, controlled clock/randomness, captured action intents | Replayed the stated run under a pinned environment |
| Live evaluation | Registered providers, explicit model bindings, effect authorization and receipts | Evaluated using the identified live services |

A deployment may restrict expression functions, network access, model classes, or action handlers. Label rejection as deployment policy or unsupported capability, as applicable; do not claim RUML itself forbids a feature it permits. A policy-limited tool must qualify its conformance claim if it rejects otherwise conformant inputs it claims to support.

Combiners should be deterministic but may use random numbers/current time. The spec explicitly permits JSONata `$random`, `$now`, `$millis`, and `$eval`, recommending capture of drawn values. Do not describe all RUML evaluation as inherently deterministic. [§3.6][operators]

`ruml:ai-query.config.deterministic` is a hint, not a proof of reproducibility. `model` is symbolic and resolved by tool settings; an inline `prompt` overrides the configured template. Record the concrete model/version and effective prompts when evaluating. [§4.9][ai-query]

## Effect adapters

Recommended adapter records contain invocation identity, inputs, resolved configuration/version, output or error, timing, and enough evidence to replay the decision. Keep credentials in the application's secret infrastructure; symbolic references in RUML do not authorize arbitrary command execution.

| Adapter | Input/output boundary | Key verification |
| --- | --- | --- |
| External DataPoint | Symbolic `binding.ref` → value or unavailable outcome | Declared type, units, provenance, fallback handling |
| Computed DataPoint | Expression + dependency values → value | Acyclic dependencies, JSONata version, expression validity |
| AI decision | Effective prompts + explicitly selected inputs → `true`/`false`/`undefined` | Concrete model binding; response validation; captured response |
| Included tree | Immutable version URI + node anchor + invocation context → decision | Target identity, inclusion-cycle rules, dependency record |
| Reaction | `operation`, `ref`, `config` at evaluated status → receipt | Authorized handler, occurrence identity, actual execution status |

These adapter interfaces are application architecture, not additional standard payload fields. Use allowed capability-result payloads or separate application records to store evidence; do not add invented fields to closed schema objects.

For action retries, a useful idempotency identity includes evaluation ID, node path, reaction-entry ordinal, and handler. LexID alone is insufficient because modular nodes and repeated capability entries can create distinct occurrences. A simulated event is an intent, not a successful external receipt.

If actions or providers can affect later observations, define and record scheduling. Buffering every action until the end can change behavior; parallelizing ordered decisions can invoke a provider or reaction that should never have run. Optimize only after proving preservation of observable traversal and effect behavior for the deployed policy.

## Errors and result states

The categories below are recommended implementation distinctions. They do not introduce new RUML rule IDs or result statuses.

| Category | Examples | Handling |
| --- | --- | --- |
| Input/document error | Invalid JSON, missing child, incompatible sidecar, unknown required capability | Reject; report exact existing rule IDs where available |
| Artifact integrity/authenticity error | Hash mismatch, invalid signature | Report error; do not process the affected artifact as verified |
| Runtime undecidability | Missing input, non-Boolean query output, no definitive fallback | `undefined`, generally reason `type: "default"` |
| Runtime technical failure | Provider timeout, evaluation exception, recursion limit | `undefined` with reason `type: "error"` when it prevents the node result |
| Intentional skip | Short-circuit, manual skip, conditional deactivation | `ignored` with its required structured reason |
| Effect failure | Authorized action handler failed | Record the failure; do not fabricate success or silently redefine a previously established decision |

The last row is an application boundary recommendation; RUML does not supply a universal transaction/rollback protocol for external systems. Keep it separate from the node's decision unless an explicit capability contract defines more.

Undefined reasons have exactly `type` (`error` or `default`) and non-empty `message`. Ignored reasons require `type`, `trigger`, `operator`, and `mode`; `shortCircuit` must not name `OR`, `NOT_OR`, or `DELEGATED`. `true` and `false` reasons are strings. `pending` is represented by absence, not a stored status. [§5.0][statuses] [Result schema][result-schema]

For unsupported container algorithms, apply the specific behavior: unsupported hash → warning and skipped verification; unsupported signature format → report unverified, never call it signed; unsupported encryption/no key → unreadable affected file, with other files still processable. “Verified” and “not verified” must remain different. [§7.6][container]

## Replay and reproducibility

Capture a replay envelope outside the core rule definition:

- Exact base/sidecar bytes or content hashes, schema pin, input format version, included immutable versions.
- Runtime build, JSONata implementation/version, capability implementation versions and relevant locale/numeric settings.
- Input values and their observation times, computed-dependency results, provider responses and model bindings.
- Evaluation ID, mode, clock values, recursion limit, invocation path, capability-entry positions, and scheduling policy.
- Nondeterministic draws, effective prompts, action intents, effect receipts, and any manual decisions.

Two operations should be distinguished: **replay** reuses captured external observations; **reevaluation** asks current providers again and may legitimately differ. Freezing a clock and model temperature cannot make an unrecorded external service reproducible.

Compare node paths, statuses, consumed inputs and capability results first. Compare reasons according to the test contract; their prose can vary without changing the decision. A result alone is sufficient for reconstruction only if the needed inputs and observations were actually recorded. A hash identifies content; it does not establish the legal adequacy of that content.

## Conformance goals

An implementation plan should name which normative role it is pursuing and produce evidence for that role:

- Parser: accept valid supported versions/capabilities, reject invalid documents, preserve required ordering and perform container behavior when presented.
- Producer: emit valid versioned artifacts, declare capabilities, and never emit the draft-only undefined operator in a non-draft document.
- Evaluator: meet parser requirements, operator/modular semantics and implemented decision-capability semantics, then produce conformant results.
- Validation tool: additionally cover every `schema` and `semantic` catalogue rule, with unavailable external checks made visible.

Use actual upstream descriptor assertions and focused tests for partial inputs, mode differences, skipped descendants, repeated capabilities, modular paths and recursion boundaries. See [validation-and-tooling.md](validation-and-tooling.md) for the current runner/prose drift and package limitations.

## Sources

[results]: https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/05-result-format/5-1-result-model.md
[statuses]: https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/05-result-format/5-0-status-types.md
[result-schema]: https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/schemas/ruml-result.schema.json
[container]: https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/07-container/7-6-processing.md
[parser-obligations]: https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/04-capabilities/4-6-parser-obligations.md
[rules]: https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/08-validation/index.md
[tree-reference]: https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/04-capabilities/4-15-ruml-tree-reference.md
[tree-include]: https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/04-capabilities/4-16-ruml-tree-include.md
[datapoints]: https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/04-capabilities/4-7-data-points.md
[query]: https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/04-capabilities/4-8-ruml-query.md
[modular]: https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/06-modular-nodes/6-3-evaluation.md
[operators]: https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/03-data-model/3-6-operators.md
[node-capabilities]: https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/04-capabilities/4-3-capabilities-node-field.md
[recursion]: https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/06-modular-nodes/6-4-recursion.md
[actions]: https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/04-capabilities/4-10-ruml-actions.md
[versioning]: https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/02-file-format-basics/2-3-versioning.md
[ai-query]: https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/04-capabilities/4-9-ruml-ai-query.md
[conformance]: https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/01-introduction/1-4-conformance.md
