---
name: ruml-engineering
description: "Use when reading, authoring, validating, evaluating or debugging RUML (Rulemapping Logic Format) or Law as Code rulemaps — .ruml, .ruml-result, .ruml-ext, .rumlc, legal or policy decision models, AND/OR/XOR evaluation modes, JSONata queries, DELEGATED combiners, DataPoints, modular nodes, ruml:ai-query, result traces, signatures, conformance fixtures, Akoma Ntoso, LegalRuleML or DMN mappings."
---

<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# RUML Engineering

Treat RUML as a versioned exchange format for explicitly modeled decision logic.
Keep source interpretation, structural validity, evaluator behavior, and the adequacy
of a particular decision separate. Work independently of any application framework,
programming language, graph store, or other skill.

Use **RUML specification 1.0.0, dated 2026-11-15**, as this skill's baseline.
Its JSON documents carry **`"$specVersion": "1.0"`**, not `"1.0.0"`.
The inspected upstream revision is `d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4`.
Verify current releases and implementation support before claiming that a limitation
is still present. Read [sources and versioning](references/sources-and-versioning.md)
for source authority, provenance, licenses, and refresh instructions.

## Select the needed references

| Task | Read |
| --- | --- |
| Understand fields, IDs, metadata, document states, or structural rules | [Core data model](references/core-data-model.md) |
| Predict exact operator results, early exits, or unknown values | [Operators and evaluation](references/operators-and-evaluation.md) |
| Turn source text into a reviewed, maintainable rulemap | [Modeling workflow](references/modeling-workflow.md) |
| Reuse nodes, bind occurrence-specific context, or handle recursion | [Modules and recursion](references/modules-and-recursion.md) |
| Declare, extend, or merge capabilities and sidecars | [Capabilities and extensions](references/capabilities-and-extensions.md) |
| Model inputs or implement JSONata checks and threshold combiners | [DataPoints and JSONata](references/datapoints-and-jsonata.md) |
| Integrate LLM checks, source material, human review, or actions | [AI, actions, and context](references/ai-actions-and-context.md) |
| Store results, explain paths, or connect provenance | [Results and provenance](references/results-and-provenance.md) |
| Hash, sign, encrypt, or process `.rumlc` containers | [Containers and integrity](references/containers-and-integrity.md) |
| Choose parsers, validate files, or run the actual conformance fixtures | [Validation and tooling](references/validation-and-tooling.md) |
| Build a language-neutral evaluator or integration service | [Runtime architecture](references/runtime-architecture.md) |
| Compare or bridge legal, decision, RDF, or provenance standards | [Interoperability](references/interoperability.md) |
| Diagnose rejected files, semantic surprises, or upstream inconsistencies | [Troubleshooting](references/troubleshooting.md) |
| Start from original fixtures and use the local helper scripts | [Worked examples](references/worked-examples.md) |
| Verify a claim, choose a baseline, or update this material | [Sources and versioning](references/sources-and-versioning.md) |

Load the relevant reference directly. Do not read the entire bundle for a narrow
question. Use the examples as educational inputs; do not substitute their synthetic
policy for the user's actual rule.

## Establish the task contract

Identify the requested outcome: explanation, rulemap authoring, validation, diagnosis,
runtime implementation, integration, or migration. Inspect supplied artifacts first.
For a new model, establish the decision to answer, relevant facts, expected outcomes,
source edition, and applicable time or jurisdiction when they matter.

Use reasonable assumptions for an illustrative task and label them. Ask only when
missing source meaning or implementation requirements materially change the result.
Do not require a legal source for a synthetic example or an internal policy.

For execution, state the supported capabilities, data-binding policy, evaluation mode,
JSONata implementation/version, external adapters, and result-storage contract. Treat
symbolic external references as unresolved until the host explicitly binds them.

## Build or repair a rulemap

1. **Define the decision and interpretation.** Separate source text, modeled conditions,
   input evidence, and conclusions. Record ambiguous wording or discretionary judgments
   explicitly. Source anchors support review; they do not establish semantic equivalence.
2. **Choose the supported profile.** Pin the spec, schemas, relevant test fixtures, and
   parser/evaluator versions. Verify the precise requested feature against the selected
   tool; a parser package is not automatically an evaluator or container processor.
3. **Create stable structure.** Put nodes in `rulemap.nodes`, use LexID `"1"` for the root,
   and link ordered `children` by LexID. Assign distinct document and node UUIDs. Keep
   runtime results out of the rulemap. Use the appropriate document lifecycle metadata.
4. **Model required facts and checks.** Declare DataPoints with explicit types, sources,
   and constraints. Place `ruml:query` or `ruml:ai-query` on leaves. Use a `DELEGATED`
   combiner for arithmetic combinations of child statuses. Explain missing inputs and
   exceptions without silently coercing them into a negative decision.
