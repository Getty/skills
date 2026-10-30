# Extraction contracts and evidence

Read this when turning pages into structured records, designing a schema, normalizing values, or explaining what a validator establishes.

## Define the result before prompting

Specify the entity, its identity key, required fields, accepted source representations, and what a completed record means. Distinguish product from offer, company from office, article from revision, or the extractor merges entities in valid JSON.

Describe fields with source-oriented examples. Price: current or former, unit or package, currency, tax, variant. Date: publication, update, event, retrieval. Permit uncertainty instead of filling fields from general knowledge.

In JSON Schema a present `null` differs from a missing property. Set extra-property behavior, pin the dialect, check the provider's supported schema subset for generation, and keep a separate application validator for the full contract. [JSON Schema objects](https://json-schema.org/understanding-json-schema/reference/object)

## Preserve the representation being interpreted

Save the exact UTF-8 snapshot the extractor read, with its SHA-256. When HTML becomes text or Markdown, record the transformation identity and link the result to the original response; keep equivalent immutable identity for JSON, images, and documents. A hash proves byte identity, not reliability.

Record requested and final URL, retrieval time, response classification, locale or session context, extractor version, and, where they affect reproducibility, model, prompt version, schema version, and normalization rules. Keep secrets out. A later retrieval is a new observation, even for the same URL.

Model lineage as source entity → processing activity → derived entity ([W3C PROV-DM](https://www.w3.org/TR/prov-dm/)); the full vocabulary is not needed.

## Use explicit field states

| Status | Meaning | Value and evidence |
|---|---|---|
| `observed` | The inspected source supplies the value. | Normalized value plus supporting evidence. |
| `absent` | Not observed within the inspected record. | Null; implies nothing about the rest of the site. |
| `explicit_null` | Structured source explicitly represents null. | Null; keep the source location. |
| `unparseable` | Relevant material exists but cannot be normalized under the contract. | Null; keep the problematic evidence. |
| `conflict` | Observations disagree and the selection rule cannot resolve them. | Null; keep the competing evidence. |

Only `observed` fields carry values. Never encode uncertainty as an invented zero, empty string, `false`, or guessed category: a free product has an observed zero price, an unavailable price does not; a disabled feature has an observed `false`, an unmentioned one does not.

Put calculations and inferences in a separate derived layer with input references and transformation IDs; a computed discount, inferred country, or guessed date is never an extracted field.

## Attach evidence to the correct record

Reference an immutable snapshot via `snapshot_ref` and give each record its source span. Field evidence keeps `start`, `end` (exclusive), and `quote`, with a declared offset unit and representation: UTF-8 bytes, Unicode code points, and UTF-16 positions are not interchangeable.

Verify that the quote equals the snapshot slice and lies inside the record span; reject a valid quote borrowed from a neighboring product. When a field combines sources, keep separate observations and an explicit merge decision, not one invented span.

A JSON pointer is useful extra evidence for payloads, image identity plus region for screenshots; neither a CSS selector nor a coordinate stays valid across page versions.

The bundled validator is a narrow text-span example. Production contracts may tie record evidence to shared page-level context (a header fixing currency or tax for many prices) through an explicit association rule; never widen every record span to the whole page to make the demo pass.

Evidence matching is mechanical: the quote may still be an old price, another variant, a negation, or misinformation. Assess semantic support separately.

## Normalize conservatively

Keep raw observations. Use explicit, allowlisted exact/string, strict integer, or strict decimal transformations, without hidden locale inference or arithmetic. Resolve decimal separators, units, currency, date order, and time zone through an explicit domain rule, otherwise return an unresolved state.

Reject unexpected types before conversion. Pydantic coerces by default; strict mode keeps type-specific JSON exceptions, so test the actual entry point. [Strict mode](https://pydantic.dev/docs/validation/2.12/concepts/strict_mode/)

Reject duplicate JSON keys and nonfinite numbers before schema validation; Python's default decoder accepts both. Use decoder hooks and disallow nonfinite serialization. [Python JSON](https://docs.python.org/3.11/library/json.html#standard-compliance-and-interoperability)

## Separate the acceptance layers

Check transport, JSON parsing, schema, field-state consistency, evidence integrity, normalization, semantic support, and entity coverage independently, recording which layer rejected a result. A re-prompt is a bounded repair attempt with the original evidence; it never erases the original failure or fabricates a quote.

Establish semantic correctness with human-reviewed fixtures ([evaluation](evaluation.md)). The offline validator proves its declared contract only, not that a model understood the page, that every entity was found, or that the source is true.
