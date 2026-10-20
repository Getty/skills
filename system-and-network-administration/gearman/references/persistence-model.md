# Persistence: what is and is not recovered

Read before making durability claims or enabling a queue backend. Evidence: [G2, G9, S1, S2, S3](sources.md).

The C server keeps its active queues in memory. A persistent backend records eligible **background** jobs and replays unfinished stored work at startup. Enabling it is not a spill-to-disk mechanism for reducing the live queue's memory footprint. It is also not a completed-result history. Storage changes made outside the daemon do not automatically update the live queue.

## Model the acceptance boundary

Write down the observed order of storage acceptance, live-queue insertion and client acknowledgement for the exact build/backend. Then model a crash between every pair of steps. Treat an acknowledgement as evidence only of the guarantees verified for that backend's own commit/sync policy. A callback returning success is not, by itself, proof that bytes survive power loss on your storage stack.

Model completion separately: worker effect, result-store commit, terminal packet, backend deletion and client observation do not form one transaction. A crash or backend-delete failure can leave replayable work after the business operation succeeded. This is why the application's idempotency boundary remains necessary with persistent queues.

## Failure matrix

| Failure point | Required application response |
|---|---|
| Before dispatch | Outbox/reconciliation decides whether work is still owed |
| Submission acknowledgement lost | Outcome is ambiguous; reconcile request identity |
| Worker disappears mid-operation | Re-execution may occur; protect the side effect |
| Effect committed, terminal packet lost | Return the stored result on a duplicate request |
| Server restarts | Reconcile replayed jobs with application outcomes |
| Storage deletion fails | Alarm and investigate; do not equate completed side effect with queue removal |
| Backend unavailable | Bound connection/retry behavior; avoid unbounded producer flood |

## Acceptance tests

Use a dedicated backend namespace. Queue background jobs with no workers, stop and restart the daemon, then run workers and verify every request ID. Repeat with a hard kill after acceptance. Repeat while a worker is active and immediately after its result-store commit. Verify that completed requests are not executed twice at the business boundary even when assignments are repeated.

Run a separate foreground restart test; do not extrapolate background persistence to it. Test empty and explicitly assigned unique keys, but use explicit non-empty unique keys in deployed background submissions. Observe storage row counts and live queue counts separately; they need not be identical during transitions.

## Recovery ownership

One active daemon should own a given queue storage namespace unless the backend/source explicitly implements coordination that you have verified. Two daemons reading the same rows are not a replicated cluster. Back up and restore with writers fenced, then compare recovered queue records with the application's outbox/results. Recovery is complete only when all owed requests are accounted for, not when the daemon answers ECHO.
