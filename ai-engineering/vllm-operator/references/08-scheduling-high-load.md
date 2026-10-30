# 08 — Scheduling, High Load, and Controlled Overload

## Three different optimization goals

**Single request:** one person should see a useful answer early.
**Capacity:** many concurrent requests should run efficiently overall.
**Service quality:** an agreed proportion of requests should stay within TTFT,
visible-answer, and E2E limits despite realistic bursts. These goals are not
identical. A large batch can increase tokens/s while making interactive users
wait longer. A faster single request does not prove higher capacity.
Define the goal in the [workload contract](../templates/workload-contract.md).

## Chunked prefill and the two most important budgets

With chunked prefill, the documented V1 scheduler prioritizes pending decode
work and uses the remaining token budget for prefill; large prefills can be
spread across steps. `max_num_batched_tokens` limits token work scheduled in
one step; `max_num_seqs` limits concurrently running sequences. Neither alone
guarantees a global queue limit or customer capacity. Behavior also depends
on the model and scheduler. [S03–S04](28-sources.md)

| Change | Plausible benefit | Cost to watch |
|---|---|---|
| Smaller batched-token budget | Smaller prefill spikes, often smoother decode | Longer prefill duration, potentially lower throughput |
| Larger batched-token budget | More efficient processing of large prefills | Larger steps and potentially worse ITL under mixed load |
| Fewer active sequences | Less KV pressure and preemption | More queueing or lower utilization |
| More active sequences | Better amortization of weight access during decode | More KV, longer steps, worse tail latency |
| Shorter permitted outputs | Earlier release of occupied slots/KV | Product quality and completeness may deteriorate |

Words such as “often” are deliberate: only the target hardware's load curve
settles the question. Starting values of 8 sequences / 2,048 batched tokens
are an **experimental hypothesis** in this package, not a general recommendation.
A 32B model on constrained hardware may need substantially less; a small model
may support substantially more.

## A queue is not extra compute capacity

When work consistently arrives faster than it can be processed, waiting time
grows. Increasing `max_num_seqs` cannot solve this indefinitely. Little's law,
`L = λ × W`, applies to a stable system with consistent measurement boundaries;
as a planning intuition, longer residence time ties up more requests at the
same arrival rate. Stationary conclusions are invalid for a growing unbounded
queue.

The gateway needs a **bounded admission budget**: global and per-tenant active
requests, estimated input/output tokens, queue length, and maximum queue age.
Reject early and transparently rather than timing out after a long wait.
The gateway implements the specific HTTP status/retry guidance; do not assume
vLLM automatically implements this product policy. Do not send requests through
unbounded layers of proxy, SDK, and engine queues.

Initially separate interactive traffic and long batch jobs by time or by
separate small replicas. A priority flag alone does not replace fair,
tenant-aware capacity planning. A constantly prioritized tenant can starve
others; aging and minimum shares are gateway decisions.

## KV pressure and preemption

Longer running sequences need additional KV memory. Under pressure, V1 can
interrupt work and later restore it through **recomputation**; old V0
explanations presenting swap as the default are misleading here. Preemption
consumes latency and compute budget and can further overload an already full
instance. Observe preemptions alongside KV occupancy, queueing, and tail
latencies. [S03–S04, S08](28-sources.md)

Counter-test: run the same load with fewer active sequences, shorter outputs,
or more genuinely available KV. Blindly setting `gpu_memory_utilization` to
0.99 can introduce runtime, graph, or competing-process OOMs instead of solving
the problem. Use newer scheduler options such as full-input reservation,
watermarks, and async scheduling only after checking local help, model/backend
compatibility, and a reproducible A/B test; their existence guarantees no gain.

## A useful load-test sequence

1. Check a warm single request and correctness. Then test fixed concurrency
   1/2/4/8, or suitably smaller steps, to **characterize saturation**.
2. Next test independent, finite arrival rates under realistic length
   distributions. Do not hide a client semaphore before the timer starts.
3. Add bursts, long outputs, a cache-miss storm, and sudden cancellations.
   Client retries multiply load; set an explicit retry budget and jitter.
4. Choose an operating limit below the observed SLO knee. The reserve depends
   on burst/failure risk; it is not a universal percentage.

Acceptance includes errors/timeouts/rejections, queue p95/p99, client TTFT,
first-answer latency, E2E, ITL, SLO goodput, KV, and preemption.
A queue that does not shrink again after a burst has not passed the load test.

## Native admission controls in the documented releases

The consulted serving CLI documents `--max-num-queued-reqs` for all in-flight
requests (**waiting and running**) and `--max-num-queued-tokens` for the prefill
token backlog; new requests are rejected with 503 when a limit is exceeded.
The token counter is conservative: partially computed prompts remain fully
counted, and cache hits become known only later. Do not infer exact available
GPU work from this counter. Use these flags as a coarse native protection layer
when the target version supports them; tenant quotas, user token budgets,
and deadlines remain additional responsibilities. [S45](28-sources.md)
