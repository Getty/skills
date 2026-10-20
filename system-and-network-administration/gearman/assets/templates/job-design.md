# Job contract design

Function name/version: ___. Responsible worker pool: ___.

Input schema, maximum bytes and allowed encodings: ___.
Application request identity and fingerprint fields: ___.
Gearman unique strategy and delivery-attempt identity: ___.
Output/error schema and durable result ownership: ___.
Deadline behavior before start and during execution: ___.
Side effects and atomicity/idempotency boundary: ___.
Dependency timeouts, concurrency, resources and authorization: ___.
Logical retries, backoff, retry-intent storage and quarantine: ___.
Cancellation/cooperative stop and already-committed-effect behavior: ___.
Old queued-payload compatibility and rollout order: ___.

## Required tests
Success, empty result, invalid types/limits, expired deadline, conflicting repeated ID,
concurrent duplicates, worker crash before/after effect, lost completion, restart/replay,
and the application's external-provider idempotency boundary.
