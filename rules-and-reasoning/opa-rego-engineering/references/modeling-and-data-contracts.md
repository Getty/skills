# Modeling and data contracts

## Define the question

Write the question in one sentence, such as whether authenticated subject S may
perform action A on authoritative resource R at time T. Alternatively define the
expected violation set or transformation. Specify what the caller does with each
result category. Separate business vocabulary from transport envelopes.

| Field | Example source | Question |
| --- | --- | --- |
| Subject | Verified session | Which issuer and identity namespace? |
| Action | Application route mapping | Which real operation is being authorized? |
| Resource owner/tenant | Application database | Are these current authoritative facts? |
| Membership | Versioned identity snapshot | What revocation delay is acceptable? |
| Evaluation time | Trusted host clock | Which units and replay behavior? |

These are design questions, not fields mandated by OPA.

## Separate shape and trust

Validate required fields and types in the host. A correctly shaped string saying
“admin” proves no entitlement. Authenticate the principal and map trusted facts
before evaluating policy. Keep caller claims distinct from verified attributes.

OPA can replicate or receive identity/resource facts, but its copy is not inherently
the source of truth. Choose update mechanics according to size, frequency, and
consistency needs. [External data](https://www.openpolicyagent.org/docs/external-data).

Specify stale-data behavior, not only missing-data behavior. A last-known snapshot
may continue to grant a revoked account. Define acceptable age, refresh signals,
and application response when that age is exceeded. A policy hash cannot reconstruct
a decision whose underlying facts changed without recorded revisions.

## Design stable outputs

Choose a Boolean or a documented object:

```json
{"allow":false,"reason_codes":["TENANT_MISMATCH"],"policy_revision":"demo-v1"}
```

Use stable codes for machines and separate prose for people. Avoid returning
internal group membership or sensitive record details to an unauthorized caller.
Keep audit details under the application's normal access controls.

If multiple modules contribute allow/deny candidates, define their combination
explicitly. OPA does not infer deny precedence from the document name. Test a case
matching both, plus a case matching neither. Keep denial reasons derived from the
same conditions as the final decision so explanations do not drift.

## Keep domain logic reviewable

Name concepts such as tenant match, active membership, and permitted action. Keep
input adaptation, reference facts, and final decisions separately testable. Avoid
large “generic” helper interfaces that obscure which facts a permission uses.

For translations from DMN, Cedar, XACML, or JSON Logic, compare value types, absence,
errors, combining behavior, and enforcement first. Preserve source examples and
counterexamples. Agreement on a few happy paths is insufficient to claim semantic
equivalence. When a source has richer diagnostic states, model those explicitly
instead of flattening everything to one Boolean and losing the reason for failure.
