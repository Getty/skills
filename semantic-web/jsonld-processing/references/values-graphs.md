# Values, collections, and named graphs

## Represent values explicitly

Use an `@id` object for a node reference and an `@value` object for a literal when compact coercion would hide an important distinction. A value object can express a datatype or a language tag; a language-tagged value is not simultaneously an arbitrary typed literal. JSON-LD syntax rules also constrain which other keywords may accompany each kind of object.

```json
{
  "@context": {"ex": "https://example.org/"},
  "@id": "ex:sample9",
  "ex:title": [
    {"@value": "River sample", "@language": "en"},
    {"@value": "Flussprobe", "@language": "de"}
  ],
  "ex:mass": {
    "@value": "12.50",
    "@type": "http://www.w3.org/2001/XMLSchema#decimal"
  },
  "ex:storedAt": {"@id": "ex:cabinet3"}
}
```

The mass uses a string lexical form with an explicit decimal datatype so ordinary JSON floating-point handling need not alter its spelling. Verify the RDF conversion behavior of the actual processor and preserve source lexical data separately if exact byte reconstruction matters.

JSON booleans and numbers have defined RDF conversion rules, but host-language parsing can already have lost numeric precision. Reject or specially handle numbers outside the required exact range before that happens. JSON `null` is generally ignored in JSON-LD processing; it is not a universal RDF null node.

## Distinguish sets from lists

Multiple values of an ordinary property are unordered. An input JSON array does not by itself create an ordered RDF sequence. Use `@list` when order is semantic. Repeated entries in an RDF list can be represented through distinct list cells, while repeated identical RDF property triples collapse under graph set semantics.

A term with `@container: "@set"` helps keep compacted values as arrays, including single values. It does not impose ordering or validate uniqueness. A term with `@container: "@list"` exposes an ordered list naturally. JSON-LD 1.1 supports lists of lists, including recursively interpreted nested arrays under a list container. Check processing mode and actual processor support when interoperating with JSON-LD 1.0 systems; do not impose their older restriction on a 1.1 document. Explicit intermediate nodes remain useful when individual collections need identifiers or additional properties.

Language maps, index maps, identifier maps, and type maps are alternate compact organizations. Their map keys do not all become ordinary RDF properties. Plain `@index` metadata can be lost in RDF conversion unless a mapping makes that information part of the graph. Document which structure is presentation and which is semantic data.

Under an `@list` container, singleton and empty lists remain arrays in compacted output. Do not switch to an unordered set merely to retain that interface shape.

## Reuse nodes and express direction

Repeat an `@id` to add descriptions of the same node. Nesting a node object does not imply ownership, isolation, or a fresh identity. Without an identifier, an object can produce a blank node; generated blank-node labels are not durable API keys.

When combining independently processed documents or RDF outputs, standardize their blank nodes apart unless a deliberate shared-identity contract says otherwise. Two separate conversions can both generate `_:b0`; concatenating those labels can accidentally merge unrelated nodes. Use dataset-aware merging with fresh per-input blank-node mappings, while preserving intended blank-node sharing within each input dataset. Stable cross-document identity should use deliberate IRIs or an explicit identity scheme.

Use `@reverse` for an incoming relationship when that JSON view is helpful. Reverse properties still describe the same directed RDF predicates; they do not create a new inverse-property definition. Reverse relationships must point to nodes, not literal values.

## Organize graphs deliberately

An object with `@id` and `@graph` can identify a named graph. A top-level `@graph` without a graph identifier commonly groups nodes in the default graph. Do not interpret arbitrary nesting as a named-graph boundary.

```json
{
  "@context": {"ex": "https://example.org/"},
  "@id": "ex:surveyGraph",
  "@graph": [
    {"@id": "ex:sample9", "ex:collectedBy": {"@id": "ex:team2"}}
  ]
}
```

The graph name does not automatically assert who collected, published, or trusts all its statements. Add explicit metadata according to the chosen vocabulary. Check whether the destination retains empty named graphs and dataset-wide blank-node sharing.

JSON-LD 1.1 also offers direction information and `@json` values. Confirm the processor's RDF-conversion options and downstream datatype support; do not assume these features become native RDF 1.2 terms automatically. See the [Syntax specification](https://www.w3.org/TR/json-ld11/) and [RDF conversion algorithms](https://www.w3.org/TR/json-ld11-api/#rdf-serialization-deserialization-algorithms).
