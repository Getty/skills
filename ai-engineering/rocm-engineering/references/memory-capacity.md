# Memory and capacity planning

Use this for feasibility, sharding, OOM diagnosis and hardware comparisons. Formulas below are planning models; validate real allocator peaks and application quality.

## Contents

- [Identify memory domains](#identify-memory-domains)
- [Budget inference](#budget-inference)
- [Use the estimator](#use-the-estimator)
- [Budget training and creative pipelines](#budget-training-and-creative-pipelines)
- [Diagnose allocation and choose hardware](#diagnose-allocation-and-choose-hardware)

## Identify memory domains

Record physical boards, logical HIP devices, partitions and memory reported per logical device. Distinguish discrete HBM/GDDR, shared APU system memory, host-pinned memory and remotely accessible peer memory. A board with multiple GPU dies or a partitioned device may expose several allocation domains. Ask the runtime, then explain the topology.

Use bytes internally and state units. `GiB = bytes / 2^30`; decimal GB uses `10^9`. If a budget literally means 160 billion bytes, it is about 149.0 GiB. Do not assume every vendor label uses the same convention; inspect the runtime's usable memory.

Memory capacity, bandwidth and compute throughput are distinct. Shared APU memory can enable larger models while having different bandwidth/coherence behavior than dedicated HBM. Reserve host capacity for the OS, data loading and services. Reported GTT limits or resizable BAR address space are not additional physical VRAM. See [hardware](hardware.md) and [HIP unified memory](https://rocm.docs.amd.com/projects/HIP/en/latest/how-to/hip_runtime_api/memory_management/unified_memory.html).

## Budget inference

Build a per-device budget:

`resident weights + KV/state cache + temporary activations + library workspace + graph buffers + communication buffers + allocator/runtime overhead + reserve`.

For `P` parameters stored at nominal `b` bits, the raw weight term is `P × b / 8` bytes. Then account for scales, zero points, padding, unquantized tensors, repacking, duplicate copies during loading, and format-specific metadata. Model files on disk can differ from runtime representation. A 4-bit label alone is insufficient.

For a conventional full-attention decoder with separate K and V caches:

`KV bytes = 2 × layers × KV heads × head dimension × cached tokens × simultaneous sequences × bytes per cache value`.

Use **KV heads**, not query heads, for GQA/MQA. Include prompt tokens plus generation reserve. Real servers allocate pages/blocks and can retain prefix caches, so add allocation rounding and policy effects. Quantized KV requires its actual representation and scale overhead. See the runtime's cache implementation; [Transformers caching](https://huggingface.co/docs/transformers/cache_explanation) provides a conceptual entry point.

This formula does not directly model MLA, state-space/recurrent layers, cross-attention, mixed local/global attention, multimodal encoder caches, or speculative-model state. Sum each layer/state type according to its implementation. A sliding window only bounds memory if the selected backend actually evicts or reuses its cache accordingly.

Tensor parallelism may shard weights and KV differently; few KV heads can cause replication. Pipeline stages need uneven layer budgets and transfer buffers. Expert parallelism changes expert placement, while shared/dense weights can remain replicated. MoE active-parameter count estimates work, not the complete resident weight set. Inspect actual placement instead of dividing every memory term by GPU count.

## Use the estimator

The [memory estimator](../scripts/memory_budget.py) implements only the conventional formula with explicit assumptions. It does not download a model or infer architecture from a model name.

```bash
# Synthetic architecture, not a claim about a named model or measured workload.
python3 scripts/memory_budget.py \
  --parameters-b 70 --weight-bits 4 --weight-overhead 0.15 \
  --layers 80 --kv-heads 8 --head-dim 128 \
  --tokens 32768 --sequences 1 --kv-bytes 2 \
  --runtime-gib 4 --device-gib 80
```

With these inputs, the weight allowance is approximately 37.49 GiB and KV is 10 GiB. Adding the explicitly assumed 4 GiB runtime allowance yields about 51.49 GiB. Reserving 15% of physical capacity requires about 60.57 GiB total capacity. These are arithmetic results, not evidence that a 70B model fits or its backend exists.

Increasing simultaneous sequences to four raises this conventional KV term to 40 GiB. Longer context and concurrency therefore change feasibility even with identical weights. Prefix sharing may reduce some real allocations, but do not count on it without the server's documented behavior and measurements.

`--weight-shards` and `--kv-shards` are separate assumptions. Use them only after verifying the engine's layout. The helper requires an even KV-head split; for replicated KV, keep `--kv-shards 1`. It does not model unbalanced pipeline stages, replicated tensors, communication peaks or KV heads padded by a specific engine.

The default 15% weight overhead, 2 GiB runtime allowance and 15% capacity reserve are **planning defaults**, not universal safe values. Replace them with measured representation/workspace data. A result within the assumed budget still needs a full-context execution test.

## Budget training and creative pipelines

For training, sum weights, gradients, optimizer states, optional master weights, activations, temporary workspaces and communication buffers. Example bookkeeping for each trainable parameter: 2 bytes for a low-precision weight, 2 for a low-precision gradient, 4 for an FP32 master copy and 8 for two FP32 Adam moments totals 16 bytes before activations. Different optimizer/gradient/master-weight choices change this figure. Do not hardcode “16 bytes per parameter” as a framework guarantee.

LoRA reduces trainable state, but the base model and activations still occupy memory. QLoRA adds backend-specific quantized storage and dequantization workspace. Activation checkpointing trades compute for retained activation memory. Gradient accumulation changes effective batch size without making every activation term proportional to the effective batch. See [training](training-finetuning.md).

For image/video generation, profile text/vision encoding, denoising, attention and VAE decoding separately. A pipeline can fit the denoiser and fail at output decoding. Frames, resolution, batch size, attention implementation, latent dimensions and tiling interact. Stage offload and independent jobs are distinct multi-GPU strategies; neither automatically shards a single denoising operation. See [diffusion/video](diffusion-video.md).

## Diagnose allocation and choose hardware

Separate framework **allocated** tensor memory, allocator **reserved** memory and device-wide telemetry. Reserved blocks may be reusable inside the process; they are not necessarily a leak. Device-wide usage includes other processes, drivers and allocations outside the framework. See [PyTorch memory behavior](https://docs.pytorch.org/docs/2.14/notes/hip.html).

For an OOM, capture the phase, exact request/shape, allocation size and per-device state. Reduce one dimension, then verify the result. Check unintended model replicas, long-lived references, concurrent jobs, graph capture, loading peaks and stale workers. Cache-emptying calls cannot free live tensors or create enough memory for an inherently oversized allocation.

For capacity purchases, compare at least: supported backend, usable memory per device, memory bandwidth, target compute precision, topology, host RAM/CPU/I/O, cooling/power and maintainability. Four smaller devices may improve independent throughput while being a poor substitute for one large device for latency-sensitive sharded inference. Quantify the actual communication pattern before treating aggregate capacity as usable capacity.
