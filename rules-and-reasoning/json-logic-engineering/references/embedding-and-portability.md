# Embedding and portability

## Build a narrow adapter

Evaluate an approved rule revision against validated plain data and return a typed
envelope. Resolve authoritative rule revisions server-side; a submitted expression
is not trusted just because the UI supports JSON Logic previews.

The reference package exposes `apply(rule,data)` and `truthy(value)`. Lock the
dependency. Keep the extension registry immutable during request handling; global
registration/removal can affect other requests. Custom functions and `log` can
introduce effects.

Application fields such as `ruleId`, `revision`, `engineProfile`, `expression`,
and `inputSchemaRevision` belong in an outer envelope. They are not core syntax.
Distinguish business results from invalid input, unknown operators, and exceptions.

## Test portability, do not infer it

Select a shared operator subset and run typed cases on each named implementation.
Check precision, coercion, null, truthiness, records, collection scope, Unicode,
string indexing, and extensions. Compare actual values/types; converting everything
to Boolean can conceal incompatible results.

Treat alternative “JSON logic” engines, compilers, and rule-builder DSLs as separate
implementations until measured. If both compilation and interpretation are used,
test each execution path. A common JSON shape does not imply semantic compatibility.

## Keep preview and authority aligned

Return an immutable rule revision with a preview. At final submission, reevaluate
authoritatively; if policy changed, communicate the revision change. Do not trust a
browser-produced Boolean as an access-control decision.

Cache expression artifacts by revision plus runtime/extension profile. Cache results
only when all relevant fact versions, identity, resource, and revocation requirements
are represented. A user-ID-only cache is wrong for resource-specific authorization.

Use an interruptible execution boundary if required. Perform data lookup before
evaluation where possible; an HTTP custom operation adds latency, credentials,
failure handling, and replay ambiguity.

Authority: [package API](https://github.com/jwadhams/json-logic-js),
[custom operations](https://jsonlogic.com/add_operation.html), and
[project test corpus](https://jsonlogic.com/tests.json).