5. **Add source links and reuse.** Anchor the relevant wording, distinguish a semantic
   reference from executable inclusion, and preserve referenced versions. Mark reused
   nodes as modular where required. Specify host context binding separately from core
   RUML; do not invent per-call parameter fields.
6. **Validate in layers.** Check strict JSON handling, official JSON Schema, cross-object
   semantic rules, capability support, expression parsing, and actual evaluation.
   Review whether the model answers the intended source question as a separate step.
7. **Exercise meaningful cases.** Cover a passing case, failing case, boundary value,
   missing input, and relevant error path. For ordered operators compare both modes.
   For modules use distinct occurrence contexts; for recursion exercise termination and
   the depth limit. Stub external effects during tests.
8. **Deliver traceable output.** Return the files or code requested, source/profile
   assumptions, exact observed checks, and remaining untested behavior. Preserve
   occurrence-level results and explain the actual failing condition when repairing.

## Preserve the non-obvious semantics

- Keep the three versions distinct: specification publication `1.0.0`, JSON envelope
  `$specVersion: "1.0"`, and the rulemap's own `metadata.version`.
- Keep four identifiers distinct: document UUID, node UUID, file-local LexID, and
  occurrence path. Path segments after the root identify **one-based child positions**;
  the result's `lexId` identifies the referenced node. Never cache all occurrences by UUID.
- Treat RUML `XOR` as its specified ordered disjunction. It does not calculate Boolean
  exclusive-one or parity. Exclusivity is a modeling assumption, not an engine check.
- Preserve `children` order. Optimized `AND` stops at the first `false` **or `undefined`**;
  optimized `XOR` stops at the first `true` **or `undefined`**. Complete mode can therefore
  change the result, not merely add a longer trace. `OR` evaluates all direct children.
- Keep negation from turning `undefined` into a Boolean. `ignored` documents a skipped
  occurrence; `pending` is an implicit runtime state represented by absence from results.
- Run a `DELEGATED` combiner only after all children are evaluated and none is undefined.
  Require its prose description and required combiner capability. Do not use a leaf
  decision capability as a parent-node combiner.
- Return `undefined` for a query/combiner result that is not a Boolean; do not apply
  generic truthiness. Stored result statuses are strings, not JSON booleans.
- Distinguish root capability declarations from ordered node capability entries and
  UUID-keyed sidecar maps. Require support for a required capability before accepting
  the file for that capability profile; do not silently skip required behavior.
- Treat `ruml:ai-query` model names and many bindings as host-dependent. A deterministic
  configuration hint, temperature zero, or a prompt does not prove reproducibility.
- Load `.ruml-result` as documentation. Never repeat actions merely because a result
  is opened. Keep live effects behind explicit host bindings and the user's task scope.
- Verify integrity against the exact representation specified for that surface.
  Use RFC 8785 tooling for canonical JSON; `json.dumps(sort_keys=True)` is not a general
  JCS implementation. A valid hash or signature does not prove that a rule is correct.
- Preserve documented source disagreements. Separate structural schema authority,
  normative prose, fixture assertions, implementation gaps, and deployment choices.
  Never silently change RUML semantics to make a test green.

## Use the bundled tools

Run tools from the skill directory, or substitute its absolute path. None of these
helpers performs a network request, invokes an LLM, or executes an action.

```bash
python3 scripts/inspect_rulemap.py assets/examples/workspace-access.ruml
python3 scripts/validate_schema.py assets/examples/workspace-access.ruml --schemas-dir /path/to/pinned-ruml/schemas
python3 scripts/probe_operator.py AND undefined true false --mode both
python3 scripts/probe_operator.py XOR true true false --mode complete
```

`validate_schema.py` requires `jsonschema[format]`; it validates against caller-supplied,
local, self-contained official schemas. It refuses to silently omit a required format
checker. Its exit status reports schema/preflight outcome, not complete conformance.
`inspect_rulemap.py` provides an inventory and selected static checks.
`probe_operator.py` explains six built-in operators over supplied statuses; its output
is not a `.ruml-result` and it is not a general RUML evaluator.

Read [worked examples](references/worked-examples.md) for dependency setup, helper
limits, expected outputs, example provenance, and how to reproduce checks.

## Report the actual evidence

For a validation result, name the artifact, schema/spec revision, checked layers, and
unsupported capabilities. For an evaluator, name the mode and runtime dependencies,
show the relevant occurrence paths, and distinguish domain failure from technical error.
For integration, explain the source of facts and who or what resolves ambiguous checks.

Do not claim universal portability from a shared JSON shape, full conformance from
schema acceptance, or legally correct interpretation from a completed execution.
When no real evaluator was run, say so. Recommend concrete next work only when it
resolves a remaining limitation relevant to the requested task.
