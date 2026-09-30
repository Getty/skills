# 21 — LoRA, Model Lifecycle, Sleep, and Training Boundaries

## One base model with many adapters

LoRA serving uses compatible adapters for a base model and can serve
adapter-specific requests. This saves resources compared with many complete
base-model copies, but it is not universal multi-model hosting. Rank, target
modules, tokenizer/vocabulary, quantization/parallelism support, and limits
must match. Adapter identity belongs in cache identity; do not treat different
adapters as semantically equivalent through the same KV prefix.
[S22, S06](28-sources.md)

Flags such as `--enable-lora`, `--max-loras`, `--max-lora-rank`, and CPU adapter
limits affect memory and batch compatibility. The number of loaded adapters
is not the same as the number active simultaneously. Frequent switching among
many adapters can add loading, cache, and batching costs. Run a reuse/hot-set
test rather than checking only that “one adapter works.” [S03, S22](28-sources.md)

Dynamic loading/unloading is an administrative capability. Allow only trusted,
versioned adapters from controlled paths, and do not expose management endpoints
publicly. Do not let users load arbitrary local paths or remote adapters through
the product endpoint. Rollback includes the base model **and** adapter revision.

## Sleep is not a complete autoscaler

Sleep modes can release GPU memory and incur different restoration costs on
wake-up. The documented level-1 path backs weights up to CPU memory and discards
KV; more aggressive release paths can discard weights and require reloading
or reinjection. Verify exact semantics and hardware support against applicable
documentation and a local test. [S26](28-sources.md)

Before sleep, drain requests, pause admission, and do not let new requests
enter endless queues. Re-enable readiness only when weights, required adapters,
and warmup are demonstrably ready. Do not assume the prefix cache is preserved.
Asleep does not mean “free”: rented GPU, host, and volumes may continue to be
billed unchanged.

On unified-memory systems, interpret CPU/GPU memory savings physically
correctly; a CPU backup is not a second independent memory system. Alternating
between multiple models can be useful but adds switching and warmup latency.
Include those latencies in user SLOs.

## Weight replacement and external training systems

vLLM can support inference/rollouts and weight transfer in external RL/training
workflows. This does not make backpropagation, optimizers, data curation, or
general fine-tuning fully part of vLLM. On small hardware, separate training
and serving clearly by time/resources where possible. [S38](28-sources.md)

During weight updates, complete or cancel running requests consistently;
record the model version for each result; check KV/adapter/compile compatibility;
and invalidate old, semantically stale KV states. “Hot-loading new weights”
must not produce requests that mix versions. Required synchronization and
transfer protocols are integration-specific.

## Model changes, canaries, and rollback

Validate a new revision on a separate small test set first, then under
representative load. Without a second GPU, promise a planned maintenance
window rather than apparently uninterrupted blue/green deployment. The API
alias may stay stable, but the exact revision must remain visible internally.
Do not silently switch to models with incompatible embeddings/tools behind
the same alias.

Acceptance covers cold/warm startup, memory release, sleep/wake time, the first
actual request after wake, adapter changes under load, load-failure behavior,
and demonstrated return to the previous revision. A green process status
is not sufficient.

## Caution with the online sleep path

The consulted online guide additionally requires `VLLM_SERVER_DEV_MODE=1`.
This makes development/administrative endpoints available; enable it only in
an isolated management network and after an explicit test, not as the default
for a public inference service. [S26](28-sources.md)
