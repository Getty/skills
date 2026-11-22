# Simulation and event systems

## Contents

- Choose the rule boundary
- Schedule work by meaning
- Separate commands, state and presentation
- Make replay requirements explicit
- Manage asynchronous work and reload
- Use the reference rule example

This reference is engine-independent design guidance. Lua provides functions, tables, errors and cooperative coroutines; it does not prescribe an ECS, game tick, network model or scheduler. [Sources: Lua introduction](https://www.lua.org/manual/5.5/manual.html#1), [coroutines](https://www.lua.org/manual/5.5/manual.html#2.6).

## Choose the rule boundary

Let Lua express domain decisions such as recipe eligibility, job priority, progression, dialogue, events and production rules. Expose host operations at a useful granularity: request_route, reserve_items, apply_command, query_nearby. Avoid requiring every rule to traverse native internals property by property.

Choose where state lives: Lua records, native data, or an explicit hybrid. Each field should have one authoritative owner. Define copies, borrowed views, snapshot validity and invalidation if both layers can observe it. Do not maintain two independent mutable inventories and assume they remain synchronized.

Keep this optional: small games can use simple modules and tables. Introduce ECS, component stores or native batch processors only when the workload and maintenance needs justify them.

## Schedule work by meaning

Distinguish render time from simulation time. Use explicit updates/events for needs, production and decisions. A task completion can trigger new work; a stable citizen does not necessarily need a fresh full decision every frame.

For each system define input data, update cadence, ordering dependencies and maximum work per update. Use dirty sets, event queues or grouped updates when they reduce measured work without hiding state changes. Preserve event order where it affects outcomes.

Specify queue semantics: immediate versus deferred delivery, whether events enqueued during processing run now or next pass, duplicate handling, cancellation, recursion limits and error behavior. Treat callbacks as potentially reentrant unless the API explicitly prevents it.

Choose a catch-up policy for fixed ticks. A wall-clock stall should not create an unbounded number of updates in one frame. Document pause and time-scale behavior independently from rendering.

## Separate commands, state and presentation

Commands request a change; the authoritative simulation validates and applies it; events/results describe what happened. Presentation consumes relevant state and effects. This separation can exist entirely within one process.

Use explicit command records with IDs and schema when commands cross persistence/network boundaries. Validate permissions and feasibility in the authoritative owner. An earlier UI feasibility check is a preview, not a guarantee at commit time.

Keep definitions distinct from instances: recipe quantities and building capabilities are shared definitions; inventory, progress and assigned workers are mutable state. Use stable IDs for relationships and resolve native handles through an adapter.

For shared client/server code, share definitions and pure calculations. Loading the same Lua file on two machines does not synchronize their variables. Choose host replication, snapshots/deltas or an explicit deterministic protocol according to the game requirements.

## Make replay requirements explicit

Decide whether tests need repeatability, saves need coherent snapshots, debugging needs recorded input, or multiplayer needs deterministic lockstep. These are different requirements.

For deterministic replay, control update order, unordered table traversal, numeric behavior, random streams, external input, clocks and async completion order. Record code/content versions. A fixed seed is insufficient if a cosmetic operation consumes the same random stream as an authoritative decision. [Language constraints: table traversal](https://www.lua.org/manual/5.5/manual.html#pdf-next), [random](https://www.lua.org/manual/5.5/manual.html#pdf-math.random).

Avoid promising portable bit-identical simulation across runtimes/native libraries without testing the complete contract. Server-authoritative snapshots can avoid that requirement when lockstep is unnecessary.

## Manage asynchronous work and reload

Attach world/session identity, request ID and relevant generation to work that returns later. Discard stale results after object destruction, rule replacement or changed intent. Do not run a Lua coroutine on arbitrary threads because it looks like a task object.

Use host thread-safe queues to deliver plain results to the owning VM/thread. Preserve cancellation and completion ownership. Never resume a coroutine after its VM has been closed.

Hot reload should quiesce or version outstanding work. Replace rule dispatch only after validating new code and migrating the affected state. Keep save-data schemas independent from live closures. A failed reload should leave the old running state valid or stop clearly; half-old/half-new rules are difficult to reason about.

## Use the reference rule example

assets/rules.lua provides a synchronous production operation for plain inventory and recipe tables. All returned validation failures occur before writes. Inputs/outputs may refer to the same item; the operation checks available input before applying output. Quantities use a documented cap safe for the tested number models.

The fixture illustrates domain constraints and explicit state. It does not implement storage capacity by volume, async reservations, networking, persistence, work scheduling or rollback after memory exhaustion. Add only the contracts required by the target game. semantic_checks.lua verifies successful production, rejected input, overflow rejection, no partial consumption and same-item net changes.
