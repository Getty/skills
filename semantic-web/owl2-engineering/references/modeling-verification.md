# Practical modeling and verification

## Begin with competency questions

For a library model, ask: which items count as checked out; which members must have some membership card; can a visitor be a registered member; and which items belong to a broader collection category? Then specify an unwanted inference, such as treating every person mentioned in a note as a member.

Translate each question into a small semantic requirement before choosing an axiom. “Registered members have some card” supports an existential restriction. “Every input member record contains exactly one supplied card IRI” is an explicit-data requirement. “Two distinct cards are impossible for this member” additionally depends on what counts as distinct.

## Exercise an identity edge case

```turtle
@prefix ex: <https://example.org/library/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .

ex:hasCard a owl:ObjectProperty, owl:FunctionalProperty .
ex:Lea ex:hasCard ex:cardA, ex:cardB .
```

Under the intended OWL semantics, these assertions can imply that `ex:cardA` and `ex:cardB` are the same individual. They are not automatically an input-cardinality error. Adding `ex:cardA owl:differentFrom ex:cardB` creates a conflict with functionality. This tiny graph distinguishes identity reasoning from a closed-record validator.

## Stage verification by the claim being made

1. Parse the selected syntax and preserve the original artifact.
2. Resolve imports and record the complete versioned closure.
3. Check the selected structural/profile restrictions.
4. Check ontology consistency before relying on broad entailment output.
5. Check important named classes for satisfiability.
6. Run the explicit competency questions and forbidden-inference cases.
7. Compare converted or inferred outputs at the appropriate structural or semantic level.

A graph-isomorphism check can verify an RDF-preserving conversion; it cannot prove ontology equivalence under every entailment. Conversely, two differently structured ontologies can entail the same selected queries without being fully equivalent. Name the scope of the comparison.

## Diagnose conflicts with evidence

If the ontology is inconsistent, isolate the relevant individuals, axioms, and imported definitions. Use explanations or justifications when the reasoner supports them. An explanation is usually one sufficient set, not necessarily the only possible cause. Removing an arbitrary axiom until the reasoner succeeds can conceal a domain error.

Typical causes include disjoint classes inferred through an unexpected domain, functional properties with provably different values, impossible datatype ranges, and a newly imported property characteristic. Check asserted and inferred types separately when tracing the cause.

For an unsatisfiable class, inspect inherited restrictions and disjointness. A class may become empty through the combination of otherwise reasonable axioms. Decide whether the class should be empty, the axiom was too strong, or the intended model needs context-specific relations.

## Maintain the ontology as a semantic contract

Version changes according to their consequences: a new label is usually different from a new equivalent-class axiom, key, disjointness axiom, or domain. Check representative downstream inference after import updates. Deprecate terms with a clear mapping rather than reassigning an existing IRI a different meaning.

Return a concise evidence record: ontology/version, import content, syntax, profile, reasoner/version, settings, consistency result, satisfiability checks, and selected entailments. If a check did not run, say so. Avoid equating “no exception” with successful complete reasoning.

Use the [OWL 2 Conformance](https://www.w3.org/TR/owl2-conformance/) document for conformance terminology, and the [Primer](https://www.w3.org/TR/owl2-primer/) for explanatory modeling examples. All examples here are original.
