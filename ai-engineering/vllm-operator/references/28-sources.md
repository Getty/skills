# Sources, Evidence, and Updates

Original research: **September 21, 2026**. The original source record reports
that the official release page marked **v0.29.0 (September 9, 2026)** as Latest.
That observation does not establish that every item at a moving `stable` URL
belongs to exactly that date. The target installation takes precedence.

The texts in this package are an independent technical synthesis and operational
designs. Hardware figures are manufacturer specifications; memory calculations
are explicit models; starting values are experiment parameters, not measured
recommendations. Claims about a combination require a local compatibility test.

English localization: **September 30, 2026**. Source IDs, titles, URLs, and the
original research date are retained. Source annotations are translated; this
localization does not claim that external sources or release status were
rechecked on the translation date.

## S01 — vLLM Releases

<https://github.com/vllm-project/vllm/releases>

Release listing: v0.29.0, September 9, 2026; do not equate it with an arbitrary state of the stable documentation.

## S02 — GPU installation

<https://docs.vllm.ai/en/stable/getting_started/installation/gpu/>

Linux, platforms, wheel/CUDA/Python compatibility.

## S03 — Engine arguments

<https://docs.vllm.ai/en/stable/configuration/engine_args/>

Flag names, value ranges, version-dependent defaults.

## S04 — Optimization and tuning

<https://docs.vllm.ai/en/stable/configuration/optimization/>

Scheduler, chunked prefill, CPU and multimodal processing.

## S05 — Automatic prefix caching – usage

<https://docs.vllm.ai/en/stable/features/automatic_prefix_caching/>

APC accelerates reusable prefill, not decode directly.

## S06 — Automatic prefix caching – design

<https://docs.vllm.ai/en/stable/design/prefix_caching/>

Hash chains, cache identity, cache_salt, lifecycle.

## S07 — Native KV offloading

<https://docs.vllm.ai/en/stable/features/kv_offloading_usage/>

OffloadingConnector, CPU, and additional storage tiers.

## S08 — Production metrics

<https://docs.vllm.ai/en/stable/usage/metrics/>

Metric families and semantics; the local scrape is authoritative.

## S09 — Per-request metrics

<https://docs.vllm.ai/en/stable/features/per_request_metrics/>

Request timing, units, boundaries, and CPU overhead.

## S10 — OpenTelemetry example

<https://docs.vllm.ai/en/stable/examples/observability/opentelemetry/>

OTLP configuration, protocols, and instrumentation.

## S11 — Profiling vLLM

<https://docs.vllm.ai/en/stable/contributing/profiling/>

Profiler configuration, Nsight, PyTorch, substantial measurement overhead.

## S12 — Quantization support

<https://docs.vllm.ai/en/stable/features/quantization/>

Backend/hardware/quantization matrix.

## S13 — Quantized KV cache

<https://docs.vllm.ai/en/stable/features/quantization/quantized_kvcache/>

FP8, scales, calibration, and layer exceptions.

## S14 — Attention backend support

<https://docs.vllm.ai/en/stable/design/attention_backends/>

Combination of architecture, dtype, attention, and features.

## S15 — Benchmark CLI overview

<https://docs.vllm.ai/en/stable/benchmarking/cli/>

Datasets, prefix repetition, timed traces, multimodal workloads.

## S16 — vllm bench serve reference

<https://docs.vllm.ai/en/stable/cli/bench/serve/>

Request rate, concurrency, percentiles, goodput, result files.

## S17 — OpenAI-compatible server

<https://docs.vllm.ai/en/stable/serving/online_serving/openai_compatible_server/>

APIs, additional fields, templates, and protocol boundaries.

## S18 — Supported models

<https://docs.vllm.ai/en/stable/models/supported_models/>

Model/task matrix, native implementation, and integrations.

## S19 — Structured outputs

<https://docs.vllm.ai/en/stable/features/structured_outputs/>

JSON Schema, grammars, and version-dependent backends.

## S20 — Tool calling

<https://docs.vllm.ai/en/stable/features/tool_calling/>

Model/parser/template compatibility.

## S21 — Reasoning outputs

<https://docs.vllm.ai/en/stable/features/reasoning_outputs/>

Parsers, visible answers, reasoning, and streaming.

## S22 — LoRA

<https://docs.vllm.ai/en/stable/features/lora/>

Adapter serving and dynamic loading.

## S23 — Speculative decoding

<https://docs.vllm.ai/en/stable/features/speculative_decoding/>

Methods and their compatibility.

## S24 — Multimodal inputs

<https://docs.vllm.ai/en/stable/features/multimodal_inputs/>

Multimodal inputs, resource limits, reuse.

## S25 — Pooling models

<https://docs.vllm.ai/en/stable/models/pooling_models/>

Embeddings, scoring, classification, and token pooling.

## S26 — Sleep mode

<https://docs.vllm.ai/en/stable/features/sleep_mode/>

Memory release and recovery.

## S27 — Security

<https://docs.vllm.ai/en/stable/usage/security/>

Trust boundaries, API and system protection.

## S28 — Parallelism and scaling

<https://docs.vllm.ai/en/stable/serving/parallelism_scaling/>

TP/PP, topology, and distributed serving.

## S29 — Hybrid KV cache manager

<https://docs.vllm.ai/en/stable/design/hybrid_kv_cache_manager/>

