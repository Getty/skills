<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# RUML modular nodes, occurrence contexts and recursion

Baseline: specification **1.0.0**, wire version **`"1.0"`** at commit
`d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4`.
Reference text adapts the specification © 2026 Rulemapping Group GmbH, **CC BY-SA-4.0**;
linked schema/test material is **Apache-2.0**. See [upstream licence](https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/LICENSE.md).
**Engineering advice** identifies host-runtime design choices that the format does not standardize.

## Contents

- [Definition versus occurrence](#definition-versus-occurrence)
- [Static references and modular flags](#static-references-and-modular-flags)
- [Binding inputs for each occurrence](#binding-inputs-for-each-occurrence)
- [Direct recursion and termination](#direct-recursion-and-termination)
- [Nesting and external reuse](#nesting-and-external-reuse)
- [Checks, coverage and specification gaps](#checks-coverage-and-specification-gaps)

## Definition versus occurrence

RUML stores a reusable node **once** and reaches it through multiple child references. Reuse shares
the definition, not the evaluation result. Label, operator, child order, capabilities and normative
text anchors remain the same at every use. An occurrence's inputs and outcome may differ.

| Identity | What it identifies | Correct storage/use |
| --- | --- | --- |
| LexID, e.g. `"8"` | A node definition inside one document | `nodes` key and child reference |
| UUID v4 in `id` | The node's external identity | Cross-document references and overlays |
| Path, e.g. `"1.2.1"` | One runtime occurrence | Result-map key and execution context |

Path segments after the root are **one-based child-array positions**, never LexIDs. A repeated
LexID therefore has multiple paths. The source node contains no `path` or `lexId` field, but each
result entry must contain `lexId` to map its occurrence back to the source definition.

**Engineering advice:** keep immutable definitions separate from runtime frames. A useful internal
frame contains document identity/version, LexID, occurrence path, resolved inputs and recursion
counters. This is an implementation data structure, not a proposed RUML extension. Store the final
result by occurrence path; a cache keyed only by UUID or LexID incorrectly merges distinct cases.

Sources: [§2.5](https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/02-file-format-basics/2-5-identifier-system.md), [§6.3](https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/06-modular-nodes/6-3-evaluation.md), [§5.1](https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/05-result-format/5-1-result-model.md).

## Static references and modular flags

**Specification:** a node is modular when its LexID occurs more than once across the document's
`children` arrays. Count entries, not distinct parents. A self-reference counts. Such a node must
have `modular: true`; a node referenced only once should not have the flag, but is not invalid
merely because it does. Multiple references never create duplicate entries in `nodes`.

This original **structure table**, not a full RUML file, illustrates the distinction:

| LexID | Children | Operator | `modular` | Role |
| --- | --- | --- | --- | --- |
| `"1"` | `["8", "20"]` | `AND` | Omitted | Root |
| `"8"` | `["9"]` | `AND` | `true` | Shared check |
| `"9"` | Omitted | Omitted | Omitted | Leaf inside shared check |
| `"20"` | `["8"]` | `OR` | Omitted | Alternative use |

Every actual node also needs a unique UUID and label. LexID `"8"` appears twice in static child
arrays, so it is modular. LexID `"9"` appears only once statically, yet it is evaluated separately
under both occurrences of `"8"`:

| Occurrence path | LexID | Context |
| --- | --- | --- |
| `1.1` | `"8"` | Direct root use |
| `1.1.1` | `"9"` | Leaf in direct use |
| `1.2.1` | `"8"` | Use through LexID `"20"` |
| `1.2.1.1` | `"9"` | Leaf in alternative use |

Do not mark every descendant of a modular subtree as modular just because it has multiple runtime
occurrences. Conversely, `["8", "8"]` in one parent's array requires `"8"` to be modular and
creates two distinct positions. Duplicate child references are discouraged, not automatically
rejected when the flag is correct; the conformance test expects acceptance with a warning.

Sources: [§6.2](https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/06-modular-nodes/6-2-implementation.md), [modular tests](https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/tests/06-modular-nodes/6-2-implementation.test.yaml), [duplicate-child test](https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/tests/03-data-model/3-5-node-object.test.yaml).

## Binding inputs for each occurrence

**Specification:** §6.3 requires the evaluator to consider the path by which a modular node is
reached. `ruml:query` runs against a JSON input document keyed by datapoint IDs. A datapoint's
`binding.type` is `input`, `external` or `computed`; an external binding's symbolic `ref` is mapped
to a concrete service in tool configuration, not by embedding that configuration in the rulemap.

These rules do **not** define a standard call-argument field on child references. Children are
LexID strings, not objects with per-call `bindings`. Nor does chapter 6 define automatic variable
rebinding, iteration indexes, inherited mutable state or a recursive state-advance expression.
Do not invent `arguments`, `contextBinding`, `iteration`, `parent` or similar core node fields.

**Engineering advice:** define an explicit host adapter for a repeated check. For example, a
reviewer-check occurrence may receive different person records at `1.1` and `1.2.1`; the adapter
must state which record each path sees and record the resolved datapoint values used by queries.
If no adapter supplies distinct inputs, reuse alone does not manufacture a different data context.
Prefer a stable mapping from domain instance identity to runtime frame over positional guesses.
Review that mapping whenever child order changes, because path-based configuration may shift.

`ruml:context` is also not a generic runtime variable scope. It supplies reference material or
documents under examination. Its node-level `payload.refs` selects context IDs; `subject: true`
identifies material being assessed. Keep that documented capability distinct from the evaluator's
internal occurrence context and from actual datapoint values.

A module's `ruml:text-reference` anchors remain properties of its definition. Every use represents
the same norm. If two similar checks implement different normative anchors, use distinct
definitions or a deliberately modeled shared sub-check; do not patch anchors per occurrence.

Sources: [§6.2](https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/06-modular-nodes/6-2-implementation.md), [§6.3](https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/06-modular-nodes/6-3-evaluation.md), [§4.7 bindings](https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/04-capabilities/4-7-data-points.md#472-binding-types), [§4.8 input document](https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/04-capabilities/4-8-ruml-query.md), [§4.11 context](https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/04-capabilities/4-11-ruml-context.md).

## Direct recursion and termination

A recursive node is modular and lists **its own LexID** in `children`. For example, a node
`"4"` with `operator: "XOR"`, `modular: true`, `children: ["5", "6", "4"]` checks two exit
conditions before entering another occurrence of itself. The node still appears only once in
`nodes`; runtime expansion creates the distinct paths.

The required structural rules are:

- A self-referencing node must have `modular: true`.
- The self-reference must not be the first child (`MOD-04`).
- At least one child must not be a self-reference (`MOD-05`).
- Processors must warn for recursive `AND`, `NOT_AND`, `OR` or `NOT_OR` (`MOD-03`). This warning
  alone does **not** invalidate the file.

The recommended exit pattern is `XOR` or `NOT_XOR` with a nonrecursive exit condition before the
self-reference. In **optimized** mode, a true earlier child prevents recursion. An earlier
undefined child also stops optimized evaluation, with an undefined result. The operator name and
child position alone do not prove an exit will eventually become true.

Implementations must impose a maximum recursion depth; the specified default is **500**, and it
should be configurable. Count self-reference traversals, not total path length. The first
occurrence is depth 0; with limit `n`, depths 0 through `n` are evaluated, and the occurrence at
`n + 1` receives undefined with reason type `error`. The error is logged.

| Path in the example | LexID | Self-recursion depth |
| --- | --- | --- |
| `1.2` | `"4"` | 0 |
| `1.2.3` | `"4"` | 1 |
| `1.2.3.3` | `"4"` | 2 |

If the limit is 1, `1.2.3.3` is the over-limit instance. Its result can use:

```json
{
  "lexId": "4",
  "status": "undefined",
  "reason": {
    "type": "error",
    "message": "Recursion depth 2 exceeds the maximum recursion depth of 1"
  }
}
```

The limit applies to that occurrence; ancestor results then follow their operators. Do not force
the entire root undefined without applying aggregation rules.

**Important specification interaction:** complete mode evaluates every child and therefore cannot
use the earlier true child to avoid self-reference. Chapter 6's safe-recursion rationale assumes
early exit and does not resolve this tension. Use the depth limit in complete mode and report the
mode-dependent trace. Never promise finite exhaustive unrolling of an unbounded recursive graph.

**Engineering advice:** for a multi-round process, document what changes input between rounds and
what provides an exit. A deterministic exit test on unchanged input can recurse until the bound.
Use explicit runtime frames or an iterative stack to avoid exhausting the language call stack
before the RUML limit. Separate operational budgets from the standard's own depth semantics.

Sources: [§6.4 recursion](https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/06-modular-nodes/6-4-recursion.md), [§3.6 modes](https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/03-data-model/3-6-operators.md), [§5.0 error reasons](https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/05-result-format/5-0-status-types.md).

## Nesting and external reuse

Modular nodes may contain other modular nodes, and an inner module may also be referenced
independently. The specification places no inherent limit on modular **nesting** depth. This is
distinct from the mandatory limit on recursive self-reference depth. A small definition graph can
expand into many runtime occurrences; size planning must count occurrences as well as definitions.

Keep three reuse mechanisms separate: `modular: true` reuses a definition inside one file;
`ruml:tree-reference` links to nodes in another versioned file; `ruml:tree-include` evaluates an
external subtree through an including leaf. Cross-file reference cycles are permitted, while
inclusion cycles are prohibited. Neither capability turns `children` into external URI references.

Sources: [§6.5](https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/06-modular-nodes/6-5-nesting.md), [§4.15](https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/04-capabilities/4-15-ruml-tree-reference.md), [§4.16](https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/04-capabilities/4-16-ruml-tree-include.md).

## Checks, coverage and specification gaps

**Engineering advice:** verify static reference counts separately from runtime paths. For reused
subtrees, test different inputs and different results at two paths, including descendant paths.
For recursion, test an immediate exit, a later exit, undefined before recursion, the exact depth
boundary and complete mode. Check that skipped subtree descendants have no result entries.

The pinned `tests/06-modular-nodes` directory contains the §6.2 reference-count fixtures, not a
runtime suite proving recursive context rebinding or depth behavior. Derive those checks from the
specification and label added engine tests accordingly. The text does not fully specify arbitrary
mutual cycles such as A → B → A; do not claim that the direct-self-reference rules settle them.

§5.1's summary that regular nodes have exactly one path needs qualification for descendants of a
reused subtree: §6.2 defines modularity by direct static references, while §6.5 allows expanded
occurrences. Preserve both identities rather than propagating flags to make the summary literal.

Sources: [§6.2 tests](https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/tests/06-modular-nodes/6-2-implementation.test.yaml), [§6.4](https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/06-modular-nodes/6-4-recursion.md), [§5.1](https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/05-result-format/5-1-result-model.md).
