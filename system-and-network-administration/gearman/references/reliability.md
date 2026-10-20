# Retries, duplicates, idempotency, and poison jobs

Read before handling any nontrivial side effect. Evidence for native behavior: [S1, S2, G1, P1](sources.md). The recovery patterns are application recommendations.

## State the guarantee precisely

Gearman does not supply a universal exactly-once application execution guarantee. Without the relevant persistence/recovery controls jobs can be lost; with reconnect/replay/republication they can be assigned more than once. Build to tolerate repeated delivery and explicitly account for owed work rather than advertising unconditional at-least-once delivery under every failure.

Native coalescing uses a function plus non-empty unique key on one server while the job is known there. It is not a permanent completed-request ledger and does not span independent servers. The inspected code treats an empty key differently and supports a special `-` payload-based lookup path. Avoid depending on such implicit behavior for business identity; assign explicit keys and test backend interactions.

## Explicit failure versus interruption

On the inspected C server, WORK_FAIL and WORK_EXCEPTION lead to terminal cleanup; disconnect-driven requeue follows the separate retry/drop path. A retry threshold can discard a poison assignment without creating a dead-letter record. Read [the version reference](version-compatibility.md) before setting its value. Do not use it as the sole audit record for logical attempts.

## Application idempotency

For a database-local effect, use one transaction that checks/claims the request identity, validates its business fingerprint, performs the effect and stores the outcome. Concurrent duplicate attempts must serialize at the database constraint/lock boundary, not at an in-process set. Returning an already committed result is often safer than executing the effect again.

For external effects, use a downstream idempotency key, conditional version/fencing token, or an explicit compensating workflow. Record unknown outcomes for reconciliation. A lease expiring does not prove the original process stopped; stale owners must be prevented from committing effects. Avoid calling remote services while holding a long database transaction unless the failure and locking consequences are deliberately accepted.

## Retry policy

Classify failures; retry only those with a safe effect contract. Use capped exponential backoff plus jitter, a maximum age, an attempt budget and per-dependency circuit breaking. Persist retry eligibility outside the current assignment. Do not sleep an expensive worker indefinitely or recursively submit child retries without admission limits.

A retry submitted with the same function/unique while the old job exists can coalesce into the current job. New transport delivery IDs with a stable business request ID avoid confusing queue coalescing with business deduplication. They also allow more duplicate assignments, so the business guard must be correct first.

## Poison-job handling

Record safe request identity, schema version, error class, worker version and a redacted fingerprint. Quarantine the application request after its policy threshold; stop hot-loop requeue/restart storms. A dead-letter/quarantine table in this design is your application component, not a feature claimed for gearmand. Redrive requires an operator decision, a new transport delivery and preservation of the original business identity unless intentionally creating new work.

Test the duplicate boundary by committing a result, dropping the terminal packet, and executing the request again. Success means one business effect and a consistent outcome, not one observed worker invocation.
