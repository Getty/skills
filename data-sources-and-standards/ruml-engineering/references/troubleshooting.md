<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# Troubleshooting

Baseline: RUML 1.0.0, specification commit `d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4`. Rule IDs below are the existing chapter-8 identifiers. Runtime requirements without catalogue IDs are cited by section; do not invent new standard rule codes.

## Contents

- [Triage before repair](#triage-before-repair)
- [Format and structure failures](#format-and-structure-failures)
- [Capability and expression failures](#capability-and-expression-failures)
- [Traversal and result failures](#traversal-and-result-failures)
- [Sidecars, text and external trees](#sidecars-text-and-external-trees)
- [Implementation-specific failures](#implementation-specific-failures)
- [Known source contradictions](#known-source-contradictions)
- [Minimal diagnostic report](#minimal-diagnostic-report)
- [Sources](#sources)

## Triage before repair

1. Preserve the failing bytes, artifact type, base/sidecars, schema pin, tool version and first reproducible error.
2. Identify the failing layer: encoding/JSON, schema, semantic validation, provider/expression execution, result serialization, or container integrity.
3. Reduce to the smallest example that retains the failure. Keep required metadata and IDs distinct; do not accidentally introduce a different error while reducing.
4. Compare against the pinned schema and relevant rule/fixture. Treat parser bugs, source inconsistencies and invalid user documents as separate diagnoses.
5. Repair the authoring source, rerun the affected check, then validate the emitted artifact. Preserve original signed/hashed artifacts rather than editing their evidence in place.

Report “not checked” when a required external dependency is unavailable. A schema pass and an unresolved semantic check are different outcomes. [Chapter 8][rules]

## Format and structure failures

| Failure | Checks | Repair |
| --- | --- | --- |
| Unsupported version | `$specVersion`, schema enum, tool-supported major/minor (`FMT-04`, `FMT-09`) | Use `"1.0"` for this release's wire format; package release `1.0.0` belongs elsewhere |
| Looks like JSON but fails loading | UTF-8, comments, trailing commas, nonstandard numbers, object root (`FMT-01`, `FMT-02`) | Emit strict JSON; `jsonc` specification snippets are not literal `.ruml` files |
| Decoder accepts a duplicate node key | Original byte/token stream, not only the decoded map (`FMT-12`) | Assign one definition per LexID; do not let last-key-wins decoding silently remove a rule |
| Header passes schema but ordering is rejected | First two root fields (`FMT-05`) | Emit `$format` then `$specVersion` first; do not infer this check from JSON Schema |
| Extra root or node properties | `/`, `/rulemap/nodes/<lexId>` (`FMT-07`, `NODE-03`) | Remove invented `root`, `parent`, node `lexId`, or runtime `status`; move supported information to its actual schema location |
| Wrong node identity | Lowercase v4 UUID pattern, duplicate node UUIDs, equality to `metadata.id` (`FMT-10`, `NODE-08`) | Generate the correct distinct identity at authoring time; do not arbitrarily regenerate existing stable identities |
| Invalid child structure | LexID strings, child existence, root as child, empty arrays (`FMT-11`, `NODE-10`, `NODE-05`, `NODE-06`) | Use string keys such as `"2"`; omit `children` on a leaf; reference existing non-root nodes |
| Operator/leaf conflict | Child presence and `metadata.status` (`NODE-07`, `NODE-12`, `OP-07`) | Parent needs an operator; non-draft leaf must omit it; unfinished `"undefined"` operator stays draft-only |

Small distinction:

```json
{ "id": "cb07d69b-333f-4a67-a643-79d30aa59020", "label": "Leaf" }
```

This is a **node fragment**, not a complete RUML file. Adding `"children": []` does not describe the same valid shape; omit that field for a leaf. A result entry, by contrast, must carry `lexId` and a runtime status in the separate result artifact. [§3.5][nodes] [§5.1][results]

Metadata failures often arise from independent clocks: compare `modified >= created` (`META-03`), `validUntil > validFrom` when both exist (`META-09`), and status-specific fields (`META-10`–`META-12`). Validate against a recorded “now” when testing `expired`; a timestamp ordering failure is not repaired by changing an unrelated document version. [Chapter 8][rules]

## Capability and expression failures

| Failure | Checks | Repair |
| --- | --- | --- |
| Unknown required capability | Root `id`, `required`, actual implementation registry (`CAP-01`) | Install/implement the declared capability or choose a compatible runtime; do not erase requiredness to obtain partial execution |
| Node capability undeclared | Root declarations and every node entry (`CAP-14`, `CAP-15`) | Add the correct root declaration; node `payload` alone never declares support |
| Role rejected | Official IDs versus draft/reverse-domain IDs (`CAP-03`–`CAP-05`) | Official IDs omit `role`; custom IDs declare it, matching the implementation |
| Duplicate capability rejected | Role and location (`CAP-06`, `CAP-10`) | Root IDs are unique; node `decision`/`reaction` entries may repeat; node `data` entries may not |
| Query on a parent | Non-empty `children` with a `decision` capability (`CAP-07`) | Move the decision to a leaf or deliberately model a `DELEGATED` parent with a combiner |
| Delegated node has no usable rule | `operator`, combiner count, `description`, root `required` (`OP-02`, `OP-04`, `CAP-08`, `CAP-11`) | Supply exactly one combiner and its description; declare official `ruml:expression` as required |
| Expression accepted by schema but unusable | Parse JSONata; identify undeclared reads (`CAP-29`, `CAP-38`, `DP-18`) | Correct syntax and DataPoint declarations; a string type check cannot establish expression validity |
| Computed value loops | `binding.type: "computed"`, dependencies (`DP-11`, `DP-12`) | Remove direct/transitive dependency cycles; preserve the intended calculation |

For an expression `dp_age >= 18`, declare `dp_age` under the `payload.data` of the root `ruml:datapoints` entry, for example this DataPoint fragment:

```json
"dp_age": {
  "name": "Age in completed years",
  "type": "number",
  "binding": { "type": "input" }
}
```

Then provide the value in the evaluation input object as `{"dp_age": 21}`. Do not insert the runtime value into the DataPoint definition or treat a missing value as `0`. Query input without a value has no entry; a query producing no Boolean result yields `undefined`. [§4.7][datapoints] [§4.8][query]

When a valid expression yields `undefined`, log the actual input object and native result type. `"true"` is a string, not native Boolean `true`; numbers/objects/no result do not become definitive decisions. An exception and a legitimate missing result need different diagnostic reasons. [§4.8][query] [§5.0][statuses]

## Traversal and result failures

| Symptom | Likely check | Correct behavior |
| --- | --- | --- |
| `XOR(true,true)` returns false | Conventional XOR implementation | RUML XOR behaves as disjunction, with early exit only in optimized mode |
| OR skips later children | Generic Boolean short-circuit optimization | `OR` and `NOT_OR` evaluate all children in both modes |
| Optimized AND ignores an earlier unknown | Child ordering and stopping condition | An encountered `undefined` stops optimized AND immediately, even if a later child would be false |
| Complete and optimized produce different status | Compare first decisive/unknown child and complete-mode precedence | Can be correct: `[undefined,false]` under AND differs by mode |
| DELEGATED runs with an undefined child | Combiner gate (`OP-03` and §3.6 contract) | Evaluate all children, then return undefined without running the combiner |
| Fallback chooses a different answer after serialization | Node capability array order (`CAP-20`) | Preserve order; first definitive decision wins |
| Reused node overwrites an earlier result | Result map keyed by UUID/LexID | Key by invocation path and retain `lexId` in each entry |
| Skipped branch has fabricated descendants | Short-circuit result construction | Mark skipped direct child ignored; omit its descendants |
| Actions fire on skipped nodes | Traversal occurrence versus previous/global state | Only nodes actually evaluated this traversal may trigger handlers |

These behaviors are specified in [§3.6][operators], [§4.3][node-capabilities], [§4.10][actions], and [§5.1][results]. Do not “fix” a specified mode difference to match ordinary Boolean optimization assumptions.

For `children: ["8", "8"]`, results `1.1` and `1.2` both have `lexId: "8"`, but are distinct instances. Node `8` needs `modular: true` even though both references have the same parent (`MOD-01`). The upstream `referenced-twice-by-one-parent-without-modular` case checks this exact distinction. [Modular fixture descriptor][modular-tests]

For recursion failures, count self-reference transitions rather than total path depth. First instance is depth 0; with maximum 1, depth 2 returns undefined/error. Check `modular: true`, a non-first self-reference, and at least one non-self child (`MOD-01`, `MOD-04`, `MOD-05`). The `MOD-03` warning for recursive AND/OR variants is not automatic document rejection. [§6.4][recursion]

Result reason fragment for an evaluated but undecidable node:

```json
{
  "lexId": "8",
  "status": "undefined",
  "reason": { "type": "default", "message": "dp_age is unavailable" }
}
```

Use `type: "error"` for a technical failure. An `ignored` reason instead needs `type`, `trigger`, `operator`, and `mode`; a bare string is invalid there. Never serialize `status: "pending"`: missing entries express that state. Do not add stack traces as extra fields inside the closed reason object. [§5.0][statuses] [Result schema][result-schema]

## Sidecars, text and external trees

| Symptom | Checks | Repair |
| --- | --- | --- |
| Sidecar will not attach | `$base.id`, canonical base hash (`CAP-24`, `CAP-25`) | Find the intended exact base; if it changed intentionally, rebase/regenerate the sidecar and review changes; never bypass comparison |
| Sidecar node missing | EXT `nodes` keys versus base node UUIDs (`CAP-26`) | Use the base node's UUID, not its LexID or result path |
| Duplicate extension payload | Same node/capability inline or across sidecars (`CAP-27`) | Resolve one authoritative placement; do not merge conflicting meanings silently |
| Text anchor no longer resolves | `refs[].id`, `refs[].element`, content GUIDs (`TXT-19`, `TXT-20`) | Match the correct text entry/version and preserve continuing GUIDs; do not replace GUID with eId |
| Text schema passes but XML fails | Root namespace and dialect validator (`TXT-15`, `TXT-16`, `TXT-18`) | Render according to §4.12, validate the actual dialect; JSON shape validation is insufficient |
| Text digest mismatch | RFC 8785 form of `content`, UTF-8, SHA3-256 (`TXT-09`) | Hash the specified content representation, not pretty-printed JSON or XML source bytes |
| Tree anchor rejected | Immutable version URI plus `#node/<uuid>` (`TREE-02`, `TREE-04`, `TREE-06`) | Resolve the exact version and target; local `#node/...` is not an external node anchor |
| Cycle diagnosis seems wrong | `tree-reference` versus `tree-include` (`TREE-05`, `TREE-09`) | Permit reference cycles; reject inclusion cycles; do not conflate either with allowed modular self-reference |

Container hash/signature failures and unsupported algorithms have separate prescribed behavior. Hash mismatch and invalid signature are errors; unsupported verification must be reported as not performed, never as success. See [runtime-architecture.md](runtime-architecture.md) and [§7.6][container].

## Implementation-specific failures

See [validation-and-tooling.md](validation-and-tooling.md) for exact parser pins and source links.

- Python `ruml-parser==1.0.0` needs Python 3.14+. An environment-version failure says nothing about the document's RUML validity.
- Its internal mapping explicitly rejects computed bindings with `NotImplementedError`. Preserve the valid source and report the implementation gap.
- A generated Pydantic model accepting input does not establish schema conformity. Use `RumlParser` on raw JSON/dicts; `parse_model` may already have normalized invalid original values.
- JS repository development uses pnpm 11; `catalog:` entries are not ordinary npm version strings. Published-package use and repository installation differ.
- JS `queryDatapointRefs` does not reject syntax errors: it returns no reads on parse failure. Call `validateQueryExpression` too; default text scanning is less complete than the AST reader.
- A different JSONata runtime can alter parse/evaluation behavior. Record the resolved version: RUML names 2.2.0, while the inspected JS catalog permits `^2.2.1`.

For an apparently missing semantic check, minimize the counterexample and compare the implementation to the rule. Do not label a file invalid solely because one library lacks support, and do not call a file fully validated solely because one library accepts it.

## Known source contradictions

These are observed at the baseline commit, not universal statements about future RUML versions.

| Evidence | Discrepancy | Working treatment |
| --- | --- | --- |
| [Runner prose][runner] versus [descriptor schema][test-schema] and operator YAML | Prose uses path-keyed leaf statuses and `expect` result files; current tests use DataPoint `inputs` and JSONata `assertions` | Run current descriptors as written and record the compatibility choice |
| Same sources | Prose examples use `test`, file-level `spec`, and optional diagnostic assertions; schema requires `title,tests`, disallows file-level spec and differs on diagnostics | Validate descriptor shape; state whether codes/locations/warnings are asserted |
| [§4.10 action example][actions] versus §§3.6/5 and current operator assertions | Example calls unreached siblings undefined; operator/result rules use ignored direct siblings | Use normative traversal and current assertions; never trigger actions on unreached siblings |
| [§8 package paragraph][rules] versus [npm manifest][npm-manifest] | Old package scope `@law-as-code-institute/ruml-schema` versus `@law-as-code/ruml-schema` | Use actual pinned manifest/README package identity |
| [§4.8 credit-check example file][credit-example] versus `NODE-08` | `metadata.id` equals `rulemap.nodes["1"].id` | Treat the example as needing an identity repair before reuse; schema-only validation cannot catch the collision |

Keep the failing original and a separately identified corrected example. Do not silently alter upstream tests or broaden acceptance to accommodate an inconsistent example. If sources disagree beyond these recorded cases, cite the exact clauses/files, explain the uncertainty, and avoid claiming full conformance for the disputed behavior.

## Minimal diagnostic report

Return the affected artifact and source/tool versions; observed failure and expected behavior; layer and rule/section; exact JSON Pointer or runtime path; minimal reproducer; proposed repair; and verification performed. Include unresolved dependencies and intentional test exclusions. This is enough to make the next action reviewable without exposing private inputs or provider credentials.

## Sources

[rules]: https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/08-validation/index.md
[nodes]: https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/03-data-model/3-5-node-object.md
[results]: https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/05-result-format/5-1-result-model.md
[datapoints]: https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/04-capabilities/4-7-data-points.md
[query]: https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/04-capabilities/4-8-ruml-query.md
[statuses]: https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/05-result-format/5-0-status-types.md
[operators]: https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/03-data-model/3-6-operators.md
[node-capabilities]: https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/04-capabilities/4-3-capabilities-node-field.md
[actions]: https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/04-capabilities/4-10-ruml-actions.md
[modular-tests]: https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/tests/06-modular-nodes/6-2-implementation.test.yaml
[recursion]: https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/06-modular-nodes/6-4-recursion.md
[result-schema]: https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/schemas/ruml-result.schema.json
[container]: https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/07-container/7-6-processing.md
[runner]: https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/appendix/A-spec-tests/runner-contract.md
[test-schema]: https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/tests/schema/spec-test.schema.json
[npm-manifest]: https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/packages/npm/package.json
[credit-example]: https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/04-capabilities/4-8-ruml-query.examples/credit-check.ruml
