# Gearmand internals and source navigation

Baseline: tag 2.1.0, commit `516ffac9376a533413a748eef9295808f1bf319a`. Evidence: [S1–S4, G1](sources.md). Some paths were inventoried rather than fully audited; do not interpret this map as a complete code review.

## Start from the state transition

For a scheduling or duplicate problem, follow `gearman_server_job_add_reducer` in `libgearman-server/job.cc`. It resolves the function, searches active uniqueness state, applies admission limits, creates the job, persists background work through the queue interface and queues the job. Follow the corresponding free path to understand which hashes/lists and counters are removed.

For a protocol behavior change, start in `libgearman-server/server.cc`: identify the command switch, validate packet argument expectations, follow the selected job/connection helper, and inspect the generated response. The inspected terminal handlers remove persistent state and the live job. The `PRE_SLEEP` path rechecks for runnable work to prevent a missed wakeup race.

For redelivery, inspect `gearman_server_job_queue` when an assigned worker already exists. It increments the retry counter, may notify clients and drop the job, otherwise detaches the worker, resets progress and requeues. This is distinct from receiving an explicit terminal failure packet. Track every caller into this path before changing its semantics.

## Ownership inventory

Write down who owns packet buffers, copied workload bytes, job objects, client registrations, worker registrations, connection objects and timer callbacks. For every error return, determine which caller still frees the original buffer. The release notes include double-free and lifecycle-race fixes; copied code that looks innocuous can violate these boundaries.

Queue state is spread across structures for functions, active jobs, unique lookup, client subscriptions and worker assignments. Changing one counter/list without the others can produce leaks, stranded work or use-after-free. Maintain explicit invariants such as running not exceeding total and each live job having a coherent ownership state.

## Concurrency and timers

Do not assume every callback runs on the same thread. The epoch wakeup code distinguishes event-thread timer work from the processing thread's queue ownership and uses separately protected pending timestamps. A “simple” timer scan over a processing-owned list can introduce a race. Analyze lock order, callback lifetime and shutdown cancellation together.

Before changing connection lifecycle, locate IO/proc queues, dead/removed flags and final-free ownership. Reproduce a reconnect/shutdown stress case with a fixed seed. An atomic flag does not by itself protect the object it points to from being freed.

## Patch workflow

Reproduce on the deployed tag, state the violated invariant, add a regression test, make the smallest ownership-preserving change, and run the relevant upstream suite plus sanitizer configurations. Diff protocol and persistence compatibility separately from internal refactoring. Record behavior changes in release-facing documentation, especially retry counts, ordering and unsupported packet handling.
