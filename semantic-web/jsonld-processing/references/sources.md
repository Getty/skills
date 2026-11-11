# Primary sources and versions

Use exact processor versions and dated context content for reproducible work. This skill selects the following Recommendations as its baseline without claiming that all implementations support every option.

## JSON-LD 1.1 Recommendations

- [JSON-LD 1.1 Syntax](https://www.w3.org/TR/json-ld11/) — **16 July 2020**. Defines contexts, node/value/list/graph objects, containers, IRIs, and syntax constraints.
- [JSON-LD 1.1 Processing Algorithms and API](https://www.w3.org/TR/json-ld11-api/) — **16 July 2020**. Defines expansion, compaction, flattening, context processing, remote document loading, and RDF conversion.
- [JSON-LD 1.1 Framing](https://www.w3.org/TR/json-ld11-framing/) — **16 July 2020**. Defines graph-to-tree framing and its processing controls.
- [JSON-LD API tests](https://w3c.github.io/json-ld-api/tests/) and [framing tests](https://w3c.github.io/json-ld-framing/tests/) — primary interoperability resources. Passing selected cases is evidence for those cases, not universal compliance.

Use the specifications' errata links for corrections. A library's API method names and document-loader interface are implementation details, even when they implement the standard algorithms.

## Related standards

- [RDF 1.1 Concepts](https://www.w3.org/TR/rdf11-concepts/) — RDF term, graph, and dataset model relevant to conversion.
- [RDF Dataset Canonicalization](https://www.w3.org/TR/rdf-canon/) — Recommendation, **21 May 2024**; defines **RDFC-1.0**. Canonicalization is a separate operation from JSON-LD expansion or framing.
- [XML Schema Datatypes 1.1](https://www.w3.org/TR/xmlschema11-2/) — lexical/value semantics for common typed literals.
- [RFC 8259](https://www.rfc-editor.org/rfc/rfc8259) — JSON syntax and interoperability considerations, including numbers and object names.

## Evolving compatibility boundary

[RDF 1.2 Concepts](https://www.w3.org/TR/rdf12-concepts/) is a later revision than the RDF that JSON-LD 1.1 maps to. Its triple terms, directional language-tagged literals, and version signaling do not imply that a JSON-LD 1.1 processor supports equivalent newer features. Check the selected syntax and implementation explicitly, and distinguish experimental extensions from the 1.1 contract.

Examples and implementation workflows in this skill are original synthesis. Remote-loading controls are operational recommendations; their exact configuration depends on the processor and environment.
