<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# RUML core data model

Baseline: RUML specification **1.0.0**, dated 2026-11-15; wire version **`"1.0"`**.
Specification commit `d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4`.
This reference adapts specification text © 2026 Rulemapping Group GmbH under **CC BY-SA-4.0**.
The linked schemas, fixtures and tests are **Apache-2.0**; see the upstream [licence statement](https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/LICENSE.md).
Statements labelled **Engineering advice** describe a workflow, not additional RUML requirements.

## Contents

- [Document envelope and layers](#document-envelope-and-layers)
- [Three identities](#three-identities)
- [Nodes and graph integrity](#nodes-and-graph-integrity)
- [Metadata, versions and time](#metadata-versions-and-time)
- [Lifecycle and working copies](#lifecycle-and-working-copies)
- [Draft and release checks](#draft-and-release-checks)
- [Validation boundaries and source discrepancies](#validation-boundaries-and-source-discrepancies)

## Document envelope and layers

**Specification:** `.ruml` is UTF-8 JSON with a root object. Write `$format` and `$specVersion`
as its first two properties, in that order (`FMT-05`). The required root fields are `$format`,
`$specVersion`, `metadata` and `rulemap`; `capabilities` is optional. No other root fields are allowed.
At this baseline, `$format` is `"RUML"` and the schema accepts only `$specVersion: "1.0"`.

| Layer | RUML location | Responsibility |
| --- | --- | --- |
| Document identity and lifecycle | `metadata` | Version, authoring times, status, descriptive information |
| Decision structure | `rulemap.nodes` | Flat node map and ordered child references |
| Declared extensions | Root and node `capabilities` arrays | Typed inputs, queries, sources, reactions and other specified extensions |
| Evaluation | Separate `.ruml-result` | Results for particular runtime occurrences |
| Integrity packaging | Separate `.rumlc` container | Hashes, signatures and encryption |

`rulemap` currently has exactly one field: `nodes`. Do not move document title, type or evaluation
state into it. Do not add a hash or signature of the document to `metadata`.

This is a complete **structural draft**, not an executable decision:

```json
{
  "$format": "RUML",
  "$specVersion": "1.0",
  "metadata": {
    "id": "8453e23e-9716-497e-a917-1d01e7e9ec80",
    "version": "0.1.0",
    "created": "2026-11-19T00:00:00Z",
    "modified": "2026-11-19T00:00:00Z",
    "status": "draft"
  },
  "rulemap": {
    "nodes": {
      "1": {
        "id": "c538d61d-3338-49ae-85d8-b6372da0b197",
        "label": "Decision to be modeled"
      }
    }
  }
}
```

Sources: [§2.1](https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/02-file-format-basics/2-1-general-properties.md), [§2.2](https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/02-file-format-basics/2-2-file-structure.md), [§3.4](https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/03-data-model/3-4-rulemap-object.md), [schema](https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/schemas/ruml.schema.json).

## Three identities

| Identifier | Example | Scope and use |
| --- | --- | --- |
| LexID | `"12"` | A `rulemap.nodes` key and a reference in `children`; local to one document |
| UUID v4 | `c538d61d-3338-49ae-85d8-b6372da0b197` | `metadata.id` or a node's `id`; used for external identity |
| Occurrence path | `"1.2.1"` | Runtime position: first child of the root's second child; key in result records |

LexIDs match `^[1-9][0-9]*$`; they are **strings**, including inside `children`. `"0"`, `"01"`,
negative values and JSON numbers are invalid. Root is always `nodes["1"]`; gaps are permitted.
The node's LexID is its map key: a node must not repeat it as a `lexId` field.

UUIDs must be lowercase **version 4**, not arbitrary UUID strings. Node UUIDs must be distinct from
each other and from `metadata.id` (`NODE-08`). An external reference may repeat the target's UUID;
the uniqueness rule concerns definitions, not references. Generate new identities with a UUID v4
library rather than hand editing version/variant bits.

A path contains **one-based child indexes**, not LexIDs. If `children` is `["8", "20"]`, `1.2`
identifies the occurrence of LexID `"20"`. Moving a child changes occurrence paths. It does not
automatically change the node UUID or LexID. Paths are not permitted fields on RUML node definitions.

Sources: [§2.5](https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/02-file-format-basics/2-5-identifier-system.md), [§3.5](https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/03-data-model/3-5-node-object.md), [§5.1](https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/05-result-format/5-1-result-model.md), [identifier tests](https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/tests/02-file-format-basics/2-5-identifier-system.test.yaml).

## Nodes and graph integrity

**Specification:** all node definitions belong in one flat map. `children` holds ordered LexID
references, never embedded node objects. Relationships point from a parent to direct children;
nodes must not store parent pointers, explicit node types or derived positions.

- Every node needs `id` and a nonempty `label` (`NODE-01`, `NODE-09`).
- A parent has a nonempty `children` array and one `operator` for **all** direct children.
- A leaf omits `children`; `children: []` is invalid (`NODE-06`).
- Every referenced LexID must exist (`NODE-10`). No `children` array may contain `"1"` (`NODE-05`).
- Optional node fields are `altText`, `description`, `capabilities`, `metadata`, `decisionMode`,
  `modular`, plus `children`/`operator` subject to their structural rules.
- `description` is limited to 10,000 characters. Node `metadata` is for nonstructural information.
- Preserve `children` order when loading, editing and serializing (`NODE-04`). Reordering may
  change both evaluation and result paths.
- A LexID referenced more than once needs `modular: true`, including two references from one
  parent. Do not deduplicate child arrays automatically. Duplicate references are discouraged,
  but accepted with a warning when the target is modular.

**Engineering advice:** build a LexID index, UUID index and static incoming-reference counts in one
pass; validate edges in a second pass. Inspect unreachable nodes and indirect cycles separately.
Do not claim that every unreachable node or every cycle is forbidden by the pinned core rules:
explicit self-recursion is supported, and not every graph pathology has a specified rejection rule.
See [modules-and-recursion.md](modules-and-recursion.md) before imposing a tree-only validator.

Sources: [§3.1](https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/03-data-model/3-1-architecture-principles.md), [§3.5](https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/03-data-model/3-5-node-object.md), [node tests](https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/tests/03-data-model/3-5-node-object.test.yaml), [§8 node/modular rules](https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/08-validation/index.md).

## Metadata, versions and time

The five required metadata fields are `id`, `version`, `created`, `modified` and `status`.
`modified` must be at least `created`. Update `modified` and revalidate structure on every change.
Timestamps use RFC 3339 `date-time`, including `Z` or an explicit UTC offset; compare parsed instants,
not textual strings. If both validity bounds exist, `validUntil` must be strictly after `validFrom`.

`$specVersion` and `metadata.version` are independent. The first has major/minor components only;
specification patch release `1.0.0` still uses `"1.0"` on the wire. Content version is a free-form
string. The spec recommends SemVer for rulemaps, a version date for laws, and a tag-compatible
pattern `[A-Za-z0-9_][A-Za-z0-9._-]{0,127}`. These recommendations are not schema requirements.

A parser accepts its major version and minor versions no higher than its own. A different major or
higher minor must fail clearly. For a base file plus overlays, evaluation's input version is the
highest `$specVersion` among them; the result declares that input version and preserves its behavior.

Optional metadata includes title, description, authors, publishing organization, jurisdiction,
legal domain, tags, language, validity dates, replacement links, derivation and comment.
If `authors` appears, it has at least one object and each has `name`. An author's organization is
an affiliation; `metadata.organization` is the publisher responsible for the document.
Jurisdiction begins with an ISO 3166-1 alpha-2 code and may have hyphenated subdivisions.
Language is an ISO 639-1 code; a two-letter regex alone cannot verify actual code membership.

`documentType` is optional and has these exact values: `law`, `regulation`, `guideline`, `decision`,
`procedure`, `form`, `documentGeneration`, `other`. There is no `rulemap.type` substitute.

Sources: [§2.3](https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/02-file-format-basics/2-3-versioning.md), [§3.2](https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/03-data-model/3-2-data-types-and-formats.md), [§3.3](https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/03-data-model/3-3-metadata-object.md), [§3.8](https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/03-data-model/3-8-integrity-validation.md).

## Lifecycle and working copies

| `metadata.status` | Required condition | Specification recommendation |
| --- | --- | --- |
| `draft` | No extra lifecycle field | Unfinished operators may be present |
| `review` | Normal nondraft structure | Supply `authors` |
| `approved` | Normal nondraft structure | Supply publishing `organization` |
| `inForce` | `validFrom` | Supply `jurisdiction`; avoid modifying the original |
| `suspended` | Normal nondraft structure | Supply `validUntil` or `comment` |
| `expired` | `validUntil`, in the past | Evaluate relative to an explicit validation clock |
| `replaced` | `replacedBy` | This status cannot be changed back to another status |

The validation-clock recommendation above is **Engineering advice**; the other required conditions
are normative. Recheck status on every content change. `replaces` and `replacedBy` may coexist.
There is no `published` status: use that word as a workflow description, not a new enum value.

For a working copy of an `inForce` document: assign a **new document UUID**, set status to `draft`
and record `derivedFrom`. That object requires `originalId`, `originalStatus`, `derivationType`
and `derivedAt`; `derivationType` is `workingCopy`, `amendment` or `revision`. `originalHash` is
optional and `derivedBy` recommended. A document marked `workingCopy` must not be `inForce`.
The specification does not turn this into an instruction to regenerate every node UUID: decide
node identity deliberately so existing references remain understandable.

Sources: [§3.3 lifecycle and working copies](https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/03-data-model/3-3-metadata-object.md), [suspended-with-comment test](https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/tests/03-data-model/3-3-metadata-object.test.yaml).

## Draft and release checks

**Specification:** a parent always needs an operator. `operator: "undefined"` is permitted only
in `draft`; it is a literal enum string, not JSON null or a runtime result. A draft leaf may carry
any allowed operator, including `DELEGATED`; evaluation ignores that leaf operator. Outside
`draft`, a leaf must omit `operator` entirely, and no node may use `"undefined"` as its operator.

**Engineering advice:** before moving to review, resolve every structural placeholder, remove leaf
operators, verify capability support, review interpretation and run scenario tests. Structural
validity does not mean all leaves have a decision mechanism or all runtime data will be available.
A draft is not a general exemption from UUID, reference, capability or metadata rules.

Sources: [§3.6](https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/03-data-model/3-6-operators.md), [leaf-operator tests](https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/tests/03-data-model/3-5-node-object.test.yaml).

## Validation boundaries and source discrepancies

Use draft-2020-12 schema validation **with format assertions**, then semantic checks for UUID
uniqueness, references, timestamp ordering, code membership and modular counts. A schema-only pass
cannot establish full RUML validity. Preserve object-member information while parsing to detect
duplicate LexID keys; a parser that silently overwrites duplicates loses the evidence for `FMT-12`.
History-dependent rules, such as refusing reversal of `replaced`, also need the prior version.

At the pinned revision, §3.2.6 still illustrates registry locations as `capabilities[].data`.
The schema and current capability declarations use **`capabilities[].payload.data`**. Treat this
as an upstream prose discrepancy, not permission for both formats. Several explanatory pages
mention runtime `pending`; §5.0–5.1 and the result schema require omission of pending entries,
not serialization of a fifth status. The complete §4.8 example duplicates `metadata.id` in the
root node, contradicting `NODE-08`; validate examples before adopting them.

Sources: [§8](https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/08-validation/index.md), [§4.2 payload structure](https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/04-capabilities/4-2-capabilities-field.md), [§4.8 example](https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/04-capabilities/4-8-ruml-query.md), [result schema](https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/schemas/ruml-result.schema.json).
