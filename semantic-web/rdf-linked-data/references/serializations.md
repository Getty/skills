# Serializations and loss-aware conversion

## Select a representation

| Format | Main use | Graph scope | Usual media type |
| --- | --- | --- | --- |
| Turtle | Human-readable authoring and review | One graph | `text/turtle` |
| N-Triples | Simple line-oriented graph exchange | One graph | `application/n-triples` |
| TriG | Readable dataset exchange | Default and named graphs | `application/trig` |
| N-Quads | Line-oriented dataset exchange | Default and named graphs | `application/n-quads` |
| RDF/XML | XML-based RDF interchange | One graph | `application/rdf+xml` |
| JSON-LD | JSON-based linked-data exchange | Graphs and datasets through JSON-LD processing | `application/ld+json` |

A filename extension does not settle the format. An `.owl` file may use RDF/XML, Turtle, OWL/XML, or another ontology syntax. OWL/XML is not RDF/XML. Set the parser format explicitly when content negotiation or metadata is unreliable.

## Read Turtle correctly

```turtle
@base <https://example.org/catalog/> .
@prefix ex: <https://example.org/vocab/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<item/42> a ex:Specimen ;
    ex:name "River stone"@en ;
    ex:mass "12.50"^^xsd:decimal ;
    ex:foundAt <place/7> ;
    ex:tags "smooth", "grey" .
```

The semicolon repeats the subject for a new predicate. The comma repeats subject and predicate for another object. `a` abbreviates `rdf:type`; it is not a general keyword usable wherever an IRI appears. Relative IRIs resolve against the base. Changing the base can change the resulting graph without changing the visible relative strings.

The six statements can be serialized in any order. Prefix names, indentation, and choice of full or abbreviated IRIs do not change their meaning. Numeric shorthand has datatype consequences: integer, decimal, and exponent notation do not all create the same literal datatype.

## Preserve graph membership

```trig
@prefix ex: <https://example.org/> .

ex:release ex:label "November snapshot" .
ex:graphA {
    ex:sample1 ex:observedBy ex:teamA .
}
ex:graphB {
    ex:sample1 ex:observedBy ex:teamB .
}
```

The first triple belongs to the default graph. The following blocks belong to two named graphs. Serializing their union as Turtle loses graph membership. A conversion tool must ask for or document a selection/union policy rather than claiming a lossless dataset-to-graph conversion.

The named-graph statements in N-Quads are:

```nquads
<https://example.org/sample1> <https://example.org/observedBy> <https://example.org/teamA> <https://example.org/graphA> .
<https://example.org/sample1> <https://example.org/observedBy> <https://example.org/teamB> <https://example.org/graphB> .
```

N-Triples and N-Quads require fully expanded IRIs. Their predictable records are useful for streaming, but splitting arbitrary Turtle or TriG at newlines is unsafe: statements, strings, collections, and graph blocks can span lines.

## Check conversion fidelity

Parse before transforming. Preserve datatype IRIs, language tags, blank-node connectivity, and named graphs. Check serializer limitations on relative IRIs, invalid datatype lexicals, and unsupported extension terms. A parse/serialize round trip may legitimately change bytes and blank-node labels while retaining the graph.

For a graph, compare isomorphism if blank nodes are present. For a dataset, compare graph membership and shared blank-node structure across the whole dataset. For byte-stable hashing or signing, use an explicitly selected canonicalization algorithm; sorting ordinary Turtle or raw N-Quads is insufficient when blank-node labels vary.

## Gate RDF 1.2 features

The checked RDF 1.2 Concepts draft adds triple terms in object position, directional language-tagged strings, and version signaling. Do not assume older RDF-star syntax or vendor “quoted triple” support is identical to the current 1.2 model. Inspect the specific syntax document and exact parser release. Agree on an export fallback or reject unsupported terms explicitly; silently discarding annotations or direction information changes the data.

Primary format links and the RDF 1.2 documents are collected in [sources](sources.md).
