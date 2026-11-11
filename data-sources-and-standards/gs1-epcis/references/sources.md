# Primary sources and artifact baseline

Examples and workflow recommendations are original synthesis; use the normative sources for exact field and interface rules.

| Source | Purpose |
|---|---|
| [EPCIS archive](https://ref.gs1.org/standards/epcis/archive) | Published version history and persistent links |
| [EPCIS 2.0.1 artifacts](https://ref.gs1.org/standards/epcis/2.0.1/artefacts) | Matched schemas, context, SHACL, ontologies, and API files |
| [EPCIS normative PDF](https://ref.gs1.org/standards/epcis/2.0.1/) | Event model, service behavior, time, corrections, and bindings |
| [CBV archive](https://ref.gs1.org/standards/cbv/archive) | CBV publication history |
| [CBV 2.0.0](https://ref.gs1.org/standards/cbv/2.0.0/) | Vocabulary meanings, identifier forms, and event-hash procedure |
| [EPCIS/CBV implementation guideline](https://ref.gs1.org/guidelines/epcis-cbv/2.0.0/) | Process modeling and implementation explanation |
| [EPCIS linked-data model](https://ref.gs1.org/epcis/) | Browsable classes and properties |
| [CBV linked-data vocabulary](https://ref.gs1.org/cbv/) | Browsable vocabulary values |
| [REST OpenAPI](https://ref.gs1.org/standards/epcis/2.0.1/openapi.json) | Exact endpoints, headers, response codes, and capture-job behavior |
| [JSON-LD context](https://ref.gs1.org/standards/epcis/2.0.1/epcis-context.jsonld) | Term expansion and datatypes |
| [JSON Schema](https://ref.gs1.org/standards/epcis/2.0.1/epcis-json-schema.json) | Structural validation rules |
| [Official examples](https://ref.gs1.org/docs/epcis/2.0.1/examples/) | Non-normative XML and JSON/JSON-LD samples |
| [EPC Tag Data Standard archive](https://ref.gs1.org/standards/tds/archive) | EPC identity and tag encoding versions |
| [Digital Link URI Syntax](https://ref.gs1.org/standards/digital-link/uri-syntax/) | GS1 web identifier encoding and canonicalization |

The archive identifies EPCIS **2.0.1** and CBV **2.0.0**. The PDF served through the EPCIS 2.0.1 link can still carry the cover label “Release 2.0, Ratified, Jun 2022”. Record actual artifact versions; do not invent a schemaVersion of 2.0.1 merely from the bundle path. The Tag Data Standard and the Digital Link URI Syntax are versioned on their own; read the version from each page. Later supporting standards do not automatically change the normative references of an older EPCIS/CBV profile.

Recheck these sources for operational integrations. Validate against the partner's supported baseline and sector profile, and preserve distinctions between normative specifications, implementation guidance, schemas, and illustrative examples.
