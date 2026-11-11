# Primary sources and version status

Keep Recommendation, Working Draft, Working Group Note, and implementation extension labels explicit.

## Stable baseline

- [Shapes Constraint Language (SHACL)](https://www.w3.org/TR/shacl/) — **W3C Recommendation, 20 July 2017**. Defines Core and SHACL-SPARQL, target and path semantics, report structure, failure behavior, and processor conformance.
- [W3C SHACL test suite](https://github.com/w3c/data-shapes/tree/gh-pages/data-shapes-test-suite) — primary test artifacts. Select cases for the advertised feature set rather than claiming universal conformance from a few examples.
- [SHACL Advanced Features](https://www.w3.org/TR/shacl-af/) — **Working Group Note**, separate from the 2017 Recommendation. Covers custom targets, functions, node expressions, and rules; support must be verified.
- [SHACL JavaScript Extensions](https://www.w3.org/TR/shacl-js/) — separate Working Group Note and execution model; do not assume ordinary Core support includes it.

## Active SHACL 1.2 work

- [SHACL 1.2 Core](https://www.w3.org/TR/shacl12-core/) — the 1.2 revision of Core; read its publication status at the canonical URL.
- [SHACL 1.2 SPARQL-Related Features](https://www.w3.org/TR/shacl12-sparql/) — the 1.2 revision of SHACL-SPARQL, with a publication status of its own.
- [W3C standards and drafts index](https://www.w3.org/TR/) — consult individual headers for node-expression, inference-rule, profiling, and other related work. These documents can advance independently.

The newer family does not make every 1.2 feature part of the 2017 contract. Record the selected edition and actual implementation support. In particular, do not infer portable recursion or rule semantics merely from a validator claiming SHACL support.

## Related standards and implementation evidence

- [SPARQL 1.1 Query](https://www.w3.org/TR/sparql11-query/) — expression and query semantics relevant to SHACL-SPARQL and Core definitions.
- [RDF 1.1 Concepts](https://www.w3.org/TR/rdf11-concepts/) and [XML Schema Datatypes](https://www.w3.org/TR/xmlschema11-2/) — term identity, sets of triples, literal lexical/value spaces.
- [OWL 2 Direct Semantics](https://www.w3.org/TR/owl2-direct-semantics/) — why ontology inference and explicit-data validation differ.
- [Apache Jena SHACL](https://jena.apache.org/documentation/shacl/) and [pySHACL](https://github.com/RDFLib/pySHACL) — primary implementation documentation; verify the installed release, options, inference mode, and advanced features.

Examples and operational workflows in this skill are original synthesis. Engine-specific command syntax is deliberately not treated as a timeless part of the standard.
