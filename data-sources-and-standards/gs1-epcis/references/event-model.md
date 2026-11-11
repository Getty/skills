# Event model and event-type selection

## Describe visibility with a business assertion

Start with an event sentence: “At this time and place, these identified objects were observed during shipping.” Determine which parts are measured, recorded by an operator, or inferred by a system. Model the business occurrence after suitable interpretation of raw reader data; do not assume every repeated barcode or RFID read deserves a distinct business event.

The [EPCIS implementation guideline](https://ref.gs1.org/guidelines/epcis-cbv/2.0.0/) explains the use of visibility data across processes. Use it for business modeling; use the normative event definitions for exact fields and constraints.

## Select among the five concrete event types

| Event type | Central meaning | Original example | Critical distinction |
|---|---|---|---|
| ObjectEvent | Observation or lifecycle assertion about identified objects | Observe cases at dispatch | No parent-child relationship is created merely by co-observation |
| AggregationEvent | Add, observe, or remove objects from a physical aggregation | Pack serialized cases onto a pallet | Objects retain identities; containment changes |
| TransactionEvent | Associate objects with or disassociate them from business transactions | Associate cases with a purchase-order reference | Transaction association is not proof of physical movement |
| TransformationEvent | Relate inputs to outputs of a transformation | Consume ingredient lots to produce a finished lot | Input/output genealogy differs from repacking unchanged objects |
| AssociationEvent | Associate objects with a parent object or physical location | Install a replaceable component in a machine | Keep installed associations distinct from temporary loads |

Read the [EPCIS core event definitions](https://ref.gs1.org/standards/epcis/2.0.1/) and [linked-data model](https://ref.gs1.org/epcis/) for the complete constraints. Do not treat the common base event type as a sixth interchangeable business pattern.

## Interpret actions in context

For an ObjectEvent, an action concerns the objects' lifecycle within the modeled process. For AggregationEvent and AssociationEvent, it concerns the parent-child relationship. For TransactionEvent, it concerns transaction association. An `OBSERVE` does not necessarily enumerate every child or every object known to a system. A `DELETE` does not mean that the EPCIS record should be deleted.

For a TransformationEvent, use the input and output instance or quantity lists. A transformation identifier can correlate multiple events belonging to one transformation; it is not a substitute for an event identifier. Do not add an action field merely to make the shape resemble an ObjectEvent.

## Choose by identity continuity

Use aggregation when identifiable objects are grouped while retaining identity: cases placed onto a pallet or pallets loaded into a container. Use transformation when inputs contribute to outputs: material consumption, mixing, cutting, or production of a new identified output. A packaging process can involve both patterns if it changes some identities while retaining others; describe each actual proposition rather than force one universal event.

Use association for qualifying physical relationships such as a component installed in equipment or an object assigned to a physical location. The [standard's AssociationEvent explanation](https://ref.gs1.org/standards/epcis/2.0.1/) distinguishes these from more temporary aggregations. This prevents unloading a vehicle's cargo from being confused with removing its installed components. Do not use AssociationEvent as a generic relationship graph between arbitrary organizations or documents.

## Model a small trace

For a fictional food batch, identify ingredient lots, record their transformation into a finished lot, serialize or count the packed trade items at the required granularity, aggregate those items into logistics units, and record shipping and receiving observations. Separate product identity from the carrier of the product and from its transaction references.

Ask what each event allows a consumer to infer. Does an aggregation imply co-location until a later removal under the agreed semantics? Does the available transformation identify all consumed inputs or only a partial contribution? Are receiving and shipping observations from different parties? Retain those qualifications when constructing a trace.

## Avoid unsupported conclusions

A shipping event does not prove delivery. A receiving event does not by itself prove legal title. A sequence missing a shipping event can reflect incomplete sharing rather than impossible movement. A transformation edge establishes reported genealogy, not a validated mass-balance equation. Define additional business rules and evidence requirements explicitly when those conclusions are needed.
