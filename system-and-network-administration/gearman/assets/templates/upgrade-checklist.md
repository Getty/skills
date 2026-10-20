# Upgrade / recovery gate

From/to server and libgearman versions: ___. Bindings/runtime matrix: ___.
Changed defaults and options (especially retries): ___. Scheduling expectations: ___.
Stored-data format compatibility and rollback reader: ___. TLS/build changes: ___.
Queue owners and fencing: ___. Backup consistency point: ___.
Old payload handling and worker rollout overlap: ___. Delayed-job migration: ___.

## Before production
Record isolated success, explicit failure, interruption/requeue counts, unknown submission,
persistence replay, external-effect deduplication, TLS negatives, capacity and drain tests.
Attach the evidence, not just check marks. Preserve a tested rollback artifact.

## Go/no-go
Owner: ___. Accepted residual uncertainty: ___. Rollback triggers: ___.
Post-change reconciliation and queue-origin checks: ___.
