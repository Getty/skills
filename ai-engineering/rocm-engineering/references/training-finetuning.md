# Training and fine-tuning on ROCm

Evidence checked: 2026-10-30. Begin with a supported framework/device tuple and [pytorch.md](pytorch.md). Validate the actual optimizer, attention and quantization implementations before committing to a large training run.

## Contents

- [Select a training strategy](#select-a-training-strategy)
- [Build a memory budget](#build-a-memory-budget)
- [Validate a minimal training lifecycle](#validate-a-minimal-training-lifecycle)
- [LoRA and quantized adapter training](#lora-and-quantized-adapter-training)
- [Distributed training](#distributed-training)
- [Precision and optimized kernels](#precision-and-optimized-kernels)
- [Checkpoint and resume](#checkpoint-and-resume)
- [Measure useful progress](#measure-useful-progress)

## Select a training strategy

Record the model architecture and revision, sequence or image shape, global batch target, dataset size, quality metric, available GPUs and interconnect, and whether the goal is adapter tuning, full fine-tuning, continued pretraining or training from scratch. Distinguish "the model fits for inference" from "a complete optimizer step and checkpoint fit."

| Strategy | What remains trainable | Main capacity/throughput consideration |
| --- | --- | --- |
| Full fine-tuning | Most or all weights | Gradients, optimizer state and often master weights dominate beyond inference memory |
| LoRA/PEFT | Selected adapters | Frozen base weights still occupy memory; activations and sequence length remain significant |
| QLoRA-style tuning | Adapters over a quantized base | Requires functioning quantized forward and backward-related adapter paths |
| DDP | Full replica per rank | Improves data throughput; does not shard the full model state |
| FSDP/ZeRO | Depends on sharding strategy | Trades communication and temporary gathers against per-rank state memory |
| Tensor/pipeline/expert parallelism | Partitioned computation/state | Requires architecture support, topology planning and balanced partitions |

Use the simplest strategy that meets measured requirements. A large training framework with custom fused kernels can add compatibility work that a plain PyTorch/Transformers baseline avoids. Conversely, large pretraining runs may justify a specialized stack after its exact AMD recipe is verified.

[Transformers' AMD guide](https://huggingface.co/docs/transformers/amd_gpu) confirms the shared PyTorch device conventions and RCCL integration. It does not make every third-party optimizer or model extension portable. For AMD's large-scale training stack, follow the [Primus entry point](https://rocm.docs.amd.com/projects/primus/en/latest/) and pin its supported model/backend recipe; this reference does not assume any uninspected Primus release is compatible.

## Build a memory budget

Compute separate terms for model weights, trainable gradients, master weights if used, optimizer states, activations, temporary kernels, distributed buckets and checkpoint assembly. Include host RAM and storage for data preprocessing, optimizer offload and checkpoint merging.

For illustration, a conventional mixed-precision Adam configuration can have 2 bytes of working weights, 2 bytes of gradients, 4 bytes of master weights and two 4-byte moment states per trainable parameter: approximately 16 bytes before activations and workspaces. This is an accounting example, not a universal requirement; actual parameter/gradient/optimizer storage depends on the optimizer and framework.

For adapters, count trainable adapter parameters separately from the frozen base. Quantized base weights also need scales, metadata and temporary dequantization buffers. Long sequences can make activations the dominant term even when adapter parameters are small.

Reduce a measured bottleneck in a controlled order: microbatch size, unnecessary padding, sequence/image size if the task permits, activation checkpointing, appropriate precision, then state sharding or offload. Gradient accumulation raises the effective batch without raising the microbatch, but does not repair the memory required by one oversized example. Measure the extra recomputation and communication costs of each change.

## Validate a minimal training lifecycle

Before scaling the dataset or GPU count:

1. Run a few fixed examples with a simple optimizer and eager execution.
2. Confirm finite loss and gradients, correct masking, and updates to intended parameters only.
3. Overfit a tiny known dataset sufficiently to demonstrate that the objective and data path are connected.
4. Save a checkpoint, exit the process, reload and resume. Compare the next-step behavior under a fixed seed and fixed data ordering.
5. Add the target dtype, attention backend, fused optimizer or quantization one at a time.
6. Repeat a representative longest example and a realistic microbatch to expose peak-memory behavior.

Do not judge training correctness solely by a decreasing displayed loss. Inspect padding labels, prompt versus response masking, train/eval mode, learning-rate schedule, gradient accumulation and clipping. Track NaN/Inf incidence and optimizer-step counts. A process that silently skips updates after overflow is not productive training.

## LoRA and quantized adapter training

Use PEFT's [quantization and adapter guidance](https://huggingface.co/docs/peft/developer_guides/quantization) for model preparation, adapter targeting and format constraints. Resolve the target module names from the actual architecture, then verify trainable parameter counts. Avoid assuming that every model exposes `q_proj` and `v_proj`, or that merged adapters preserve a quantized format without conversion.

For an already-loaded compatible base model, the structural pattern is:

```python
from peft import LoraConfig, get_peft_model

config = LoraConfig(
    task_type="CAUSAL_LM", r=16, lora_alpha=32,
    target_modules="all-linear", lora_dropout=0.0,
)
model = get_peft_model(model, config)
model.print_trainable_parameters()
```

This is an example configuration, not a recommended rank for every task. Quantized bases additionally require the preparation step and compute dtype appropriate to the selected quantization backend. Test that a backward pass produces finite adapter gradients and updates them while leaving the base frozen.

Do not repeat the outdated blanket statement that bitsandbytes is CUDA-only. At the evidence date, its maintained [installation guide](https://huggingface.co/docs/bitsandbytes/installation) documents ROCm support across CDNA/RDNA and separate platform wheel target lists. However, the Transformers summary and engine-specific integration tables may be narrower. Resolve the exact bitsandbytes release, wheel target, torch ABI and requested optimizer/quantization operation. Test the operation itself. Support in bitsandbytes does not imply support in vLLM or every fine-tuning application.

For Unsloth, LlamaFactory, TRL or another orchestration layer, inspect that project's current AMD path and transitive kernels. Preserve a plain PEFT baseline so an extension regression can be isolated. Do not infer training support from a successful inference demo. Avoid inference-oriented `device_map="auto"` as an improvised distributed-training strategy.

## Distributed training

Use one process per intended GPU and map `LOCAL_RANK` explicitly. Run [the distributed smoke test](../scripts/distributed_smoke.py) before model training; inspect its `--help` and verify rank-dependent expected sums rather than accepting a process exit as correctness.

Start on two GPUs in one node before moving to the full topology. Confirm equal optimizer-step counts, correct data sharding, no unintended sample duplication and consistent gradient accumulation. Check that evaluation and checkpoint code do not make only one rank enter a collective required by all ranks.

For FSDP, choose FSDP1 or FSDP2 deliberately and use matching framework recipes. Wrapping, optimizer initialization, frozen/trainable parameter mixtures and state-dict formats are version-sensitive. [Accelerate's FSDP guide](https://huggingface.co/docs/accelerate/usage_guides/fsdp) describes sharding and checkpoint integration; apply its version-matched instructions instead of assembling configuration fields from multiple generations.

For DeepSpeed, validate the specific ZeRO stage, offload settings and optimizer build. A successful RCCL all-reduce does not prove a fused optimizer extension is present. For multi-node runs, establish network and collective bandwidth/correctness independently, then inspect dataloader stalls and checkpoint I/O. Keep topology-specific RCCL tuning separate from model hyperparameters.

## Precision and optimized kernels

Enable mixed precision only after numerical baseline checks. Use the model's intended BF16 or FP16 path, loss scaling where required, and appropriate accumulation precision. The [PyTorch AMP lifecycle](https://docs.pytorch.org/docs/2.14/notes/amp_examples.html) covers ordering of scaling, unscaling, clipping and optimizer updates.

An attention backend that supports inference may lack the required dropout, head dimension, masking or backward variant. Validate forward and backward together. Apply the same discipline to FP8 training: hardware dtype support is insufficient without scaling, optimizer integration and stable training behavior.

At ROCm 10.1.0, release notes contain model-specific MI350X training regressions and other resolved regressions. Consult the [versioned release notes](https://rocm.docs.amd.com/en/docs-10.1.0/about/release-notes.html) for the exact model/framework scope. Do not flatten that information into "training is broken" or "all regressions are fixed."

## Checkpoint and resume

Retain model and optimizer state, scheduler, scaler where used, RNG states, consumed-data position, tokenizer, model configuration, adapter/base revisions and the complete environment. Distinguish resumable training checkpoints from weights exported for inference.

Test recovery in a new process before a long run. For distributed checkpoints, verify the supported world-size behavior; loading at another GPU count may require resharding or consolidation. Estimate peak RAM and disk space before gathering a full state dictionary. Write checkpoints atomically or use the framework's supported transactional workflow, and preserve the previous valid checkpoint until the new one is validated.

## Measure useful progress

Report useful tokens or samples per second, excluding padding where appropriate; optimizer steps per second; peak VRAM/RAM; communication fraction; data-loading wait; checkpoint duration; and validation quality. Compare equal effective batch, sequence distribution and optimization objective. Include total wall time to the target quality when possible. A faster kernel that changes convergence or silently drops examples is not a better training configuration.
