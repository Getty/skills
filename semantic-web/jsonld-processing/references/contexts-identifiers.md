# Contexts and identifiers

## Expand names before judging meaning

A JSON-LD context maps compact terms to IRIs and supplies interpretation rules. Two documents with different aliases can describe the same graph. Two documents with identical property names can describe different graphs when their contexts differ.

```json
{
  "@context": {
    "@version": 1.1,
    "@base": "https://example.org/items/",
    "@vocab": "https://example.org/vocab/",
    "id": "@id",
    "kind": "@type",
    "label": "http://www.w3.org/2000/01/rdf-schema#label",
    "locatedIn": {"@id": "https://example.org/vocab/locatedIn", "@type": "@id"}
  },
  "id": "sample-8",
  "kind": "Specimen",
  "label": "Basalt fragment",
  "locatedIn": "cabinet-3"
}
```

Here `id` and `kind` alias JSON-LD keywords. The relative node identifier resolves against the base. `Specimen` expands using the vocabulary mapping. The `locatedIn` coercion turns its string into a node reference. Without that coercion, a plain string value generally becomes a string literal, not a link.

## Separate base and vocabulary expansion

Use `@base` for relative document/node identifiers and `@vocab` for vocabulary-relative terms where vocabulary expansion applies. Do not treat them as interchangeable defaults. The supplied document URL and API options can affect relative-IRI processing, so a copied document can change meaning when it relies on location.

An `@base` entry in an external context is ignored. Moving an embedded context into a remotely loaded context can therefore change relative-identifier behavior; preserve the intended document base or use explicit identifiers and verify expansion.

Define prefix terms deliberately and use `@prefix` where JSON-LD 1.1's prefix behavior must be explicit. A compact IRI such as `ex:Record` is not the same mechanism as an arbitrary JSON key. Do not assume every colon-containing string is a mapped prefix or every unknown key is an error. Inspect expanded output.

Use an explicit null term mapping to suppress a key intentionally. Distinguish that decision from accidentally omitting a term definition. A broad `@vocab` makes otherwise unmapped keys become IRIs, which is convenient but can turn spelling mistakes into unintended predicates.

## Control value interpretation

A term definition can set `@type` to a datatype IRI, `@id`, or `@vocab`. Choose `@id` for document-relative links and `@vocab` when values should expand as vocabulary terms. Set default language or direction only when it matches the actual content. Override those defaults locally for exceptions.

Context coercion does not validate a datatype's lexical space. Mapping a field to `xsd:date` does not prove that every input string is a valid date. Similarly, coercing to `@id` does not verify that an identifier exists or denotes an instance of an expected class.

## Manage scope and evolution

Context arrays are processed in order, and nested contexts can change interpretation within their scope. Property-scoped and type-scoped contexts make compact documents easier to read but require careful tracing of the active context. `@propagate` controls propagation in supported contexts; do not assume every local context behaves as a global replacement.

Use `@protected` when term definitions must resist incompatible redefinition within the processing rules. It is an interpretation safeguard, not a network trust mechanism or signature. A protected context retrieved from an untrusted location remains untrusted input.

Publish versioned context IRIs for contracts that require reproducible interpretation. Test context changes against expanded fixtures, not only rendered JSON. Renaming an alias may be graph-preserving; changing a mapped predicate, datatype coercion, base, or container can be semantically breaking.

Consult [JSON-LD 1.1 Syntax](https://www.w3.org/TR/json-ld11/) and the [Context Processing algorithm](https://www.w3.org/TR/json-ld11-api/#context-processing-algorithm) for edge cases.
