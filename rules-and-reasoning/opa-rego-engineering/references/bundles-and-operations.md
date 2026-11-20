# Bundles and operations

## Define ownership and activation

Bundle policy and reference data that must move together. Set explicit roots so
independent producers do not own overlapping namespaces accidentally. Separate
download, signature verification, parsing, and activation. A successful fetch is
not evidence that the new policy is active.

Use manifest `rego_version` and per-file declarations where needed. Current docs
describe values beyond v1; match consumers before using them. Manifest declarations
can override global compatibility switches. Keep revisions traceable.
[Bundles](https://www.openpolicyagent.org/docs/management-bundles).

## Distribute coherently

Define refresh cadence and acceptable last-known policy age. A rule requiring a
new field must not activate before compatible data exists. Multiple independent
bundles do not imply a globally atomic update across all consumers.

Verify publisher signatures where required by the deployment's trust model. Manage
keys, expected claims, and rotation. Artifact provenance and integrity do not prove
that the business rule is correct. Keep rollback bundles and compatible facts
available before a broad rollout.

## Observe distinct channels

Use status to inspect active revisions, activation failures, and staleness. Process
liveness is weaker evidence than a successfully activated expected bundle.
[Status](https://www.openpolicyagent.org/docs/management-status).

Use decision logs to correlate requests and answers with policy revisions. Mask
sensitive paths through the documented masking policy; account for buffering,
delivery failures, retention, and dropped events. Enabling logs alone does not
create a complete durable audit system.
[Decision logs](https://www.openpolicyagent.org/docs/management-decision-logs).

Use discovery for trusted runtime configuration bootstrapping. A discovery change
may redirect policy or logging services, so review it as runtime configuration
rather than ordinary business logic.
[Discovery](https://www.openpolicyagent.org/docs/management-discovery).

## Roll out and recover

Run known decisions through representative consumers after activation. Use staged
rollout or shadow comparison for broad permission changes. Verify rollback by
observing the active revision and actual answers; restoring a source file alone
does not revert distributed state.

During incidents, record entrypoint, policy/data revisions, request shape, evaluator
error, and consumer behavior. Separate management-plane access from evaluation.
Bound request size, CPU, memory, and execution time according to the deployment.
Restrict network-capable built-ins and external data access where appropriate.

Design startup readiness around the facts needed for reliable decisions. A listening
HTTP socket with no required bundle loaded is not necessarily ready for traffic.
Keep the distinction between “can answer a request” and “has the expected revision”
visible to routing and operations.
