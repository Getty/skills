# LLM inference and serving on AMD GPUs

Evidence checked: 2026-10-30. Resolve exact model, GPU, OS and engine versions before selecting kernels or promising performance. Use [quantization-attention.md](quantization-attention.md) for precision and backend compatibility.

## Contents

- [Select the execution model](#select-the-execution-model)
- [Resolve a reproducible engine build](#resolve-a-reproducible-engine-build)
- [Budget memory by device](#budget-memory-by-device)
- [Establish a serving baseline](#establish-a-serving-baseline)
- [Scale and tune deliberately](#scale-and-tune-deliberately)
- [Use llama.cpp and Ollama appropriately](#use-llamacpp-and-ollama-appropriately)
- [Diagnose the serving lifecycle](#diagnose-the-serving-lifecycle)
- [Report a useful benchmark](#report-a-useful-benchmark)

## Select the execution model

Choose from workload requirements rather than GPU memory alone. Record model architecture and revision, weights format, context length, prompt/output distribution, concurrency, streaming needs, structured output, tool parsing, multimodal inputs and adapter requirements.

| Workload | Candidate | Main acceptance question |
| --- | --- | --- |
| Concurrent API serving with continuous batching | vLLM | Does the exact ROCm build support this model, attention path and quantization? |
| Serving with structured generation or specialized scheduling | SGLang | Is the selected AMD model/kernel combination covered by its release? |
| Local GGUF inference and CPU/GPU placement control | llama.cpp | Does HIP or Vulkan implement the model and quantization efficiently? |
| Managed local model lifecycle and simple API | Ollama | Which backend is actually selected, and how are layers placed? |
| Model investigation or unusual architecture | Transformers/PyTorch | Does eager execution establish a correct baseline before engine conversion? |

Engine model support, GPU support, dtype support and optimized-kernel support are different sets. A model can load through a slower fallback without its intended fast path. A CUDA model recipe that imports a NVIDIA-specific kernel cannot be assumed portable merely because its Python tensors use `cuda` names.

## Resolve a reproducible engine build

Use [vLLM's AMD installation instructions](https://docs.vllm.ai/en/latest/getting_started/installation/gpu/) and [AMD's validated vLLM recipe](https://rocm.docs.amd.com/projects/ai-ecosystem/en/latest/inference/vllm.html) together. At the evidence date they describe different packaging lines: upstream has ROCm-specific wheel variants, while AMD's ROCm 10.1 recipe ties its vLLM 0.29 family to PyTorch 2.13 and a specific Python environment. Do not replace that torch dependency with the newest standalone torch release.

Apply the same rule to [AMD's SGLang recipe](https://rocm.docs.amd.com/projects/ai-ecosystem/en/latest/inference/sglang.html) and [upstream SGLang AMD guidance](https://docs.sglang.io/docs/hardware-platforms/amd_gpu). On the evidence date the AMD installation page still displayed a 10.0/0.5.15 recipe while newer release-overview and upstream versions existed. Treat this as a reason to resolve a real published artifact, not synthesize a container tag from version numbers.

For each candidate:

1. Pin the image digest or complete wheel/source revisions, including PyTorch, Triton, AITER and attention packages.
2. Confirm its supported target list and compare against actual inventory. A default Instinct image might omit a Radeon kernel path.
3. Start with the container's documented environment. Do not mount a competing host ROCm library tree over it.
4. Run the PyTorch smoke test, then a small local model through that engine.
5. Record startup logs identifying attention, GEMM, MoE, quantization and collective paths.
6. Retain the working artifact before experimenting with another backend or compiler.

Copy version-specific workarounds only when their triggering conditions match. Scope environment overrides to the process or deployment configuration so a later upgrade does not inherit a forgotten workaround.

## Budget memory by device

Include weights, quantization scales, KV cache, activations, graph-capture buffers, temporary workspaces, runtime allocations and reserve for variation. A checkpoint's disk size alone is not its serving memory requirement.

For a conventional dense transformer with standard K/V storage, a first approximation is:

`KV bytes ≈ active tokens × layers × KV heads × head dimension × 2 × bytes per KV element`.

Use KV heads rather than query heads for GQA. Treat this as a planning estimate; MLA, sliding-window or hybrid architectures, alignment, paging and replicated cache change the result. Inspect the engine's actual cache allocation and token capacity. Reducing weight precision does not necessarily reduce KV precision.

Evaluate every rank's budget. Tensor parallelism partitions specific tensors and adds communication; it does not make every allocation divisible by GPU count. Pipeline parallelism partitions layers but has activation and scheduling costs. Mixture-of-experts models need expert and routing analysis. Heterogeneous GPU memory can make the smallest rank decisive.

Prefer one GPU when the complete workload fits with useful headroom and latency is the objective. Consider replicas for independent throughput. Use TP, PP or expert parallelism when supported and justified by capacity or measured throughput. Check topology and collective correctness before model-scale tests.

## Establish a serving baseline

Use a model already downloaded to an approved local path and a known-compatible engine environment. This is a conservative **command template**, with limits to adjust after measurement:

```bash
vllm serve /models/example \
  --host 127.0.0.1 --port 8000 \
  --tensor-parallel-size 1 \
  --max-model-len 4096 \
  --max-num-seqs 4 \
  --gpu-memory-utilization 0.80
```

Confirm the installed release's `vllm serve --help` before applying flags. Omit a forced quantization or attention backend initially unless the model format requires it. Verify tokenizer, chat template, stop tokens and model revision; malformed formatting can look like broken GPU inference.

For SGLang, begin from its pinned image's launch example and inspect `python -m sglang.launch_server --help`; keep its own argument names and environment conventions. Do not translate vLLM flags mechanically. Bind local evaluation services to loopback; deployment exposure and authentication belong to the requested deployment design.

Acceptance checks should include deterministic short completions where supported, long-prompt requests, the intended structured output or tools, cancellation, and a small concurrency ramp. Compare outputs against a trusted model implementation, allowing documented numerical differences rather than demanding identical sampled prose.

## Scale and tune deliberately

Tune one axis at a time: context budget, concurrent sequences, batched tokens, prefix caching, chunked prefill, attention backend, quantization, graph capture, TP/PP/EP, then speculative decoding if supported. Keep accepted quality and latency limits fixed during comparisons.

Prefix-cache benefits depend on reusable token prefixes and cache residency; report hit rates rather than promising a universal speedup. Chunked prefill changes the tradeoff between prompt processing and active decode latency. Speculative decoding adds draft-model or extra-head costs and requires model/backend support; acceptance rate determines whether it helps. These features need separate cold-start and loaded-server measurements.

For multi-GPU or multi-node deployment, validate rank-to-GPU assignment, RCCL collectives, network interfaces and memory headroom first. A single GPU's tokens/s cannot predict distributed scaling. Do not transplant MI300X BIOS or kernel tuning recipes onto an unrelated Radeon workstation.

## Use llama.cpp and Ollama appropriately

[llama.cpp's build guide](https://github.com/ggml-org/llama.cpp/blob/master/docs/build.md) documents distinct HIP and Vulkan paths. A HIP build uses `GGML_HIP`; a Vulkan build uses `GGML_VULKAN`. Build for a verified GPU target and pin the source revision. Do not use the guide's example target as a substitute for inventory.

Inspect backend initialization, device enumeration, offloaded layers, tensor placement and actual context allocation. CPU+GPU inference can fit a model that does not fit wholly in VRAM, but transfer and CPU compute can dominate. Benchmark prompt processing and token generation separately. Compare HIP and Vulkan on the same model/quant/context only after confirming both use the intended device.

[Ollama's hardware documentation](https://docs.ollama.com/gpu) maintains its own GPU/backend support lists. Its bundled runtime and device coverage may differ from system ROCm. Verify the server process's environment, selected library, visible devices and offload report. A successful Vulkan run is useful AMD acceleration, but does not establish HIP compatibility for another application. Treat architecture overrides as experiments with numerical validation, not official support upgrades.

## Diagnose the serving lifecycle

| Failure stage | Investigate first |
| --- | --- |
| Import or engine construction | Python ABI and native dependency tuple |
| Weight load | Model format, revision, shards, quantization implementation, peak load memory |
| First inference | Kernel target, attention/quantization dispatch, real input shapes |
| Graph capture | Extra capture memory, graph-safe operators, selected capture sizes |
| Long context or concurrency | KV allocation, active tokens, fragmentation and batch limits |
| Multi-GPU startup | Topology, rank mapping and collectives before model details |
| Restart only | Surviving workers and GPU memory release from the old deployment |

ROCm 10.1.0 documents a restart-memory issue for large tensor-parallel vLLM deployments on MI350X/MI300X. Verify that previous workers exited and memory was released before restart; do not diagnose this scoped issue as every vLLM OOM. See the [release known issues](https://rocm.docs.amd.com/en/docs-10.1.0/about/release-notes.html).

## Report a useful benchmark

Report time to first token, inter-token latency, p50/p95/p99 request latency, prompt and generation tokens/s, successful requests/s and rejection/error counts. Preserve prompt/output distributions, concurrency or arrival rate, tokenizer, model revision, precision, hardware topology and clock/power state. Include cold start and model reload where operationally relevant. A saturated throughput run and a low-concurrency interactive run answer different questions; provide both when the deployment needs both.
