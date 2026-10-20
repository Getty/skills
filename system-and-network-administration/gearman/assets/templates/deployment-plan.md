# Deployment decision record

Status: draft. Owner: ___. Date: ___. Change authorization: ___.

## Inventory and requirements
Server implementation/version/build: ___. Linked libraries/bindings: ___.
Functions and schema versions: ___. Arrival/burst rate, payload/result limits: ___.
Execution slots and dependency concurrency ceilings: ___. Latency/age SLO: ___.

## State and reliability
Foreground/background choice: ___. Durable queue backend and commit policy: ___.
Queue owner/fencing: ___. Stable operation ID, conflict rule and result store: ___.
Outbox/reconciliation, retry budget/backoff, quarantine ownership: ___.
Unknown-outcome procedure and external-effect idempotency: ___.

## Operations and security
Endpoints, private networking and administrator access: ___. TLS trust/negative tests: ___.
Service identity, secrets, resource limits, graceful stop: ___. Metrics/alerts: ___.
Backup/restore and replay window: ___. Rollback constraints: ___.

## Acceptance evidence
Attach versions, options, failure-matrix results, committed-effect counts and limitations.
No readiness approval until unresolved assumptions have an explicit owner and disposition.
