# Priorities, fairness, delayed work, and ordering

Read when work is starved, task ordering changes, or scheduled jobs are requested. Evidence: [G1, S1, S2, G3](sources.md).

## Priority is not a latency guarantee

In the reviewed 2.x server, priority selection is global across eligible registered functions on a worker connection. This is still constrained by worker capabilities; a worker cannot execute a high-priority function it does not provide. High-priority admission can delay lower-priority work indefinitely. Running work is not automatically preempted by a newly queued higher-priority job.

Use dedicated pools for resource or latency classes when isolation matters. Define per-class admission budgets and oldest-job-age alerts. Do not place all functions into a single universal worker and expect priority alone to provide predictable service to every class.

## Registration and task-order changes

Round-robin is the 2.x default and the old option remains for compatibility rather than disabling the behavior. Libgearman's task list now submits FIFO. Neither fact gives you global FIFO completion across workers or servers. Different runtimes, priorities, retries and processing times can reorder results.

When business order matters, maintain a sequence/version in durable state. A worker applies an operation only when the required prior state exists, or an orchestrator serializes access to that business key. Treat hash-based routing and a single worker as optimizations, not a replacement for the state invariant during failover.

## Epoch scheduling

The current release line includes improved `SUBMIT_JOB_EPOCH` handling and sleeping-worker wakeups. Verify the deployed server, backend and binding support the actual call path before using it. Persisted timestamp width and signedness are part of the storage review; old schemas are not proof of long-horizon scheduling correctness.

Test a job queued before its due time, no busy workers, server restart before the deadline, restart after the deadline, system-clock changes and a worker reconnect near the deadline. Record seconds versus milliseconds explicitly. A due time is eligibility, not a promise of start time when capacity is unavailable.

## Cron-like scheduling is not implied

The inspected server rejects `SUBMIT_JOB_SCHED`; its appearance in protocol material must not become a fabricated cron feature. For periodic work use a separately identified scheduler that issues idempotently identified occurrences. Store the occurrence ID and due time in application state, and define behavior for missed runs and duplicated scheduler leaders.

## Delay/retry patterns

Keep retry eligibility in a durable application record or verified scheduler. Avoid workers sleeping for minutes while holding expensive capacity. Avoid immediately resubmitting the same function and unique key before the old assignment is terminal: it may coalesce with the existing job rather than create a future attempt. Prefer a new transport delivery ID with the same business request ID, plus an explicit retry policy and durable deduplication.
