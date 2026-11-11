---
name: owl2-engineering
description: "Use when designing, inspecting or reasoning over an OWL 2 ontology — classes, properties, axioms, restrictions, cardinality, open-world semantics, owl:sameAs, DL and EL/QL/RL profiles, imports, reasoners."
---

# OWL 2 Engineering

Use OWL 2 to state a domain theory with formally defined meaning and derive consequences from it. Explain what each axiom commits the model to before discussing syntax or tools. OWL can describe categories, relationships, identity, and constraints on possible interpretations; required input fields and closed record contracts usually need a separate validation mechanism.

Use the OWL 2 Second Edition Recommendations of 11 December 2012 as the baseline. Select the intended semantics and language profile explicitly. Parsing RDF containing OWL vocabulary is not the same as verifying OWL 2 DL conformance or completing a reasoning task.

## Navigate the references

- [Semantics and reasoning questions](references/semantics-reasoning.md): open world, identity, consistency, satisfiability, entailment, and the distinction from data validation.
- [Classes, properties, and axioms](references/axioms-modeling.md): restrictions, cardinalities, equivalence, disjointness, property characteristics, keys, and consequence-driven modeling.
- [Profiles and reasoner selection](references/profiles-tools.md): OWL 2 DL, EL, QL, RL, RDF-based semantics, global restrictions, and execution boundaries.
- [Documents, imports, and datatypes](references/documents-imports-datatypes.md): ontology identities, import closure, annotations, serializations, datatype definitions, and loss-aware conversion.
- [Practical modeling and verification](references/modeling-verification.md): original examples, competency questions, staged checks, diagnosis, and maintenance.
- [Sources and versions](references/sources.md): primary specifications, related standards, and dated status notes.

The material is independent of any programming language, database, application architecture, or sibling skill. Load the reference relevant to the question rather than all documents by default.

## Establish the semantic task

Identify whether the user wants an explanation, a vocabulary, an ontology, a reasoning result, a conversion, or a repair. Inspect existing terms and representative data when available. Write a few concrete questions the ontology should answer and one conclusion it should not imply.

Separate domain concepts, individual instances, statements about documents, and application input requirements. For example, “every registered member has some membership card” is different from “this submitted record must contain a card identifier.” The first can be an existential domain axiom; the second requires checking explicit data against a contract.

Choose the smallest suitable profile supported by the actual toolchain. State any unsupported construct and its effect rather than silently weakening or dropping the axiom. Keep inferred facts distinct from original assertions when explanation or provenance matters.

## Design axioms by consequence

1. Assign stable term IRIs and choose class, object-property, data-property, annotation-property, datatype, or individual roles deliberately.
2. Use subclass axioms for necessary conditions. Use equivalence only when the conditions are also sufficient.
3. Read domain/range as type implications. Multiple domains or ranges accumulate conditions; they are not alternative choices.
4. Evaluate existential, universal, and cardinality restrictions under open-world semantics. Missing assertions do not automatically violate them.
5. Account for the absence of a general unique-name assumption. Maximum object cardinality can entail identity between named values.
6. Introduce disjointness or explicit difference only when the domain supports it. Similar labels do not justify equivalence or identity.
7. Keep temporal, contextual, and multi-party relationships explicit rather than assigning global properties an overloaded meaning.

## Resolve documents and execution

Distinguish ontology IRI, version IRI, document URL, and term namespace. Resolve and record the transitive import closure. A prefix declaration alone does not import a vocabulary. Pin import content or versions when results must be reproducible.

Choose a parser, structural/profile checker, and reasoner appropriate to their separate jobs. Record versions and effective settings. A rule materializer may support useful entailments without implementing complete OWL 2 DL reasoning. A timeout or unsupported feature is not evidence of consistency or non-entailment.

## Verify and deliver

Parse the artifact, check the selected profile, verify import resolution, and run the reasoning questions relevant to the change. Keep ontology consistency, individual classification, class satisfiability, and selected entailments separate in the report. Include a negative case when it guards against an unintended equivalence, identity, or subclass relation.

For conversions, verify that logical axioms, annotations, imports, and nested expressions are retained. For repairs, identify the smallest relevant conflicting set when the tool can provide it and explain the domain decision required.

Return the ontology or explanation, a concise mapping from requirements to axioms, the semantic/profile assumptions, and observed verification results. State unchecked limits precisely. Avoid treating a clean serialization or a successful reasoner launch as proof that the ontology expresses the intended domain.
