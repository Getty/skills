# Observability and native administration

Evidence: [G5–G7, S1](sources.md). The bundled [ops tool](../scripts/gearman_ops.py) restricts remote administrative requests to `version`, `status`, and `workers`. A read-only request can still reveal sensitive names or infrastructure metadata; keep outputs controlled.

## Four layers of health

A TCP connection proves listener reachability. A binary ECHO round trip proves a small request can be processed. A known harmless function proves an execution path. An application outcome query proves a particular logical request completed. Do not use the first as evidence for all four.

Gearman 2.1's CLI `--ping` is an ECHO-based probe and needs no worker. The bundled Python probe provides that limited test explicitly. Avoid health probes that create unbounded jobs when workers are unhealthy. Separate process liveness from service readiness and from dependency health.

## Interpreting status

The text `status` response has function name, total jobs, running jobs and capable worker registrations, followed by a dot terminator. Compute waiting as `total - running`; the second field is not already waiting-only. Capable registrations are not idle execution slots, and a process registered for multiple functions can appear multiple times. `prioritystatus` reports waiting queues by priority, so do not combine its counters as though all commands use identical definitions.

The parser must handle fragmented/coalesced TCP reads, exact terminators, total timeouts, malformed numbers and an output byte cap. Do not read until connection close: the server can keep the connection open. Do not execute arbitrary text supplied through an “admin command” parameter; whitelist the operations a diagnostic actually requires.

## Application telemetry

Record submission attempts, accepted requests, rejected requests, uncertain outcomes, assignment starts, execution duration, terminal transport decisions and committed application outcomes as separate events. Correlate `request_id`, operation version, origin endpoint, handle and worker identity. Avoid high-cardinality request IDs as metric labels; retain them in bounded logs/traces.

Useful measurements include backlog and oldest pending age by service class, arrival/completion rate, p50/p95/p99 end-to-end and execution latency, worker saturation, retries by cause, persistent-backend latency/errors, result-store errors, CPU/RSS/file descriptors and reconnect rate. Gearman's native status does not supply a durable history or all these application metrics; instrument producers/workers and your outcome store.

## Alerts and administrative changes

Alert on sustained age/SLO violations, missing capable workers for a nonempty queue, repeated uncertain outcomes, rejected admission, memory pressure, replay delays and backend errors. “Queue length is positive” alone is usually an inadequate alert.

Commands that change limits, create/drop functions, cancel jobs or stop the server are mutations. Capture before/after state and require the operator's intended scope. A diagnostic script must not silently issue `maxqueue`, cancellation or shutdown as a repair. See [troubleshooting](troubleshooting.md) for evidence-first procedures.
