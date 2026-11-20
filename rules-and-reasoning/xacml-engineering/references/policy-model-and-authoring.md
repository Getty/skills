# Policy model and authoring

## Build a clear hierarchy

A PolicySet combines policies or policy sets, including resolvable references.
A Policy combines Rules. Each Rule has an Effect of Permit or Deny, with optional
target and condition. A false condition does not reverse the Effect; it means
the rule does not apply. A policy can also define variables and obligation/advice
expressions. Preserve schema element order when authoring XML.

Choose stable PolicyId, PolicySetId, and RuleId values. Keep version selection and
reference resolution explicit. A file path is not necessarily a policy identity,
and a loaded directory is not automatically the intended root policy. Detect
unresolved references, cycles, unintended duplicate versions, and ambiguous roots.

## Separate target and condition

Targets define applicability. An empty Target matches everything. A Target combines
its AnyOf children with AND; each AnyOf combines AllOf alternatives with OR; each
AllOf combines Match elements with AND. Model alternatives at the correct layer.
Adding a second AnyOf narrows scope, whereas adding another AllOf inside an AnyOf
can broaden it.

A Match compares a literal with values selected from an attribute source using its
named matching function. Conditions support richer Boolean expressions through Apply,
functions, designators, selectors, and variables. Do not replace the target structure
with an invented free-form expression field.

Keep action/resource scope near the policy boundary. A condition that checks a role
without constraining the resource/action may unintentionally apply to many requests.
Do not use a catch-all Permit as a convenient fallback unless that is the reviewed
requirement.

## Make maintenance changes reviewable

Use an attribute dictionary with category, ID, datatype, cardinality, issuer policy,
source, and freshness. Use descriptive synthetic IDs in examples; do not borrow
production user identifiers. Include acceptance and rejection cases for every rule,
and at least one request outside the policy's scope.

Changing combining algorithms, target structure, or missing-data handling can alter
outcomes beyond the edited rule. Review those changes against the full effective
policy set, not just one XML fragment.

Use the actual published namespace
`urn:oasis:names:tc:xacml:3.0:core:schema:wd-17`.
The `wd-17` suffix is part of the normative 3.0 schema identifier. Do not “modernize”
it by substituting an invented final-version namespace.

Authority: [core schema and policy elements](https://docs.oasis-open.org/xacml/3.0/errata01/os/xacml-3.0-core-spec-errata01-os-complete.html)
and [official XSD](https://docs.oasis-open.org/xacml/3.0/errata01/os/schema/xacml-core-v3-schema-wd-17.xsd).
