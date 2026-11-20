# Decisions and combining

## Preserve the outcome space

| Decision | Meaning for diagnosis |
| --- | --- |
| Permit | Applicable policy permits under its conditions/obligations |
| Deny | Applicable policy denies |
| NotApplicable | No applicable decision at that evaluation scope |
| Indeterminate | Evaluation could not determine an ordinary result |

Transport failure is not a fifth XACML Decision; represent it in the adapter's error
contract. Internal Indeterminate{P}, {D}, and {DP} retain which effects could have
occurred and influence combining. Serialize the standard external Indeterminate
value, with appropriate status/diagnostics, rather than inventing new wire values.

## Choose the algorithm by requirement

| Algorithm | Key behavior | Trap |
| --- | --- | --- |
| Deny-overrides (3.0) | Explicit Deny dominates; errors retain potential effects | Not equivalent to “all errors become Deny” |
| Permit-overrides (3.0) | Explicit Permit dominates; errors retain potential effects | A broad Permit may defeat a Deny |
| First-applicable | Select first non-NotApplicable outcome in order | Order is policy meaning |
| Only-one-applicable | Select based on one applicable policy target | Not a count of Permit rules |
| Deny-unless-permit | Permit if any Permit, otherwise Deny | Collapses distinctions in final result |
| Permit-unless-deny | Deny if any Deny, otherwise Permit | Default permissive behavior |
| Ordered override variants | Override semantics with specified evaluation order | Not identical to first-applicable |

Use exact rule-combining versus policy-combining URIs. Some valid algorithms retain
older URI version prefixes; do not rewrite every URI to 3.0. Legacy override
algorithms and the 3.0 definitions differ in their treatment of Indeterminate.
The name alone is insufficient for migration.

## Test combinations that expose errors

For 3.0 deny-overrides: Deny with Permit produces Deny. Permit with Indeterminate{D}
produces Indeterminate{DP}. Permit with Indeterminate{P} can still produce Permit.
These distinctions matter when a missing attribute affects a potential prohibition.

For first-applicable, an early Indeterminate is not skipped as if no rule applied.
For only-one-applicable, two matching policy targets can be an error even if one
policy's internal rules ultimately would not Permit. Do not use it as a uniqueness
checker for arbitrary business outcomes.

Follow normative algorithm definitions when implementing or verifying a PDP.
Use an existing conforming implementation when possible. A hand-written Boolean
reducer cannot preserve this result algebra.

## Keep enforcement separate

An application may block every outcome other than an acceptable Permit. Preserve
the original decision/status in telemetry and test the actual PEP. Normalizing
unknown outcomes to Deny inside a converter can alter behavior when another policy
later combines them.

Authority: [core Appendix C and evaluation rules](https://docs.oasis-open.org/xacml/3.0/errata01/os/xacml-3.0-core-spec-errata01-os-complete.html)
and [additional combining algorithms profile](https://docs.oasis-open.org/xacml/xacml-3.0-combalgs/v1.0/xacml-3.0-combalgs-v1.0.html).
