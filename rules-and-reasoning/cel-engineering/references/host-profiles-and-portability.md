# Host profiles and portability

## Treat the environment as part of the rule

A useful portability record includes runtime release, variable names/types,
namespace, descriptors, enabled macros, functions, optional-value support, cost
limits, error handling, and expected result type. Source syntax alone is not enough.
Keep this record beside expressions and fixtures.

The official [implementation API matrix](https://cel.dev/reference/api-reference)
tracks features with stack-specific support. Do not infer identical extension
availability from the shared CEL name. Test the deployed release, not just a moving
README or playground.

## Envoy

Envoy RBAC can include a CEL condition in a larger permissions/principals policy.
Its evaluation context and HTTP/network attributes depend on the filter and build.
A true condition does not replace the other matching requirements. Shadow policies
can observe outcomes without enforcing them when configured that way.
[RBAC documentation](https://www.envoyproxy.io/docs/envoy/latest/intro/arch_overview/security/rbac_filter).

Pin the API field and Envoy release before emitting configuration. Latest docs may
show development or work-in-progress xDS APIs, and parsed/checked/string expression
fields can have different availability. Do not choose a field from an unstable
newer proto merely because it accepts CEL source.
[CEL xDS proto](https://www.envoyproxy.io/docs/envoy/latest/xds/type/v3/cel.proto).

## Google Cloud IAM Conditions

IAM uses CEL conditions within a larger authorization model. Available attributes
and functions vary by policy type and supported resource/service. Verify whether
the task concerns allow policies, deny policies, or another condition-bearing surface.
A conditional role binding can coexist with unconditional grants elsewhere.
[Conditions overview](https://docs.cloud.google.com/iam/docs/conditions-overview).

Test with the service's policy tooling and supported attributes. A locally true
condition neither proves the caller has the required role nor proves that no other
binding grants broader access. Preserve etags/version requirements when editing
policy documents through the actual API.

## Kubernetes

CRDs expose `self` and potentially `oldSelf`; admission policy uses its own objects,
request, parameter, and authorization context. Neither is a generic CEL prelude.
Kubernetes libraries and list semantics are versioned host features. Keep test
corpora per host rather than silently rewriting generic expected results.

## Translate with evidence

Choose a shared feature subset and run the same semantic cases through both hosts.
Include adapters and result consumers. Compare absence, nulls, errors, numeric
mapping, temporal boundaries, and macro semantics. Where a host lacks a feature,
prefer an explicit adapter or documented limitation over an unverified replacement
that merely resembles the original expression.
