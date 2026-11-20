# Sources and versioning

Examples and task workflows are original. Use the language
specification for core semantics, implementation documentation for API/support,
and product documentation for embedded environments.

## Baseline

The executable corpus targets official **cel-expr-python 0.1.3**, a Python wrapper
for CEL C++. This is distinct from other Python packages using CEL-related names.
It enables no custom host extensions. The official multi-stack reference inspected
lists baseline versions including CEL Go 0.32.0+, C++ 0.16.1, Java 0.14.0, and Python
0.1.3; those reference baselines are not a claim about the user's installed versions.

The Kubernetes examples use stable `apiextensions.k8s.io/v1` and
`admissionregistration.k8s.io/v1` APIs. Verify server version and extension support.
Moving Kubernetes and Envoy latest documentation can contain newer or development
features; pin the deployed product's documentation when implementing.

## Primary source map

| Topic | Source |
| --- | --- |
| Language definition | https://github.com/cel-expr/cel-spec/blob/master/doc/langdef.md |
| Overview/lifecycle | https://cel.dev/overview/cel-overview |
| Functions and stack support | https://cel.dev/reference/api-reference |
| Go embedding | https://github.com/cel-expr/cel-go/blob/master/README.md |
| Python API | https://github.com/cel-expr/cel-python/blob/main/README.md |
| Python package/release | https://pypi.org/project/cel-expr-python/ ; https://github.com/cel-expr/cel-python/releases |
| Python codelab | https://github.com/cel-expr/cel-python/blob/main/codelab/index.lab.md |
| Kubernetes CEL | https://kubernetes.io/docs/reference/using-api/cel/ |
| CRD validation | https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/ |
| Admission policy | https://kubernetes.io/docs/reference/access-authn-authz/validating-admission-policy/ |
| Policy API | https://kubernetes.io/docs/reference/kubernetes-api/admissionregistration/validating-admission-policy-v1/ |
| Binding API | https://kubernetes.io/docs/reference/kubernetes-api/admissionregistration/validating-admission-policy-binding-v1/ |
| IAM | https://docs.cloud.google.com/iam/docs/conditions-overview |
| Envoy | https://www.envoyproxy.io/docs/envoy/latest/intro/arch_overview/security/rbac_filter ; https://www.envoyproxy.io/docs/envoy/latest/xds/type/v3/cel.proto |
| Regex syntax | https://github.com/google/re2/wiki/Syntax |

## Refresh and verification

Inspect release changes and the actual host contract before updating examples.
Replay errors, missing fields, numerical adaptation, macros, and temporal boundaries.
Review new optional libraries separately from the core language. Update the source
date only after checking these surfaces.

The local corpus verifies expression behavior in its named wrapper. It does not
establish full CEL conformance, unknown-activation support, Kubernetes admission,
Envoy authorization, or IAM grant behavior. No live services are configured by the
bundle. Reproduce host-specific checks on the requested target before reporting
a deployment as validated.

## Observed preparation checks

Official **cel-expr-python 0.1.3** evaluated the **24** bundled cases
with **24/24** expected outcomes, including expected static/runtime failures.
The runner's mismatch and invalid-fixture paths returned statuses 1 and 2.
Both YAML examples parsed (three Kubernetes resource documents total); skill
frontmatter, JSON fixtures, and local links passed structural checks.
Kubernetes server validation, Envoy, IAM, unknown activations, and other CEL stacks
were not executed. YAML parsing is not cluster admission validation.
