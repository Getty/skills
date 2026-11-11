# Model and modeling decisions

## Concepts, terms, and resources

Treat a concept as a unit of meaning identified independently of the words used to express it. A single concept may have several language-specific labels. A single word may name several concepts. Before minting IRIs, ask whether two source entries express one meaning, two meanings, or an unresolved distinction.

For example, an indexing vocabulary can contain separate concepts for a river bank and a financial bank. The string "bank" alone cannot determine which concept a document concerns. A concept's definition and scope note provide that distinction; its IRI keeps it stable when editors improve the wording. Do not merge homonyms merely because their labels normalize to the same string.

A resource classified by a concept remains separate from the concept. A local predicate or a suitable subject property can connect an article to a concept. Choose the indexing relation and its direction explicitly. SKOS does not prescribe every application relationship between documents and subject concepts.

## Concepts and OWL classes

Use an OWL class when membership and logical class relationships are part of the model. Use a SKOS concept for a controlled indexing meaning. These approaches answer different questions:

| Question | Suitable starting model |
| --- | --- |
| Which preferred term should the catalog display? | SKOS label |
| Which topic is broader for browsing? | SKOS hierarchy |
| Which objects are instances of a defined type? | RDF class membership, possibly OWL axioms |
| Must a class have particular restrictions? | OWL and/or an explicit validation profile |
| Which external term expands retrieval suitably? | Reviewed SKOS mapping |

SKOS does not declare `skos:Concept` disjoint with `owl:Class`. Deliberate combined models are possible, including OWL 2 punning. That freedom does not make the two interpretations equivalent. Document the interpretation of a dual-use IRI, the reasoning regime, and the export behavior. For most simple catalogs, separate concept and class IRIs reduce accidental entailments and simplify explanations.

## Schemes and their boundaries

Use `skos:ConceptScheme` for the organized vocabulary. Link a concept with `skos:inScheme`; identify navigational roots through `skos:hasTopConcept` or its inverse `skos:topConceptOf`. Top-concept membership entails scheme membership. A broader link alone does not transfer membership from one concept to another.

A concept can participate in multiple schemes. Scheme membership is not a container that owns every triple about its concepts. An RDF file may describe several schemes; a scheme may be described across multiple files. `skos:inScheme` does not say that the enumerated members are exhaustive. Where completeness matters, define a release manifest and a closed validation dataset as application conventions.

Keep these identities separate: the ongoing scheme, a dated release, a distribution file, and the concepts. A corrected typo usually changes a release while preserving the concept IRI. A substantive split of meaning may require new concepts and documented migration links. SKOS itself provides no complete version-management protocol.

## Select a profile rather than inventing constraints

Write a short publishing profile before conversion. Specify required languages, supported RDF serialization, expected definitions, allowed external mappings, scheme-membership policy, notation uniqueness scope, and deprecation handling. Explain which conditions come from SKOS and which are stricter local decisions.

Use the [normative reference](https://www.w3.org/TR/skos-reference/) for vocabulary semantics and the [Primer's modeling discussion](https://www.w3.org/TR/skos-primer/#seccombining) for concept/class design patterns. The practical recommendations above are application guidance, not extra SKOS axioms. Do not present a preference for one parent, acyclic hierarchy, or one scheme per concept as a universal standard requirement.
