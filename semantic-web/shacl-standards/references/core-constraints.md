# Core constraint design

## Combine presence, kind, and content

Use `sh:minCount` and `sh:maxCount` to constrain the number of distinct values reached by a property path. Use `sh:nodeKind` for IRI, blank node, literal, or supported combinations. Use `sh:datatype` for literal datatype and valid lexical form, and `sh:class` for SHACL class membership.

These conditions are independent. An IRI need not have the required type; an instance of a class can be represented by a blank node; and a datatype constraint alone generally allows a missing property because there are no value nodes to violate it.

```turtle
@prefix ex: <https://example.org/> .
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

ex:ReferenceShape a sh:NodeShape ;
    sh:property [ sh:path ex:site ;
        sh:minCount 1 ; sh:maxCount 1 ;
        sh:nodeKind sh:IRI ; sh:class ex:Site ] ;
    sh:property [ sh:path ex:confidence ;
        sh:datatype xsd:decimal ;
        sh:minInclusive "0"^^xsd:decimal ;
        sh:maxInclusive "1"^^xsd:decimal ] .
```

The site is mandatory; confidence is optional but constrained whenever present. Reference the node shape from another shape or add a target to apply it directly.

## Choose value constraints

Use inclusive/exclusive bounds for numeric or otherwise comparable values. Comparability and datatype correctness matter; do not compare numeric-looking strings as if they were numbers. Preserve decimal lexical precision and define timezone policy for temporal comparisons.

Use `sh:minLength`, `sh:maxLength`, `sh:pattern`, and `sh:flags` according to their defined string behavior. The pattern follows SPARQL's regular-expression semantics rather than an arbitrary host-language dialect. Use `sh:languageIn` for allowed language ranges and `sh:uniqueLang` to limit repeated nonempty language tags.

`sh:in` limits values to an RDF list of allowed terms; `sh:hasValue` requires a specified value among the values. Exact RDF-term distinctions can matter for typed and language-tagged literals. Do not assume numerically equivalent lexical forms are interchangeable in every constraint.

## Compose and compare

`sh:node` requires conformance to another shape. `sh:and`, `sh:or`, `sh:not`, and `sh:xone` combine conformance tests; `sh:xone` requires exactly one alternative to conform. Give alternatives meaningful conditions so that two overlapping branches do not unexpectedly defeat exclusive choice.

Property-pair constraints such as `sh:equals`, `sh:disjoint`, `sh:lessThan`, and `sh:lessThanOrEquals` compare values against another property of the focus node. Check behavior for several values and incomparable terms; the meaning is not necessarily “compare two scalar fields.”

Qualified counts use `sh:qualifiedValueShape` with a qualified minimum/maximum to count only values conforming to that shape. `sh:qualifiedValueShapesDisjoint` changes interactions with sibling qualified shapes; verify that intended categories overlap or exclude one another as required.

## Close records narrowly

`sh:closed true` rejects outgoing predicates outside the permitted set derived from relevant property shapes with simple predicate paths and `sh:ignoredProperties`. Explicitly allow `rdf:type` when needed. A complex path is not a general declaration that its first predicate is permitted.

Closedness is local to the checked node. It does not close the whole RDF world, require all permitted properties, or prohibit unknown incoming relationships. Add minimum counts for required properties and nested shapes for related-node structure.

Use the [Core constraint definitions](https://www.w3.org/TR/shacl/#core-components) for exact component semantics. For named OWL datatype ranges, validate the actual builtin literal datatype and explicit facets unless the selected validator documents an additional datatype policy.
