# Language and semantics

## Contents

- [Decision algebra](#keep-the-decision-algebra-explicit)
- [Guarded denial for missing facts](#deny-when-an-acceptable-fact-is-not-established)
- [Policy structure](#read-a-policy-structurally)
- [Values and operators](#preserve-values-and-operators)

## Keep the decision algebra explicit

Evaluate each relevant policy against one principal/action/resource/context tuple.
Combine satisfied policies as follows: a satisfied forbid determines Deny; otherwise
one or more satisfied permits determine Allow; otherwise return Deny. An evaluation
error omits that policy and produces diagnostics. Order does not provide priorities.
See the [authorization specification](https://docs.cedarpolicy.com/auth/authorization.html).

Use this table when reviewing error handling:

| Permit outcome | Forbid outcome | Cedar decision |
| --- | --- | --- |
| true | false | Allow |
| true | true | Deny |
| false | false | Deny |
| error | false | Deny |
| true | error | Allow, with an error diagnostic |

The last row is essential: a broad permit plus a fragile forbid can unintentionally
authorize when the forbidding condition cannot be evaluated. Require reliable inputs
for important prohibitions and exercise the exact error case. If the application
rejects every response containing errors, document that additional enforcement rule;
it changes availability and is not Cedar's combining semantics.

## Deny when an acceptable fact is not established

For a User/action population whose suspension status must be explicitly known false,
use a guarded condition rather than letting a missing attribute make a prohibition
error. This standalone fragment passed strict validation in CLI 4.15.0 against a
schema with `suspended?: Bool` and a read action applying to User principals:

```cedar
forbid(principal, action, resource)
unless { principal has suspended && principal.suspended == false };
```

In that profile, a matching broad permit alongside this forbid produced these results
in actual evaluation without schema-based input rejection:

| Principal data supplied | Decision | Evaluation errors |
| --- | --- | --- |
| `suspended: false` | Allow | 0 |
| `suspended: true` | Deny | 0 |
| Attribute absent | Deny | 0 |
| String `"false"` instead of Boolean | Deny | 0 |
| Principal entity absent, or entire entity slice empty | Deny | 0 |

The `has` guard avoids dereferencing an absent attribute/entity, and equality accepts
only the intended Boolean false. A schema-aware input path should reject wrong-typed
loaded data before evaluation. The optional field is explicit in this example; do
not weaken a genuinely required production field merely to suppress input errors.
See the [operator semantics](https://docs.cedarpolicy.com/policies/syntax-operators.html).

Constrain the policy scope if the store also serves principal types or actions for
which this suspension contract does not apply. The broad fragment would otherwise
deny those populations too. This rule protects this one condition: it does not prove
resource existence, ownership, tenant isolation, freshness, or authenticity. Continue
to require trusted hydration and inspect diagnostics from the full policy set.

## Read a policy structurally

A policy has an effect, mandatory principal/action/resource scope, optional `when`
and `unless` conditions, and a terminating semicolon. A `when` condition must hold;
an `unless` condition must not hold. Multiple conditions constrain the same policy.
Use scope conditions for identity, type, or hierarchy restrictions and Boolean
conditions for attributes. Keep names fully qualified outside their schema namespace.
See [basic policy syntax](https://docs.cedarpolicy.com/policies/syntax-policy.html).

Do not use `unless` as a substitute for explicit error handling. If evaluating its
expression fails, the entire policy fails. Make optional accesses safe with `has`.
For example, `context has mfa && context.mfa` is a Boolean expression that treats
an absent optional value as false while retaining the distinction in caller logs.

## Preserve values and operators

Use Bool, signed 64-bit Long, String, Set, Record, entity references, and supported
extension types. There is no implicit truthiness, general floating-point number,
or general null literal. Arrays in Cedar input JSON represent sets. Set order is
irrelevant; duplicate handling must not carry application meaning.

`==` compares entity identity. `in` checks reflexive, transitive membership, whereas
set membership uses collection operations such as `contains`. Test a subject equal
to the supposed container when equality would be too permissive. `has` checks
attribute presence; `is` tests an entity type. `like` is Cedar pattern matching,
not a full regular-expression engine. Preserve `&&`/`||` short-circuit structure
when guarding attribute reads. Check [operators](https://docs.cedarpolicy.com/policies/syntax-operators.html)
for exact accepted operands rather than borrowing JavaScript semantics.

Parse IP addresses, decimals, datetimes, and durations using supported extension
constructors or schema-aware input handling. Decimal has fixed precision; datetime
and duration are distinct types, not raw Long timestamps. Check extension availability
in the host. Use literal constructors in strictly validated policies and provide
dynamic extension values through properly typed input. See [data types](https://docs.cedarpolicy.com/policies/syntax-datatypes.html).

Treat string normalization as an application decision. Case folding, Unicode
normalization, URI interpretation, and email aliases must agree across identity,
resource loading, and policies. Never apply an ad hoc normalization only at the
policy boundary and assume that it preserves identity.
