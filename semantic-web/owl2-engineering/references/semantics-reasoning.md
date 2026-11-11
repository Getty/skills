# Semantics and reasoning questions

## Interpret an ontology as a theory

An OWL ontology describes the interpretations that satisfy its axioms. A reasoner checks consequences that hold across those interpretations. This perspective explains why OWL behaves differently from a database that checks only currently stored rows.

Under the open-world assumption, an absent assertion is not automatically false. If every registered member must have a card and `ex:Lea` is a registered member, the ontology can require the existence of a card without an explicit triple naming one. This is not evidence that an application record contains the required card identifier.

An existential consequence need not become a concrete newly named individual in a reasoner's output. Ask whether existence is entailed separately from whether a named witness is available for display or integration.

## Keep identity explicit

OWL does not impose a general unique-name assumption: two different individual IRIs may denote the same individual. `owl:sameAs` asserts identity; `owl:differentFrom` and `owl:AllDifferent` can assert difference. These are stronger claims than similar labels, matching codes, or different source records.

If a person has at most one object-property value and two named values are asserted, a reasoner may conclude that those values are the same individual. The situation becomes inconsistent if they are also forced to be different. For a functional data property, two genuinely different datatype values cannot be repaired by equating different numbers.

Do not confuse RDF term equality with OWL individual identity. An RDF query can return two IRI terms even when an equality-aware reasoner treats them as the same individual; store policies for materialization and representative identifiers vary.

## Separate common reasoning tasks

| Task | Question |
| --- | --- |
| Ontology consistency | Is there any interpretation satisfying all axioms? |
| Class satisfiability | Can this class have an instance in some satisfying interpretation? |
| Subsumption | Must every instance of one class be an instance of another? |
| Classification | What class hierarchy follows from the axioms? |
| Instance checking | Must this individual belong to this class? |
| Realization | What most-specific named classes classify an individual under the chosen task? |
| Entailment | Does a specified axiom hold in every model? |

A class can be unsatisfiable while the ontology remains consistent, provided nothing requires that class to have an instance. Asserting an instance of an unsatisfiable class can make the ontology inconsistent. Report these outcomes separately.

## Understand negative conclusions

Failure to derive a statement is not derivation of its negation. An incomplete reasoner, missing imports, timeout, or unsupported datatype also prevents a sound “not entailed” conclusion. State whether a result is proved, disproved under a defined task, unknown, unsupported, or unfinished.

Explicit negative property assertions deny a particular relationship between specified participants; they do not close the entire property. Disjoint classes prohibit shared membership, but missing a positive type assertion is not proof of membership in the complementary class.

In classical semantics, an inconsistent theory has no models, so ordinary entailment becomes uninformative. Do not use a long list of inferred facts from an inconsistent ontology as reliable domain knowledge. Diagnose the conflict first or use a separately specified nonclassical approach.

## Distinguish validation

A shape can require an explicitly available value, constrain a record's allowed predicates, or validate a datatype. OWL domain/range and cardinality axioms constrain interpretations and can infer additional information. Translating between these approaches requires a declared policy; matching vocabulary names are insufficient.

The [OWL 2 Direct Semantics](https://www.w3.org/TR/owl2-direct-semantics/) supplies the formal inference definitions. The [OWL 2 Primer](https://www.w3.org/TR/owl2-primer/) provides the broader modeling context; SHACL is a separate [validation Recommendation](https://www.w3.org/TR/shacl/).
