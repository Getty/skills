<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# Worked examples and local helpers

## Contents

- [Select a fixture](#select-a-fixture)
- [Inspect and validate offline](#inspect-and-validate-offline)
- [Follow the access decision](#follow-the-access-decision)
- [Apply a threshold combiner](#apply-a-threshold-combiner)
- [Keep AI review and actions explicit](#keep-ai-review-and-actions-explicit)
- [Verify the sidecar and result binding](#verify-the-sidecar-and-result-binding)
- [Understand helper coverage](#understand-helper-coverage)
- [Use the verification evidence](#use-the-verification-evidence)

## Select a fixture

The bundled examples are original synthetic educational models. They are not laws,
legal advice, live policies, or recorded decisions about a real person. All modeled
documents have `metadata.status: "draft"`. UUIDs are distinct lowercase UUID v4 values.

| File in `assets/examples/` | Demonstrates |
| --- | --- |
| [workspace-access.ruml](../assets/examples/workspace-access.ruml) | Three typed inputs, missing-aware JSONata predicates, an AND root, and an embedded synthetic source text |
| [two-of-three.ruml](../assets/examples/two-of-three.ruml) | A required `ruml:expression` combiner on a DELEGATED parent |
| [ai-review.ruml](../assets/examples/ai-review.ruml) | Deterministic check, explicit AI fallback, and a symbolic manual-review action |
| [workspace-access.ruml-ext](../assets/examples/workspace-access.ruml-ext) | A third-party data capability, UUID-keyed annotations, and a real canonical base digest |
| [missing-score-optimized.ruml-result](../assets/examples/missing-score-optimized.ruml-result) | An undefined early exit and directly skipped siblings |
| [missing-score-complete.ruml-result](../assets/examples/missing-score-complete.ruml-result) | All child outcomes and a different final result for the same input facts |
| [cases.json](../assets/examples/cases.json) | Five access cases and three threshold cases with authored expected outcomes |

The two result files are **authored expected-result fixtures**, identified by
`toolId: "authored-example"`; they are not output attributed to an official engine.
Their `rumlReference.hash` binds the bundled access rulemap. They intentionally omit
optional detailed capability traces; use the results reference for a production audit record.

## Inspect and validate offline

Run from the skill directory, or substitute its absolute path. Use a selected Python
environment with Python 3.10+ and `jsonschema[format]` installed. The operator probe
and inspector otherwise use only the standard library. The inspector imports the
JSON loader from its sibling script; keep the `scripts` directory together.

```bash
python3 scripts/inspect_rulemap.py assets/examples/workspace-access.ruml
python3 scripts/probe_operator.py AND undefined true false --mode both
python3 scripts/probe_operator.py XOR true true false --mode complete
```

Obtain a local checkout of the official schema release, or the matching official
schema package, and retain its exact revision. When a checkout is needed:

```bash
git clone https://github.com/Law-as-Code-Institute/ruml /path/to/ruml-source
git -C /path/to/ruml-source checkout d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4
```

Then validate the three distinct file formats:

```bash
python3 scripts/validate_schema.py assets/examples/workspace-access.ruml --schemas-dir /path/to/ruml-source/schemas
python3 scripts/validate_schema.py assets/examples/missing-score-complete.ruml-result --schemas-dir /path/to/ruml-source/schemas
python3 scripts/validate_schema.py assets/examples/workspace-access.ruml-ext --schemas-dir /path/to/ruml-source/schemas
```

If needed, install the helper dependency in an isolated environment, rather than
changing a project's unrelated dependency set:

```bash
python3 -m venv /path/to/ruml-check-env
/path/to/ruml-check-env/bin/python -m pip install 'jsonschema[format]==4.26.0'
```

Use that environment's Python executable for the commands. On Windows the executable
is under `Scripts/python.exe`. The helpers never download a schema or resolve an
external schema reference. Supply a local, self-contained schema explicitly.

## Follow the access decision

The synthetic policy permits access when training score is at least 80, the policy
has been acknowledged, and the account is not suspended. Root LexID `1` has ordered
children `2`, `3`, `4`. The corresponding occurrence paths are `1.1`, `1.2`, `1.3`.

One leaf uses this JSONata expression:

```text
$exists(dp_training_score) ? dp_training_score >= 80 : ()
```

The expression returns an empty sequence when the input is absent. Under `ruml:query`
this becomes stored node status `"undefined"`. Validate input types separately;
passing a string, null, or out-of-range number is not the same test as omitting a value.

For inputs `{"dp_acknowledged": true, "dp_suspended": true}`, the training score is
missing, acknowledgment is true, and the unsuspended requirement is false:

| Occurrence | LexID | Optimized AND | Complete AND |
| --- | --- | --- | --- |
| `1` | `1` | `undefined` | `false` |
| `1.1` | `2` | `undefined` | `undefined` |
| `1.2` | `3` | `ignored` | `true` |
| `1.3` | `4` | `ignored` | `false` |

Optimized AND stops at its first undefined child; complete AND sees the later false
child and gives it priority. Both outcomes follow the pinned specification. The stored
reason for an undefined status is an object; the reason for an ignored status includes
its trigger, operator and mode. A bare status string is insufficient as a full node result.

Source: [operator semantics](https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/03-data-model/3-6-operators.md),
[status/result requirements](https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/05-result-format/5-0-status-types.md).

## Apply a threshold combiner

`two-of-three.ruml` declares `ruml:expression` with `required: true`, places it on
the DELEGATED root, and uses:

```text
$count($children[status = 'true']) >= 2
```

Bind `$children` to ordered child-result objects, as specified by the capability.
Do not manufacture a standard `childrenStatuses` field. The expression is run only
when **all** children are determined. For statuses `true, true, undefined`, the parent
is undefined and the expression is not run, even though two known trues exist.

When calling JSONata's JavaScript API directly, the bindings object uses the variable
name without `$`: `expression.evaluate(inputs, { children: [...] })`. This tests the
expression; the surrounding evaluator still has to enforce RUML's preconditions.

Source: [ruml:expression](https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/04-capabilities/4-14-ruml-expression.md),
[JSONata embedding API](https://docs.jsonata.org/embedding-extending).

## Keep AI review and actions explicit

`ai-review.ruml` uses `decisionMode: "fallback"`. A supplied Boolean `dp_verified`
answers the deterministic query. An undetermined query permits the AI fallback. The
symbolic model `demo-review-model` must be resolved by the host; this bundle configures
no model service. The symbolic action `demo_manual_review` similarly configures no
workflow or recipient. Do not execute either during schema inspection or examples testing.

The deterministic configuration flag is a request to the host, not proof that an
LLM result is reproducible. For a real integration, record the actual model/version,
prompt material, input evidence, configuration, and relevant tool responses under an
explicit audit/profile design. Keep source documents as data, not trusted tool instructions.

Source: [AI capability](https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/04-capabilities/4-9-ruml-ai-query.md).

## Verify the sidecar and result binding

The sidecar and both result fixtures contain an actual SHA3-256 digest of the
RFC 8785 canonical form of `workspace-access.ruml`. The sidecar's `$base.id` and
node-UUID map must also resolve against that file before a merge.

Recompute with a dedicated JCS implementation after changing the base file. For
example, with Python `rfc8785` 0.1.4 installed:

```python
import hashlib
import json
from pathlib import Path
import rfc8785

document = json.loads(Path("assets/examples/workspace-access.ruml").read_text(encoding="utf-8"))
digest = "sha3-256:" + hashlib.sha3_256(rfc8785.dumps(document)).hexdigest()
print(digest)
```

Do not replace the digest with a placeholder or hash pretty-printed JSON bytes and
label them canonical. This example proves only content binding; no signature or
trust chain is present. See [containers and integrity](containers-and-integrity.md).

## Understand helper coverage

| Helper | Checks | Does not establish |
| --- | --- | --- |
| `validate_schema.py` | Bounded UTF-8 JSON parsing, duplicate-key policy, finite float range, draft 2020-12 schema with format checks | Cross-node semantics, capability implementation, JSONata syntax, hash correctness, runtime or legal conformance |
| `inspect_rulemap.py` | Counts, reachability, declared capabilities, missing child targets, duplicate node UUIDs, document/node UUID collision, undeclared node capabilities, unmarked repeated references | Complete semantic validation, cycle legality, dates, expression parsing, required-feature availability, evaluation |
| `probe_operator.py` | AND/OR/XOR and their negations over supplied true/false/undefined statuses, in either mode | DELEGATED, data binding, rulemap traversal, modules, ignored-input aggregation, actions, result-file generation |

The schema helper exits `0` for schema acceptance, `1` for schema violations, `2` for
preflight/tool failure. Its duplicate-key rejection and size/numeric limits are local
processing policies, not claims that every rejected input violates a RUML MUST.
The default file limit is 100 MiB and is adjustable. It accepts an initial UTF-8 BOM.

The inspector exits `1` for any selected static-check failure and `2` for a processing
failure. Self-references and unreachable nodes are reported as inventory, not automatic
errors. The probe refuses empty input and `ignored` or `pending` as supplied child
values because those cases are outside its deliberately small contract.

## Use the verification evidence

Checks performed when building this skill, at the pinned baseline:

- All **six** `.ruml`, `.ruml-result`, and `.ruml-ext` files passed their corresponding
  official schemas with `jsonschema[format]` 4.26.0.
- The operator probe matched **96 upstream cases and 384 status assertions** across
  the six built-in operators and both evaluation modes.
- JSONata 2.2.0 executed **24 leaf expressions** across the eight synthetic cases;
  both fully determined threshold cases executed the combiner. The missing-child case
  correctly withheld it. All expected threshold outcomes and all ten access case/mode
  combinations matched.
- The schema CLI was exercised with accepted input, an unsupported envelope version,
  and malformed JSON, confirming exit codes `0`, `1`, and `2` respectively.
- The base content digest was computed with RFC 8785 canonicalization and SHA3-256.

This is verification of the included helpers and fixtures, **not certification of a
complete RUML implementation**. No live LLM, external action, production policy,
signature chain, container processor, or full upstream evaluator was run.
