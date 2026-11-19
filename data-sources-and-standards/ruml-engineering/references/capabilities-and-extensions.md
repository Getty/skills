<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# Capabilities and extensions

Evidence: official RUML specification release 1.0.0 (2026-11-15), commit `d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4`. Files declare `$specVersion: "1.0"`; the release label is not the file value.
Normative statements below summarize the pinned specification. **Implementation recommendation** and **Snapshot gap** identify guidance or incompleteness rather than additional RUML requirements.

## Contents

- [Declaration and use](#declaration-and-use)
- [Roles and multiplicity](#roles-and-multiplicity)
- [Complete official registry](#complete-official-registry)
- [Namespaces and unsupported capabilities](#namespaces-and-unsupported-capabilities)
- [Ordered evaluation](#ordered-evaluation)
- [Inline and sidecar delivery](#inline-and-sidecar-delivery)
- [Merge procedure](#merge-procedure)
- [Implementation boundaries](#implementation-boundaries)
- [Evidence and tests](#evidence-and-tests)

## Declaration and use

RUML's core describes a rule structure; capabilities add typed inputs, executable decisions, supporting material, and reactions. A capability identifier is a declaration of a contract, not an instruction to download or install code. [C1]

There are two distinct locations:

| Location | Entry shape | Meaning |
| --- | --- | --- |
| Root `capabilities` | `{ "id": ..., "required"?: ..., "role"?: ..., "payload"?: ... }` | Declare a capability and its global artifacts/configuration |
| Node `capabilities` | `{ "id": ..., "payload": ... }` in an ordered array | Apply that declared capability to the node |

Every node entry needs both `id` and an object `payload`; arrays, primitives, and `null` are invalid payloads. Root entries may omit `payload`. Do not move `required` or `role` onto a node entry. [C2][C3]

Root capability identifiers are unique, including third-party identifiers. A node identifier must resolve to a root declaration even when the parser does not implement it. If root `capabilities` is absent or empty, every node must omit the field entirely; an empty node array still violates CAP-14. [C2]

`payload.data` is a named-artifact map for capabilities that define one; `payload.config` is global configuration where specified. These are conventions, not permission to invent fields on each official payload. `ruml:datapoints` additionally defines `payload.sets`. Tree-reference and tree-include root entries prohibit `payload`. [C2][C7]

**Implementation recommendation:** build a declaration index before traversing nodes. Retain the original ordered arrays separately from that lookup index, because a dictionary cannot preserve repeated node uses of the same decision or reaction identifier.

## Roles and multiplicity

Official roles are fixed by the specification and **must not** be declared in an official root entry. Every `ruml:draft/...` or reverse-domain root entry **must** declare one of the four roles. An implementation that recognizes the identifier must reject a role that conflicts with its implementation. [C1]

| Role | Placement | Repetition of one identifier on a node | Effect |
| --- | --- | --- | --- |
| `data` | As allowed by the capability's scope | At most once | Supplies material or input definitions |
| `decision` | Leaves only | Allowed | Returns a leaf decision |
| `combiner` | A parent with `operator: "DELEGATED"` | Exactly one combiner overall when the parent has children | Combines direct child results |
| `reaction` | As allowed by the capability's scope | Allowed | Reacts to an evaluated status |

Role permission does not override capability scope: `ruml:protocol` is a reaction but has no node payload; `ruml:datapoints` currently defines its data at root. The future node-scoped computed-datapoint extension described in §4.14 is not implemented by the published format. [C1][C7]

A capability has exactly one role. A provider offering equivalent logic as both a leaf decision and a parent combiner needs two identifiers. Multiple data capabilities with different identifiers may coexist. The prohibition counts repeated identifiers, not repeated roles. [C1][C3]

Decision and combiner contracts yield `true`, `false`, or `undefined`. A combiner cannot be substituted for a leaf decision. A nonempty `DELEGATED` node needs exactly one combiner and its prose description; its children are evaluated before the combiner runs. [C1][C7]

## Complete official registry

The following ten identifiers are the complete official set in this snapshot. The default `required` is `false` except for `ruml:expression`, which must explicitly set it to `true`. [C4][C7]

| Identifier | Role | Root use | Node use / principal distinction |
| --- | --- | --- | --- |
| `ruml:datapoints` | `data` | `payload.data`, optional `payload.sets` | No standardized node-scoped value definition |
| `ruml:query` | `decision` | Declaration | JSONata expression on a leaf |
| `ruml:ai-query` | `decision` | Declaration; optional `payload.config.systemPrompt` | Symbolic model, prompt, selected inputs, execution hints |
| `ruml:actions` | `reaction` | Declaration | `onTrue`, `onFalse`, `onUndefined` handlers |
| `ruml:context` | `data` | `payload.data` context pool | `payload.refs` referring to context IDs |
| `ruml:text-reference` | `data` | `payload.data` text pool | Local text anchors in `payload.refs` |
| `ruml:protocol` | `reaction` | Declaration; optional `payload.config.level` | Forbidden on rule nodes; result protocol is evaluation-level |
| `ruml:expression` | `combiner` | Declaration with `required: true` | JSONata combiner on nonempty `DELEGATED` parent |
| `ruml:tree-reference` | `data` | Declaration without payload | References another file's nodes without evaluating them |
| `ruml:tree-include` | `decision` | Declaration without payload | Evaluates another file's subtree in place of a leaf |

`ruml:text-reference` anchors into the same file's text pool. `ruml:tree-reference` and `ruml:tree-include` use immutable-version node URIs of other files. A reference is descriptive; an include participates in evaluation. Include input sharing is explicitly undefined in this version. [C7]

See [datapoints-and-jsonata.md](datapoints-and-jsonata.md), [ai-actions-and-context.md](ai-actions-and-context.md), and [results-and-provenance.md](results-and-provenance.md) for payload details.

## Namespaces and unsupported capabilities

| Namespace | Status | Validation consequence |
| --- | --- | --- |
| `ruml:<official-name>` | Reserved official contract | An identifier absent from this version's registry is invalid, regardless of `required` |
| `ruml:draft/<name>` | Experimental RUML namespace | Non-official role declaration required; changes may be incompatible |
| `<reverse-domain>/<name>` | Provider-defined contract | Non-official role declaration required; provider owns the domain hierarchy |

Identifiers are lowercase, contain no whitespace, and have at most 128 characters. Local/hierarchical components use letters, digits, `_`, and `-`; namespace separators include `.`, `:`, and `/`. Use the published patterns, not a generic URI validator. [C4][C8]

The pinned schema accepts draft IDs matching `^ruml:draft(?:/[a-z0-9_-]+)+$` and reverse-domain IDs matching `^[a-z0-9_-]+(?:\.[a-z0-9_-]+)+(?:/[a-z0-9_-]+)+$`. Pattern acceptance does not establish ownership of the declared provider domain. [C8]

An experimental identifier becoming official receives a new identifier; migration is not an automatic alias. The specification advises against production reliance on required experimental capabilities. [C4]

| Capability support | `required` | Required behavior |
| --- | --- | --- |
| Supported | Either value | Validate its specified payload and semantics |
| Unsupported but permitted namespace | `true` | Reject with an error naming the identifier; no silent partial processing |
| Unsupported but permitted namespace | `false` or absent | Ignore its payload and node data; continue; warning recommended |
| Unrecognized reserved official `ruml:` identifier | Either value | Reject as invalid namespace use |

`required: false` is not a request to ignore a supported capability. `required: true` is not a grant of filesystem, network, credential, or side-effect privileges. The latter are runtime controls outside the declaration mechanism. [C2]

## Ordered evaluation

Node capability arrays have meaningful order. Tools must preserve it and must not sort entries by identifier. Reordering can change fallback decisions and reaction order. Repeated decisions and reactions are valid inline and must not be deduplicated. [C3]

`decisionMode` belongs to the node, outside its capability entries:

- `fallback` is the default: evaluate decisions in list order; the first `true` or `false` decides; continue after `undefined`.
- `agreement` evaluates all decisions and yields `undefined` on disagreement.
- `majority` evaluates all decisions and yields `undefined` on a tie.
- Parent nodes ignore `decisionMode`; a leaf with one decision gains nothing from setting it. [C3]

**Snapshot gap:** the complete treatment of `undefined` votes in `majority`, and all mixed cases in `agreement`, is not stated as a truth table. Do not invent a purported standard rule such as discarding all undecidable votes. Record the chosen runtime interpretation and obtain interoperability agreement where it matters.

**Snapshot discrepancy:** §4.6 says root declaration order is insignificant, while the schema descriptions of `Capabilities` and `CapabilityEntry` call it significant. Preserve root order when round-tripping; derive execution order from node arrays, not root declarations. [C6][C8]

## Inline and sidecar delivery

Delivery is a packaging choice. There is no generic `delivery` field in the root capability entry. Inline data is part of the base file and therefore covered when that file is hashed or signed. A sidecar is a separate document with separate identity binding and optional container protection. [C1][C5]

A `.ruml-ext` document requires exactly the root fields `$format`, `$specVersion`, `$base`, `capabilities`, and `nodes`; the discriminator is `RUML-EXT`. `metadata`, `rulemap`, and `evaluation` are not sidecar root fields. [C5][C9]

The important shape difference is:

```json
{
  "nodes": {
    "0eb360a6-626a-406d-89a1-9f434ced141b": {
      "ruml:query": { "expression": "age >= 18" }
    }
  }
}
```

This is a **fragment**, not a complete sidecar. Its node key is the base node's UUID, and its inner key is a capability ID; the value is the payload directly. It is not the inline `{id,payload}` array shape. [C5][C9]

Root sidecar artifacts still travel inside the declaring capability's `payload.data` or other defined payload fields. They do not become new root fields. Every sidecar node UUID must exist in the base, and each inner capability ID must be declared by the sidecar. [C5]

`ruml:expression` cannot appear in a sidecar. Its parent combiner belongs in the base; a second combiner would violate the `DELEGATED` contract. `ruml:protocol` may be declared at root but cannot be attached to a sidecar node. [C7][C9]

## Merge procedure

Normative checks from §4.5 must precede application of extension data:

1. Validate the sidecar discriminator, supported specification version, and schema.
2. Match `$base.id` to the base file's `metadata.id`.
3. Canonicalize the base using RFC 8785 and compute the declared hash.
4. Require exact equality with `$base.hash`; abort the merge on mismatch.
5. Resolve every sidecar node UUID to an existing base node.
6. Reject any `(node UUID, capability ID)` already present inline or supplied by another sidecar.
7. Check declarations, role constraints, payload schemas, and resulting references for the combined view. [C5]

Steps 1–6 summarize explicit format/merge requirements; step 7 is the practical way to enforce the obligations that remain after composition. Each sidecar must be checked independently against the original base. Do not hash a previously merged in-memory view as though it were the signed base.

`$base.hash` uses `<algorithm>:<hex>`. The sidecar schema permits exactly `sha3-256`, `sha256`, or `blake3`, followed by 64 lowercase hexadecimal digits. It is not a manifest-style `{algorithm,value}` object. [C9]

The base hash comparison cannot be disabled by a development mode or an explicit override under the published rules. To adapt a stale sidecar, review it against the changed base and create an updated artifact; do not claim the old sidecar was validly merged. [C5]

Conflicts are errors, even when a node's role would allow repeated inline decisions or reactions. Sidecar objects also cannot encode repeated identical keys as a supported repetition mechanism. Silent overwrite, last-writer-wins, and deep merge are not specified conflict policies. [C5]

**Snapshot gap:** the format does not fully define ordering when unordered sidecar capability maps are combined with ordered inline lists, nor every root artifact/configuration collision. A concrete merger needs an explicitly documented composition policy. Avoid assuming JSON object member order supplies a normative fallback order.

## Implementation boundaries

**Implementation recommendation:** keep the immutable base, each verified sidecar, and the effective runtime view as distinguishable objects. Report the base digest, sidecar digests, merge policy, and capability implementation versions in deployment records.

Schema validation cannot prove domain ownership, implementation support, arbitrary custom-ID uniqueness, referenced-node existence, base hash equality, or all role compatibility. Those require semantic or runtime checks. A complete RUML validator covers every schema and semantic rule in Chapter 8, including capabilities. [C6]

Read `$format` and `$specVersion`, then declarations, before structurally processing the rulemap; this enables rejection of unsupported required capabilities before partial evaluation. Do not execute capability code merely to discover whether its declaration is acceptable. [C6]

For custom capabilities, document identifier ownership, role, payload schema, supported versions, input/output contract, deterministic behavior, error mapping, and any effects. These are implementation documentation practices; RUML does not supply a universal plugin ABI or executable extension package format.

## Evidence and tests

The upstream §4.2 tests cover custom roles, duplicate official/custom declarations, and an empty node array without root declarations. The §4.3 tests distinguish repeated decisions from repeated data capabilities, undeclared IDs, absent payloads, and forbidden node-level protocol entries. They do not establish a complete sidecar merge ordering. [C10]

[C1]: https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/04-capabilities/4-1-concept.md
[C2]: https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/04-capabilities/4-2-capabilities-field.md
[C3]: https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/04-capabilities/4-3-capabilities-node-field.md
[C4]: https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/04-capabilities/4-4-namespaces.md
[C5]: https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/04-capabilities/4-5-ruml-ext.md
[C6]: https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/04-capabilities/4-6-parser-obligations.md
[C7]: https://github.com/Law-as-Code-Institute/ruml/tree/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/04-capabilities
[C8]: https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/schemas/ruml.schema.json
[C9]: https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/schemas/ruml-ext.schema.json
[C10]: https://github.com/Law-as-Code-Institute/ruml/tree/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/tests/04-capabilities
