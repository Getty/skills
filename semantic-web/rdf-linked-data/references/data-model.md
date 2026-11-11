# Data model and identity

## Triples, graphs, and datasets

Read an RDF triple as a subject, a predicate, and an object. In RDF 1.1 the subject is an IRI or blank node, the predicate is an IRI, and the object is an IRI, blank node, or literal. The predicate names the relationship; it is not a field label whose meaning changes with a surrounding table.

An RDF graph is a set of triples. Repeating a triple neither creates another event nor raises a count. Triple order has no semantic significance. To represent three measurements that happen to have the same value, create three measurement resources or another explicit event structure.

An RDF dataset contains one default graph and zero or more named graphs. Each named graph pairs a graph name with a graph. The abstract RDF 1.1 model permits an IRI or blank node as a graph name, although some stores and query interfaces require IRI names. The default graph is not inherently the union of the named graphs. Decide that behavior at the application or query-service layer.

## Identify things deliberately

An IRI is an identifier, not an obligation to fetch a resource whenever it occurs. HTTP IRIs are useful because they can also lead to descriptions, but an RDF parser does not need to dereference every term. Prefixes are only syntactic abbreviations: `ex:river` and its full IRI denote the same term after expansion.

RDF IRI equality compares the IRI strings according to RDF's rules; do not silently equate identifiers by lowercasing paths, removing fragments, decoding arbitrary percent escapes, or following redirects. A web server can redirect two document URLs without asserting that the RDF resources they identify are identical.

A blank node represents an unnamed resource. Labels such as `_:b1` are scoped to the parsed data and are not portable global identifiers. When merging independent documents, preserve the distinction between their local blank nodes. Conversely, preserve shared blank nodes across graphs when the input dataset intentionally shares them. Skolemization replaces blank nodes with fresh, recognizable IRIs under a documented policy; it should not reuse human labels as identifiers.

## Preserve values

An RDF literal combines a lexical form with a datatype, and a language-tagged string additionally carries a language tag. In RDF 1.1, an untagged string has datatype `xsd:string`; a language-tagged string uses `rdf:langString`. The strings `"01"^^xsd:integer` and `"1"^^xsd:integer` are different RDF terms even though a datatype-aware comparison can recognize the same integer value.

Keep three questions separate: is the literal legal RDF syntax, is its lexical spelling valid for its datatype, and does the value satisfy the domain requirement? A parser may accept `"tomorrow"^^xsd:date` as a literal term while a datatype-aware component rejects its lexical value. Unknown datatype IRIs do not supply executable validators.

Use exact decimal lexical forms for quantities that need decimal precision. Preserve timezone absence rather than inventing UTC. Use language tags for natural-language strings; a document's general language does not automatically tag all literals.

## Structure and absence

Represent ordered sequences with RDF lists using `rdf:first`, `rdf:rest`, and `rdf:nil`; ordinary multiple property values are unordered. Lists require structural checks for broken links and cycles when consumed as sequences. RDF containers and RDF lists have different vocabularies and conventions.

RDF has no universal null value. An absent triple, an empty string, zero, an empty list, and an explicit domain-specific “unknown” resource mean different things. Define any unknown/not-applicable convention before importing null-bearing source data.

Read the [RDF Concepts specification](https://www.w3.org/TR/rdf11-concepts/) for the formal term definitions and [XML Schema Datatypes](https://www.w3.org/TR/xmlschema11-2/) for lexical/value-space distinctions.
