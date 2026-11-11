# Primary sources and version boundaries

Follow dated publications when reproducibility matters. “Latest published” URLs can advance; a newer Working Draft is not a Recommendation.

## Stable RDF 1.1 baseline

- [RDF 1.1 Concepts and Abstract Syntax](https://www.w3.org/TR/rdf11-concepts/) — Recommendation, 25 February 2014; graph/dataset structure, RDF terms, literal equality, and blank nodes.
- [RDF 1.1 Semantics](https://www.w3.org/TR/rdf11-mt/) — formal entailment regimes and datatype semantics.
- [RDF Schema 1.1](https://www.w3.org/TR/rdf-schema/) — classes, properties, subclass/subproperty, domain/range, and descriptive vocabulary.
- [RDF 1.1 Turtle](https://www.w3.org/TR/turtle/), [TriG](https://www.w3.org/TR/trig/), [N-Triples](https://www.w3.org/TR/n-triples/), [N-Quads](https://www.w3.org/TR/n-quads/) — normative serialization grammars and media-type information.
- [RDF/XML](https://www.w3.org/TR/rdf-syntax-grammar/) — RDF's XML serialization; distinct from OWL/XML.
- [RDF 1.1 Test Cases](https://www.w3.org/TR/rdf11-testcases/) — test-suite organization; a useful verification aid, not proof that untested features work.

## Active RDF 1.2 work

- [RDF 1.2 Concepts](https://www.w3.org/TR/rdf12-concepts/) — the 1.2 revision of RDF 1.1 Concepts; read its publication status from the document.
- [RDF 1.2 Semantics](https://www.w3.org/TR/rdf12-semantics/) — the 1.2 revision of the semantics, with a publication status of its own.
- [RDF 1.2 Turtle](https://www.w3.org/TR/rdf12-turtle/) and related 1.2 syntax documents — independently evolving documents; consult their headers and [W3C publication index](https://www.w3.org/TR/) before claiming a status or exact syntax.

Treat triple terms, reification/annotation syntax, directional language-tagged strings, and version signaling as explicit compatibility decisions. Older RDF-star implementations may differ from current RDF 1.2 drafts.

## Related Recommendations and guidance

- [JSON-LD 1.1](https://www.w3.org/TR/json-ld11/) — Recommendation, 16 July 2020; JSON-based linked-data syntax and context semantics.
- [RDF Dataset Canonicalization](https://www.w3.org/TR/rdf-canon/) — Recommendation, 21 May 2024; RDFC-1.0. Check errata and algorithm/version compatibility for signatures.
- [XML Schema Datatypes 1.1](https://www.w3.org/TR/xmlschema11-2/) — datatype lexical and value spaces.
- [Cool URIs for the Semantic Web](https://www.w3.org/TR/cooluris/) — W3C Note; useful URI publication patterns rather than an additional RDF requirement.
- [Data on the Web Best Practices](https://www.w3.org/TR/dwbp/) and [Linked Data Platform](https://www.w3.org/TR/ldp/) — publication/lifecycle practices and a specific HTTP platform model.

All examples in this skill are original teaching examples. Workflow recommendations synthesize the standards without requiring a specific language, database, vendor, or application architecture.
