# Authoritative sources and limits

Reopen mutable endpoints before using current services or software. Use versioned specifications for stable semantics and distinguish normative rules from examples and operational recommendations.

| Source | Role |
| --- | --- |
| [SKOS Reference, Recommendation, 18 August 2009](https://www.w3.org/TR/2009/REC-skos-reference-20090818/) | Normative concepts, schemes, labels, notations, notes, relations, mappings, collections, integrity, and SKOS-XL appendix |
| [Current SKOS Reference entry point](https://www.w3.org/TR/skos-reference/) | Publication status and errata links; checked as the 2009 Recommendation |
| [SKOS Primer, Working Group Note](https://www.w3.org/TR/skos-primer/) | Modeling examples, migration guidance, and combining SKOS with other approaches; informative, not a second normative definition |
| [SKOS vocabulary](https://www.w3.org/2004/02/skos/core) | Machine-readable vocabulary; inspect the returned representation and its license |
| [SKOS-XL vocabulary](https://www.w3.org/2008/05/skos-xl) | Machine-readable extension terms for label resources |
| [RFC 5646: Tags for Identifying Languages](https://www.rfc-editor.org/rfc/rfc5646) | BCP 47 language-tag structure; consult the IANA registry for current subtags |
| [Best Practice Recipes for Publishing RDF Vocabularies](https://www.w3.org/TR/swbp-vocab-pub/) | W3C Note on persistent identifiers and representation access; adapt dated server examples |
| [SPARQL 1.1 Query Language](https://www.w3.org/TR/sparql11-query/) | Property paths and query semantics |
| [Shapes Constraint Language](https://www.w3.org/TR/shacl/) | Optional validation mechanism for explicitly declared application profiles |

The references are original explanatory and implementation guidance, not reproductions of the specifications. Examples use synthetic identifiers and data. They illustrate small patterns rather than constituting a comprehensive SKOS conformance suite.

Read the normative statements and their accompanying notes together. In particular, do not turn conventions concerning direct links, scheme separation, or top concepts into integrity rules. Do not assume an OWL engine implements every SKOS condition, or that a SHACL shape library implements the exact profile requested. Tool support, serialization choices, and release-management practices need separate verification. This skill does not require any particular RDF store, editor, or companion skill.
