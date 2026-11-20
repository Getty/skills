# Templates and schema linking

## Reuse authorization statements safely

A template contains `?principal`, `?resource`, or both in supported scope positions.
A linked policy binds those slots to concrete entities and retains a relationship
to the template. Slots are not arbitrary expression parameters and there is no
generic `?action` slot. Do not implement templates by concatenating unescaped user
text into policy source. See [templates](https://docs.cedarpolicy.com/policies/templates.html).

For example, a sharing template can constrain `principal == ?principal` and
`resource == ?resource` while fixing the read action. Bind both UIDs through the
SDK's link operation, validate the template, and check the linked instance. If the
scope uses `in`, the binding means a hierarchy scope rather than one exact object.
That distinction materially changes the grant.

Track the template revision, linked policy ID, bound slots, creator, and revocation
history. A template edit changes every linked policy that uses it once the edited
policy set is deployed. Test representative linked instances before release. For
permission revocation, remove or disable the effective link and invalidate caches;
merely changing a user's display name does nothing to the bound immutable ID.

Preserve annotations as metadata. Do not rely on an annotation as an access constraint
unless the host explicitly interprets it before evaluation. The example `@id` labels
are recognized by the CLI for useful test diagnostics; portable SDK code should use
explicit policy IDs when constructing its policy set.

## Compose schema ownership separately

Language 4.6 introduced external entity/action declarations and schema linking.
A team can declare a type it references while another schema fragment defines it.
Link fragments using the selected SDK's supported linker, inspect diagnostics, and
require a complete resulting schema where complete validation is intended. Do not
replace an unresolved external type with an unconstrained record.

See [schema linking](https://docs.cedarpolicy.com/schema/schema-linking.html) and the
[language history](https://docs.cedarpolicy.com/other/doc-history.html). This is versioned
language functionality; a managed service or older binding may not expose it.

When schemas are owned by multiple teams, establish naming ownership, allowed parent
relationships, action applicability, and release compatibility. Detect contradictory
definitions before releasing policies that reference them. Test the complete linked
schema against the full policy set, not just each fragment against its own examples.

Keep schema linking distinct from template linking: one resolves type/action
definitions; the other produces concrete policy instances. Neither operation loads
runtime entity facts, performs authentication, or establishes trusted tenant routing.
