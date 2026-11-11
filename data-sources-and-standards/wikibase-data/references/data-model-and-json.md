# Data model and canonical JSON

## Identify entities and source boundaries

Scope identifiers to their repository. On Wikidata, items commonly use Q IDs and properties P IDs; additional entity types include lexemes, forms, and senses, while other Wikibase extensions can define their own structures. Do not implement every identifier as a Q prefix plus integer. Prefer the full supplied ID, including entity type, and preserve a full entity IRI where available.

An item can carry multilingual labels, descriptions, aliases, statements, and sitelinks. Properties also declare a datatype. Other entity types have different fields. State which types the parser supports and how it retains or rejects unsupported ones. Do not assume every object has sitelinks or that every statement collection is named `claims`; for example, extension-specific representations can differ.

Separate a response envelope from its entities. An API response may contain errors, continuation, missing-entity indicators, redirects, and metadata alongside content. A filtered response may omit whole components. Missing labels in a filtered response do not prove the source entity has none.

## Retain statement context

A statement contains a main snak, rank, and statement identifier, with optional qualifiers and reference groups. A snak is the property/value assertion component; it can occur as the main value, a qualifier, or a reference component. Preserve its property identifier, `snaktype`, property `datatype`, and `datavalue.type` separately. The latter two describe different layers and are not always the same string.

| Snak type | Meaning | Parser behavior |
| --- | --- | --- |
| `value` | A concrete value is supplied | Preserve and validate the typed datavalue |
| `somevalue` | A value exists but is unspecified | Preserve the explicit unknown-value state |
| `novalue` | The statement says there is no value | Preserve the explicit no-value assertion |

Neither unknown nor no value is equivalent to a missing statement, empty string, zero, or database NULL. Require a datavalue for a concrete snak; flag contradictory datavalues attached to special snak types under the selected contract. Preserve unfamiliar structures in raw data rather than coercing them to strings.

## Treat rank as selection metadata

Retain preferred, normal, and deprecated statements. For best-rank selection, choose all preferred statements for an entity/property if any exist; otherwise choose all normal statements. Do not fall back to deprecated statements. Qualifiers can still make the selected value conditional, historical, or method-specific.

A normal statement is not inherently old or uncertain. A preferred statement is not necessarily the only current value. Deprecated statements may be useful for audit and explanation; dropping them from a convenience view differs from erasing them from source preservation. State the chosen selection policy and whether application acceptance adds further review.

## Preserve multiplicity, grouping, and order

Retain each qualifier occurrence, including repeated values for a property. Retain each reference group as a group of snaks; group boundaries distinguish different evidence descriptions. Keep reference/snak hashes as source metadata rather than universally unique permanent identities. Scope occurrences to their statement and source snapshot.

Treat statement IDs as opaque. Do not rely on letter casing or a fixed internal GUID layout. Associate each statement representation with the entity revision from which it was obtained. A statement can change while retaining its identifier.

JSON object-key order has no semantic significance. Preserve relevant arrays and explicit `qualifiers-order` and reference `snaks-order` arrays. If an order array is absent, record that absence and use an explicitly local display order if needed. Validate that listed property groups exist; do not silently invent missing groups. RDF exports do not preserve all original display ordering.

Use the [canonical JSON specification](https://doc.wikimedia.org/Wikibase/master/php/docs_topics_json.html) for exact fields and the [Wikibase DataModel](https://www.mediawiki.org/wiki/Wikibase/DataModel) for meaning. The [statement](https://www.wikidata.org/wiki/Help:Statements), [qualifier](https://www.wikidata.org/wiki/Help:Qualifiers), [source](https://www.wikidata.org/wiki/Help:Sources), and [rank](https://www.wikidata.org/wiki/Help:Ranking) guides explain Wikidata's editorial conventions.
