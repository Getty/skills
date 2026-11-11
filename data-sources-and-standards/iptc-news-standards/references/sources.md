# Primary sources and verified publication status

Prefer exact schemas/specifications to marketing landing-page summaries. Record approval date, standard version, document revision, distribution identity, and provider deployment separately.

| Source | Purpose |
| --- | --- |
| [NewsML-G2 overview](https://iptc.org/standards/newsml-g2/) | Item families and official release entry points |
| [NewsML-G2 distribution](https://www.iptc.org/std/NewsML-G2/) | Available versioned packages |
| [NewsML-G2 2.35 specification](https://www.iptc.org/std/NewsML-G2/2.35/specification/NewsML-G2-2.35-specification.html) | Item identity, versioning, QCodes, status, embargo, content, packages, and processing model |
| [NewsML-G2 2.35 Power XSD](https://www.iptc.org/std/NewsML-G2/2.35/specification/NewsML-G2_2.35-spec-All-Power.xsd) | Concrete XML validation contract; retain imported dependencies |
| [NewsML-G2 guidelines](https://www.iptc.org/std/NewsML-G2/guidelines/) | Implementation examples; checked as covering 2.35 |
| [ninjs distribution](https://www.iptc.org/std/ninjs/) | Available JSON Schema versions |
| [ninjs user guide](https://www.iptc.org/std/ninjs/userguide/) | Version-family differences, mappings, and examples; checked as covering 3.2, 2.3, and 1.7 |
| [ninjs 3.2 schema](https://www.iptc.org/std/ninjs/ninjs-schema_3.2.json) | Directly verified JSON Schema 2020-12 contract for the bundled example |
| [IPTC Autumn Meeting 2026 report](https://iptc.org/news/autumn-meeting-2026-report/) | Approval announcement for NewsML-G2 2.36 and ninjs 3.3/2.4/1.8 — the example of an approval that preceded its published files |
| [NewsCodes guidelines](https://www.iptc.org/std/NewsCodes/guidelines/) | Concept identity, multilingual terms, maintenance, retirement, and mapping |
| [Media Topics](https://iptc.org/standards/media-topics/) and [CV server](https://cv.iptc.org/newscodes/mediatopic) | Subject taxonomy and actual concepts |
| [RightsML 2.0](https://www.iptc.org/std/RightsML/2.0/RightsML_2.0-specification.html) | IPTC rights profile; specification document revision 2.0.2 |
| [ODRL 2.2](https://www.w3.org/TR/odrl-model/) | Underlying rights information model |

The newer approval announcement and verified distribution resources differed at checking time. Direct requests for the expected NewsML-G2 2.36 directory and ninjs 3.3 schema returned 404. Do not describe the older examples as the newest approved releases, and do not infer a newer schema's content from the announcement. Recheck before implementing new fields.

Examples are original synthetic data, with one real Media Topics identifier used to illustrate classification. They do not reproduce publisher content or establish rights to external material. Schema checks cover structure; they do not establish factual truth, rights validity, complete provider conformance, or successful handling of every item family. No particular database, ontology, or sibling skill is required.

## Pinned example-schema fingerprints

SHA-256 values of the schema resources retrieved for the examples:

- ninjs 3.2 JSON Schema: `c489437541ff243c5a314d303e2ae8e935303b2251c2c94d9964ae2ae0097fee`.
- NewsML-G2 2.35 Power XSD: `06ef1c5076a32f2568ac8955994029890afac0268f795e3c26642ded52cf0181`.
- Its `xml.xsd` dependency: `61960fb3131e38022caad5360e2f33a3382578ab3c80cd58bd74320ede61b20c`.

Recompute these when downloading; changed bytes require an explicit decision about the validation contract.
