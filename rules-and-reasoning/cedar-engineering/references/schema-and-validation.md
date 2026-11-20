# Schema and validation

## Design one contract for policies and facts

Define entity types, permitted parent types, attributes, actions, and action-specific
principal/resource/context types. Use a human-readable `.cedarschema` for review or
the equivalent JSON schema representation for tooling. Cedar's schema JSON is its
own defined format; running an arbitrary JSON Schema validator does not validate
Cedar policies. See [schema overview](https://docs.cedarpolicy.com/schema/schema.html)
and [Cedar schema format](https://docs.cedarpolicy.com/schema/human-readable-schema.html).

Model one business action at a time. If `read` uses `Document` and `approve` uses
`Invoice`, declare those applicability differences explicitly. A schema action
without an appropriate `appliesTo` declaration does not imply unrestricted use.
Keep optional attributes optional only when absence is meaningful. Distinguish an
attribute that is absent from one that is present with false, an empty set, or an
empty string. Cedar does not supply generic JSON null semantics.

Use common types for repeated record shapes, with names that do not accidentally
shadow primitive or extension types. Use namespaces for stable type qualification.
For a multi-tenant application, decide whether all tenants share a reviewed schema
or require genuinely different models; generating a namespace per tenant is not
itself a security boundary.

## Validate in separate layers

| Layer | Establishes | Does not establish |
| --- | --- | --- |
| Policy parse | Accepted syntax and policy structure | Correct types or intended permissions |
| Policy validation | Compatibility with a chosen schema | Truth of facts or presence of every entity |
| Entity/context schema parsing | Input shape and supported value types | Authoritative origin of supplied values |
| Request validation | Action applicability and request types | That all referenced objects are loaded |
| Host hydration/completeness check | Required principal/resource records and policy-relevant facts were loaded from the designated sources | Correct permissions or future freshness by itself |
| Authorization | Decision for supplied policy/data snapshot | Future validity or actual enforcement |
| Domain review | Agreement with reviewed permission requirements | Universal correctness from a few examples |

Keep the schema revision with both policy release and input adapters. Revalidate
existing policies after a schema change even when an API validates newly submitted
policies automatically. Treat warnings separately from errors: an impossible rule
can be safe to evaluate while still being a broken intended grant.

The official [validation guide](https://docs.cedarpolicy.com/policies/validation.html)
bounds its soundness claim. With conforming inputs, validated policies avoid many
evaluation errors; missing entity data and integer overflow can remain. Request
validation does not prove that the entity store contains every entity a policy will
dereference. Strict validation constrains extension constructors; a permissive mode
can introduce extra runtime error possibilities.

Distinguish a loaded malformed entity from an absent entity. With a required
`suspended: Bool` attribute, schema-aware loading rejects a supplied User lacking
that attribute. It does not require a User record to exist merely because the request
contains its UID. In the official CLI 4.15.0, a broad permit plus a forbid reading
`principal.suspended` returned **Allow with a missing-entity error** for an empty
entity slice, even when the required-field schema and request validation were used.
Require hydration completeness in the host; do not treat successful request validation
as evidence that the suspension, tenant, ownership, or resource records were loaded.

## Repair a validation failure

Minimize the failing policy and the action/schema combination. First check spelling,
namespace qualification, action applicability, and field type. Then inspect optional
attributes and branch guards. Repair the model or the expression that is wrong;
do not make every attribute optional or turn validation off to clear a diagnostic.

For a schema evolution, test old policies with new data, new policies with old data,
and the intended simultaneous release. A change from String tenant IDs to Tenant
entity references is a contract migration, not a harmless rename. Plan a bounded
transition and retain both versions for audit rather than accepting mixed values
implicitly.

Schema composition introduced `external` declarations and linking in language 4.6.
Resolve every required external definition before validation against the resulting
complete schema. A fragment that parses is not necessarily a standalone contract.
See [schema linking](https://docs.cedarpolicy.com/schema/schema-linking.html).
