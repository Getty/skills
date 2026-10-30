# 25 — Specialized Capabilities, Extensions, and Deliberate Boundaries

This reference keeps less frequently needed areas visible without adding them
to every single-GPU baseline. “Documented” is not evidence for the selected
GPU/model/feature combination. [S03, S18, S28–S40](28-sources.md)

## Offline inference and batch processing

The Python engine can run local generation/pooling jobs without an HTTP
frontend. Online streaming SLOs and maximum offline throughput are different
goals. Reuse the engine process instead of loading a model for every prompt.
Split large jobs into bounded work units with persisted IDs/results; do not
unnecessarily accumulate all data and outputs in RAM.

Discover CLI batch/benchmark subcommands such as `run-batch`, `bench throughput`,
`bench latency`, `bench startup`, and applicable sweep tools through local help.
HTTP benchmarks show the end-to-end path; offline benchmarks isolate different
components. Do not compare their figures without clear labeling.
[S15–S17, S45](28-sources.md)

## Hybrid models, MLA, SSM, and sliding windows

An MHA/GQA calculator is formulated for homogeneous full attention. MLA stores
different states; SSM/Mamba and full/sliding hybrids have different memory
lifecycles and grouping. The hybrid KV manager handles these differences;
disabling it can change allocation and is not a general memory optimization.
[S18, S29](28-sources.md)

Do not change sliding windows or RoPE/context extensions without understanding
the model. A higher `max_model_len` does not create trained capability to use
relevant information reliably across arbitrary distances. Long-context quality,
startup validation, and runtime costs are separate tests.

## MoE, experts, and elasticity

Active parameters do not determine total resident weight memory. Expert
distribution, load balancing, all-to-all communication, and quantization kernels
can be decisive. Specialized EP/DP/elastic paths require suitable workers and
networks. Choose them for a small setup only when the desired model or workload
justifies them; do not extrapolate large-cluster benchmarks to two consumer
cards. [S18, S28](28-sources.md)

## Disaggregated prefill/decode

Separate prefill and decode workers can decouple resource selection and
scheduling policy. However, KV states must be transferred promptly and
compatibly; routers, connectors, networks, failure/retry paths, and memory
duplication add complexity. On small systems, KV transfer can eliminate the
expected latency benefit. Treat this as an experiment after establishing a
stable single instance. [S07, S33](28-sources.md)

## IndexCache and other model-specific shortcuts

According to the documentation, IndexCache is a specialized DSA path for
DeepSeek-V3.2 or compatible models: top-k token indices are reused between
certain layers instead of being recomputed everywhere. It is **not** generic
cross-request prefix caching. Its configuration belongs to model overrides
and needs a separate quality/performance gate; do not add it to every model
as merely “another cache.” [S40](28-sources.md)

## Extensions and custom code

Custom model implementations, parsers, logits processors, plugins, or backends
can enable integrations but expand the trusted codebase. Release/ABI changes,
security review, unit/integration tests, and clear owners must be addressed.
A custom plugin is not automatically covered by official support. Do not run
arbitrary code from an unknown model repository with host secrets on a rented
instance. [S18, S20, S27](28-sources.md)

Prompt-embedding/token-ID paths may save frontend work but require correct
shapes, tokenizer identity, and a trusted input system. The consulted CLI
specifically warns about incorrectly shaped prompt embeddings. Do not enable
them publicly without validation. Development, trace replay, and weight-update
paths are not standard product endpoints either. [S45](28-sources.md)

## Limits that no flag list removes

vLLM guarantees neither factual accuracy, safe tool execution, nor training
quality. RAG, retrieval evaluation, data preparation, agent permissions, and
external training methods remain separate layers. Streaming improves perceived
progress but does not necessarily accelerate the complete result. Caching
does not replace semantic memory. Offload does not replace fast memory
bandwidth. More replicas can increase capacity without accelerating
single-request decode.

For one laptop user, a lighter local stack suited to the platform may be more
practical; for high GPU concurrency, vLLM may fit well. This package makes
that decision through functional, quality, and load tests, not an eternally
valid blanket ranking of alternative projects.
