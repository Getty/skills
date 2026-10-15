# Reference index

Read only the references needed for the current task. These files describe a
reusable architecture, not a mandatory framework or a module to depend on.

| Reference | Read when |
|---|---|
| [Architecture and extraction boundaries](architecture.md) | Whether a DSL is justified and what belongs in each layer |
| [Exporters and ownership](exporters-and-caller.md) | Class/role entry points, with_meta, as_is, goto, cleanup |
| [Registry and lifecycle](registry-and-lifecycle.md) | Validation, load timing, defensive copies, sealing, reloads |
| [Composition and inheritance](composition-and-inheritance.md) | Role discovery, parent buckets, diamonds, order, conflicts |
| [Plan compilation](planning-and-dependencies.md) | Phases, DAG checks, binding, group validation, manifests |
| [Predicate contracts](predicates.md) | Readers, maps, callbacks, purity, equality, safe parsing |
| [Execution and results](runner-and-results.md) | Runner API, state, errors, output validation, same-instance reruns |
| [Parallelism and Futures](parallelism-and-futures.md) | Real concurrency, aggregation, cancellation, loop integration |
| [Durable resume](resume-and-idempotency.md) | Checkpoint identity, crash windows, idempotency, leases |
| [Progress and observability](progress-and-observability.md) | Active counts, dynamic gates, events, heartbeats, redaction |
| [Attribute and form sugar](attributes-and-forms.md) | Traits, UI projections, validation boundaries, secret fields |
| [Tool schemas](tool-schemas.md) | Pure helpers, nullable enum, dialects, provider adapters |
| [Validation and localization](validation-and-localization.md) | Preflight reuse, freshness, message IDs, deferred translation |
| [Security and trust](security-and-trust.md) | Loading code, authorization, untrusted inputs, tool dispatch |
| [Testing and debugging](testing-and-debugging.md) | Negative tests, caller debugging, integration gates, determinism |
| [Performance](performance.md) | Measurement, safe caching, planner complexity, copying, backpressure |
| [Corrections and adoption](corrections-and-adoption.md) | Common misstatements, reference-implementation choices, migrating an existing DSL |
| [Practical recipes](recipes.md) | Incremental adoption and what to extract first |
| [Primary-source register](sources.md) | Checking API facts, dates, and evidence boundaries |

## Fast routes

**New DSL:** architecture → exporters → registry → planner → executable example.

**Existing caller-based DSL:** correction map → relevant affected layer → regression tests.

**Async or durable execution:** planner → predicates → Futures or resume → observability → security.

**Agent-facing inspection:** planner manifests → tool schemas → security → evaluation cases.

## Executable material

[Reference implementation and commands](../examples/reference/README.md),
[validation record](../VALIDATION.md), and
[manual agent evaluation cases](../evaluations/README.md).

The index and source register are included in the total of 20 reference files.
