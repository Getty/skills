# Storage and lifecycle

## Store executable meaning with its dependencies

Store an immutable rule revision and an application envelope containing its semantic
purpose, input/result schema revisions, supported runtime profile, and author/reviewer
metadata where needed. Do not insert metadata keys beside an operator: a second key
can stop an object being interpreted as an operation.

Use stable rule identity independently of content revision. A display title can
change without changing the decision. Keep expression bytes for reproducible hashing;
if canonical JSON is required, use a named canonicalization scheme and real tooling.
Sorting keys in an arbitrary serializer is not automatically a standard canonical form.

## Publish controlled revisions

Validate, execute relevant cases, review the requirement change, then activate an
immutable revision. Use an atomic pointer or versioned deployment object. Keep old
revisions available for rollback and historical evaluation. Bind extension and input
schema changes to the same release process.

For parallel browser/server deployments, tolerate or reject mixed revisions
explicitly. A stale preview should never bypass current authoritative evaluation.
Return the revision used with the decision.

## Explain without overclaiming a trace

The base evaluator returns a value, not a standardized explanation document. Design
application-level reason codes, reviewed decision branches, or instrumentation if
explanation is required. A post-hoc natural-language explanation can disagree with
the executed path; derive reasons from actual evaluated facts and stable branch IDs.

Do not eagerly evaluate every branch just to produce a trace, because that changes
lazy error/effect behavior. If tracing requires instrumentation, test the traced and
untraced evaluator for matching decision results under the supported pure profile.

## Replay and retention

Record enough to identify the rule/runtime and reconstruct relevant facts, subject
to data minimization and retention requirements. Separate fact references from fact
snapshots. A link to a mutable database row alone does not reproduce the old input.

For cached decisions, include fact freshness, identity, resource, action, and rule
revision. Revocation requirements may prohibit caching even if expression evaluation
is cheap. Logs should distinguish denied, invalid input, and failed evaluation without
exposing sensitive raw data.

These lifecycle fields are original host-design guidance. JSON Logic itself does
not define a deployment protocol or audit-envelope standard.
