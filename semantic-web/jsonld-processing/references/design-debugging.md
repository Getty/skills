# Practical design and debugging

## Start with a graph sketch

For a small collection API, first state the intended relationships in ordinary language: specimen 8 has an English label, was collected at site 3, and has two unordered classifications. Then assign the resource and predicate IRIs. Only afterward choose compact JSON keys and containers.

This ordering exposes accidental literal links and unstable identifiers early. A key named `site` is ambiguous until its mapping and value treatment are known. A context can preserve a readable API while making `site` a link and `label` a language-tagged string.

```json
{
  "@context": {
    "@version": 1.1,
    "ex": "https://example.org/",
    "id": "@id",
    "label": {"@id": "ex:label", "@language": "en"},
    "site": {"@id": "ex:collectedAt", "@type": "@id"},
    "classification": {"@id": "ex:classification", "@type": "@vocab", "@container": "@set"},
    "Basalt": "ex:Basalt",
    "Igneous": "ex:Igneous"
  },
  "id": "ex:specimen8",
  "label": "Riverside fragment",
  "site": "ex:site3",
  "classification": ["Basalt", "Igneous"]
}
```

The classifications are links to vocabulary terms. Their array order has no RDF ordering meaning. If the labels need several languages, replace the default-language convenience with explicit values or a language container according to the public interface contract.

## Diagnose disappearing properties

Expand the document under the actual context and base. If a field is missing, inspect its term mapping, local context scope, null value, and container form. An unmapped key without a suitable vocabulary expansion may be dropped rather than reported as an ordinary unknown-field validation error.

If a value survives with the wrong kind, inspect coercion: `@id` and `@vocab` produce node references, datatype IRIs produce typed values, and no coercion usually leaves strings as literals. Compare full IRIs rather than compact aliases when two datasets fail to join.

## Diagnose shape changes

If one value becomes a scalar after compaction, inspect `@set` and array-compaction options. If a related object stops being embedded, inspect framing and reference structure rather than assuming that the underlying relationship disappeared. If a named graph becomes a collection in the default graph, inspect the `@id`/`@graph` arrangement and processor API used.

Avoid debugging by rearranging keys until an output looks right. Produce a minimal input, record the operation/options, inspect expanded output, and compare the resulting RDF quads where relevant. Keep the exact context bytes with the reproduction.

## Migrate an existing JSON interface

Inventory keys that should become predicates, identifiers, presentation-only metadata, or ignored values. Define deliberate handling for nulls and numeric precision. Preserve existing client expectations through a versioned API contract; graph equivalence alone does not preserve a client's field layout.

Test representative documents from each structural variant rather than only a happy-path sample. Include missing optional fields, several values, an explicit node reference, multilingual content, and a context scope boundary. Check whether the input parser rejects duplicate JSON keys before JSON-LD sees the document.

Report a conversion as loss-aware when indexes, empty named graphs, or presentation details cannot round-trip. For general JSON that carries essential non-RDF structure, retain the original document alongside the RDF projection rather than claiming an exact reversible transformation.

Use [JSON-LD 1.1](https://www.w3.org/TR/json-ld11/) for interpretation and [Framing](https://www.w3.org/TR/json-ld11-framing/) for tree-oriented output. The examples above are original and intentionally avoid external retrieval dependencies.
