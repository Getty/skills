# 17 — NVIDIA DGX Spark: Large Shared Memory, Different Limits

## The right mental model

DGX Spark combines GB10 with an Arm CPU and, according to the manufacturer,
**128 GB of coherent unified memory** at **273 GB/s memory bandwidth**.
This memory is shared by the whole system: it is not 128 GB of dedicated VRAM
in addition to a separate 128 GB CPU RAM pool. The OS, model, KV, compilation,
and other processes compete within the available budget. The official
specifications also list ConnectX-7 at up to 200 Gbit/s and 10 GbE connectivity.
[H06](28-sources.md)

The advertised FP4 peak is a specific theoretical compute metric, not a general
token-generation speed. For dense batch-1 decode, repeatedly reading large
weights can be a central limitation. Large memory capacity can enable a large
model while a dedicated card answers faster with a suitable smaller model.
This is a tradeoff to measure, not a blanket verdict for or against Spark.

## Do not copy the software path from an x86 workstation

Arm/aarch64, GB10, drivers, CUDA, PyTorch, vLLM, and the chosen kernels must
fit together. A familiar image name does not guarantee a build for the same
architecture. Use the official NVIDIA vLLM playbook, read its supported build
path and model conditions, and then pin the successfully tested image by digest.
[H07–H08, S02, S32](28-sources.md)

There is deliberately no guessed “always current” container tag here.
In particular, a kernel path tested on other Blackwell products must not be
treated as approved for GB10 without evidence. The fastest practical path is
to functionally test an official compatible example unchanged first, then
incrementally substitute the desired model/quantization format.

## Memory planning for Spark

**Budget:** physical shared memory minus OS/host processes, actual weights and
metadata, runtime/graphs/multimodal memory, and reserve gives a rough upper
bound for KV. Also account for container limits and host pressure. The baseline
script has no Spark autodetection and must not be interpreted as automatic
approval to allocate all 128 GB.

CPU KV offload into the same shared memory does not create another physically
separate RAM pool. A different allocation/tiering path can change specific
behavior but must be measured for bandwidth and copies. NVMe expands how much
data can be stored, not the speed of GPU DRAM. Evaluate KV and weight offload
separately as well. [S07, H06](28-sources.md)

## Three useful experiment classes

**A — Developer/agent server:** moderate model, realistic tools, reasoning budget,
stable system prefixes; prioritize TTFA and short tool cycles.
**B — Larger local model:** test whether the desired quality improvement
outweighs longer decode time; do not infer high concurrency from capacity alone.
**C — Small multi-user service:** measure batching gains against queueing and
longer ITL; impose limits before the SLO knee.

For each class: single request, concurrency sweep, cold/warm APC, long outputs,
host memory, and sustained load. When a 70B model is slow, “an even larger one
also fits” is not a latency solution.

## Two Sparks

NVIDIA documents a specialized two-system path with a suitable connection and
distributed serving. First verify cabling, interface configuration, private
addresses, framework versions, and worker communication exactly against the
playbook. 2 × 128 GB is **not** a transparent shared 256 GB allocator and does
not automatically mean twice the tokens/s. [H07–H08](28-sources.md)

Compare distributing a large model against two independent replicas of a
suitable smaller model. Report individual latency, total capacity, communication,
rank memory, and failure behavior. Do not build a cluster merely because a
second device exists; the benefit must justify the extra maintenance.

## Required handover fields

Device model/RAM, host software versions, container architecture and digest,
model/tokenizer revision, selected quantization/attention path, all limits,
available system memory before/after startup, warmup time, actual TTFT/TTFA/TPOT
curves, and sustained-load observations. Clearly distinguish manufacturer
specifications from your own measurements.
