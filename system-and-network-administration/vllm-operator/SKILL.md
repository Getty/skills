---
name: vllm-operator
description: >-
  Plan, install, operate, measure, and optimize vLLM. Use for vLLM serving,
  consumer GPUs, DGX Spark, small rented GPU servers, TTFT/ITL/TPOT,
  high concurrency, prefix/KV caching, KV offloading, tracing, Prometheus,
  quantization, OOM, tool calling, multimodal workloads, and multi-GPU decisions.
  Produces reproducible configurations, experiments, and rollback plans rather
  than blanket performance promises.
metadata:
  version: "1.0.1"
  language: en
  researched: "2026-09-21"
  translated: "2026-09-30"
  scope: "1–4 GPUs; consumer hardware, small workstations, DGX Spark, small rented instances"
---

# vLLM Operator — Small Hardware, Reliable Serving

## Mission

Optimize **correct, useful answers within a latency budget per euro**,
not just nominal tokens/s. This skill is an operations and diagnostic tool,
not a model-training course or a data-center architecture kit.

Load references on demand. Do not load every file into every context.
Explain decisions in English; preserve API and CLI identifiers unchanged.
For installed skills, resolve script and reference paths relative to this file,
not an arbitrary project working directory. Write measurements to a separate,
approved experiment directory, not into the skill installation.

## Non-negotiable rules

1. **Version first.** Read [Versioning](references/03-installation-versioning.md).
   Check the local CLI, model revision, GPU/architecture, driver, and image digest.
   Research dated 2026-09-21; observed release v0.29.0. `stable` is a moving target.
   Do not mix old V0 guidance with Engine V1 or Model Runner V2.
2. **Quality is a gate.** A faster model, different quantization,
   different parser, or shorter context is a product change, not a free
   infrastructure upgrade.
3. **State measurement boundaries.** Client TTFT, first-answer latency, queue time,
   engine TTFT, TPOT, ITL, and SSE chunk spacing are different quantities.
4. **Distinguish caches.** APC ≠ response cache ≠ KV offload ≠ weight offload
   ≠ compile cache. A hit does not automatically accelerate decode.
5. **Operational safety.** No unprotected public serving, no prompts or secrets
   in default logs, and no arbitrary remote-code or administrative capabilities.
   Derive salts and cache namespaces from a trusted identity.
6. **Small steps.** One hypothesis, a fixed workload, and a rollback per experiment.
   Driver changes, rented instances, network exposure, power limits, and
   persistent-data changes require explicit approval. Scripts do not rent servers.
7. **No fabricated evidence.** Distinguish `documented`, `locally checked`,
   `measured`, `hypothesis`, and `not verified`.

## Collect inputs

Record hardware/OS; GPU count, VRAM or unified memory, PCIe/P2P; CPU/RAM/NVMe;
model ID and exact revision; task/modality; quantization/KV dtype;
context distribution; output/reasoning lengths; arrival rate/bursts/active sessions;
cache reuse and tenant boundaries; TTFT/answer/TPOT/E2E SLOs; cost ceiling.

Record missing data as assumptions. With little information, plan for **one GPU,
a suitable small model, a short bounded context, and no offload**.
Do not ask again for hardware details already provided.

Artifact: [Workload contract](templates/workload-contract.md).
Audit: `python scripts/audit_env.py --out ./audit` (local, read-only;
review output files before sharing).

## Workflow

### A. Does the requested combination work?

[Capability matrix](references/02-capability-map.md) →
[Hardware](references/16-consumer-hardware.md) or
[Spark](references/17-dgx-spark.md) →
[Installation](references/03-installation-versioning.md).

Check model architecture, task/runner, dtype, quantization format, kernel,
tokenizer, template, parser, and API. A successful server start does not prove
correct tools, embeddings, or long-context behavior. Run a basic prompt and
representative tasks before optimizing.

### B. Does the model fit in memory under the intended load?

Read [Memory sizing](references/04-memory-capacity.md), then run
`python scripts/capacity.py --help`.
Weights + KV + activations + CUDA Graphs + runtime/multimodal memory + reserve.
Do not apply the MHA/GQA calculator to MLA, Mamba, or hybrid models.
Compare the calculation with the actual KV capacity reported at startup.

### C. Establish a baseline

Read [Deployment](references/22-deployment-security.md) and
[Experiment recipes](references/24-recipes.md). Use a local or private endpoint;
bound output; initially retain `dtype=auto` and a working attention backend.
Record observations before and after warmup.

Client probe: `python scripts/stream_probe.py --help`.
APC probe: use the same file twice; missing `cached_tokens` means unknown, not zero.
Keep resolution/quality tests separate from load tests.

### D. Measure under load

Read [Measurement methodology](references/09-benchmarking.md),
[Metrics](references/10-metrics.md), and [Scheduler](references/08-scheduling-high-load.md).

`python scripts/bench_sweep.py --help` generates a plan by default.
Execution requires `--execute`. It uses the official `vllm bench serve`
CLI and checks flags against the locally installed help output.

