<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# Sources, baseline, and maintenance

## Contents

- [Pinned baseline](#pinned-baseline)
- [Use each source for its actual purpose](#use-each-source-for-its-actual-purpose)
- [Source map](#source-map)
- [Refresh the skill deliberately](#refresh-the-skill-deliberately)
- [Attribution and reuse](#attribution-and-reuse)

## Pinned baseline

Specification: **RUML 1.0.0, 2026-11-15**.
The JSON envelope version is `1.0`. The English specification is authoritative;
the German edition is a translation. Distinguish this publication version from
`metadata.version` and from every implementation's package version.

| Source | Inspected identity | Purpose |
| --- | --- | --- |
| [RUML specification, schemas, tests](https://github.com/Law-as-Code-Institute/ruml/tree/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4) | `d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4` | Authoritative snapshot for this skill |
| [Python parser](https://github.com/Law-as-Code-Institute/ruml-python/tree/1a421333ba0a2b4d134054417dc418c1142916ec) | `1a421333ba0a2b4d134054417dc418c1142916ec` | Concrete parser behavior and requirements |
| [TypeScript parser](https://github.com/Law-as-Code-Institute/ruml-js/tree/cb7d754b42ff53940e154ae924b7f72f7fa8b218) | `cb7d754b42ff53940e154ae924b7f72f7fa8b218` | Concrete parser APIs, optional checks, dependencies |
| [Public specification site](https://ruml.org/) | Moving latest | Discover releases; do not use alone for reproducible citations |
| [Institute's format overview](https://law-as-code.org/ruml/) | Moving overview | Context and intended use; not normative execution rules |

The bundled [baseline manifest](../assets/baseline.json) records the exact schema-file
SHA-256 checksums used for example validation. These are **raw file checksums for
research reproducibility**, not RUML container/JCS digests.

The three schema files are `ruml.schema.json`, `ruml-result.schema.json`, and
`ruml-ext.schema.json`. A container manifest schema is not included in this snapshot.
Do not infer result/container conformance coverage from the mere existence of a
format chapter: inspect which cases the actual test suite contains.

## Use each source for its actual purpose

1. **Read English normative prose for semantics.** Track MUST, SHOULD, MAY and their
   stated scope. Treat a local deployment restriction as a local restriction.
2. **Read the JSON Schemas for structural contracts.** They are explicitly the
   structural source of truth. A shape check cannot establish every cross-reference,
   expression, temporal, or execution rule.
3. **Read conformance descriptors and fixtures for observable cases.** The current
   descriptor schema and concrete files matter more than a stale illustrative runner
   snippet. A finite set of passing cases is evidence of that coverage.
4. **Read implementation source for actual support.** A released package can implement
   only part of the specification. An unsupported feature is not thereby invalid RUML.
5. **Use product pages for claims about product availability.** Verify them separately
   from the normative format. A hosted workspace and an open parser have different scopes.

These are different kinds of evidence, not a universal precedence list that erases
contradictions. If sources disagree, record the exact revision and passages, reproduce
the difference, choose an explicit interoperability profile if necessary, and report
the remaining uncertainty. Do not silently rewrite normative behavior to match a library.

Known snapshot-specific issues are documented where they affect work: operator modes
and recursion in their references; sidecar ordering and decision-mode gaps in the
capability reference; parser/package/runner differences in validation and troubleshooting;
hash requirements and container layout in the container reference.

## Source map

All paths below are within the pinned RUML repository above. Use that commit rather
than `main` when citing the behavior documented in this skill.

| Question | Primary source path |
| --- | --- |
| Scope and conformance levels | `spec/en/01-introduction/1-1-introduction.md`, `1-4-conformance.md` |
| Version compatibility | `spec/en/02-file-format-basics/2-3-versioning.md` |
| UUIDs, LexIDs, node paths | `spec/en/02-file-format-basics/2-5-identifier-system.md` |
| Metadata and lifecycle | `spec/en/03-data-model/3-3-metadata-object.md` |
| Node structure and integrity | `spec/en/03-data-model/3-5-node-object.md`, `3-8-integrity-validation.md` |
| Exact aggregation behavior | `spec/en/03-data-model/3-6-operators.md` and `tests/03-data-model/3-6-operators--*.test.yaml` |
| Extension roles and obligations | `spec/en/04-capabilities/4-1-concept.md` through `4-6-parser-obligations.md` |
| Typed data and expression context | `spec/en/04-capabilities/4-7-data-points.md`, `4-8-ruml-query.md`, `4-14-ruml-expression.md` |
| AI decisions and effects | `spec/en/04-capabilities/4-9-ruml-ai-query.md`, `4-10-ruml-actions.md` |
| Context, source text, audit protocol | `spec/en/04-capabilities/4-11-ruml-context.md` through `4-13-ruml-protocol.md` |
| References versus inclusion | `spec/en/04-capabilities/4-15-ruml-tree-reference.md`, `4-16-ruml-tree-include.md` |
| Stored statuses and occurrences | `spec/en/05-result-format/5-0-status-types.md`, `5-1-result-model.md` |
| Modular reuse and recursive expansion | `spec/en/06-modular-nodes/` |
| Container processing and integrity | `spec/en/07-container/` |
| Rule identifiers and validation layers | `spec/en/08-validation/index.md`, `schemas/README.md` |
| Actual fixture contract | `tests/schema/spec-test.schema.json`, specific `.test.yaml` descriptors; compare `spec/en/appendix/A-spec-tests/` |

Follow the direct section links within each subject reference for exact evidence.
For JSONata use the [official language documentation](https://docs.jsonata.org/) and
[2.2.0 release](https://github.com/jsonata-js/jsonata/releases/tag/v2.2.0).
For canonical JSON use [RFC 8785](https://www.rfc-editor.org/rfc/rfc8785).
For adjacent standards use the official sources linked in [interoperability](interoperability.md).

## Refresh the skill deliberately

1. Inspect the upstream release history and record the actual commit, release version,
   and date. Do not treat a changed moving `main` as an unchanged specification.
2. Compare changed chapters, all three schemas, fixture descriptors, and relevant
   implementation manifests. Review text, schema, and implementation independently.
3. Confirm the JSON envelope compatibility range. Keep old files associated with the
   version under which they were authored; do not bulk-change version strings alone.
4. Re-run example schema checks, semantic checks available in the chosen parser,
   expression checks, and the relevant operator cases. Add cases for the changed behavior.
5. Revisit every documented gap and limitation. Remove a caveat only when its correction
   is verified at the newly selected source revision.
6. Update pinned links, the baseline manifest, tested versions and results, and example
   hashes. Explain migrations that affect decisions or the shape of stored traces.

For a narrow implementation question, refresh only the relevant facts first. A full
bundle refresh is appropriate when changing the skill's declared baseline.

## Attribution and reuse

This is an independent engineering skill, not an official RUML specification or
an endorsement by its publisher.

RUML specification attribution: **RUML – Rulemapping Logic Format, version 1.0.0,
© 2026 Rulemapping Group GmbH, published by Law as Code Institut GmbH, licensed
under CC BY-SA 4.0.** The explanatory skill and reference prose adapts that material
through reorganization, paraphrase, practical workflows, cross-checking, and explicit
implementation cautions. It is distributed under **CC BY-SA 4.0**. Preserve attribution
and license terms when redistributing adapted prose.

The original helper scripts and synthetic example files in this skill are provided
under **Apache-2.0**. Upstream schemas, tests, and examples are also Apache-2.0; upstream
license attribution remains with their authors. This skill does not bundle the full
upstream specification or claim ownership of it. License texts are included under
`LICENSES/`.

The specification states that its ShareAlike terms apply to adaptations of the
specification text, not to software implementing RUML or rulemaps authored with it.
Treat trademarks and any separately relevant patent terms as distinct questions;
do not infer a blanket patent clearance or usage restriction from the document license.

Sources: [specification status and license](https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/spec/en/index.md),
[repository licensing](https://github.com/Law-as-Code-Institute/ruml/blob/d2ac818f6ed87c2bcf5b69430adf2efa8ba3c6a4/LICENSE.md).
