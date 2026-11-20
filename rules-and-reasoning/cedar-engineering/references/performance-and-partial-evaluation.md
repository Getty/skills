# Performance and partial evaluation

## Measure the complete decision path

Measure parsing/validation at deployment, policy selection, entity retrieval,
serialization, evaluation, and response handling separately. A fast authorizer
cannot hide a slow or inconsistent relationship lookup. Record tail latency,
entity counts, policy counts, input sizes, and cache state along with throughput.
Benchmark the normal denial path as well as successful requests.

Use specific policy scopes to support efficient policy selection. Retain every
potentially applicable forbid when narrowing a policy set. Test a selector against
full evaluation on a representative corpus; a selector that only retrieves obvious
permits changes the decision semantics. The [scope guidance](https://docs.cedarpolicy.com/bestpractices/bp-populate-policy-scope.html)
and [policy level validation](https://docs.cedarpolicy.com/policies/level-validation.html)
explain mechanisms relevant to retrieving bounded entity information.

Slice the entity graph only under a documented dependency contract. Consider nested
attributes, parent closures, policy literals, context references, and dynamic tags.
An omitted node that only supplied a prohibition is as significant as an omitted
node that supplied a grant. Maintain a full-input differential test when optimizing
loading.

## Treat partial results as a different API

Ordinary authorization expects a concrete request. Partial evaluation leaves selected
inputs unknown and returns a residual or specialized policy representation. Unknown
is not false, absent, empty, or an anonymous identity. Never flatten a residual into
Allow because a permit remains possible.

The [SDK 4.15.0 feature documentation](https://docs.rs/cedar-policy/4.15.0/cedar_policy/#experimental-features)
marks `tpe` (type-aware partial evaluation/batched authorization) and `partial-eval`
as experimental, and recommends TPE over the older API. Their signatures and behavior
can change outside normal stability expectations. Pin the exact feature flags and
SDK version, and preserve a conventional authorization fallback.

For an accessible-resources query, specify which variables may be unknown, what the
query guarantees, and how residual conditions are translated into the data store.
A database filter must preserve forbids, type assumptions, missing data, and tenant
boundaries. Verify returned resources with concrete authorization where the design
requires it. Do not assume arbitrary residual Cedar can be mechanically translated
to equivalent SQL.

## Keep optimization evidence reproducible

Record the policy/schema revisions, dataset, request distribution, runtime build,
feature flags, and hardware with each benchmark. Compare final decisions and error
classes before comparing speed. Use policy compilation or cache warm-up consistently
across candidates. A performance improvement that silently removes diagnostics or
changes revocation latency is a behavior change requiring explicit review.
