# Shapes, targets, and property paths

## Separate the graph roles

The data graph contains the RDF statements to check. The shapes graph contains shape definitions and their parameters. They are both RDF graphs, but their roles are different. A validator may accept an additional ontology graph or dataset interface; the exact merge and inference behavior is implementation-specific and must be recorded.

A focus node is a node validated against a shape. A value node is a node evaluated by that shape's constraints. For a node shape, the focus node itself is the value node. For a property shape, values are reached from the focus node through `sh:path`.

A node shape must not have a property path; a property shape has exactly one path. A property shape can be attached through `sh:property` or have targets of its own. Give reusable shapes stable IRIs; use blank nodes for local definitions when external references are unnecessary.

## Select targets explicitly

| Target | Nodes selected |
| --- | --- |
| `sh:targetNode` | Explicitly named RDF nodes |
| `sh:targetClass` | SHACL instances of the specified class |
| `sh:targetSubjectsOf` | Subjects using a specified predicate |
| `sh:targetObjectsOf` | Objects of a specified predicate |

Class targeting follows the SHACL instance relation, which includes the relevant `rdf:type` and available `rdfs:subClassOf` chain. The subclass triples needed for that check must be available in the data graph used by validation. Arbitrary OWL entailment is not automatically performed.

Shapes that are also declared as appropriate RDFS classes can have implicit class targets under the standard's rules. Avoid accidental implicit targeting when reusing class IRIs for shape resources. A reusable shape without targets can still be invoked through another shape; it is not automatically applied to every node.

A record missing its expected `rdf:type` may never become a focus node for `sh:targetClass`. Use an independent record inventory, subject/object targets, or explicit target nodes when that risk matters. A successful report does not itself prove that every input record was checked.

## Read paths as sets of reachable values

A simple predicate IRI is the most common path. Core also supports inverse, sequence, alternative, zero-or-more, one-or-more, and zero-or-one paths through their RDF encodings.

```turtle
@prefix ex: <https://example.org/> .
@prefix sh: <http://www.w3.org/ns/shacl#> .

ex:SiteCodeShape a sh:PropertyShape ;
    sh:path ( ex:collectedAt ex:code ) ;
    sh:minCount 1 ; sh:maxCount 1 .

ex:IncomingSampleShape a sh:PropertyShape ;
    sh:path [ sh:inversePath ex:collectedAt ] ;
    sh:minCount 1 .
```

The sequence path reaches site codes from a sample. It does not separately require exactly one intermediate site: several sites could share the same code value. Add a shape on `ex:collectedAt` when the number or structure of sites matters.

Counts apply to distinct value nodes in the path's result set, not to the number of traversal routes or duplicate source rows. Zero-length paths can include the focus node. Cycles and wide paths can affect performance and should be tested on realistic graph shapes.

## Keep path structure separate from closure

A complex path describes how to find values. It does not automatically permit each traversed predicate in a closed shape or validate every intermediate node. Attach explicit nested shapes and simple property paths when those conditions are required.

The [SHACL Recommendation](https://www.w3.org/TR/shacl/) defines target selection, focus/value nodes, and path encodings. Consult its syntax rules when generating paths; a well-formed RDF list is necessary but does not alone prove a valid SHACL path.
