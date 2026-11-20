---
name: cedar-engineering
description: "Use when writing, validating, testing, integrating or debugging Cedar authorization policies — .cedar and .cedarschema files, permit/forbid rules, principal-action-resource-context requests, entities and hierarchies, RBAC/ABAC/ReBAC, policy templates, multi-tenant access, partial evaluation, Rust or Wasm embedding, Amazon Verified Permissions, or migrating authorization to or from Cedar."
---

# Cedar Engineering

Treat Cedar as a permission decision language with an explicit application contract.
Separate the policy decision, input authenticity, and enforcement of the operation.
Use this skill independently of a framework, cloud provider, or other skill.

Use **Cedar language 4.7 / Rust SDK 4.15.0** as the researched baseline.
Keep language version, SDK version, binding version, and managed-service feature
support separate. Older examples intentionally use a small
stable subset. Read [sources and versioning](references/sources-and-versioning.md)
before assuming that a new feature is available in a selected runtime.

## Choose the relevant reference

| Task | Read |
| --- | --- |
| Predict the result of permit, forbid, errors, or type operations | [Language and semantics](references/language-and-semantics.md) |
| Design a schema or diagnose validator failures | [Schema and validation](references/schema-and-validation.md) |
| Construct trusted requests and entity graphs | [Entities and context](references/entities-and-context.md) |
| Model roles, attributes, relationships, and tenant boundaries | [Modeling patterns](references/modeling-patterns.md) |
| Reuse policy templates or compose schema fragments | [Templates and schema linking](references/templates-and-schema-linking.md) |
| Embed the authorizer or build a decision service | [Runtime integration](references/runtime-integration.md) |
| Test policies and interpret determining policies or errors | [Testing and diagnostics](references/testing-and-diagnostics.md) |
| Improve latency, slice entities, or partially evaluate | [Performance and partial evaluation](references/performance-and-partial-evaluation.md) |
| Deploy through the AWS managed service | [Amazon Verified Permissions](references/verified-permissions.md) |
| Convert an existing authorization system | [Migration and interoperability](references/migration-and-interoperability.md) |
| Run the original example and helper | [Worked examples](references/worked-examples.md) |
| Check upstream evidence, versions, and guarantees | [Sources and versioning](references/sources-and-versioning.md) |

Read only the references needed for the task. Load example policies as synthetic
fixtures, not as a ready-made authorization design for the user's application.

## Establish the authorization contract

Inspect existing policies, schemas, caller code, entity loaders, and enforcement
points before proposing changes. Identify:

- The principal, action, resource, and request-specific context (PARC).
- The authoritative origin of every attribute, parent relationship, and context key.
- The action-to-API mapping and exact operation that an Allow will enable.
- The entity snapshot, policy revision, tenant boundary, and freshness requirement.
- The runtime, enabled extensions, schema validation mode, and error-handling contract.

Use labeled assumptions for an illustrative task. Ask only when missing application
meaning changes who can perform which action. Do not invent authentication claims,
role memberships, trusted network locations, or entity ancestry.

## Build or repair a policy set

1. **Define the requested permission.** Use domain actions such as `viewDocument`
   or `approveInvoice`; map API endpoints to these actions explicitly. Split compound
   operations when one permission would conceal multiple protected effects.
2. **Model identity and relationships.** Assign immutable, non-reused entity IDs.
   Choose attributes for facts and parent edges for intended membership semantics.
   Keep a direct `owner` relationship distinct from membership in a container.
3. **Write a schema.** Declare entities, allowed parent types, attributes, action
   applicability, and context shapes. Mark genuinely optional values optional.
   Validate all policies and templates against the same schema revision.
4. **Write narrow permit rules.** Constrain principal, action, and resource in the
   scope where practical. Add required facts in `when`. Add `forbid` rules for
   explicit denials that must defeat every matching permit.
5. **Handle missing values deliberately.** Guard optional attribute access with
   `has` and suitable type/scope guards. Treat unknown entities and malformed context
   as integration problems rather than silently manufacturing permissive defaults.
