# Typed values and RDF projections

## Preserve precision before normalization

For quantities, retain signed arbitrary-precision decimal strings, unit identifiers, and supplied upper/lower bounds. Do not parse through binary floating point before storing an exact decimal. The JSON unit marker `"1"` means unitless. Missing or null bounds mean unspecified uncertainty, not an exact quantity. Bounds are not confidence probabilities.

Synthetic quantity snak from a fictional Wikibase repository; P99 here has no Wikidata meaning:

```json
{
  "snaktype": "value",
  "property": "P99",
  "datatype": "quantity",
  "datavalue": {
    "type": "quantity",
    "value": {
      "amount": "+9007199254740993.10",
      "unit": "1",
      "lowerBound": "+9007199254740993.00",
      "upperBound": "+9007199254740993.20"
    }
  }
}
```

Retain time strings with calendar model, precision, timezone, and supplied before/after fields. Year or month precision does not authorize inventing an exact day. JSON dates can use unknown components and historical year conventions that an ordinary ISO-date parser rejects or misinterprets. Keep a separately derived interval or sortable date with its conversion policy when an application needs one.

Retain coordinate globe and angular precision; do not assume Earth, metres, or a particular projected CRS. Preserve monolingual text's language tag. Preserve external-ID strings exactly, including leading zeros and case where significant. A URL, string, external identifier, media filename, and entity reference can share a simple JSON value type while having different property datatypes.

## Read the RDF predicate family

| Prefix family | Role in the Wikidata RDF export |
| --- | --- |
| `wd:` | Entities |
| `wdt:` | Direct best-ranked values |
| `p:` | Entity to statement node |
| `ps:` / `psv:` | Statement's simple value / full value node |
| `pq:` / `pqv:` | Qualifier simple value / full value node |
| `pr:` / `prv:` | Reference simple value / full value node |
| `psn:` / `pqn:` / `prn:` | Normalized full-value forms where supported |
| `wds:` / `wdref:` / `wdv:` | Statement, reference, and value resources |

Read actual namespace IRIs rather than assuming the same prefixes in every file. Statement nodes carry ranks, qualifiers, and reference links; direct values omit that context. A full export and a truthy export serve different purposes. Simple literal values can omit units, bounds, calendar, or precision carried by full value nodes.

Unknown-value and no-value statements have specific RDF encodings. Dump blank nodes and WDQS Skolem IRIs can differ for unknown values; test the representation's documented predicate or function instead of assuming `isBlank` always works. No-value representation is not simply an absent triple. Do not project these forms into ordinary value strings.

## Account for representation differences

JSON and RDF time encodings are not interchangeable byte strings. The RDF mapping can convert calendar dates to Gregorian values and uses XSD year numbering, while canonical JSON uses its documented original calendar/year conventions. Preserve the original representation and full-value metadata when converting historical dates.

WDQS is an indexed representation with documented differences from dumps, including omitted redundant type triples, metadata placement, and unknown-value handling. A query that works against a dump may need adjustment on WDQS. Query-service results can also lag source revisions; record retrieval time and endpoint.

For a bounded full-statement query, select the statement node and its rank, then separately retrieve relevant qualifier and reference structure. Flattening several qualifiers and references into one joined table can multiply rows. Group by statement and reference identity when reconstructing the structure, and avoid counting joined rows as independent statements.

Use the [RDF Dump Format](https://www.mediawiki.org/wiki/Wikibase/Indexing/RDF_Dump_Format) and [canonical JSON](https://doc.wikimedia.org/Wikibase/master/php/docs_topics_json.html) specifications for exact encodings. Preserve export-format metadata such as RDF `schema:softwareVersion` separately from entity revision metadata. Unknown future types require an explicit compatibility policy, not silent lossy conversion.
