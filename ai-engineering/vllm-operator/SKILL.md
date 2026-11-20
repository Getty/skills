---
name: vllm-operator
description: "Use when installing, running or tuning vLLM — small or consumer GPUs, DGX Spark, TTFT and throughput under concurrency, KV/prefix caching, quantization, OOM, tool calling."
metadata:
  version: "1.0.1"
  language: en
  researched: "2026-09-21"
  translated: "2026-09-30"
  scope: "1–4 GPUs; consumer hardware, small workstations, DGX Spark, small rented instances"
---

# vLLM Operator — Small Hardware, Reliable Serving

For operating and diagnosing vLLM on 1–4 GPUs: consumer cards, small workstations, DGX
Spark, small rented instances. Optimize **correct, useful answers within a latency budget
per euro**, not just nominal tokens/s. Not a model-training course or a data-center
architecture kit.

Explain decisions in English; preserve API and CLI identifiers unchanged. In an installed
skill, resolve script and reference paths relative to this file, not an arbitrary project
working directory. Write measurements to a separate, approved experiment directory, not
into the skill installation.

## Non-negotiable rules

1. **Version first.** Read [versioning](references/03-installation-versioning.md); check
   the local CLI, model revision, GPU/architecture, driver and image digest. Research
   dated 2026-09-21, observed release v0.29.0; `stable` is a moving target. Do not mix
   old V0 guidance with Engine V1 or Model Runner V2.
2. **Quality is a gate.** A faster model, different quantization, different parser or
   shorter context is a product change, not a free infrastructure upgrade.
3. **State measurement boundaries.** Client TTFT, first-answer latency, queue time,
   engine TTFT, TPOT, ITL and SSE chunk spacing are different quantities.
4. **Distinguish caches.** APC ≠ response cache ≠ KV offload ≠ weight offload ≠ compile
   cache. A hit does not automatically accelerate decode.
5. **Operational safety.** No unprotected public serving, no prompts or secrets in default
   logs, no arbitrary remote-code or administrative capabilities. Derive salts and cache
   namespaces from a trusted identity.
6. **Small steps.** One hypothesis, a fixed workload and a rollback per experiment.
   Driver changes, rented instances, network exposure, power limits and persistent-data
   changes require explicit approval. Scripts do not rent servers.
7. **No fabricated evidence.** Distinguish `documented`, `locally checked`, `measured`,
   `hypothesis` and `not verified`.

## Collect inputs

Fill the [workload contract](templates/workload-contract.md): hardware and memory, exact
model revision, task/modality, quantization/KV dtype, length and arrival distributions,
cache reuse and tenant boundaries, SLOs, cost ceiling. Record missing data as
assumptions; with little information, plan for **one GPU, a suitable small model, a
short bounded context and no offload**. Do not ask again for hardware details already
provided.

Audit: `python scripts/audit_env.py --out ./audit` (local, read-only; review output files
before sharing).

## Workflow

**A. Does the requested combination work?**
[Capability map](references/02-capability-map.md) →
[hardware](references/16-consumer-hardware.md) or [Spark](references/17-dgx-spark.md) →
[installation](references/03-installation-versioning.md). A successful server start does
not prove correct tools, embeddings or long-context behavior: run a basic prompt and
representative tasks before optimizing.

**B. Does it fit in memory under the intended load?**
Read [memory sizing](references/04-memory-capacity.md), then run
`python scripts/capacity.py --help`. Do not apply the MHA/GQA calculator to MLA, Mamba or
hybrid models. Compare the calculation with the actual KV capacity reported at startup.
An OOM already happens: find its phase (loading, graph capture, load) in the
[diagnostic cards](references/23-troubleshooting.md) before changing any memory flag.

**C. Establish a baseline.** Read
[deployment and security](references/22-deployment-security.md) and
[recipes](references/24-recipes.md): local or private endpoint, bounded output, initially
`dtype=auto` and a working attention backend. Client probe:
`python scripts/stream_probe.py --help`. APC probe: the same file twice; missing
`cached_tokens` means unknown, not zero.

**D. Measure under load.** Read [benchmarking](references/09-benchmarking.md),
[metrics](references/10-metrics.md) and [scheduler](references/08-scheduling-high-load.md).
`python scripts/bench_sweep.py --help` generates a plan by default; execution requires
`--execute`. Report errors, timeouts, cancellations and SLO goodput alongside
p50/p95/p99. Do not present a p99 from a handful of requests as reliable evidence.

**E. Select one bottleneck; do not tune flags at random.**
[Diagnostics](references/23-troubleshooting.md): its bottleneck triage gives each
observation a first reference and the next controlled experiment; its diagnostic cards
cover symptoms such as OOM, broken tool calls or empty panels.

**F. Deliver** a concise operational decision: assumptions, compatible configuration,
measurements, quality tests, cost calculations, known limits and rollback, in the
[experiment record](templates/experiment-record.md) and
[handover](templates/handover.md). Without a GPU test, explicitly state
`not validated on target hardware`; never present script unit tests as GPU benchmarks.

## Reference router

Load references on demand, never all at once. The workflow links 02–04, 08–10, 16–17
and 22–24; the rest by topic:

| Topic | File |
|---|---|
| Architecture, prefill/decode, PagedAttention | [01](references/01-engine-fundamentals.md) |
| All cache types and their effects | [05](references/05-cache-mechanics.md) |
| Agent prompts, stable prefixes, salts, isolation | [06](references/06-cache-layout-isolation.md) |
| Native KV tiers, LMCache, NVMe, transfer | [07](references/07-external-kv-offload.md) |
| OpenTelemetry, distributed request traces | [11](references/11-tracing.md) |
| PyTorch/Nsight, overhead, safe diagnostics | [12](references/12-profiling.md) |
| Weight/KV quantization and quality gates | [13](references/13-quantization.md) |
| Attention backends, graphs, compilation, speculation | [14](references/14-kernels-compilation.md) |
| 2–4 GPUs, TP/PP/DP/EP/CP, P2P, replicas | [15](references/15-multi-gpu.md) |
| Vast.ai/Runpod, small rented GPUs, costs | [18](references/18-rented-gpus-costs.md) |
| APIs, templates, tools, JSON, reasoning, agents | [19](references/19-api-agents.md) |
| Vision, audio, video, embeddings, reranking | [20](references/20-multimodal-pooling.md) |
| LoRA, multiple models, sleep, RL boundaries | [21](references/21-lora-lifecycle.md) |
| Specialized features and deliberate boundaries | [25](references/25-advanced-boundaries.md) |
| Flag register with consequences | [26](references/26-flag-register.md) |
| Glossary and formulas | [27](references/27-glossary.md) |
| Primary sources and updates | [28](references/28-sources.md) |

## Scripts, templates, configs

Execute scripts, do not read them; start each with `--help`. Beyond the workflow:
`serve_single.sh` (single-GPU launcher, plan only unless `--execute`), `cost.py`,
`metrics_inventory.py`, `validate_skill.py`. More templates:
[compatibility matrix](templates/compatibility-matrix.md),
[hardware scorecard](templates/hardware-scorecard.md),
[upgrade checklist](templates/upgrade-checklist.md). `configs/` holds deliberately
bounded examples. [README](README.md) explains usage and tests;
[VALIDATION](VALIDATION.md) records checks actually performed.
