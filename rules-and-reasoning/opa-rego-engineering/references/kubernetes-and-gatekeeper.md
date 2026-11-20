# Kubernetes and Gatekeeper

## Identify the product

Distinguish OPA Gatekeeper from native Kubernetes CEL validation. Gatekeeper has
its own templates, constraints, inventory, audit, and embedded OPA release. A `.rego`
file alone does not register admission enforcement. Native ValidatingAdmissionPolicy
uses CEL and bindings; use `cel-engineering` for that surface.

## Author a template and constraint

A ConstraintTemplate defines a constraint kind and its parameter schema. A constraint
instance supplies actual parameters and matching scope. For
`templates.gatekeeper.sh/v1`, supply explicit structural schema types and test that
invalid parameters are rejected.

Current docs select Rego v1 through `spec.targets[].code[]`, `engine: Rego`, and
`source.version: "v1"`. Do not paste v1 syntax into the legacy `rego` field and
assume an import chooses the right parser. Inspect the deployed Gatekeeper/OPA
pair. [Constraint templates](https://open-policy-agent.github.io/gatekeeper/website/docs/constrainttemplates/).

Use target `admission.k8s.gatekeeper.sh` with the appropriate violations contract.
A set of violation objects is different from a Boolean permission. Keep domain
helpers behind an adapter rather than renaming `allow` without changing its type.

## Use the actual envelope

Read reviewed object fields through `input.review.object` and constraint parameters
through `input.parameters`. Inspect operation, old object, kind, resource, namespace,
and identity for the actual mode. Audit cannot provide every admission-only field;
handle rules depending on request context accordingly.
[Admission review input](https://open-policy-agent.github.io/gatekeeper/website/docs/input/).

For DELETE and subresources, verify which object exists before accessing nested
fields. Pod admission and Deployment template checking see different structures
and different lifecycle stages. Match the resource that actually reaches the rule.

## Verify applicability and effects

Check separately that the template established its CRD, the constraint accepted
parameters, matching selected the intended resources, policy logic emitted the
expected violations, and enforcement actually produced the requested outcome.

Use disposable environments or supplied fixtures. Track exclusions, webhook failure
policy, controller health, and audit lag during rollout. A clean audit report cannot
prove every admission operation was enforced. Preserve recovery access while making
scope changes explicit and reviewable.

For inventory-dependent rules, account for synchronization delay and missing related
objects. Avoid assuming that a cache snapshot is transactionally identical to the
API server state under evaluation. Record whether a rule is a best-effort consistency
check or a strict admission invariant and test its documented failure behavior.
