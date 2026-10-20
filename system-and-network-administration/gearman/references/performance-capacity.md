# Capacity planning and performance investigation

Evidence for scheduling and implementation-specific behavior: [G1, S1](sources.md). The equations and experiment design below are analytical models, not advertised Gearman benchmark numbers.

## Model execution capacity first

For arrival rate λ jobs/second and mean execution time S seconds, the average required busy execution slots are approximately λS. With c independent slots, utilization is approximately λS/c. Operation near full utilization leaves little room for burstiness or tail latency. Measure service-time distributions and external bottlenecks instead of treating the mean as an SLO.

Little's law relates average in-system work L, throughput λ and average time W as L = λW under a stable measurement regime. It does not determine a safe queue limit during overload. If arrivals exceed sustainable completions, backlog grows until admission, resources or deadlines intervene.

Estimate memory from measured per-job overhead plus payloads, live connections, worker/server structures, in-flight result buffers and backend-client allocations. Persistence is not a promise to evict pending jobs from memory. Oversized payloads may be better represented by an authorized object reference plus content digest and expiry policy.

## Benchmark layers independently

Measure ECHO for transport overhead, a tiny deterministic function for dispatch overhead, realistic CPU work, realistic I/O work, large results and persistent submissions. Include connection reuse and connection churn, foreground and background, one/multiple functions, each priority, idle wakeup, and replay after restart. Then repeat with the real TLS/backend/topology and representative failure injection.

Record exact hardware, process/thread counts, OS limits, server/library versions, backend durability settings, payload/result distribution, warmup and duration. Report successful committed operations and latency percentiles, not merely submitted packets per second. Include error, duplicate and unknown-outcome rates.

## Scaling knobs and limits

Increase worker execution slots only while downstream systems can absorb them. Separate CPU-heavy and latency-sensitive functions when shared pools cause head-of-line blocking. Use bounded producer concurrency and an explicit queue-full response. Check whether high-priority admission can starve normal/low work; priority is not a deadline scheduler.

Server thread counts are not worker process counts. More server threads can change contention and memory use without increasing business execution capacity. Test rather than assuming linear speedup. Connection keepalive/proxy timeouts influence failure detection, not only throughput.

For multiple independent servers, monitor each queue and its eligible worker pool. Aggregate averages can hide a stranded shard. If routing changes, run the failover deduplication drill before interpreting a throughput gain as a reliability gain.

## Capacity acceptance artifact

State workload, expected sustained/burst rates, maximum age, worker/resource budgets, downstream concurrency limits, queue/payload limits, overload behavior, recovery time objective and reconciliation policy. Test at realistic failure conditions and document the point at which admission should reject work. “Supports many jobs” is not a measurable acceptance criterion.
