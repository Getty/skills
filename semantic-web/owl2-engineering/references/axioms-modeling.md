# Classes, properties, and logical axioms

## Use necessary and sufficient conditions carefully

`SubClassOf(A B)` states that membership in A requires membership in B. `EquivalentClasses(A B)` makes the class extensions equal, allowing inference in both directions. A definition assembled from convenient examples can become too strong when made equivalent rather than necessary.

Use intersection for simultaneous membership, union for alternatives, complement for nonmembership in a class, and disjointness when simultaneous membership is impossible. An enumeration such as `ObjectOneOf` names a class whose members are the specified individuals; it is not a list of string labels.

A Turtle example defines a checked-out item as an item currently loaned to some member:

```turtle
@prefix ex: <https://example.org/library/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

ex:Item a owl:Class .
ex:Member a owl:Class .
ex:loanedTo a owl:ObjectProperty ;
    rdfs:domain ex:Item ; rdfs:range ex:Member .
ex:CheckedOutItem a owl:Class ;
    owl:equivalentClass [ a owl:Class ; owl:intersectionOf (
        ex:Item
        [ a owl:Restriction ; owl:onProperty ex:loanedTo ;
          owl:someValuesFrom ex:Member ]
    ) ] .
```

This is an explicit semantic choice: any item with such a loan relationship qualifies. If historical loans are retained, model current loan state separately or the definition will classify items based on stale relationships.

## Read restrictions precisely

| Restriction | Meaning to assess |
| --- | --- |
| Some values from C | At least one property value belongs to C |
| All values from C | Every property value belongs to C; no existence is required |
| Has value v | The specified value is a property value |
| Minimum cardinality n | At least n distinct qualifying values exist |
| Maximum cardinality n | At most n distinct qualifying values exist |
| Exact cardinality n | Both the minimum and maximum hold |
| Has self | The individual relates to itself through the property |

An all-values restriction is satisfied by an individual with no values for that property. Combine it with an existential if existence is also intended. Qualified cardinalities count only values in the qualifying class or data range. A missing type assertion does not prove that a value falls outside that qualifier.

## Model property consequences

Object properties relate individuals; data properties relate individuals to data values. Domain and range induce classifications from assertions. Multiple domain declarations mean intersection-like requirements, not a union.

Property characteristics include functional, inverse-functional, transitive, symmetric, asymmetric, reflexive, and irreflexive forms, subject to language restrictions. Choose them because the relationship has that meaning across the entire interpretation. A few transitive-looking examples do not establish a generally transitive relationship.

Property chains can infer one relationship from a sequence of others. They do not record the intermediate evidence automatically, and they are constrained by OWL 2 DL's global restrictions. Keep role, time, and context explicit when a binary property would otherwise conflate several meanings.

## Treat keys and annotations distinctly

OWL keys can infer individual identity within their defined scope. They are not SQL uniqueness checks and do not reject a record merely because a key field is missing. Evaluate their interaction with equality and the open world before using them for entity resolution.

Annotations describe ontology entities or axioms without acting as ordinary logical axioms under Direct Semantics. An explanatory note saying “required” does not create an existential restriction or an input constraint. Preserve annotations during conversion because humans and applications can still depend on them.

Use the [Structural Specification](https://www.w3.org/TR/owl2-syntax/) for exact constructs and restrictions, and [Direct Semantics](https://www.w3.org/TR/owl2-direct-semantics/) for their consequences.
