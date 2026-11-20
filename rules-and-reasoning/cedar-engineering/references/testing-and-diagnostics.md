# Testing and diagnostics

## Test permissions as observable behavior

Build a request matrix before expanding a policy. For every intended grant, include
a nearby denial by changing one relevant fact: tenant, owner, role, action, resource,
MFA status, suspension, or relationship. Include a no-matching-policy case and an
explicit-forbid case; both return Deny but have different diagnostic evidence.

| Family | Useful counterexample |
| --- | --- |
| Hierarchy | Direct member, indirect member, unrelated entity, and container itself |
| Attributes | Required present, optional absent, wrong type, and changed value |
| Tenant boundary | Same IDs/display names in another tenant; cross-tenant owner |
| Explicit denial | Permit and forbid both match; forbid alone; forbid errors |
| Revocation | Cached prior grant after membership, policy, or suspension change |
| Enforcement | Authorized object differs from the object passed to storage |
| Schema evolution | Old/new policy and data combinations during deployment |

Assert the decision and whether errors occurred. Where useful, assert determining
policy IDs, while avoiding an incidental dependence on their returned order. All
matching permits may determine an Allow; Deny can identify matching forbids or have
an empty reason set under default denial. Diagnostics are not a full execution trace
of every expression. See [authorization responses](https://docs.cedarpolicy.com/auth/authorization.html).

Use the official CLI's `run-tests` format or the pinned SDK test APIs. Keep test
inputs separate from production records, and make expected grants reviewable by a
person responsible for the permission model. Regression tests should preserve the
counterexample that motivated a policy repair.

## Validate negative behavior too

Keep invalid-policy tests apart from valid-policy authorization tests. A deliberately
unguarded optional attribute should fail validation when its schema makes the access
unsafe. A missing required input should fail schema-aware parsing or request validation;
without that boundary check it may instead reach the evaluator and produce a policy
error. These are different intended assertions, not conflicting results.

Exercise the dangerous combination of a matching permit and an erroring forbid.
The bundled `unsafe-forbid.cedar` is intentionally invalid for the bundled schema
and demonstrates why a policy diagnostic cannot be ignored blindly. It is not a
recommended production policy.

## Diagnose the narrowest failed layer

For an unexpected Deny, inspect: authenticated principal UID; action mapping; exact
resource UID; policy revision; required entity parents and attributes; context; matching
permit; matching forbid; evaluation diagnostics. Do not immediately broaden the
permit. For an unexpected Allow, inspect competing permits, missing forbids, hierarchy
reflexivity/transitivity, spoofable facts, and stale cached grants.

Validation can prove particular typing properties under its assumptions. It does
not prove the intended tenant separation or ownership semantics. Formal analysis
and symbolic tools can strengthen selected properties when their supported language
profile and assumptions are explicit; keep those claims separate from example tests.
See [validation guarantees](https://docs.cedarpolicy.com/policies/validation.html) and
[the verification paper](https://www.amazon.science/publications/how-we-built-cedar-a-verification-guided-approach).
