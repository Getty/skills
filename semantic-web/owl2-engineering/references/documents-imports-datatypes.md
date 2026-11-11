# Documents, imports, annotations, and datatypes

## Separate ontology identity from retrieval

An ontology can have an ontology IRI and a version IRI. Its document can be retrieved from a different URL, and its terms can use yet another namespace. Record all relevant identities rather than treating a prefix as the ontology's version.

`owl:imports` brings another ontology's axioms into the import closure. A namespace declaration does not import anything. Resolve imports transitively, detect retrieval failures, and avoid silent substitution of a convenient local ontology with different content.

For reproducible reasoning, pin the intended versions or exact imported documents, record digests, and keep a resolver/catalog mapping. An ontology result can change when an upstream import changes even if the local file is untouched. Distinguish deliberate use of a latest-release IRI from an immutable release contract.

## Preserve the full document

OWL supports RDF/XML, Turtle through RDF mapping, OWL/XML, Functional Syntax, and other documented syntactic presentations such as Manchester Syntax. The `.owl` extension does not identify one format. OWL/XML and RDF/XML have different structures and parsers.

Conversions must retain logical axioms, declarations, annotation assertions, axiom annotations, import declarations, and nested anonymous expressions. Generic RDF processing can preserve a graph while a structural conversion rejects it as outside OWL 2 DL. A tool can also ignore annotations or unsupported constructs; inspect output rather than assuming completeness.

Ontology annotations and entity annotations are valuable documentation. Under Direct Semantics they do not impose ordinary domain constraints. Keep deprecation notes, labels, language tags, and provenance annotations even when the reasoner does not use them logically.

## Understand datatype definitions

A datatype has a lexical space and value space. OWL datatype restrictions select subsets of values, using supported facets such as inclusive/exclusive bounds. A named datatype definition does not invent a fresh lexical parser for arbitrary strings bearing its IRI.

```turtle
@prefix ex: <https://example.org/measure/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

ex:UnitInterval a rdfs:Datatype ;
    owl:equivalentClass [ a rdfs:Datatype ;
        owl:onDatatype xsd:decimal ;
        owl:withRestrictions (
            [ xsd:minInclusive "0"^^xsd:decimal ]
            [ xsd:maxInclusive "1"^^xsd:decimal ]
        ) ] .
ex:confidence a owl:DatatypeProperty ; rdfs:range ex:UnitInterval .
ex:reading7 ex:confidence "0.85"^^xsd:decimal .
```

The literal remains typed as `xsd:decimal`; the property range restricts its value to the defined interval. Check that the chosen reasoner supports the datatype and relevant facets. Do not silently treat unsupported datatypes as ordinary strings.

## Preserve lexical distinctions when needed

Different lexical forms can denote the same datatype value. OWL's value-based semantics can identify values that remain different RDF literal terms. A serializer or host library may normalize lexical spellings, so retain source lexicals separately if auditing requires exact reconstruction.

Use exact decimal handling where required, preserve timezone absence, and distinguish language-tagged strings from untagged strings. XML Schema regular-expression syntax differs from many programming-language regex dialects; a copied pattern needs verification. Unsupported facets or custom datatype mappings can change the available reasoning guarantees.

Primary references: [Structural Specification](https://www.w3.org/TR/owl2-syntax/), [Mapping to RDF Graphs](https://www.w3.org/TR/owl2-mapping-to-rdf/), [OWL/XML](https://www.w3.org/TR/owl2-xml-serialization/), and [XML Schema Datatypes](https://www.w3.org/TR/xmlschema11-2/).
