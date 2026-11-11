---
name: gs1-epcis
description: "Use when modeling, exchanging or validating GS1 EPCIS 2.x traceability events — CBV business steps and dispositions, GTIN, SSCC, GLN, Digital Link, aggregation, transformation, corrections, sensor data, capture and query interfaces."
---

# GS1 EPCIS and CBV

## Establish the purpose

Treat EPCIS as a standard for expressing and sharing visibility events across systems and organizations. Use its event model to describe what was involved, when something occurred, where it was observed, and the relevant business context; sensor data can add information about how conditions were measured. Use the Core Business Vocabulary (CBV) for shared meanings of business steps, dispositions, transaction types, and related vocabulary. Begin with the [official artifact catalogue](https://ref.gs1.org/standards/epcis/2.0.1/artefacts).

Distinguish an event assertion from a complete supply-chain history, proof of ownership, proof of authenticity, or a regulatory compliance conclusion. EPCIS supplies interoperable structure and semantics; source quality, coverage, permissions, and sector rules determine what can be concluded from the events available.

Keep the skill independent of any particular warehouse system, repository, industry, programming language, or storage technology. Work at the conceptual level for explanations and use precise artifacts and profiles for executable exchange.

## Navigate the references

- Read [event model and selection](references/event-model.md) to choose Object, Aggregation, Transaction, Transformation, or Association events and interpret actions.
- Read [identifiers and vocabulary](references/identifiers-and-vocabulary.md) for GS1 keys, instance versus class identifiers, CBV values, locations, quantities, and extension boundaries.
- Read [time, corrections, and sensors](references/time-corrections-and-sensors.md) for event and record time, timezone offsets, error declarations, event IDs, ILMD, and sensor observations.
- Read [exchange and interoperability](references/exchange-and-interoperability.md) for JSON-LD/XML, capture jobs, query behavior, subscriptions, discovery, and partner contracts.
- Read [workflow and original example](references/workflow-and-example.md) for a worked JSON document, a validation sequence, and traceability acceptance cases.
- Read [primary sources](references/sources.md) for authoritative versions, artifacts, and current-check guidance.

## Follow the working sequence

1. **Describe the real business event.** Identify the process step, participating objects, observer, location, time, and evidence. Distinguish observation from inference. Establish which traceability question the exchange must answer.
2. **Choose identity granularity.** Decide whether the objects are individually serialized, identified by product and lot, or represented as measured quantities. Identify logistics units, reusable assets, parties, and locations separately. Verify assigned identifiers and their intended scope.
3. **Select the event type.** Choose the type whose semantics match the change or observation. Use aggregation for the relevant containment relationship, transformation for input/output conversion, and association for installation or other qualifying durable physical associations. Do not choose an event type solely because it has convenient fields.
4. **Populate business context.** Select CBV business-step and disposition values by their definitions. Distinguish read point from business location, and possession from ownership. Add transaction references and source/destination types only when supported by evidence.
5. **Choose an exchange baseline.** Record EPCIS and CBV versions, identifier conventions, JSON-LD context or XML schemas, sector profile, extension definitions, and API capabilities. Use the matching official artifacts rather than inferring version strings from filenames.
6. **Validate and reconcile.** Check syntax, identifiers, vocabulary, event-specific constraints, time, quantity semantics, and trace consistency. Preserve original assertions and use the standard correction mechanism when a prior assertion is erroneous.
7. **Explain the result.** Provide the modeled event or findings, relevant definitions, validation evidence, assumptions, and any unresolved gaps. For an implementation, include the capture/query contract and trace examples; for a conceptual question, avoid unnecessary deployment detail.

## Apply interpretation rules

Treat `ADD`, `OBSERVE`, and `DELETE` as event-type-dependent business actions; `DELETE` is not a request to erase the event history. Transformation events have their own input/output model and do not use the action field.

Retain `eventTimeZoneOffset` even when event timestamps are normalized to UTC. Distinguish capture acceptance from successful storage of every event. Keep error declarations and corrective events available to downstream consumers.

Verify current primary sources before asserting a version, API feature, identifier conversion rule, or sector-specific obligation. Do not promise global discovery, complete history, product safety, or legal title from a conforming event alone.
