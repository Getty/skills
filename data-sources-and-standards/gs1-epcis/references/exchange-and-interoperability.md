# Exchange, APIs, and interoperability

## Select the matching artifacts

Use the official [EPCIS artifact set](https://ref.gs1.org/standards/epcis/2.0.1/artefacts) for JSON Schema, JSON-LD context, SHACL shapes, XML schemas, and interface descriptions. Pin a consistent baseline. EPCIS 2 supports both JSON/JSON-LD and XML; choose the form agreed by the exchanging parties and supported by their tools.

JSON parsing only establishes JSON syntax. JSON Schema adds structural checks. JSON-LD processing establishes the graph interpretation through the context. SHACL can check the relevant graph constraints. XML XSD checks do not cover every business or cross-field constraint either. State exactly which layers were checked.

The EPCIS JSON-LD context uses JSON-LD 1.1 features. Resolve and cache the official version deliberately, preserve extension contexts, and avoid replacing protected standard terms. Do not assume that arbitrary JSON with familiar EPCIS field names has the same linked-data meaning.

## Treat capture as an exchange workflow

A capture client submits events to a repository or receiving application. Confirm supported media types, versions, extensions, limits, and authentication. Validate locally, submit under the agreed contract, and retain request and response correlation without exposing credentials.

The [official REST OpenAPI](https://ref.gs1.org/standards/epcis/2.0.1/openapi.json) defines asynchronous capture behavior. A `202` response can acknowledge receipt and provide a capture-job location; it does not guarantee that every event was successfully stored. Check the job outcome and event-level failures as applicable. Do not count accepted requests as stored events.

Design retries around event identity and the receiver's documented behavior. Preserve the original payload and distinguish transport failures, validation failures, authorization failures, and partial processing. Avoid blind retries that manufacture new IDs for the same assertion.

## Query with explicit scope

Use the standard's event-query semantics, including the distinction between event time and record time, rather than inventing ad hoc filter meanings. Confirm how the interface handles lists, bounds, omitted parameters, pagination, and extension fields. Read the version-matched OpenAPI and query schema before generating exact requests.

Record query conditions, repository identity, retrieval time, and completion state. A first page is not the entire result. Concurrent capture can change results while paging unless the implementation provides a suitable consistency contract. When using overlapping time windows, deduplicate occurrences carefully without losing error declarations.

Subscriptions and callbacks can support ongoing delivery. Agree on the selection, destination, authentication, retry behavior, and recovery after interruption. Do not assume that a network callback provides exactly-once delivery or a complete replay history without an explicit service guarantee.

## Distinguish forms of discovery

Service discovery within an EPCIS interface describes available resources, capabilities, or supported values. Discovering every organization that holds data about an object is a broader supply-chain problem. EPCIS does not automatically create a universal public index of all relevant repositories.

Use partner agreements, directory or discovery services where available, and authorized endpoint information. Treat an inaccessible or unknown repository as a coverage gap. The absence of returned events can mean no matching events, insufficient access, missing data, a query mismatch, or an incomplete search scope.

## Define a partner interoperability contract

Agree the business process and event granularity; identifier forms and normalization; CBV values; required extensions; units; time conventions; error declarations; retention; capture/query versions; and validation profiles. Specify which fields each party can actually supply and which are inferred.

Use original representative traces to check interoperability. Have a receiver reconstruct a serialized item's history, a lot transformation, and an aggregation change. Confirm that corrections alter the derived view while leaving the evidence accessible. Compare semantics after JSON-LD/XML conversion rather than requiring identical field order or serialization.

## Bound the trust claim

An authenticated sender, a valid event hash, and a conforming document answer different questions. They do not independently prove that the physical event occurred as reported. Retain origin and access context, and avoid overstating a trace's completeness. Sector rules, certification evidence, commercial agreements, and physical controls may be needed for the conclusion the user wants.
