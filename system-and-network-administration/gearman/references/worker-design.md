# Production worker design

Read when adding a handler, scaling execution or isolating resource-heavy jobs. Evidence: [P2, C2, G3](sources.md); failure behavior in [S1, S2](sources.md).

## Layer the worker

Keep the transport loop thin: decode and bound bytes; validate envelope/version; load business state; check deadline/cancellation; acquire any required dedup/fencing protection; execute the operation; durably store outcome; report one terminal response. Business handlers should be unit-testable without a Gearman server.

Separate permanent domain rejection from temporary infrastructure failure. A schema error will not improve if all workers crash on it repeatedly. Store a safe failure classification before terminating the assignment when durable diagnosis is required. Explicit WORK_FAIL is not a built-in delayed retry request.

## Concurrency and resources

Bound active operations by CPU, memory, file descriptors and downstream limits, not only by the number of worker connections. A useful upper bound is the minimum of independently measured CPU slots, memory slots and dependency quotas. Leave headroom for the runtime, transport buffers and supervisor.

Use process isolation for untrusted/native/CPU-heavy work when appropriate. Start subprocesses with an argument list, a constrained working directory/environment, output byte caps, a timeout and a process-group kill strategy. Do not retain arbitrary stdout in memory. Reap every child. Ensure a killed parent does not leave an untracked child continuing a side effect.

Open Gearman/database connections after fork. Do not reuse an inherited event loop or native client object across process boundaries. With threads, use per-thread objects unless the exact library documents the desired thread-safety model. With event loops, move blocking work out of the loop and cap the offload pool.

## State and cleanup

Long-lived workers accumulate state: ORM identity maps, buffers, temporary files, caches, leaked file descriptors and stale credentials. Define per-job cleanup and an optional recycle policy based on observed leaks or safe runtime limits. Recycling is not a fix for a poison job; capture its request identity and reconcile it.

Connection recovery must re-register capabilities. A worker process being alive is not enough for readiness. Measure a progressing job loop or verify registration/end-to-end canaries through a separate safe mechanism.

## Effect safety

Deduplication and the effect should commit in the same transaction where possible. For external APIs use the provider's idempotency mechanism or application-level fencing/compensation. “Insert request ID first, then call the API” can lose the operation if the process crashes between those steps; “call the API first, then record request ID” can repeat it. Neither ordering alone creates exactly-once behavior.

The local SQLite example demonstrates an atomic effect counter plus result record, deliberately without external calls. It does not provide distributed leases or multi-host shared-file coordination.

## Shutdown

Stop taking work, drain bounded active jobs and release resources within a measured grace window. SIGKILL remains possible: idempotency must survive it. In Kubernetes, termination hooks and grace periods are deployment controls, not guarantees that no additional assignment race can occur.
