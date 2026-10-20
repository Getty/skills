# Foundations and responsibility boundaries

Read when defining the system, explaining terminology, or evaluating whether Gearman fits a workload. Evidence: [G2, G3, G13](sources.md).

A **client** requests a named function with an opaque byte payload. A **job server** matches queued work to registered capabilities. A **worker** executes application code and reports an outcome. The server does not execute the named function merely because a client submits it. Function names are routing contracts, not programming-language imports.

Keep four identities distinct: the function name, the protocol unique key, the server-issued job handle, and the application's request ID. A job handle is useful for live diagnostics but is not your permanent business key. A worker can register multiple functions, and many workers can register the same function. Registration does not by itself prove spare capacity or application health.

## Foreground and background

Foreground attaches a client to live work events and a final result. Background separates acceptance from execution; the caller obtains a handle rather than a future durable result object. This distinction also affects persistent queue eligibility on the C server. Never describe asynchronous client APIs and background jobs as synonyms: an event-driven client can run foreground jobs concurrently.

## Ownership model to write down

| Component | Owns | Must not be assumed to own |
|---|---|---|
| API/producer | Authentication, business request ID, validation, response contract | Definitive completion based only on accepted submission |
| Gearmand | Routing, active queue and worker connections | Business transactions, result retention, tenant authorization |
| Worker | Validation, execution, side-effect protection, outcome reporting | Global ordering merely because it is a single process |
| Application database | Outbox, request state, durable results, dedup records | Gearmand's live queue state unless explicitly integrated |
| Supervisor/orchestrator | Processes, resources, restart policy | Safe replay of application effects |

The last three columns are design boundaries, not restrictions on what an application may implement around Gearman. They prevent accidental promises that nobody actually maintains.

## Decision procedure

Start with one bounded pure function and measure the complete path. Add a result store when a caller must retrieve outcomes later. Add an outbox when submission must follow an application transaction reliably. Add separate worker pools when workloads have different resource or latency requirements. Add multiple independent servers only after documenting routing and stranded-job recovery.

Choose a different primary abstraction when the central requirement is a durable execution history, a complex dependency graph, transactionally ordered event replay, or built-in consumer authorization. Gearman can be a dispatch layer inside such a system, but the missing contracts must live somewhere explicit.

Acceptance questions: Who retries? Who detects work that was accepted but never completed? How are duplicate effects prevented? What identifies a completed request after its handle disappears? What happens when the original server returns after failover? An architecture without answers is incomplete even when its happy-path demo works.
