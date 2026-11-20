---
name: opa-rego-engineering
description: "Use when writing, testing or operating Open Policy Agent and Rego — .rego files, Rego v1/v2 migration, undefined results, input and data contracts, bundles, Gatekeeper, Terraform plan checks, partial evaluation, Wasm, decision logs, slow policies."
---

# OPA and Rego Engineering

Treat Rego as a versioned language for deriving decisions from structured facts.
Treat OPA as an evaluator and policy distribution runtime. Identify the component
that actually enforces a decision; evaluating `allow` alone changes no resource.

Use **Rego v1** as the bundled examples' deliberate compatibility profile. The
primary documentation also documents **Rego v2**,
opt-in `and`/`or`, and improved negation. Do not describe v1 as the only current
language profile, or assume a runtime supports a feature because online docs do.
See [sources and versioning](references/sources-and-versioning.md).

## Select the relevant material

| Task | Read |
| --- | --- |
| Predict rule values, collections, negation, or undefined results | [Rego semantics](references/rego-semantics.md) |
| Upgrade syntax or target multiple engines | [Versions and capabilities](references/versions-and-capabilities.md) |
| Model facts, identity, decisions, and data freshness | [Modeling and data contracts](references/modeling-and-data-contracts.md) |
| Check schemas, run tests, or establish release gates | [Validation and testing](references/validation-and-testing.md) |
| Embed OPA, consume REST responses, or enforce authorization | [Integration and enforcement](references/integration-and-enforcement.md) |
| Author Gatekeeper templates and constraints | [Kubernetes and Gatekeeper](references/kubernetes-and-gatekeeper.md) |
| Evaluate Terraform plans and CI artifacts | [Terraform and CI](references/terraform-and-ci.md) |
| Distribute bundles and diagnose operational state | [Bundles and operations](references/bundles-and-operations.md) |
| Optimize latency, partially evaluate, or target Wasm | [Performance and compilation](references/performance-and-compilation.md) |
| Investigate policy failures or unexpected permission | [Troubleshooting](references/troubleshooting.md) |
| Run the original examples and response helper | [Worked examples](references/worked-examples.md) |
| Verify sources, release observations, and refresh steps | [Sources and versioning](references/sources-and-versioning.md) |

Load only the references needed for the task. Use this skill independently of any
cloud, orchestrator, SDK, or other installed skill.

## Establish the policy contract

Inspect supplied policy, representative input, data, query, integration envelope,
runtime version, and actual error before proposing a rewrite. For new examples,
state reasonable assumptions rather than blocking on routine implementation choices.

Record these choices when they affect behavior:

1. **Question:** Boolean permission, violations, a structured decision, or a residual
   filter. Do not impose authorization semantics on every OPA use case.
2. **Facts:** Values from `input` versus `data`, their authoritative source, and
   their required freshness.
3. **Profile:** OPA release, Rego version, integration release, allowed built-ins,
   native/Wasm target, and strict built-in-error setting.
4. **Output:** Exact query and JSON type, including undefined, business denial,
   evaluator errors, and transport-failure behavior.
5. **Enforcement:** The application, gateway, admission controller, or CI step that
   consumes the decision and the operation it controls.

For access control, require explicit successful permission. Preserve denial versus
evaluation failure in diagnostics even when both prevent the action. A caller may
define other failure behavior; make that choice explicit.

## Author or repair a policy

1. Define a small input contract and representative cases. Include absent, null,
   malformed, cross-tenant, and revoked-principal cases when relevant.
2. Normalize identity, paths, actions, and authoritative resource attributes at the
   integration boundary. A correctly shaped caller-supplied role is not trusted identity.
3. Choose a stable package and entrypoint. Put a Boolean default on permission when
   the contract requires a defined false result for unmatched input.
4. Separate eligibility predicates, fact lookup, and final decision construction.
   Prefer named helpers over expressions with obscure variable bindings.
5. Use `:=` for assignment, `==` for comparison, and `=` when unification is intended.
   Bind iteration variables deliberately with `some`.
6. Use incremental rules for alternatives, `contains` for partial sets, and `every`
   for universal conditions. Decide separately whether empty collections are allowed.
7. Check syntax and static rules against deployment capabilities. Validate runtime
   input in the host too; compiler schema checks do not validate every request.
8. Run policy cases, then integration cases with the real envelope and consumer.
   Exercise error handling separately from expected negative decisions.
9. Measure representative latency and decision agreement before optimization or
   migration. Preserve reproducible policy and data revisions.
10. Return observed validation results and remaining unsupported behavior.

## Preserve the semantic distinctions

- Keep undefined, `false`, `null`, empty collections, and evaluator errors distinct.
  Never treat a missing REST `result` as successful permission.
- A body searches for satisfying bindings. One compliant element does not establish
  compliance for every element.
- A complete rule cannot produce incompatible values for one document. Alternatives
  returning the same Boolean differ from alternatives returning conflicting objects.
- Sets are unordered and deduplicated. Sort diagnostic arrays when presentation
  needs stable order; do not use accidental output order as policy priority.
- Check the negation profile. Legacy composite negation can fail when intermediate
  expressions are undefined. Newer opt-ins change this behavior; test migration.
- Default native built-in errors can become undefined. Strict-error support differs
  by caller/target and does not exist uniformly across every integration.
- `deny` has no magical precedence over `allow`. Define combination explicitly in
  the queried entrypoint and test overlapping conditions.
- Rego is declarative. Do not rely on textual expression order for external effects.
- `with` substitutes evaluation dependencies; it does not prove facts authentic.
- Native OPA, Gatekeeper, and Wasm hosts can differ in built-ins, dialect, and envelope.

## Run the examples

From the skill directory, with a compatible OPA binary:

```bash
opa version
opa check --strict assets/examples/policy.rego assets/examples/policy_test.rego
opa test assets/examples/policy.rego assets/examples/policy_test.rego assets/examples/data.json -v
opa eval --data assets/examples/policy.rego --data assets/examples/data.json --input assets/examples/input.json 'data.workspace.authz.decision'
python3 scripts/check_decision.py assets/examples/response-allow.json
```

The Python helper inspects a saved **Boolean Data API response** without networking
or policy execution. It returns status `0` for `result: true`, `1` for `false`, and
`2` for undefined, malformed, or wrong-type responses. It does not consume the
structured `decision` entrypoint. Read the worked-examples reference first.

## Deliver an actionable result

For authoring, return policy, query, input/data contract, important cases, and actual
checks. For incidents, separate logic, bundle activation, data freshness, and consumer
failures. For migration, state both profiles and observed decision differences.

Use `cel-engineering`, `cedar-engineering`, or `xacml-engineering` for their respective
languages when needed. Before claiming equivalent translation, compare types,
missing data, errors, combination rules, and host enforcement.
