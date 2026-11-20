# Kubernetes CRD validation

## Place the rule at the right schema node

Use `x-kubernetes-validations` in a structural CRD schema. `self` represents the
schema node to which the rule attaches; it is not always the complete resource.
Declare field types, required properties, and ordinary OpenAPI bounds first.
Use CEL for relationships that need expressions rather than duplicating every
schema constraint in custom logic.

For a quota object with required integer `used` and `limit`, attach
`self.used <= self.limit` to that object's schema. A rule attached to the numeric
`used` field instead sees a number as `self`. Inspect placement before debugging
an undeclared-field error.
[CRD validation documentation](https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/).

## Preserve Kubernetes presence and schema semantics

Check how nullable fields, defaults, pruning, and structural schemas affect the
value presented to CEL. Do not copy the general JSON-map null fixture into a CRD
assumption without testing it. Kubernetes documentation defines its own accessible
fields, type mapping, and escaping rules.

List annotations can give map/set behavior and permit correlation across versions.
For schema properties with punctuation or reserved words, use documented escaping
rather than assuming arbitrary dictionary syntax. Prefer simple field names when
designing a new API, but preserve existing public names when repairing one.
[CEL in Kubernetes](https://kubernetes.io/docs/reference/using-api/cel/).

## Model transitions explicitly

Use `oldSelf` for transition constraints when the feature and schema position
support them. A transition rule does not automatically run on creation when there
is no old value. `optionalOldSelf` changes that contract and requires compatible
version/feature support; its `oldSelf` is optional and must be handled accordingly.

Test create, unchanged update, permitted transition, forbidden transition, removal,
and reintroduction. For list members, verify whether old/new elements can be
correlated under the schema. Do not apply an immutability pattern to uncorrelatable
items and assume positional matching is stable.

## Bound work and rollout

Set meaningful `maxItems`, `maxProperties`, and `maxLength` where the data contract
allows them; these support cost estimation and constrain actual input size.
A static cost rejection is different from a runtime budget exhaustion. Rewriting a
nested comparison or using a stronger schema may be better than requesting larger
limits.

Validate the CRD on the target API server, then create and update example resources
in a disposable namespace. Ordinary YAML parsing proves only document syntax.
Check existing stored objects before tightening validation and examine ratcheting
behavior for the target release. Do not call a migration compatible merely because
new valid objects can be created.
