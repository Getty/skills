# Terraform and CI

## Evaluate the relevant artifact

For plan decisions, inspect JSON from the saved Terraform plan and preserve its
association with the later apply. Evaluating one plan and applying a regenerated
plan breaks that guarantee. Distinguish `terraform show -json` output from state,
HCL, and vendor wrappers before referencing `input.resource_changes`.
[OPA Terraform guidance](https://www.openpolicyagent.org/docs/terraform).

## Preserve unknowns and action meaning

Inspect address, type, mode, actions, before/after, and `after_unknown` for relevant
changes. A value unknown until apply differs from explicit null, omission, or known
compliance. Define whether unknown evidence rejects, defers, or requires review.
Do not use a missing-key default that quietly labels unknown evidence safe.

Treat replacement as the documented action sequence. A destructive-change rule
must handle delete/create combinations and order rather than checking only for a
create action. Inspect `format_version`, reject unsupported major formats, and
handle compatible additive fields deliberately.
[Terraform JSON format](https://developer.hashicorp.com/terraform/internals/json-format).

## Test changes that matter

Include create, update, delete, replace, no-op, and unknown-value cases when the
policy depends on them. Include nested modules and data resources found in the
workload. Report the resource address with every violation so reviewers can locate
its cause without rereading a complete plan.

For tags, distinguish missing keys from unknown values. For network rules, test
broad ranges and malformed representations, not a single public CIDR string.
For cost-related rules, state what static configuration can establish; it cannot
prove real utilization, billed amounts, or dynamic behavior after deployment.

## Enforce the answer

Make CI fail according to the output contract on violations and evaluator failure.
A zero `opa eval` exit code alone does not assert true. Use suitable flags or a
strict consumer, and run the complete CI step with a deliberately failing fixture.
Test structured violations and an undefined entrypoint separately.

Protect plan JSON as potentially sensitive. Keep minimal redacted regression data
that preserves unknown and action semantics. Pin policy/data revisions with the plan
digest. Avoid printing every input value to diagnose one condition.

Where a manual exception is allowed, represent its scope, expiry, approver, and
reason in a controlled data contract. Test that it applies only to the intended
resource/action and cannot silently become an unbounded global bypass. Do not
invent organization-wide approval rules for an ordinary educational example.
