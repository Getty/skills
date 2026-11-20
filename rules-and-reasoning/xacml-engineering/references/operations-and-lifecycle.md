# Operations and lifecycle

## Publish immutable effective policies

Version the complete effective policy graph, root selection, extension set, and
attribute-provider configuration. A policy file alone is insufficient when references
or configuration select different behavior. Validate and load the candidate before
activation, then switch to the new revision atomically where possible.

Keep a rollback revision and the associated provider configuration. A rollback
that restores XML but leaves a changed attribute meaning may not restore decisions.
Separate policy identity from release revision and document version-selection rules.

## Manage attributes as dependencies

Record which sources provide roles, group membership, tenant, classification, time,
and other decisive facts. Define freshness/revocation budgets and failure behavior.
A successful PIP lookup with stale data can be more misleading than a visible error.

Cache decisions only when the key and expiry account for subject, action, resource,
all relevant fact versions, policy revision, and revocation requirements. Do not
reuse a Permit for a different resource because the subject is unchanged. In some
systems, caching compiled policies while reevaluating each request is simpler.

## Observe useful outcomes

Track decisions, technical errors, latency by stage, missing-attribute status,
provider failures, root-policy revision, and PEP obligation failures. Redact sensitive
facts and bound logs. An increasing NotApplicable rate can signal a target/configuration
mismatch; an increasing Indeterminate rate can signal data or integration problems.

Keep decision evidence separate from enforcement evidence. Permit plus failed mask
application is not successful authorized delivery. Record a correlation ID without
assuming that a PDP automatically produces a complete compliance audit trail.

## Tune without changing meaning

Measure before optimizing. Narrow targets can reduce unnecessary rule evaluation,
but changing target logic changes scope. Reordering first-applicable policies changes
meaning. Attribute-provider caching changes freshness. A “strict” or optimized engine
mode can alter issuer or duplicate-attribute behavior. Re-run relevant cases after
such changes.

Use load tests with realistic policy overlap and attribute distributions. Bound
request/Content sizes and policy graph size. Do not benchmark only hot caches and
successful paths if provider outages or large bags matter in production.

This is original operational guidance grounded in the
[core processing model](https://docs.oasis-open.org/xacml/3.0/xacml-3.0-core-spec-en.html)
and [AuthzForce configuration surface](https://github.com/authzforce/core).
