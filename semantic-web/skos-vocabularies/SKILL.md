---
name: skos-vocabularies
description: "Use when building, mapping or validating a SKOS vocabulary — thesaurus, taxonomy, concept scheme, multilingual labels, notations, broader/narrower, exactMatch and closeMatch, collections, SKOS-XL, spreadsheet migration."
---

# SKOS Vocabularies

## Establish the modeling purpose

Use SKOS to give controlled concepts stable identifiers, labels, definitions, and relationships. Start with the questions the vocabulary must answer: which subject describes an item, which term should a user see, which broader topic supports navigation, and which external concept is a suitable retrieval match? Explain these operations before introducing ontology terminology.

Distinguish a concept used to index resources from a class whose instances satisfy a formal definition. A document about bridges can be indexed with a bridge concept without becoming a bridge. SKOS and OWL can coexist, but converting `skos:broader` into `rdfs:subClassOf`, or a concept match into `owl:sameAs`, requires a separate, justified modeling decision.

Use this skill independently. It requires no database, sibling skill, taxonomy product, or particular programming language. When implementation is requested, adapt the examples to the user's actual RDF tooling.

## Read the relevant reference

| Task | Read |
| --- | --- |
| Explain the model or choose concepts versus classes | [Model and decisions](references/model-and-decisions.md) |
| Author labels, translations, notation, notes, or SKOS-XL | [Labels and multilingual vocabularies](references/labels-multilingual-and-xl.md) |
| Design hierarchy, mappings, and collections | [Relations and collections](references/hierarchy-mapping-collections.md) |
| Convert, govern, version, and publish a vocabulary | [Authoring and publication](references/authoring-publication.md) |
| Check integrity or work through executable RDF examples | [Validation and examples](references/validation-and-examples.md) |
| Verify normative status, definitions, or source limits | [Authoritative sources](references/sources.md) |

Open only the references needed for the task. Consult the normative SKOS Reference for exact semantic claims; use the Primer for design explanations. Recheck mutable software documentation and publication endpoints when implementing against them.

## Follow the workflow

1. **Inventory the source.** Identify concepts, local codes, language columns, hierarchy conventions, scope notes, collections, and crosswalks. Preserve the original rows and identifiers. Do not assume a spreadsheet row, a term, and a concept are interchangeable.
2. **Define identity and scope.** Choose stable concept and scheme IRIs, a documented identifier policy, and the intended scheme membership. Separate a scheme from its downloadable representation or release. Avoid label-derived identity unless the naming policy explicitly accepts label changes.
3. **Author the lexical layer.** Assign preferred, alternative, and hidden labels with appropriate language tags. Keep machine codes in `skos:notation`; preserve leading zeros and the notation system. Write definitions and scope notes for ambiguous or overlapping concepts.
4. **Add relationships deliberately.** Model direct broader links, associative links, and cross-scheme mappings using their actual meanings. Permit multiple parents when the subject system needs them. Keep asserted direct edges separate from derived reachability.
5. **Check integrity and local policy separately.** Evaluate SKOS disjointness and label rules, then the additional requirements of the publishing profile. Missing labels, hierarchy cycles, multiple schemes, or absent top concepts are not all automatically SKOS inconsistencies.
6. **Review usage.** Try real indexing, search, and language-fallback tasks. Inspect whether mappings expand retrieval too broadly and whether translations preserve the concept's scope. Resolve conceptual mistakes before optimizing serialization.
7. **Publish a reproducible release.** Supply RDF, human-readable descriptions, source and license metadata, version information, and a change record. State what the release contains; `skos:inScheme` does not close a scheme under RDF's open-world semantics.

## Maintain semantic discipline

Treat `skos:broader` and `skos:narrower` as direct-link conventions, not transitive predicates. Use `skos:broaderTransitive`, an explicit closure, or a SPARQL path for reachability. Check the associative-versus-hierarchical conflict after considering indirect hierarchy.

Choose `skos:closeMatch` for context-dependent retrieval similarity. Use `skos:exactMatch` only when broad interchangeability is defensible; its symmetry and transitivity can propagate through a mapping network. Neither predicate asserts unrestricted RDF identity. Do not infer a hierarchy across an exact-match bridge without an explicit application rule.

Use collections for grouping or display order. A collection is distinct from a concept and a concept scheme. Use an ordered collection's RDF list for ordering; triple order and alphabetic labels are not substitutes.

Use SKOS-XL when labels need identities or their own metadata. Maintain the corresponding simple-label view for consumers that do not implement XL property-chain entailments. Do not add XL complexity merely to display translations.

## Deliver a usable result

For an explanation, give a small example, the intended entailments, and one likely modeling mistake. For a vocabulary or conversion, deliver the mapping decisions, vocabulary, identified losses, validation findings, and release metadata. Describe each finding as a standard inconsistency, a local policy failure, or a review warning. State whether verification covered RDF parsing, rule checks, entailment, and representative downstream use; never equate a successful parser run with SKOS correctness.
