# 23 — Diagnostic Cards: Symptom → Test → Action

Use every card with a version/workload manifest. A proposed cause remains a
hypothesis until a counter-test supports it. The flag/kernel/metric references
are listed under [Sources](28-sources.md), especially S03–S14 and S27–S28.

| Symptom | Likely cause classes | Low-cost counter-test | Possible next action |
|---|---|---|---|
| OOM during model loading | Weights/metadata/temporary loading buffers | Check raw weights, peak RAM/VRAM, and other processes | Smaller compatible quantized model or more memory |
| OOM during graph capture | Graph reservations/capture sizes | Run the same configuration once in eager mode | Adjust graph budget selectively; increase reserve |
| OOM only under load | KV growth, multimodal/activation peaks, competing process | Fewer active sequences at the same length | Admission/KV budget/output/multimodal limits |
| Low GPU load, high TTFT | CPU, tokenizer, IO, gateway | Direct local request with a small text input | Fix host path, worker count, logs, or buffering |
| TTFT rises with the queue | Overload | Finite rate below the SLO knee | Early rejection, workload separation, another replica |
| Good TTFT, user still waiting | Reasoning, tools/agent, content parser | TTFA plus tool/application timing | Check budgets/model/parser |
| Decode stutters with long prompts | Large prefill steps/mixed load | Smaller batched-token budget | Select an appropriate chunk/admission range |
| High throughput, poor p99 | Saturation, length mix, preemption | Independent arrivals; include failed requests | Operate below the SLO knee; separate classes |
| APC supposedly enabled, no hits | Tokens/template/salt/routing/eviction | Send the identical request twice directly | Prefix diff and actual cache counters |
| High APC hit rate, slow responses | Short prefixes, decode/queue dominates | Avoided prefill tokens and timing shares | Stop forcing further cache optimization |
| Offload is slower | Transfer dominates, CPU/IO pressure | APC-only under identical load | Disable offload or select a suitable hot set |
| TP=2 slower than one GPU | Collectives/PCIe/P2P/small batches | Topology, single GPU, and replicas | Larger single card, different layout, evaluate PP |
| Quantization saves memory, not time | Kernel/dequantization path/small batch | Identical load, backend log | Suitable format/kernel or retain the reference |
| Worse answers after an upgrade | Template/defaults/parser/quantization | Exact request against the old manifest | Fix correctness before performance tuning |
| Broken tool calls | Parser/template/model mismatch | Fixed tool contract including streaming | Use the officially matching parser/template |
| Prometheus panel suddenly empty | Renamed/optional metric | HELP/TYPE/scrape inventory | Version queries; do not fabricate zero values |
| Missing traces | Transport/TLS/sampling/network namespace | Local collector and one request | Check protocol, ports 4317/4318, and export logs |
| Slow only with tracing | Sampling/detail/exporter blocking | Tracing off versus light versus detailed | Less detail, bounded export queue |
| Long cold starts | Weight download, IO, compilation/capture | Timestamps per phase | Persistent cache, warmup, suitable instance |
| Cancelled request, GPU remains full | Cancellation path/retry/another request | Isolated long stream, then cancel | Check gateway/client propagation and server status |
| Slower after hours | Temperature, power, leaks, IO, competing load | Time series of clocks/RAM/VRAM/queue | Fix the measured cause rather than just restart |

## Minimal incident dataset

Time window, deployment/model revision, error rate/timeouts, active/waiting
requests, KV occupancy/preemptions, host/GPU/disk state, and **redacted** error
context. Preserve a small reproducible prompt only after approval. Do not
attach complete user conversations to public issues by default.

## Priorities during an outage

First limit/reroute user traffic, then preserve data, then return to a known
configuration. Do not simultaneously update drivers, models, quantization
formats, and scheduling during an overload incident. For recurring OOM,
establish a smaller safe serving envelope instead of adding retries.

## When should optimization deliberately stop?

When required quality needs a model that does not fit with reserve; when the
SLO remains unattainable despite sensible load limits; when the quantization/
kernel combination is unsupported; or when infrastructure effort outweighs
the benefit. Then consider a smaller model, a larger single card, targeted
rental, or another appropriately tested local stack. This is an architecture
decision, not a defeat for tuning.