Full/sliding attention, hybrid models, and memory groups.

## S30 — Batch invariance

<https://docs.vllm.ai/en/stable/features/batch_invariance/>

Numerical reproducibility across changing batches.

## S31 — GGUF

<https://docs.vllm.ai/en/stable/features/quantization/gguf/>

GGUF does not imply universal equivalence to llama.cpp.

## S32 — Docker deployment

<https://docs.vllm.ai/en/stable/deployment/docker/>

Images, platforms, shared memory, and ARM builds.

## S33 — Disaggregated prefill

<https://docs.vllm.ai/en/stable/features/disagg_prefill/>

Experimental prefill/decode split and connectors.

## S34 — Claude Code integration

<https://docs.vllm.ai/en/stable/serving/integrations/claude_code/>

Anthropic Messages compatibility in the consulted vLLM documentation.

## S35 — Codex integration

<https://docs.vllm.ai/en/stable/serving/integrations/codex/>

Reference for client/endpoint compatibility; not a performance guarantee.

## S36 — Responses with MCP tools

<https://docs.vllm.ai/en/stable/examples/tool_calling/openai_responses_client_with_mcp_tools/>

Optional server-side tool integration; do not confuse it with tool parsing alone.

## S37 — Speech-to-text APIs

<https://docs.vllm.ai/en/stable/serving/online_serving/speech_to_text/>

Model-dependent audio and streaming endpoints.

## S38 — Async RL

<https://docs.vllm.ai/en/stable/training/async_rl/>

Inference/rollouts as part of external training pipelines.

## S39 — Model runner V2

<https://docs.vllm.ai/en/stable/design/model_runner_v2/>

Do not confuse MRV2 with Engine V1/V0.

## S40 — IndexCache

<https://docs.vllm.ai/en/stable/features/index_cache/>

Specialized feature; not equivalent to generic APC.

## H01 — NVIDIA RTX 3090 / 3090 Ti

<https://www.nvidia.com/en-us/geforce/graphics-cards/30-series/rtx-3090-3090ti/>

24 GB GDDR6X; desktop models.

## H02 — NVIDIA RTX 4090

<https://www.nvidia.com/en-us/geforce/graphics-cards/40-series/rtx-4090/>

24 GB, Ada, no NVLink; desktop.

## H03 — NVIDIA RTX 5090

<https://www.nvidia.com/en-us/geforce/graphics-cards/50-series/rtx-5090/>

32 GB GDDR7, Blackwell, no NVLink; desktop.

## H04 — NVIDIA RTX A6000

<https://www.nvidia.com/en-us/products/workstations/rtx-a6000/>

48 GB workstation class; not equivalent to RTX 6000 Ada/PRO.

## H05 — NVIDIA L4

<https://www.nvidia.com/en-us/data-center/l4/>

24 GB class as an individually rented GPU.

## H06 — NVIDIA DGX Spark specifications

<https://www.nvidia.com/en-us/products/workstations/dgx-spark/>

128 GB unified memory, 273 GB/s, Arm CPU, ConnectX-7 up to 200 Gbit/s.

## H07 — NVIDIA Spark vLLM playbook

<https://build.nvidia.com/spark/vllm>

Official hardware-specific container/serving path.

## H08 — NVIDIA Spark vLLM instructions

<https://build.nvidia.com/spark/vllm/instructions>

Select the applicable container from the playbook, then pin its digest.

## C01 — Vast.ai instance types

<https://docs.vast.ai/guides/instances/choosing/instance-types>

Instance/interruption model; always check costs afresh.

## C02 — Runpod storage types

<https://docs.runpod.io/pods/storage/types>

Lifecycle of container, volume, and network storage.

## P01 — External KV cache characterization

<https://arxiv.org/abs/2609.11744>

Primary research dated September 10, 2026; break-even is setup-dependent, so do not adopt a universal speedup figure.

## P02 — LMCache paper

<https://arxiv.org/abs/2510.09665>

Architecture of external KV tiers and transfer; do not extrapolate results to consumer GPUs.

## Update protocol

At every upgrade, preserve the version, image digest, model/tokenizer revision,
driver, and local CLI help. Check changed flags, metrics, parsers, cache
compatibility, and security notes. Smoke test → quality gate → load test →
canary → rollback test. Update `sources.json` and affected references together.
Do not automatically adopt `latest` or install unreviewed instructions from
forum posts.

## S41 — OpenTelemetry Collector configuration

<https://opentelemetry.io/docs/collector/configuration/>

Collector pipeline, localhost, debug export, and configuration validation.

## S42 — NGINX proxy module

<https://nginx.org/en/docs/http/ngx_http_proxy_module.html>

SSE buffering, proxy timeouts, and upstream behavior.

## S43 — Prometheus configuration

<https://prometheus.io/docs/prometheus/latest/configuration/configuration/>

Scrape configuration and rule loading.

## S44 — vLLM benchmark HTTP implementation

<https://raw.githubusercontent.com/vllm-project/vllm/main/vllm/benchmarks/lib/endpoint_request_func.py>

Moving main revision; check OPENAI_API_KEY and the client measurement boundaries.

## S45 — vLLM serve CLI

<https://docs.vllm.ai/en/stable/cli/serve/>

Frontend/admission flags, usage, API-key path boundaries, and scheduling.
