# 07 — External KV, LMCache, and Transfer Break-Even

## Three different mechanisms

**KV offload** moves reusable context states into other storage tiers.
**Weight offload** moves model weights or their use toward the host and can
cause transfers during model steps. **Preemption/recomputation** interrupts
work and recomputes states later. An old `swap-space` recipe is not a universal
modern KV-tiering switch. [S03–S04, S07](28-sources.md)

Native connectors and external projects such as LMCache can expand cache pools
beyond GPU residency. Versions, layouts, architectures, and transfer paths
determine compatibility. The native documentation describes CPU memory as the
primary tier closest to the GPU, with additional tiers connected through CPU
staging. [S07, P02](28-sources.md)

## The economics of a hit

```text
Net saving ≈ avoided prefill time
             − additional lookup/loading/deserialization time
             − non-overlapped transfer/scheduling costs
             − opportunity costs for RAM, CPU, PCIe, and GPU
```

Asynchronous copying is not free copying. Calculate with **measured effective**
bandwidth and actual layout bytes. A synthetic example: transferring 1 GiB of
payload over a path delivering an effective 8 GiB/s already takes 125 ms for
transfer alone; lookup and staging are not included. Saving only 40 ms of prefill
would not make this hit a latency win. These numbers are a calculation example.

The cited primary research investigates exactly these setup-dependent
thresholds; do not transfer its speedups to a different GPU or workload.
[P01](28-sources.md)

## Try the native CPU tier

Only after checking local flags, confirming sufficient **actually available**
RAM, and measuring a baseline:

```bash
# Add to an already validated serving configuration; not a complete recipe:
--kv-offloading-size 4 --kv-offloading-backend native
```

The consulted CLI defines this size as the sum across TP ranks, not an additional
4 GiB per rank. Alternatively, use the explicit connector configuration in
`configs/kv-offload-native.json`. **Do not combine both configuration paths.**
The example reserves 4 GiB of host memory; first check total RAM, WSL/cgroup
limits, and pinned-memory behavior. [S03, S07](28-sources.md)

## When another tier is worthwhile

First try a CPU tier for frequently recurring long prefixes whose cache working
set exceeds GPU KV capacity. Test NVMe only when CPU capacity and reuse justify
it. Use a network cache only with realistic transfer and failover calculations.
On small servers, a smaller model or more GPU KV can be simpler and faster.

On Spark, CPU and GPU memory come from a shared pool. An additional CPU cache
does not simply create an independent second memory capacity; copies and
reservations can place extra pressure on the shared pool. Measure the actual
backend behavior. [H06–H08](28-sources.md)

## Persistence and correctness

A cache entry needs a namespace accounting for model revision, tokenizer/template,
adapter, positioning, KV dtype/layout, and tenant. Do not reuse old KV states
after weight changes or incompatible upgrades. Persistence across restarts is
a property of the specific backend, not “of APC.”

For a slow or unavailable store, provide a bounded timeout and a fallback to
recomputation where the connector/application supports it. Do not accept
incorrect data merely to finish a request quickly. Cache deletion is relevant
to privacy and must cover backups, disks, and remote tiers.

## Acceptance

Compare APC-only with APC plus offload: cold/warm/evicted states, short/long
prefixes, hit rate and **avoided prefill tokens**, transfer bytes/time,
p95/p99 TTFT, preemptions, CPU/RAM/IO pressure, and errors during store failure.
Revert offload when SLO goodput or stability worsens, even with a higher hit rate.