6. **Validate and evaluate separately.** Parse, validate policy types, validate
   request applicability, parse entities/context against the schema, and evaluate
   actual cases. Each checks a different layer.
7. **Enforce at the operation boundary.** Bind the evaluated resource to the object
   actually modified. Preserve tenant and identity context through asynchronous work.
   Recheck when the operation or relevant state changes.
8. **Deliver evidence.** Include original policy/schema/data files, supported runtime,
   meaningful passing and failing cases, diagnostics, and untested layers. Report
   domain denial separately from a failed authorization call.

## Preserve the essential semantics

- Return Allow only when at least one permit matches and no forbid matches.
  With no matching permit, the outcome is Deny.
- Do not treat policy order as precedence. A matching forbid defeats permits
  regardless of file order or policy ID.
- Preserve **skip-on-error**: an erroneous policy does not participate in the
  decision. A failed forbid can therefore leave a valid permit effective. Inspect
  diagnostics; implement any stricter application response explicitly.
- Do not infer that Deny means a forbid fired. Default denial can have no determining
  policy. Do not infer that Allow means no evaluation errors occurred.
- Keep `==` identity distinct from `in` membership. Membership is reflexive and
  transitive over the supplied hierarchy; it is not a general graph query.
- Keep entity references distinct from records containing `type` and `id`.
  Use the documented JSON entity escape or schema-aware parsing.
- Treat Cedar sets as unordered collections, not JSON lists with positional meaning.
  Cedar has no general JSON `null` value; model absence explicitly.
- Use strict typing rather than truthiness. Do not coerce strings into booleans,
  integers, entity references, or extension values inside policy construction.
- Preserve short-circuit guards. `context has mfa && context.mfa` can safely express
  an optional Boolean; unguarded access can produce an evaluation error.
- Validate templates and instantiated links. Slots are `?principal` and `?resource`
  in supported scope positions, not arbitrary string-substitution parameters.
- Do not assume that validation checks whether every referenced entity exists.
  Require trusted principal/resource hydration and the attributes needed by grants
  and prohibitions. A required schema field constrains loaded entities; an entirely
  absent entity can still leave an erroring forbid ineffective. Keep completeness
  checks separate from request and loaded-entity schema validation.
- Preserve guarded denial when absence itself must block access: permit the relevant
  condition only for an explicitly known acceptable value. Read the fail-closed
  example in the language reference; it does not replace trusted hydration.
- Missing entities and integer overflow remain possible runtime errors.
- Treat namespaces as type names, not tenant isolation. Enforce the tenant relation
  in rules and trusted data loading.
- Treat schema linking and partial evaluation as different mechanisms. Schema linking
  composes definitions; residual policies represent still-undetermined authorization.
- Pin experimental features. In SDK 4.15.0, `tpe` and `partial-eval` remain outside
  ordinary stability guarantees; a residual is not a final Allow.
- Bound untrusted input depth and size. Cedar's terminating language does not make
  unbounded parsing, entity loading, or policy management inexpensive.

## Use the bundled example

Run from the skill directory or substitute absolute paths:

```bash
python3 scripts/audit_entities.py assets/examples/entities.json --require-parents
cedar validate --policies assets/examples/policies.cedar --schema assets/examples/schema.cedarschema
```

Read the worked-example reference for the exact authorization commands and case
runner. The Python helper audits an explicit entity JSON graph; it does not evaluate
Cedar, prove policy safety, or replace the official schema validator.

## State the limits of guarantees

Describe Cedar's verification-guided development precisely: properties of formal
models and extensive differential testing support the implementation. They do not
prove that the user's policy represents their business intent, that caller-supplied
facts are true, or that all enforcement paths invoke Cedar.

When migrating, compare outcomes and diagnostics over a meaningful corpus. Never
translate a four-valued XACML decision, Rego undefined result, or a DMN business
classification into Allow without an explicit mapping.

For repair, explain the concrete counterexample and changed permission boundary.
For production integration, report policy/data revisions and revocation behavior.
For a demonstration, label observed runtime checks separately from reasoning.
