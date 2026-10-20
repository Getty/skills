# Application patterns and limits

These are design patterns, not built-in Gearman workflow guarantees. Core transport semantics: [G2, G3, S1, S2](sources.md).

## Good separation of responsibilities

Gearman routes named work to capable workers. An application defines validation, authorization, identities, deadlines, outcomes, retry policy and workflow state. Keep these layers explicit. The same worker business function should be testable without a server connection.

For media processing, submit a stable asset ID, authorized object reference, content digest and transform version rather than a very large blob. Write output under an idempotent content/job key and atomically publish the outcome. For document indexing, include source revision and index schema version so a delayed older job cannot overwrite newer state.

For notification delivery, use a provider idempotency key when available and maintain an operation ledger. A worker crash after successful delivery but before completion can otherwise send twice. For billing or irreversible operations, do not rely on Gearman unique keys or timeout assumptions as the business consistency mechanism.

## Agent/tool execution

Use fixed capability names and validated argument schemas. Do not create an unrestricted “execute this shell string” worker. Run heavyweight execution in a constrained worker identity/environment with bounded CPU, memory, time, subprocess count, filesystem and network access. Retrieve secrets locally under least privilege. Store artifacts separately and return references/digests.

A language-model request ID should remain stable across transport retries. Track provider request IDs, cost and output state separately. Gearman cannot retract an already issued external model/tool call when a client disconnects. Introduce admission/concurrency controls before expensive dependencies, not only after jobs have been accepted.

## Fan-out and aggregation

A coordinator can publish child operations and store their completion state. Give each child a deterministic identity derived from workflow ID, stage and input version. Bound fan-out and aggregation memory; record a manifest of expected children and a terminal policy for partial failure. Do not assume that task completion order is input order.

Avoid a worker synchronously waiting for children that require the same fully occupied worker pool: that can deadlock. Prefer persisted stage transitions or a separately provisioned child pool. Treat reducer/protocol extensions as version-specific capabilities; an application coordinator is often easier to reason about than undocumented server orchestration.

## Periodic work and retries

Keep schedule ownership and logical retry state in an explicit scheduler/ledger when you need durable recurrence, exponential delay, jitter, poison-job quarantine or a dead-letter workflow. An epoch submission represents delayed execution, not a complete recurring scheduler. A packet constant for scheduled work is not proof the selected server supports it.

For retries, preserve the logical operation ID but distinguish attempts and use a deliberate submission key strategy. Persist the next-attempt decision before acknowledging a failed application operation where required. Ensure a recovery loop can repair the boundary between stored retry intent and Gearman publication.

## When the fit is wrong

Evaluate a different transport/workflow design when requirements center on retained replayable event logs, native cross-server replication, fine-grained tenant authorization, complex durable workflows or strong built-in delivery/retention controls. This is a requirements boundary, not a claim that another named product automatically supplies every desired guarantee. Compare failure semantics and operational burden before migrating.