Measure cold/warm caches, different prompt/output lengths, realistic arrival
rates, bursts, and saturation. Report errors, timeouts, cancellations, and
SLO goodput alongside p50/p95/p99. Do not present a p99 from a handful of requests
as reliable evidence.

### E. Select a bottleneck; do not tune flags at random

| Observation | First reference | Next controlled experiment |
|---|---|---|
| Long queue, GPU/KV full | [High load](references/08-scheduling-high-load.md) | Bound admission/output; evaluate another replica |
| Long uncached prefills | [Caching](references/05-cache-mechanics.md) | Prefix layout; chunk budget; context |
| Missing cache hits | [Prompt layout](references/06-cache-layout-isolation.md) | Compare tokens/templates/salts/routing |
| Insufficient KV / preemptions | [Memory](references/04-memory-capacity.md) | Reduce active sequences; evaluate KV quantization |
| Slow decode | [Kernels](references/14-kernels-compilation.md) | Isolate bandwidth, batch, quantization, speculation |
| GPU frequently idle, CPU busy | [Tracing](references/11-tracing.md) | Tokenization, parsers, IPC, SDK/proxy |
| Good TTFT, late answer | [API/reasoning](references/19-api-agents.md) | Reasoning/output budget; measure visible answer onset |
| TP slower than expected | [Multi-GPU](references/15-multi-gpu.md) | Topology/P2P; compare independent replicas |
| Offload makes performance worse | [KV offload](references/07-external-kv-offload.md) | Compare transfer time with avoided prefill |
| Slow only behind the proxy | [Deployment](references/22-deployment-security.md) | SSE buffering, timeouts, cancellation propagation |

### F. Deliver the result

Provide a concise operational decision with assumptions, a compatible
configuration, measurements, quality tests, cost calculations, known limits,
and rollback. Use [Experiment](templates/experiment-record.md) and
[Handover](templates/handover.md). Without a GPU test, explicitly state
`not validated on target hardware`; never present script unit tests as GPU benchmarks.

## Reference router

| Topic | File |
|---|---|
| Architecture, prefill/decode, PagedAttention | [01](references/01-engine-fundamentals.md) |
| Capabilities, compatible combinations, and limits | [02](references/02-capability-map.md) |
| Linux/WSL/containers, versions, and upgrades | [03](references/03-installation-versioning.md) |
| Weights, KV, reserves, GQA/MLA/hybrid | [04](references/04-memory-capacity.md) |
| All cache types and their effects | [05](references/05-cache-mechanics.md) |
| Agent prompts, stable prefixes, salts, isolation | [06](references/06-cache-layout-isolation.md) |
| Native KV tiers, LMCache, NVMe, transfer | [07](references/07-external-kv-offload.md) |
| Chunked prefill, queues, overload, and fairness | [08](references/08-scheduling-high-load.md) |
| TTFT/ITL/TPOT/E2E, load tests, and goodput | [09](references/09-benchmarking.md) |
| Prometheus, dashboards, GPU telemetry | [10](references/10-metrics.md) |
| OpenTelemetry and distributed request traces | [11](references/11-tracing.md) |
| PyTorch/Nsight, overhead, and safe diagnostics | [12](references/12-profiling.md) |
| Weight/KV quantization and quality gates | [13](references/13-quantization.md) |
| Attention backends, graphs, compilation, speculation | [14](references/14-kernels-compilation.md) |
| 2–4 GPUs, TP/PP/DP/EP/CP, P2P, and replicas | [15](references/15-multi-gpu.md) |
| 8–48 GB consumer/small-workstation classes | [16](references/16-consumer-hardware.md) |
| DGX Spark/GB10 and two small systems | [17](references/17-dgx-spark.md) |
| Vast.ai/Runpod, small rented GPUs, and costs | [18](references/18-rented-gpus-costs.md) |
| APIs, templates, tools, JSON, reasoning, agents | [19](references/19-api-agents.md) |
| Vision, audio, video, embeddings, and reranking | [20](references/20-multimodal-pooling.md) |
| LoRA, multiple models, sleep, RL boundaries | [21](references/21-lora-lifecycle.md) |
| Operations, proxy, auth, cancellation, privacy | [22](references/22-deployment-security.md) |
| Symptom → cause → test → rollback | [23](references/23-troubleshooting.md) |
| Concrete startup and tuning experiments | [24](references/24-recipes.md) |
| Specialized features and deliberate boundaries | [25](references/25-advanced-boundaries.md) |
| Flag register with consequences | [26](references/26-flag-register.md) |
| Glossary and formulas | [27](references/27-glossary.md) |
| Primary sources and updates | [28](references/28-sources.md) |

## Supporting material

`scripts/` contains an audit tool, capacity and cost calculators, a streaming
probe, a benchmark sweep, a metrics inventory, and package validation.
`configs/` contains deliberately bounded example configurations.
`templates/` structures decisions and evidence. [README](README.md) explains
usage and tests; [VALIDATION](VALIDATION.md) records checks actually performed.
