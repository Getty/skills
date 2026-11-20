<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# RUML operators and evaluation

Baseline: specification **1.0.0**, wire version **`"1.0"`** at commit
`d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4`.
Reference text adapts the specification © 2026 Rulemapping Group GmbH, **CC BY-SA-4.0**.
Linked schemas, fixtures and tests are **Apache-2.0**; [upstream licence](https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/LICENSE.md).
**Engineering advice** below is implementation guidance, not a new conformance requirement.

## Contents

- [Exact aggregation rules](#exact-aggregation-rules)
- [Cases fixed by the conformance suite](#cases-fixed-by-the-conformance-suite)
- [Runtime statuses and reasons](#runtime-statuses-and-reasons)
- [DELEGATED and the combiner contract](#delegated-and-the-combiner-contract)
- [Leaf decisions and draft operators](#leaf-decisions-and-draft-operators)
- [Implementation review and unresolved edges](#implementation-review-and-unresolved-edges)

## Exact aggregation rules

A parent's single operator combines **all its direct children**. Children retain their order;
the evaluation mode is part of the result, not a formatting preference.
Use the following algorithms rather than a language's built-in boolean operators.

| Operator family | `optimized` | `complete` |
| --- | --- | --- |
| `AND` | Visit in order. First `false` returns `false`; first `undefined` returns `undefined`; all `true` returns `true`. Skip later children after either early return. | Evaluate every child. Any `false` wins; otherwise any `undefined`; otherwise `true`. |
| `OR` | Evaluate every child. Any `true` wins; otherwise any `undefined`; otherwise `false`. | Same as optimized. |
| `XOR` | Visit in order. First `true` returns `true`; first `undefined` returns `undefined`; all `false` returns `false`. Skip later children after either early return. | Evaluate every child. Any `true` wins; otherwise any `undefined`; otherwise `false`. |
| `NOT_AND`, `NOT_OR`, `NOT_XOR` | Run the corresponding positive operator, then exchange only `true` and `false`. | Same negation rule; preserve the underlying complete-mode traversal. |
| `DELEGATED` | Evaluate every child, then apply the combiner contract below. | Same as optimized. |

Negation preserves `undefined`; it does not negate individual children or turn `ignored` into a
truth value. `NOT_AND(A,B)` is a negation of the aggregate, not a general field for negating B.
For a unary logical negation, a one-child negated parent is structurally possible; choose the
operator and missing-data semantics deliberately.

**RUML `XOR` is not parity and not an exactly-one test.** Its legal modeling premise is that
alternatives are constructed to be exclusive, but the evaluator performs an ordered disjunction.
Two or three true children still yield true. Use a described `DELEGATED` count for an actual
exactly-one constraint. `OR` and `NOT_OR` never short-circuit, even in optimized mode.

`complete` can change the final answer, not just increase detail: an early undefined child blocks
optimized AND/XOR, while a later decisive child can determine complete-mode aggregation.
Do not reorder children for speed without reviewing the resulting semantic change.

Sources: [§3.6 operators](https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/03-data-model/3-6-operators.md), [§3.1 ordered hierarchy](https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/03-data-model/3-1-architecture-principles.md).

## Cases fixed by the conformance suite

Here `T`, `F`, `U`, `I` abbreviate result strings `true`, `false`, `undefined`, `ignored`.
The input column describes the three child results **if evaluated**; it is not a truthy/falsy
coercion of JSON values. The suite's queries map `yes` to true, `no` to false and `unknown` to no
JSONata result using `$lookup({'yes': true, 'no': false}, dp_answer_1)` and analogous inputs.

| Operator | Input children | Optimized parent / recorded children | Complete parent / recorded children |
| --- | --- | --- | --- |
| `AND` | `T,U,F` | `U / T,U,I` | `F / T,U,F` |
| `AND` | `U,F,T` | `U / U,I,I` | `F / U,F,T` |
| `NOT_AND` | `U,F,T` | `U / U,I,I` | `T / U,F,T` |
| `XOR` | `U,T,F` | `U / U,I,I` | `T / U,T,F` |
| `NOT_XOR` | `U,T,F` | `U / U,I,I` | `F / U,T,F` |
| `XOR` | `T,T,T` | `T / T,I,I` | `T / T,T,T` |
| `OR` | `U,T,F` | `T / U,T,F` | `T / U,T,F` |
| `NOT_OR` | `F,U,F` | `U / F,U,F` | `U / F,U,F` |

The delegated fixture means **at least two true children**. Its optimized-mode tests establish:

| Children | Parent | Why it matters |
| --- | --- | --- |
| `T,T,F` | `T` | All three children are evaluated, including the last false one. |
| `F,T,T` | `T` | An early false does not stop a threshold rule. |
| `T,T,U` | `U` | Undefined propagation applies even when two known trues meet the threshold. |
| `F,U,T` | `U` | Evaluation continues after undefined; the combiner itself does not run. |

The last two rows rule out interval-based or optimistic threshold shortcuts. The published delegated
evaluation descriptor covers optimized mode; the specification, not that descriptor, establishes
identical complete-mode obligations. Do not claim tests cover a mode they do not exercise.

Tests: [AND](https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/tests/03-data-model/3-6-operators--and.test.yaml), [NOT_AND](https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/tests/03-data-model/3-6-operators--not-and.test.yaml), [OR](https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/tests/03-data-model/3-6-operators--or.test.yaml), [NOT_OR](https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/tests/03-data-model/3-6-operators--not-or.test.yaml), [XOR](https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/tests/03-data-model/3-6-operators--xor.test.yaml), [NOT_XOR](https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/tests/03-data-model/3-6-operators--not-xor.test.yaml), [DELEGATED](https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/tests/03-data-model/3-6-operators--delegated-evaluation.test.yaml).

## Runtime statuses and reasons

Statuses are serialized strings in `.ruml-result`, never state fields on the source node.

| Status | Meaning | Required reason shape |
| --- | --- | --- |
| `true` | Evaluated and fulfilled | Human-readable string |
| `false` | Evaluated and unfulfilled | Human-readable string |
| `undefined` | Evaluation could not determine an unambiguous result | Object with `type` (`error` or `default`) and nonempty `message` |
| `ignored` | Evaluation deliberately skipped | Object with `type`, nonempty `trigger`, `operator`, `mode` |

An undefined reason uses `error` for technical failure, including a recursion-depth limit, and
`default` for other causes such as missing data. These reason objects do not permit extra fields.
An ignored reason's `type` is `shortCircuit`, `manualSkip` or `conditionalDeactivation`.
For `shortCircuit`, permitted parent operators are `AND`, `NOT_AND`, `XOR`, `NOT_XOR`, `undefined`;
`OR`, `NOT_OR` and `DELEGATED` must not generate such a skip.

An ignored child is **excluded** from parent aggregation; it is not false and not undefined.
Record each directly skipped occurrence, but do not create results for its descendants. A result
map entry requires `lexId`, `status` and `reason`; its key is the occurrence path.

```json
{
  "1.3": {
    "lexId": "40",
    "status": "ignored",
    "reason": {
      "type": "shortCircuit",
      "trigger": "1.2",
      "operator": "AND",
      "mode": "optimized"
    }
  }
}
```

This is a **result-map fragment**. If that skipped LexID has children, no `1.3.1` result is added.
Nodes not yet evaluated or skipped are absent. `pending` is an implicit runtime state, not a fifth
serialized status. A missing entry also needs structural context: an ignored ancestor explains why
its descendants were never entered.

Sources: [§5.0](https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/05-result-format/5-0-status-types.md), [§5.1](https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/05-result-format/5-1-result-model.md), [result schema](https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/schemas/ruml-result.schema.json).

## DELEGATED and the combiner contract

For a node with children, `DELEGATED` and **exactly one** capability of role `combiner` imply each
other. A combiner cannot sit on a leaf or alongside a logical operator. It needs a nonempty prose
`description` in its node payload. The official combiner is `ruml:expression`, declared at root
with explicit `required: true`; omission or false is invalid. Custom combiners require a declared
`combiner` role and required support, reducing portability to tools that implement them.

The evaluator first obtains all child results in the current mode. If any child is undefined,
the parent becomes undefined **without running the combiner**. Otherwise the expression gets the
datapoint input document plus `$children`, an ordered array of direct children containing only
`lexId`, `label` and boolean-status strings. Descendant results and arbitrary node scores are not
implicitly exposed. Nonboolean return values, including no result, produce undefined; for the
official expression a `default` reason should explain the offending value.

| Intended rule | JSONata expression fragment |
| --- | --- |
| At least three satisfied criteria | `$count($children[status = "true"]) >= 3` |
| At most one failure | `$count($children[status = "false"]) <= 1` |
| Strict majority | `$count($children[status = "true"]) * 2 > $count($children)` |
| Exactly one satisfied criterion | `$count($children[status = "true"]) = 1` |
| A specific child failed and another passed | `$children[lexId = "4"].status = "false" and $children[lexId = "5"].status = "true"` |

The exactly-one row is an **Engineering example** of the specified JSONata contract; it is not the
meaning of RUML XOR. A data override inside a combiner cannot bypass the undefined-child guard:
even `dp_override = true or ...` is not evaluated when any child is undefined.
Prefer LexID selectors when identifying a particular child. `$children[0]` is zero-based JSONata
indexing; result paths are one-based. Repeated child LexIDs make identity selection plural, so
review cardinality assumptions before selecting by LexID.

`ruml:expression` result payload contains exactly `expression`, `inputs`, `children`, `result`.
It records child `{lexId, status}` entries in order and relevant resolved datapoints; result is
the string `true`, `false` or `undefined`. It does not carry arbitrary additional fields.
Expressions should be deterministic, but `$random`, `$now`, `$millis` and `$eval` are permitted.
The generic combiner contract recommends recording nondeterministic draws; §4.14 explicitly says
the official payload does not record them. Do not promise replayability or invent a `randomValues`
field. Prefer named, captured datapoint inputs when reproducibility is a project requirement.

The official expression cannot be delivered via `.ruml-ext`. Its rule belongs in the base document.
Planned numeric values from child subtrees are explicitly outside this version; do not implement
`$children[].score` or node-local computed outputs as standard RUML fields.

Sources: [§3.6.4](https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/03-data-model/3-6-operators.md#364-the-delegated-operator), [§4.14](https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/04-capabilities/4-14-ruml-expression.md), [combiner validation tests](https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/tests/03-data-model/3-6-operators--delegate.test.yaml).

## Leaf decisions and draft operators

`ruml:query` is a leaf decision capability. Its expression uses **JSONata 2.2.0**, not JavaScript,
SQL or an unspecified expression language. Input is a JSON object keyed by declared datapoint IDs;
missing values have no entry. Only a JSON boolean answer decides the node. Numbers, strings,
objects, null and no result must not be coerced to a boolean status.

When multiple decision entries exist on a leaf, `decisionMode` belongs on the node:

- `fallback` (default): in capability-list order, take the first true/false; continue on undefined.
- `agreement`: evaluate all; disagreement gives undefined.
- `majority`: evaluate all; a tie gives undefined.

This setting is ignored on parents. Preserve node capability order; it is semantically significant.
Do not substitute `decisionMode` for a parent's aggregation operator.
In drafts, any allowed leaf operator is ignored, including `DELEGATED` without a combiner.
Outside drafts, leaves must omit operators and no node may use the `undefined` operator.

Sources: [§4.8](https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/04-capabilities/4-8-ruml-query.md), [§4.3 decisionMode](https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/04-capabilities/4-3-capabilities-node-field.md), [§3.6.5](https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/03-data-model/3-6-operators.md#365-the-undefined-operator).

## Implementation review and unresolved edges

**Engineering advice:** represent final status as an explicit enum and centralize the positive
aggregation algorithms plus boolean-only negation. Verify mode, ordered visitation, parent result,
ignored entries and absence of ignored descendants together. Test trace behavior, not only root
truth. Do not memoize results solely by node UUID or LexID; modular occurrences can have different
inputs and outcomes. See [modules-and-recursion.md](modules-and-recursion.md).

The pinned text does not fully define parent evaluation for the draft `undefined` operator,
aggregation when every child is manually ignored, or how undefined votes affect every mixed
`agreement`/`majority` case. The published operator fixtures do not settle these edges.
Likewise, the combiner's boolean-only `$children` contract needs an explicit policy for manually
ignored children. Distinguish any documented engine policy from interoperable RUML guarantees;
use a small reproducible case when reporting an upstream gap. Do not quietly invent truth tables.

Sources: [§3.6](https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/03-data-model/3-6-operators.md), [§4.3](https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/04-capabilities/4-3-capabilities-node-field.md), [§5.0](https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/05-result-format/5-0-status-types.md).
