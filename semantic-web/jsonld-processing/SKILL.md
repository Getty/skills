---
name: jsonld-processing
description: "Use when writing or debugging JSON-LD 1.1 — @context, term expansion, @id and @type, language and datatype coercion, @list and @set, named graphs, expand, compact, flatten, frame, RDF conversion, remote contexts."
---

# JSON-LD Processing

Use JSON-LD to express linked data through JSON while making identifiers and relationships explicit. Start from the desired graph meaning, then choose a JSON shape that producers and consumers can handle. A context controls interpretation; it is part of the data contract rather than a decorative dictionary of convenient names.

Use the JSON-LD 1.1 Syntax, Processing Algorithms and API, and Framing Recommendations of 16 July 2020 as this skill's baseline. Keep processor version, processing mode, document loader, and algorithm options explicit. Do not infer support for RDF 1.2 terms from a processor's JSON-LD 1.1 support. See [sources and versions](references/sources.md) for the dated standards boundary.

## Navigate the references

- [Contexts and identifiers](references/contexts-identifiers.md): context expansion, aliases, base/vocabulary IRIs, coercion, scoped/protected contexts, and term collisions.
- [Values, collections, and graphs](references/values-graphs.md): literal values, language tags, containers, ordered lists, node identity, reverse properties, and named graphs.
- [Processing operations](references/processing-operations.md): expansion, compaction, flattening, framing, RDF conversion, and the different guarantees they provide.
- [Remote loading and integrity](references/remote-loading-integrity.md): document-loader policy, reproducible contexts, denial-of-service boundaries, canonicalization, and signatures.
- [Practical design and debugging](references/design-debugging.md): original examples, a semantic inspection workflow, compatibility checks, and migration choices.
- [Sources and versions](references/sources.md): primary specifications, related standards, and version caveats.

Read only the sections relevant to the task. This skill is self-contained and does not require a particular RDF store, programming language, or sibling skill.

## Establish the intended contract

Identify the input JSON, active context, base URL, required output shape, and expected graph meaning. Determine whether the user needs an explanation, a published context, processor code, an API representation, a conversion, or a diagnosis. Keep the JSON interface contract separate from RDF semantics: an API can demand an array even when a processor could compact it to one scalar.

For a new context, list the full predicate/class IRIs first and choose aliases afterward. Distinguish links from strings explicitly. Decide how language, exact numeric values, optional data, and ordered collections are represented. Prefer stable absolute identifiers where data will move between document locations.

## Work from expansion

1. Parse JSON and detect duplicate object keys if the ingestion layer can expose them; ordinary parsers may discard one occurrence.
2. Resolve the document and contexts under an explicit loader policy.
3. Expand using the selected processing mode and base. Inspect the full IRIs and value objects.
4. Check that every intended property survived expansion and points to the intended vocabulary term.
5. Confirm whether values are IRIs, blank nodes, typed literals, language-tagged strings, lists, or graph objects.
6. Apply the requested transformation and inspect its effect at the appropriate level.

Undefined compact terms can disappear during expansion when no applicable vocabulary mapping exists. This is a major reason to inspect expansion before treating a successful processor call as proof of complete ingestion. JSON syntax validity alone does not establish JSON-LD correctness or vocabulary conformance.

## Choose the operation deliberately

Use expansion to remove context-dependent shorthand, compaction to express data with a selected context, flattening to organize node descriptions, and framing to produce an application-friendly tree. Use RDF conversion when the consumer operates on RDF graphs or datasets. None of these operations automatically validates required fields, proves factual identity, or creates a canonical signature input.

For comparisons, decide whether the invariant is exact JSON structure, expanded JSON-LD, RDF dataset structure, or a canonicalized dataset. JSON key order and compact aliases can change without changing the graph. Conversely, a small context change can alter the graph while leaving the business-facing JSON almost unchanged.

## Verify and deliver

For context edits, compare representative expanded documents before and after the change. Include links versus strings, missing terms, language tags, a multi-value field, and any ordered list or named graph used by the contract. For RDF round trips, check the complete dataset and known non-RDF information such as unmapped indexes.

Return the artifact or explanation, the selected context/version and processor assumptions, and evidence of the checks actually performed. Name losses or unsupported features precisely. If remote contexts are required, include their loading and reproducibility policy. Avoid describing a framed document as a complete graph export unless its coverage has been verified.
