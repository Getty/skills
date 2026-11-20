# Entities and context

## Establish trustworthy input

Create the principal from authenticated identity, the action from a controlled
route/operation mapping, and the resource from the object actually requested.
Hydrate roles, ownership, tenant membership, and suspension status from authoritative
application storage. Request-supplied JSON is not trustworthy merely because it
passes schema parsing. If the caller may edit `suspended`, `owner`, or `parents`,
they may edit the answer to their own authorization request.

Before evaluating this application's protected operations, require that its principal
and resource records, mandatory attributes, and relevant relationship/deny facts were
hydrated from those trusted sources. Bind the completeness check to the same snapshot
used for evaluation. A well-typed UID in the request is a reference, not proof that
its record was loaded. Distinguish request applicability, schema validation of loaded
records, and completeness of the selected entity slice. Missing required data should
be an explicit input/service failure at this boundary, not an apparently ordinary
authorization result produced after silently omitting facts.

Represent every entity by its type and immutable ID. Do not reuse a deleted user's
ID for a new account. Separate a display name from identity. The entity model and
ID risks are documented in [entities](https://docs.cedarpolicy.com/policies/syntax-entity.html)
and [identifier guidance](https://docs.cedarpolicy.com/bestpractices/bp-mutable-identifiers.html).

The standard JSON entity collection is an array of objects containing `uid`,
`attrs`, and `parents`, with optional `tags` in supporting versions. `parents`
contains parent entity references, not child IDs. Use `__entity` for entity-valued
attributes when schema-based parsing is not supplying that interpretation. A record
with fields named `type` and `id` is otherwise an ordinary record. See [entity and
context JSON](https://docs.cedarpolicy.com/auth/entities-syntax.html).

## Build the intended hierarchy

Choose an edge meaning before inserting it. A User can be in Team, and a Document
in Folder; those can be different hierarchies with different allowed parent types.
Do not add an `owner` as a parent merely to make an `in` test work: ownership and
containment may have different transitivity and delegation rules.

Ensure graph construction preserves intended transitive relationships. Reject cycles
and conflicting duplicate UIDs at your ingestion boundary. Include the ancestors and
attribute-bearing entities needed by the selected policies. A deliberately partial
slice can omit unrelated objects, but must retain relevant prohibitions as well as
grants. An absent object may still be compared by identity while dereferencing its
attributes fails; use both kinds of cases in tests.

Do not infer membership from a namespace or ID prefix. If entity IDs contain a tenant
identifier for operational convenience, still validate the authenticated tenant and
resource tenant explicitly. Reject a resource identifier that resolves differently
between authorization and execution.

## Use context for request-local facts

Put MFA state, authenticated session claims, request time, or a trusted source IP in
context when they vary per request. Put durable resource properties on entities.
Avoid copying the same property into both places unless conflict resolution is
specified. Do not let an HTTP body select the authoritative time or authentication
strength. Proxy headers require a trusted proxy configuration.

Normalize inputs once, before evaluation, using a versioned convention. Preserve
original evidence where needed for diagnostics. The [normalization guidance](https://docs.cedarpolicy.com/bestpractices/bp-normalize-data-input.html)
is relevant to strings and representations; it does not authorize collapsing distinct
identities.

## Use the graph audit helper narrowly

`audit_entities.py` detects duplicate JSON keys, repeated UIDs, malformed UID objects,
parent cycles, and optionally parents absent from the supplied collection. It does
not validate attribute types, the Cedar type-name grammar, every embedded entity
reference, or a schema. Its `--require-parents` option is a completeness check for
closed test snapshots, not a claim that all omitted parents make a Cedar input invalid.
Run the official parser and schema checks after this inexpensive data audit.
