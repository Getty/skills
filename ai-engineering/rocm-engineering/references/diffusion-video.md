# Image, video and ComfyUI workflows

Evidence checked: 2026-10-30. Evaluate the entire workflow graph, not only whether ComfyUI starts. Read [pytorch.md](pytorch.md) and [quantization-attention.md](quantization-attention.md) for the runtime underneath it.

## Contents

- [Define the workload and its dependencies](#define-the-workload-and-its-dependencies)
- [Build a reproducible baseline](#build-a-reproducible-baseline)
- [Plan image and video memory](#plan-image-and-video-memory)
- [Select attention deliberately](#select-attention-deliberately)
- [Use multiple GPUs explicitly](#use-multiple-gpus-explicitly)
- [Classify workflow failures](#classify-workflow-failures)
- [Optimize and validate output](#optimize-and-validate-output)
- [Preserve the workflow](#preserve-the-workflow)

## Define the workload and its dependencies

Collect the exact model family/revision, checkpoint precision, text encoders, VAE, input dimensions, frame count, batch, sampler, scheduler, steps, guidance and any LoRA/ControlNet/reference-image components. For video, also record temporal compression, intended output frame rate and audio requirements. Model names alone do not describe the memory or kernel requirements.

Classify every custom node:

| Node dependency | Typical AMD assessment |
| --- | --- |
| Pure Python and standard PyTorch operators | Test operators, dtype and memory behavior on the selected ROCm build |
| Native HIP or documented ROCm implementation | Check exact GPU, OS, torch/compiler and wheel support |
| Triton kernels | Inspect AMD target support and supported shapes; run numerical comparison |
| CUDA-only compiled extension | Find a maintained AMD implementation or use an alternative node |
| NVIDIA-specific inference runtime | Use an explicitly supported alternative path; do not rename device strings |
| External executable such as a video encoder | Validate its own build, codec and hardware-acceleration support |

Inspect dependency installers before executing them in the working environment. A node can replace the ROCm torch wheel or Triton version and break unrelated nodes. Build uncertain nodes in a cloned environment and keep the baseline dependency manifest.

## Build a reproducible baseline

[AMD's ComfyUI guide](https://rocm.docs.amd.com/projects/ai-ecosystem/en/latest/inference/comfy.html) starts from a supported ROCm PyTorch environment, then installs ComfyUI's dependencies. The [current ComfyUI README](https://github.com/Comfy-Org/ComfyUI/blob/master/README.md) documents separate AMD Linux and native Windows paths, including newer multi-architecture PyTorch packages on Windows. Do not claim Windows has no AMD option, or assume the Linux and Windows dependency graphs are identical.

Use this sequence:

1. Pin a ComfyUI revision and a documented torch/ROCm tuple suitable for the GPU and OS.
2. Run the PyTorch smoke test before installing custom nodes.
3. Install core requirements with a reviewed resolver plan; rerun package and GPU checks afterward.
4. Start the core application, with no optional acceleration packages and no third-party nodes.
5. Run a small, official workflow using local models with known hashes.
6. Add one required node or optimization at a time, testing both the new capability and the baseline workflow.

For an already prepared environment, the ordinary launch command is:

```bash
python main.py
```

Use the default local interface for evaluation. Before adding flags, inspect `python main.py --help` in that pinned checkout. Do not install a separate HIP SDK merely by habit when the selected torch packaging already supplies the runtime; native extension development has different requirements.

If Windows application control blocks a component, diagnose the exact blocked binary and its provenance. A vendor guide mentioning a security setting is not authorization to weaken it globally. Choose an approved package or deployment path according to the user's environment.

## Plan image and video memory

Measure peak usage by phase: checkpoint loading, text encoding, denoising, VAE decode, frame postprocessing and final encoding. Record both GPU memory and system RAM; moving work off the GPU can create a host-memory failure instead.

Weights are only one term. Video adds temporal activations, attention intermediates, latent sequences, decoded frames and encoder buffers. With global attention over spatiotemporal tokens, naive attention storage grows quadratically in token count; actual models may use temporal compression, windows or factorized attention. Do not extrapolate a one-frame benchmark linearly to a long clip without inspecting the architecture.

Prefer a measured escalation ladder:

1. One small image or the shortest valid clip, batch one.
2. Target spatial dimensions at the minimum useful frame count.
3. Target frame count, keeping all other parameters fixed.
4. Intended conditioning and adapters.
5. Concurrency or queued throughput only after one full workflow is stable.

When memory is insufficient, identify the phase before choosing a remedy. Tiled VAE decode addresses a different peak from denoiser attention. Offloading the text encoder helps only if it was resident during the peak. Lower precision may save weights but leave large activations unchanged. Use the pipeline's documented CPU/group/sequential offload method and measure transfer overhead. [Diffusers' memory guide](https://huggingface.co/docs/diffusers/optimization/memory) explains these classes of tradeoff; their benefit remains model-dependent.

For an APU, shared memory is subject to firmware, driver, OS and runtime limits, plus CPU competition for capacity and bandwidth. Treat a system-RAM figure as inventory, not a promise that one GPU allocation of that size will succeed. Keep enough headroom for the application, frames, file caches and host operations.

## Select attention deliberately

Distinguish the algorithm requested by a ComfyUI flag from the actual backend selected by torch or an extension. [AMD's attention analysis](https://rocm.blogs.amd.com/software-tools-optimization/comfyui-fa-backends/README.html) shows that installed packages and dispatch priority can change the path. Its experiments focus on Linux RDNA configurations and include experimental builds; do not convert its performance ranking into a universal recommendation.

Start with the pinned application's default or documented PyTorch SDPA path. If diagnosing dispatch, an example from current ComfyUI is:

```bash
python main.py --use-pytorch-cross-attention
```

Confirm that flag exists in the installed version and inspect runtime logs. The VAE can use a different attention path from the denoiser. A package named `flash-attn`, an AOTriton-enabled torch build, AITER and xFormers are separate components; having one installed does not validate the others.

Before adopting a faster backend, compare identical inputs, shapes and precision against the baseline. Include attention masking, conditioning and VAE output. Inspect for NaNs, blank images, color shifts, seams and temporal artifacts. For a custom SageAttention or patched kernel route, record its experimental scope and exact revision; never present a community workaround as AMD validation.

## Use multiple GPUs explicitly

Four 32-GiB GPUs provide four separate device-memory budgets. They do not automatically give an ordinary single-device ComfyUI node a 128-GiB allocation.

Choose an explicit scaling method:

- Run independent workers for independent image/video jobs when throughput is the objective. Allocate GPU(s), model cache and output paths per worker.
- Place pipeline components on different GPUs if the workflow and nodes implement that placement. Account for transfers and simultaneous residency.
- Use a model-specific sequence/context/tensor parallel implementation when available and validated for ROCm.
- Use a distributed diffusion runtime such as the route described by [AMD's xDiT guide](https://rocm.docs.amd.com/projects/ai-ecosystem/en/latest/inference/xdit.html) only after confirming the model, parallel mode and release match.

The xDiT recipe inspected here targets `gfx942`/`gfx950` Instinct systems; it is not evidence that the same container and distributed kernels support Radeon or an APU.

Do not infer parallel inference support from the presence of multiple visible GPUs. Inspect per-device allocations and utilization during each phase. A workload may use one GPU for most computation and another only during encoding, or replicate the full model on every worker. Distinguish throughput scaling from reducing the latency of one clip.

## Classify workflow failures

| Observation | First isolation step |
| --- | --- |
| ComfyUI starts but a node cannot import | Inspect that node's Python/native dependencies without changing the GPU driver |
| Model loads, denoising fails | Reduce to the same operator/dtype/shape and inspect attention or quantization backend |
| Denoising completes, decode fails | Isolate VAE precision, tiles, dimensions and its separate attention path |
| OOM only on long video | Measure temporal activations and phase peak; reduce frames before changing unrelated settings |
| Black or corrupted output | Check finite latents, VAE outputs, dtype and backend parity; preserve seed and inputs |
| One GPU sits idle | Inspect the workflow's actual placement/parallel implementation |
| Upgrading a node slows all workflows | Diff torch, Triton, attention packages and application dispatch selection |
| Encoding is slow with low GPU compute usage | Measure frame transfer, codec implementation, storage and CPU encoder work |

ROCm 10.1.0 lists a performance regression affecting ComfyUI workloads on Radeon PRO W7900, including some image and video models. Check [that release's known issue](https://rocm.docs.amd.com/en/docs-10.1.0/about/release-notes.html) before spending time on generic tuning. Preserve the affected GPU/release scope rather than generalizing to all Radeon devices.

## Optimize and validate output

Benchmark wall-clock time to a usable saved artifact, then break it into model load, prompt processing, sampling, decode and encoding. Report seconds per image or clip with dimensions, frames, steps and precision. Include peak VRAM/RAM and cold versus warm execution. Avoid comparing clips with different effective workloads as GPU speed claims.

Evaluate image fidelity, prompt adherence, temporal consistency, motion quality and any task-specific constraints. A faster path that changes outputs beyond the accepted quality tolerance is a different configuration. For stochastic pipelines, use fixed seeds and multiple representative prompts; exact pixel equality across different kernels is not always meaningful.

## Preserve the workflow

Save workflow JSON, custom-node revisions, model hashes, package manifest, GPU/OS/driver tuple, relevant flags, seeds and performance measurements. Retain one minimal core workflow and one representative full workflow as regression artifacts. Label untested nodes and experimental backends explicitly so another operator can reproduce the successful path without inheriting undocumented assumptions.
