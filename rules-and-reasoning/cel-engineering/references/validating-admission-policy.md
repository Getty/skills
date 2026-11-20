# Kubernetes ValidatingAdmissionPolicy

## Use the complete resource set

Native ValidatingAdmissionPolicy is stable since Kubernetes 1.30 and uses CEL.
A policy defines matching and expressions; a binding activates it for a scope and
selects validation actions. Parameters, when used, add another resource contract.
A policy with no applicable binding is not effective enforcement.
[Policy documentation](https://kubernetes.io/docs/reference/access-authn-authz/validating-admission-policy/).

Use `admissionregistration.k8s.io/v1` for the stable profile, checking the actual
cluster. Match operations, API groups/versions, resources/subresources, selectors,
and match conditions deliberately. Policy-local matching and binding scope both
matter. Avoid broadening scope when the user only requested a specific workload.

## Bind the right variables

Use the documented variables such as `object`, `oldObject`, `request`, `params`,
and `namespaceObject` only where available. DELETE and CREATE have different object
availability. Type checking uses matched resource schemas, so broad or wildcard
matching may affect diagnostics. Inspect status warnings without treating their
absence as complete semantic validation.

Test expressions against a real matched object. An ordinary CEL environment declaring
`object:dyn` cannot reproduce Kubernetes schema adaptation or extension functions.
[Policy API](https://kubernetes.io/docs/reference/kubernetes-api/admissionregistration/validating-admission-policy-v1/).

## Keep validation and failure handling distinct

Bindings choose actions such as Deny, Warn, and Audit. Deny and Warn cannot be
combined in one binding. `failurePolicy` controls evaluation/configuration errors;
it is not a replacement for the action taken on a false validation.

Match conditions have their own skip/error behavior. A false match condition can
skip evaluation even when another condition errors; when no condition is false,
errors are handled through the policy's failure setting. Verify the target API's
behavior rather than applying ordinary validation-result intuition.

## Handle parameters precisely

Declare `paramKind` on the policy and choose `paramRef` on the binding. Decide
what zero, one, or multiple matching parameter objects mean. Set
`parameterNotFoundAction` deliberately; `Deny` delegates missing-parameter failure
to the policy failure behavior rather than magically overriding `Ignore`.

An admission request may be evaluated for multiple applicable policy/binding/parameter
combinations, all of which must satisfy the configured enforcement. Do not assume
a more permissive parameter cancels a restrictive one. Consider authorization to
read parameter resources and namespace resolution when designing the policy.
[Binding API](https://kubernetes.io/docs/reference/kubernetes-api/admissionregistration/validating-admission-policy-binding-v1/).

## Verify actual effect

Use a constrained test namespace. Test an allowed resource, a failed validation,
a wrong operation that should not match, a missing parameter, and an expression
error. Record server version, admitted/rejected outcome, warnings/audit output,
and policy/binding versions. The bundled example is a starting artifact, not a
claim that a live cluster was configured or tested.
