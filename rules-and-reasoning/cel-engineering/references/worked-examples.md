# Worked examples

## Run the real evaluator corpus

Install `cel-expr-python==0.1.3` in an isolated environment and run:

```bash
python3 scripts/run_cases.py assets/examples/cases.json
```

The runner compiles each original expression with explicit declarations, evaluates
its bindings, and compares outcome category, CEL type, and value. It reports a
summary and per-case results. Exit 0 means every expected outcome matched; exit 1
means a semantic mismatch; exit 2 means dependency or fixture setup failed.

The corpus covers quota boundaries, missing versus null keys, wrong dynamic types,
empty universal quantification, Boolean error absorption, ordinary runtime errors,
static type failure, integer division, string patterns, and time boundaries.
Expected errors are successful tests when the observed category matches.

The runner is designed for trusted bounded local fixtures. It performs no network
calls and registers no custom functions. It is not an Internet-facing evaluation
sandbox and does not claim to enforce every resource limit required for untrusted
expressions. Use the cost/performance guidance when building such a service.

## Inspect the CRD example

`assets/examples/quota-crd.yaml` defines a synthetic namespaced Quota resource with
nonnegative integer `used` and `limit` fields and a cross-field CEL constraint.
`self` is the `spec` object at the rule's location. A valid `used: 3, limit: 5` and
invalid `used: 6, limit: 5` provide an initial create/update pair.

Validate the CRD and resources on the intended Kubernetes server to test actual
schema adaptation, cost checks, and API behavior. YAML parsing alone does not check
CEL or establish that a resource is admitted.

## Inspect the admission example

`assets/examples/deployment-policy.yaml` contains a policy and binding restricting
Deployment replicas to at most five in namespaces labeled `cel-demo: enabled`.
The expression permits an absent replicas field, relying on Kubernetes's own API
schema/defaulting contract. The binding selects Deny and Audit for matching failures.

The example deliberately uses no parameters. Add paramKind/paramRef only with a
clear missing/multiple-parameter contract and target-version tests. A separate
namespace label is required for the binding to match; no cluster is modified by
running the local expression corpus.

## Extend without hiding failure modes

Add declarations and expected typed outcomes before changing expressions. Preserve
a case that demonstrates why a presence guard or type declaration exists. Do not
replace expected runtime errors with false merely to make tests pass; change the
application contract explicitly if that is the intended behavior.
