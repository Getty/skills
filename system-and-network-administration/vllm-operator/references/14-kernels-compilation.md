# 14 — Attention Kernels, CUDA Graphs, Compilation, and Speculation

## Compatibility before micro-tuning

The attention backend, model architecture, GPU generation, dtype, KV layout,
head dimensions, sliding/full attention, multimodal support, and parallelism
must fit together. Start with `auto` and a documented combination; record what
was actually selected in the log. A list of fast kernel names does not replace
functional evidence. [S03, S14, S18](28-sources.md)

FlashAttention, FlashInfer, Triton, and architecture-specific paths are not
arbitrarily interchangeable switches. A kernel can win for one batch/context
class and lose for another. Forcing a backend can exclude features or require
different dtypes. Local help and the support matrix take precedence over old
`VLLM_*` environment-variable tips.

## Graphs and compilation costs

CUDA Graphs can reduce CPU launch overhead; compilation can optimize operations
and kernel paths. They require warmup/compilation time, additional graph memory,
and suitable shape/capture ranges. More capture sizes are not free. On a 24 GB
card, lost KV capacity can offset the launch overhead saved.
[S03–S04, S11](28-sources.md)

`--enforce-eager` is a valuable **diagnostic comparison**: when a model works only
without the graph path, that path may be the cause. It is not a general
performance recommendation. Do not simultaneously disable graphs, change
quantization, and increase batch size; the result would be uninterpretable.

Keep compile caches persistent and access-protected, but do not treat them
as binary packages portable across arbitrary drivers, images, or GPUs.
Versions, hardware architecture, compiler flags, and model paths influence
validity. Measure cold start separately: image pull, weight download,
deserialization, quantization transformation, compilation/capture, health check,
and first actual result.

## Speculative decoding — find the matching workload

A draft model, model-internal mechanism, or another supported proposal method
produces candidates; the target path verifies them. With good acceptance,
multiple output tokens can be produced per target step. Additional draft
computation, memory, and scheduling overhead can erase the gain. Especially
under high load, speculation is not an automatic throughput booster.
[S23](28-sources.md)

Classical correctly implemented rejection-based methods aim to preserve the
target distribution; this does not justify labeling every current experimental
or approximate mode and combination lossless. Floating-point paths, batch
composition, and seeds also affect practical reproducibility.
[S23, S30](28-sources.md)

Before testing, check draft/target compatibility, extra VRAM, quantization/TP/
backend support, and context limits. Validate the documented
`--speculative-config` for the chosen method instead of inserting an arbitrary
draft-model name. Compare: no speculation; short and long outputs; low and high
load; acceptance and proposal lengths; TTFA, ITL/TPOT, and SLO goodput.
A draft model can lose overall even when individual requests are faster,
because fewer active sequences fit into the remaining KV space.

## Do not forget the CPU and host path

Tokenization, JSON/tool parsers, large logprob responses, multimodal preprocessing,
and stream serialization consume CPU. Too many API workers can multiply RAM
usage and increase CPU contention. Tune threads/NUMA only after host measurements;
do not simply maximize thread counts. On rented hosts, virtual CPU count and
actually available CPU share are not the same thing.

## Reproducibility

`temperature=0` does not universally prove bit-identical results across all
batches/GPUs. Batch-invariant execution exists as a specific feature with
cost/support conditions. Enable it only when reproducibility is a real
requirement and the target combination supports it. [S30](28-sources.md)

Acceptance requires a warm, profiler-free A/B test, a quality gate, the
compilation/graph memory difference, and a realistic load curve.
“Kernel X is newer” is not a measurement.
