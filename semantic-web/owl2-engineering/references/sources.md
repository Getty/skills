# Primary sources and version boundaries

The baseline is the **OWL 2 Second Edition Recommendation family of 11 December 2012**. Read the specifications' errata links for corrections and verify tool-specific support independently.

## Normative OWL 2 documents

- [Document Overview](https://www.w3.org/TR/owl2-overview/) — architecture of the language family, semantics, syntaxes, and profiles.
- [Structural Specification and Functional-Style Syntax](https://www.w3.org/TR/owl2-syntax/) — ontology structure, entity kinds, imports, axioms, datatypes, and global restrictions.
- [Direct Semantics](https://www.w3.org/TR/owl2-direct-semantics/) — formal meaning and standard reasoning problems.
- [RDF-Based Semantics](https://www.w3.org/TR/owl2-rdf-based-semantics/) — semantics for the broader RDF formulation.
- [Profiles](https://www.w3.org/TR/owl2-profiles/) — exact EL, QL, and RL grammar restrictions and computational goals.
- [Mapping to RDF Graphs](https://www.w3.org/TR/owl2-mapping-to-rdf/) — correspondence between structural ontologies and RDF graphs.
- [XML Serialization](https://www.w3.org/TR/owl2-xml-serialization/) — OWL/XML, distinct from RDF/XML.
- [Conformance](https://www.w3.org/TR/owl2-conformance/) — conformance claims and testing boundaries.

## Explanatory and related sources

- [OWL 2 Primer](https://www.w3.org/TR/owl2-primer/) — approachable semantic explanations; use normative documents for exact edge cases.
- [Manchester Syntax](https://www.w3.org/TR/owl2-manchester-syntax/) — W3C Note describing a readable syntax; distinguish its status from the normative core.
- [XML Schema Datatypes 1.1](https://www.w3.org/TR/xmlschema11-2/) — lexical/value spaces and facets used by supported datatypes.
- [RDF 1.1 Concepts](https://www.w3.org/TR/rdf11-concepts/) — RDF terms, graphs, datasets, and literal term equality.
- [SHACL](https://www.w3.org/TR/shacl/) — the separate 2017 Recommendation for explicit RDF validation.

## Newer RDF work does not silently revise OWL

[RDF 1.2 Concepts](https://www.w3.org/TR/rdf12-concepts/) is a later revision with its own publication status; read it from the document. New RDF term kinds or syntactic extensions are not automatically part of OWL 2's structural mapping or accepted by OWL reasoners. Check the selected parser, mapping, profile checker, and semantic regime together.

This skill deliberately avoids mandatory vendor tools or architecture conventions. Examples and verification workflows are original synthesis; exact reasoner APIs, supported datatype maps, and explanation facilities require current primary implementation documentation.
