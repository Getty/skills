# Modeling workflow and original JSON example

## Work from the traceability question

For an original fictional scenario, a warehouse observes one serialized item at a dispatch door during shipping. The goal is to share that observation and its business state. The event does not claim receipt by the customer, a transfer of title, or a complete history.

Choose an ObjectEvent because the assertion concerns an observation, not a new aggregation or transformation. Use `OBSERVE`, the CBV shipping business step, and an in-transit disposition. Identify the observation point and the time. Use an event ID for traceable capture and correction.

```json
{
  "@context": "https://ref.gs1.org/standards/epcis/2.0.1/epcis-context.jsonld",
  "type": "EPCISDocument",
  "schemaVersion": "2.0",
  "creationDate": "2026-11-11T13:05:00Z",
  "epcisBody": {
    "eventList": [
      {
        "type": "ObjectEvent",
        "eventID": "urn:uuid:4d0c0fc8-57b2-4faa-93fe-9e29441ebc86",
        "eventTime": "2026-11-11T13:00:00Z",
        "eventTimeZoneOffset": "+01:00",
        "epcList": ["https://example.org/items/serialized-42"],
        "action": "OBSERVE",
        "bizStep": "shipping",
        "disposition": "in_transit",
        "readPoint": {"id": "https://example.org/locations/dispatch-door-4"}
      }
    ]
  }
}
```

The generic example.org identifiers deliberately avoid claiming a real GS1 assignment. EPCIS supports URI-based identity, but a partner's GS1 or sector profile can require particular assigned identifier forms. This illustration does not claim compliance with every CBV or sector-specific profile. Replace the identifiers with verified appropriate identities for a real exchange.

The document uses the 2.0 event schema version while pinning the published 2.0.1 artifact context. Inspect the official [JSON Schema and context](https://ref.gs1.org/standards/epcis/2.0.1/artefacts) rather than changing every version string to match a package label.

## Validate the meaning as well as the shape

Check that the example parses, satisfies the chosen JSON Schema, and expands using the expected context. Then check the business interpretation: the object identifier is instance-level; the event is an observation; the local offset is plausible for the location and date; and the CBV values express the intended step and state.

The UTC event timestamp and `+01:00` local offset are intentionally different textual offsets describing the same local context. No sender-supplied `recordTime` is included. The five-minute gap before document creation is transport/document timing, not a second movement event.

## Build a complete modeling pass

1. Describe the process step and evidence in ordinary language.
2. Inventory objects, classes/lots, parents, locations, parties, and transaction references.
3. Select an event type and confirm its action and mandatory-field rules.
4. Choose identifier forms and CBV values from the agreed baseline.
5. Populate timestamps, quantities, sensor details, and extensions with explicit meanings.
6. Validate structure, vocabulary, identifier interpretation, and process consistency.
7. Capture the event and verify the processing result, then query it under a representative access role.
8. Reconstruct the expected trace and compare it with the original business statement.

Do not fill missing quantities with zero or missing times with the current clock. Mark unresolved inputs for the caller or provide a clearly labeled partial modeling proposal.

## Use targeted acceptance cases

Check one serialized object at two observation times; one lot with an unspecified quantity; a measured quantity with its unit; a pallet whose children are partly removed; an installed component unaffected by cargo unloading; a transformation with several inputs and outputs; a late-arriving event; an erroneous assertion with a declaration; and a failed asynchronous capture job.

For identifier interoperability, compare supported EPC and Digital Link forms without losing serial or lot qualifiers. For extension interoperability, confirm that the receiver preserves and understands each required extension. For queries, test a result large enough to require pagination and verify that the final page is included.

## Report results precisely

Present the chosen event type and why it matches the business occurrence, the identifier and vocabulary decisions, the validation layers actually executed, and any missing evidence. If a trace is incomplete, specify the missing coverage. If a conversion loses an extension or changes identity granularity, report that loss directly. A clean schema result supports structural conformance; it does not establish physical truth or end-to-end traceability.
