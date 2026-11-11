# Inline XBRL, OIM, JSON, and CSV

## Select the representation

| Representation | Main strength | Interpretation requirement |
|---|---|---|
| XBRL XML instance | Established instance syntax and ecosystem | Full XBRL and taxonomy processing |
| Inline XBRL | Human-readable report with embedded machine facts | Process the document set and transformation rules |
| xBRL-JSON | Convenient exchange of OIM report facts | Preserve namespaces, dimensions, values, and taxonomy references |
| xBRL-CSV | Efficient representation of large tabular reports | Load the associated JSON metadata and table definitions |

The [Open Information Model](https://specifications.xbrl.org/work-product-index-open-information-model-open-information-model.html) defines a syntax-independent report model. It supplements XBRL 2.1 rather than replacing every legacy feature. Do not describe arbitrary JSON containing financial numbers or an ordinary CSV export as conforming xBRL-JSON or xBRL-CSV.

## Extract Inline XBRL correctly

Inline XBRL embeds tagging in HTML/XHTML-based reporting documents. Its extraction rules handle numeric and nonnumeric facts, transformations, scale, sign, continuations, relationships, and potentially multiple target reports. Use a conforming processor and the permitted transformation registry version. Read [Inline XBRL 1.1](https://specifications.xbrl.org/work-product-index-inline-xbrl-inline-xbrl-1.1.html).

Do not extract visible text and assume it equals the fact value. A displayed `123` with scale `3` can represent `123000`. A percentage display may require conversion to a decimal ratio. Text can continue elsewhere in the document; excluded content and markup handling affect extraction. Hidden facts and repeated visible occurrences also require interpretation.

Compare the rendered report with the extracted result. A visually correct number can be tagged to the wrong concept, context, unit, or scale. A technically valid fact can have an unhelpful or misleading visual placement. Preserve source element IDs or equivalent traceability.

## Read an original xBRL-JSON illustration

This fictional fragment shows the report shape. The example taxonomy URL is a placeholder, so the fragment is not a complete independently valid filing.

```json
{
  "documentInfo": {
    "documentType": "https://xbrl.org/2021/xbrl-json",
    "namespaces": {
      "demo": "https://example.org/taxonomy/2025",
      "ent": "https://example.org/entities",
      "iso4217": "http://www.xbrl.org/2003/iso4217"
    },
    "taxonomy": ["https://example.org/taxonomy/2025/entry.xsd"]
  },
  "facts": {
    "f1": {
      "value": "123000",
      "decimals": -3,
      "dimensions": {
        "concept": "demo:Revenue",
        "entity": "ent:NorthHarbor",
        "period": "2025-01-01T00:00:00/2026-01-01T00:00:00",
        "unit": "iso4217:EUR"
      }
    }
  }
}
```

Use the [xBRL-JSON specification](https://www.xbrl.org/Specification/xbrl-json/REC-2021-10-13+errata-2023-04-19/xbrl-json-REC-2021-10-13+corrected-errata-2023-04-19.html) for required members, value encoding, namespace resolution, nil representation, accuracy, and links. The fact ID identifies an occurrence within a report; it is not a globally meaningful business identifier.

## Process xBRL-CSV as a report package

The [xBRL-CSV specification](https://www.xbrl.org/Specification/xbrl-csv/REC-2021-10-13+errata-2023-04-19/xbrl-csv-REC-2021-10-13+corrected-errata-2023-04-19.html) uses metadata to describe tables, templates, columns, parameters, dimensions, and value interpretation. A row can inherit context through metadata; a cell alone may not contain enough information to create a fact.

Resolve metadata before applying spreadsheet conventions to blanks, dates, delimiters, or numbers. Preserve the distinction between absence and explicitly represented values. Check whether a receiving program supports newer optional features such as table constraints before using them.

## Assess conversion loss

Legacy tuples, unrestricted non-dimensional XML context content, and custom XML attributes can fall outside OIM representation. Consult the [xBRL-XML mapping specification](https://www.xbrl.org/Specification/xbrl-xml/REC-2021-10-13+errata-2023-04-19/xbrl-xml-REC-2021-10-13+corrected-errata-2023-04-19.html) and report unsupported constructs. Do not silently discard them while calling the conversion lossless.

For a round trip, compare semantic facts, dimension values, periods, units, accuracy, nil values, and links, with duplicate occurrences and presentation traceability handled by a declared policy. Byte-for-byte equality is unnecessary; loss of reporting meaning is unacceptable when a lossless conversion was promised.
