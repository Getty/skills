# Worker protocol state machine

Read before implementing a worker library or changing its reconnect/shutdown behavior. Evidence: [G3, S2](sources.md).

Register named abilities using `CAN_DO` or a supported timeout variant. Ask for work with the appropriate GRAB variant. A job assignment contains the handle, function, optional unique key and opaque payload. The worker reports progress/data as needed and exactly one terminal outcome for that assignment.

## Idle sequence

When a GRAB gets `NO_JOB`, send `PRE_SLEEP`, wait for `NOOP`, then ask again. NOOP is a wakeup, not a job assignment. Do not spin in a zero-delay poll loop. The inspected server's PRE_SLEEP handling rechecks for runnable work to avoid a missed-wakeup race.

Choose a GRAB variant that supplies metadata the worker actually needs. The package uses `GRAB_JOB_UNIQ`/`JOB_ASSIGN_UNIQ`. Transport unique keys are useful for diagnosis, but the application request ID belongs inside the validated payload and remains the business deduplication key.

## Execution ownership

A connection is not a general-purpose pool of arbitrary concurrent writes. Keep one owner of protocol I/O or provide explicit synchronization and handle routing. For process-based concurrency, open connections after fork and create separate database sessions. Never let multiple child processes read the same inherited Gearman socket.

When a worker connection disappears while an assignment exists, requeue behavior is controlled by server state and retry policy. Meanwhile the original process or a child process may still be performing an external side effect. A server timeout therefore does not establish exclusive execution. Use application idempotency/fencing where necessary.

## Shutdown protocol

On a termination request stop taking new work, finish or safely abandon the current bounded assignment, report the outcome when possible, close connections and exit. A worker that sends a completion before its result is durable reverses the required application boundary. A worker that receives SIGTERM during a GRAB race must account for a job that was already assigned.

The package's lab worker handles one small task at a time, sleeps with a bounded readiness wait, and finishes a job received just before the stop flag. It does not provide a production reconnect manager, process pool or remote cancellation agent. Unexpected transport errors exit nonzero for the supervisor; repeated restarts still require rate limiting.

## Terminal response discipline

Catch known validation/domain failures and map them deliberately. Do not send WORK_EXCEPTION and then mechanically send WORK_FAIL against a server that has already removed the job. Do not both return a callback result and manually emit completion unless the binding explicitly suppresses duplicate terminal packets. Verify this behavior for each binding.

Test idle termination, termination during execution, malformed assignment, unknown function, connection loss before response, and a worker that crashes repeatedly on one payload. Observe both application outcome and native queue cleanup.
