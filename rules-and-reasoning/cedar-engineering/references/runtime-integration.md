# Runtime integration

## Place the decision in a complete enforcement path

Use a pipeline with an authenticated identity, normalized action/resource mapping,
trusted data loading, Cedar evaluation, and explicit application enforcement. Keep
policy management outside ordinary untrusted request handling. An application must
invoke authorization for every protected path, including batch jobs, background
workers, alternative APIs, and administrative functions.

Prefer parsing and validating policy sets during deployment. Reuse immutable parsed
objects where the binding supports it; build request-specific context separately.
Load a coherent policy/schema/data revision and atomically replace it on a successful
release. Do not expose half-updated schemas and policies to requests.

The [Rust public API](https://docs.rs/cedar-policy/4.15.0/cedar_policy/)
provides policy sets, schemas, entities, requests, authorizers, and response diagnostics.
Use the API for the pinned crate version; bindings can lag the core language. Treat
Wasm and FFI as packaging choices whose exported API, input limits, and concurrency
behavior require their own verification. Do not invent an HTTP API for Cedar itself.

## Separate errors from decisions

Return a structured application result with decision, determining policy IDs, error
count/category, policy revision, schema revision, and relevant entity snapshot ID.
Avoid returning secret attributes or complete policy internals to an untrusted caller.
Detailed audit logs and public denial messages can have different audiences.

An SDK parse failure or a decision-service timeout is not a Cedar Deny result. Map it
through an explicit service error policy. A successful Cedar response containing
Allow and evaluation errors is possible; decide whether that is acceptable for the
application and exercise the choice under failure. Do not retry a permission decision
by silently omitting the policy that failed.

Check the operation's binding: the authorized document ID must be the document actually
updated. For mutable state, prevent a time-of-check/time-of-use gap with a transaction,
version precondition, lock, or reauthorization appropriate to the storage design.
Planning or evaluating an action does not execute it.

## Make caching and revocation measurable

Cache keys must include the permission-relevant request and revisions of policies,
entity relationships, and context. Do not cache solely by principal and action when
the resource changes. Include tenant, MFA/authentication strength, session state, and
resource version when they affect policies. A change to an ancestor group can invalidate
many descendants; design that invalidation before promising immediate revocation.

Define the acceptable delay for revoking a grant, then derive TTLs and update
propagation from it. Benchmark with cold and warm caches and with realistic entity
loads. Keep a stale cache from turning an infrastructure incident into an indefinite
grant.

## Bound hostile or excessive input

Apply policy size, entity count, graph depth, input nesting, and execution-service
concurrency limits. The SDK documents `*_with_depth_limit` parsing functions for
untrusted content; use relevant limits even when JSON has a separate parser limit.
A terminating language cannot eliminate stack exhaustion in surrounding parsers or
the cost of loading an enormous graph. Consult [SDK input guidance](https://docs.rs/cedar-policy/4.15.0/cedar_policy/#untrusted-input-and-stack-overflows)
and [security guidance](https://docs.cedarpolicy.com/other/security.html).

Keep clocks, identity verification, databases, and remote calls in trusted host
adapters. Cedar policy evaluation consumes the resulting values; it does not make
an unverified JWT or externally supplied role authoritative.
