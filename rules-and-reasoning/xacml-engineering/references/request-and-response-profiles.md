# Request and response profiles

## Distinguish context from policy

The core XML Request contains Attributes groups by category, their typed values,
and flags such as ReturnPolicyIdList and CombinedDecision. A Response contains one
or more Result elements. Decisions and status are separate; inspect obligations,
advice, included attributes, and policy identifiers when required by the contract.

The OASIS JSON Profile 1.1 defines request/response interchange between PEP and PDP.
It does not standardize a generic JSON policy language or every product's PAP API.
Do not turn an XML policy into arbitrary JSON and call it a conformant JSON Profile
policy. Some products expose additional formats; name them separately.

## Use the actual JSON profile

Use the Request wrapper and Category array with explicit CategoryId values for a
clear portable example. Each attribute carries AttributeId and Value, with datatype,
issuer, and included-in-result behavior according to the profile. The profile also
defines convenience category names and defaults; verify the selected form before
relying on those conveniences.

Use explicit datatype URIs for compatibility-critical facts. Preserve bag cardinality
and distinguish one value from multiple values. Do not let a generic XML-to-JSON
mapper invent its own array and scalar rules. Numeric and temporal values require
the profile's datatype-specific representation, not whatever a host serializer emits.

The response wrapper is Response with an array of result objects. Inspect Decision,
Status, Obligations, AssociatedAdvice, included categories, and PolicyIdentifierList
where present. JSON uses `Id` for obligation/advice identity where XML uses
ObligationId/AdviceId; do not mechanically copy XML attribute names. Treat unknown
or malformed decisions as adapter failures.

## Handle batches deliberately

CombinedDecision is not an ordinary “AND all responses” switch. Multiple decision
features have specified expansion, correlation, and combination behavior, and require
the applicable profile/engine support. Do not enable the flag merely to reduce
response size.

For a batch, correlate every result to the requested resource/action context.
Test duplicates, missing results, reordering, partial errors, and obligations.
An array of Permit results without trustworthy correlation must not authorize
unidentified resources.

The included example uses single-request XML and JSON forms with CombinedDecision
false. It avoids optional profiles and product-specific category aliases.

## Keep transport separate

Define authentication, TLS, timeout, retry, idempotency, request-size limits, and
content type in the service contract. JSON shape alone does not define a complete
network deployment. HTTP success is independent of Decision. Do not retry a protected
effect merely because a decision request was retried.

Authority: [JSON Profile 1.1 OASIS Standard](https://docs.oasis-open.org/xacml/xacml-json-http/v1.1/os/xacml-json-http-v1.1-os.html)
and [core request/response schema](https://docs.oasis-open.org/xacml/3.0/errata01/os/schema/xacml-core-v3-schema-wd-17.xsd).
