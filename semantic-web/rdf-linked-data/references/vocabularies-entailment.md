# Vocabularies, RDFS, and entailment

## Separate vocabulary from instance data

Use vocabulary terms to define reusable concepts and relations. A class groups resources by membership; a property names a relationship. Declare an instance's membership with `rdf:type`. Use `rdfs:label` for a human-readable name and `rdfs:comment` for descriptive text; neither determines identity or provides a machine-checked definition.

An illustrative vocabulary and instance graph:

```turtle
@prefix ex: <https://example.org/ecology/> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

ex:Wetland a rdfs:Class ; rdfs:subClassOf ex:Habitat .
ex:recordedIn a rdf:Property ;
    rdfs:domain ex:Survey ; rdfs:range ex:Habitat .
ex:reedMarsh a ex:Wetland ; rdfs:label "Reed marsh"@en .
ex:survey17 ex:recordedIn ex:reedMarsh .
```

Under RDFS entailment, the graph supports `ex:reedMarsh a ex:Habitat` and `ex:survey17 a ex:Survey`. These are consequences of the declared vocabulary, even if those triples were not written explicitly.

## Read domain and range as inference

`rdfs:domain` classifies the subject of a property assertion. `rdfs:range` classifies its object. Neither says that the property may appear only on resources already typed with that class. Several domains mean membership in every listed domain, not a menu of alternative classes. Several ranges similarly accumulate consequences.

For example, attaching a very broad property such as `ex:label` to a narrow domain can classify every labeled resource as that domain. Prefer a suitable existing general labeling property, or define a genuinely narrow relationship. Use local validation shapes if the requirement concerns accepted input records.

`rdfs:subClassOf` propagates class membership upward. `rdfs:subPropertyOf` propagates property assertions to a broader relationship. These relations do not create object-oriented storage layouts or require each resource to have only one class. RDF supports multiple types naturally.

## Choose an entailment regime

Simple entailment, RDF entailment, RDFS entailment, datatype entailment, and OWL reasoning answer different questions. A store may expose explicit triples, materialize selected rules, rewrite queries, or combine these approaches. Record the actual regime rather than saying merely “reasoning enabled.” A subset of RDFS rules is not automatically full standards conformance.

Keep inferred statements distinguishable from source assertions when evidence or change management matters. Removing a source triple may require retracting consequences, but a consequence supported by another derivation must remain. A reasoning cache therefore needs dependency-aware maintenance or safe recomputation.

Open-world reasoning does not treat missing statements as false. RDF also does not impose a general unique-name assumption that all different IRIs identify different things. At the same time, software still compares distinct RDF terms distinctly unless it is applying an explicit equality policy.

## Reuse and extend vocabularies

Check an external term's definition, namespace, version, domain/range, and license before reuse. Prefer a precise existing relation to a new synonym. Mint an owned term when the intended meaning is materially different. Explain mappings instead of choosing `owl:sameAs` or class equivalence based on names alone.

Keep a vocabulary's namespace, its retrievable documentation URL, and a particular published version separate. Record deprecated terms and replacement guidance without silently rewriting old data. A vocabulary import can change inferred types even when source instance triples stay unchanged.

Use [RDF Schema](https://www.w3.org/TR/rdf-schema/) for vocabulary semantics and [RDF 1.1 Semantics](https://www.w3.org/TR/rdf11-mt/) for entailment definitions. Treat validation and publication recommendations here as practical design guidance, not additional RDF axioms.
