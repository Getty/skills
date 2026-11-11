# Time, corrections, event identity, and sensors

## Preserve distinct clocks

`eventTime` identifies when the business event occurred. `recordTime` is repository bookkeeping associated with recording the event; it does not describe the real-world event itself. The capture interface does not use a sender-supplied record time as the event's authoritative business time. `creationDate` belongs to the document envelope. Sensor observations can have their own measurement time or interval. See the [EPCIS standard](https://ref.gs1.org/standards/epcis/2.0.1/).

Keep late arrival visible. An event captured today can describe something that happened yesterday. Order a trace using the question's relevant time, and retain both event and recording information for incremental retrieval and audit. Do not “repair” a late event by changing its business timestamp to the receipt time.

`eventTimeZoneOffset` captures the local offset at the event's time and place. It can be `+01:00` while `eventTime` is expressed in UTC with `Z`; the fields serve different purposes. Do not require their textual offsets to match. Determine the local offset for that date, including daylight-saving changes, rather than using the location's current offset.

## Correct an assertion without rewriting history

First distinguish a real business reversal from a statement that was wrong. If goods really moved back, model the return as ordinary events. If the original shipping assertion never happened or had erroneous data, use the standard's error-declaration mechanism as appropriate.

An error declaration repeats the prior event's fields, except for the added error declaration and potentially `recordTime`. It retains the original `eventTime` and event ID if present. Its `declarationTime` records when the error was declared. Corrective-event references can identify replacement assertions. The original remains in the history; consumers must interpret the correction relationship. Refer to the standard's ErrorDeclaration section for exact rules.

Avoid implementing corrections as an ordinary update keyed only by event ID. The correction mechanism is the defined exception to normal event-ID uniqueness. Preserve both assertion and declaration, and update derived trace views through explicit logic. A consumer that ignores error declarations can reconstruct an incorrect history even though every document parses successfully.

## Choose event identity deliberately

An event ID identifies an event assertion, not a product, shipment, or transformation process. CBV describes UUID-based and event-hash approaches. If using a content-derived event ID, follow the canonicalization procedure in [CBV](https://ref.gs1.org/standards/cbv/2.0.0/); hashing arbitrary serialized JSON is not equivalent. Key order, alternate identifier forms, and timestamp representations can otherwise produce different hashes for the same semantics.

Define a retry policy that recognizes resubmission of the same assertion without merging two distinct observations. A second scan at a later business time is not automatically a duplicate. A repeated payload with an unchanged event ID can be a transport retry, a prohibited conflict, or the permitted error-declaration case; distinguish them.

## Attach sensor evidence with context

EPCIS 2 supports sensor information associated with events. Retain the measured property, value or supported summary statistic, unit, measurement time or interval, device or method metadata where available, and reference to raw data when relevant. Use the official [sensor model and artifacts](https://ref.gs1.org/standards/epcis/2.0.1/artefacts).

A temperature value without unit, interval, or association to the monitored goods may be unsuitable for a cold-chain conclusion. An average can hide an excursion. A sensor attached to a container does not automatically measure every item's internal condition. Explain the evidentiary scope rather than converting one reading into a safety or compliance claim.

## Keep ILMD stable in purpose

Instance/Lot Master Data describes properties associated with a particular instance or lot, such as production or expiry attributes. It is intended for that object's lifecycle, not for continually changing observations such as temperature. The [implementation guideline](https://ref.gs1.org/guidelines/epcis-cbv/2.0.0/) helps distinguish master data and event information.

Follow the permitted event placements: ILMD is associated with ObjectEvent `ADD` and TransformationEvent outputs under the core rules. Do not attach it indiscriminately to every shipping observation. If a value changes because a source assertion was wrong, preserve a correction trail rather than treating mutable sensor readings as master data.
