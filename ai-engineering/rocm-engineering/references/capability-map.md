# Capability map

Evidence baseline: 2026-10-30. These are assessment routes, not a universal support matrix. Resolve combinations with [AMD's matrix](https://rocm.docs.amd.com/en/latest/compatibility/compatibility-matrix.html) and upstream application documentation.

## Assess a workload

| Goal | Candidate route | Feasibility conditions | Acceptance evidence |
| --- | --- | --- | --- |
| Tensor computation | HIP PyTorch | Target, wheel, dtype, operators | GPU result matches trusted reference |
| Workstation chat | llama.cpp, Ollama, PyTorch, applicable server | Format, backend, memory, latency | Backend identified; representative context completes |
| Concurrent LLM API | vLLM/SGLang ROCm | Target, quantizer, attention, topology | Quality plus TTFT/ITL/throughput at load |
| Embeddings/reranking | Compatible framework and model | Operators, batching, text lengths | Retrieval quality and throughput |
| Multimodal AI | Supported model implementation | Vision/audio operators and preprocessing | Complete multimodal task |
| Speech workloads | Application GPU backend | Dependency chain and model | Full representative audio pipeline |
| Image generation | Diffusers/ComfyUI | Torch, nodes, dtype, attention, VAE | Complete valid image, peak memory |
| Video generation | Compatible graph/model | Frames, resolution, temporal attention, VAE | Entire generation and decode |
| LoRA | Training framework | Backward, activations, optimizer, checkpoint | Finite gradients, update, resume |
| QLoRA | Quantizer/optimizer integration | Per-OS/GPU dequantization and backward | Learning behavior against baseline |
| Full training | Framework and RCCL | All state, activations, operators, communication | Convergence, restart, multi-rank correctness |
| Custom operations | HIP, Triton, CK, AITER | Compiler, target, contract, kernel coverage | Differential tests over relevant shapes |
| CUDA migration | HIPIFY plus manual work | Source, binary dependencies, PTX assumptions | Correct target execution and timing |
| Numerical science | Math libraries or application backend | APIs, precision, conditioning | Residual/error against reference |
| OpenMP/Fortran | Applicable offload toolchain | Compiler, target, libraries, MPI | Proven offload and correct result |
| Larger models across GPUs | TP/PP/layer/expert placement | Runtime layout, per-device peaks, links | Intended placement and scaled correctness |
| Independent parallel jobs | Processes/services per assigned GPU | Scheduling, interference, isolation | Stable throughput under coexistence |
| Multi-node work | RCCL and suitable transport | NIC/RDMA/topology and workload support | Communication and scaling tests |
| Kubernetes | Released AMD operator/device plugin | Driver ownership, scheduler resources | Allocation, health handling, restart |
| VM/partitions | Supported passthrough/SR-IOV/partition path | Exact GPU, firmware, host/guest stack | Correctness, isolation and lifecycle |
| Windows ML | Applicable native artifacts | GPU, Python/framework and component scope | Native execution of required operators |
| Linux workflow on Windows | Applicable WSL artifacts | Host driver, WSL and userspace | WSL smoke and whole application |
| CPU-only preparation | CPU checks/cross-build | Code separation and toolchain | Preparation only; GPU tests pending |

Read [inference](llm-inference.md), [training](training-finetuning.md), [diffusion/video](diffusion-video.md), [HPC](hpc-libraries.md), or [orchestration](kubernetes-virtualization.md). Do not install every candidate.

## Recognize boundaries

**NVIDIA binaries:** CUDA kernels, CUDA providers and proprietary vendor libraries need a compatible AMD implementation or source port. Installing ROCm does not supply those implementations. Evaluate translation projects as distinct experimental routes; never promise universal CUDA emulation. See [HIPIFY's source-level scope](https://rocm.docs.amd.com/projects/HIPIFY/en/latest/index.html).

**Memory:** A workload fitting one 160 GiB logical device may not fit four 40 GiB devices. Placement can replicate weights, KV heads and temporary buffers. See [capacity](memory-capacity.md).

**Quantization:** INT4, FP8, GGUF and quantization algorithm names describe different layers. Require a loader and compute backend for the precise format, shape and target. See [quantization](quantization-attention.md).

**OS parity:** A Windows PyTorch build does not establish support for a Linux server, profiler or RDMA path. A new WSL preview can coexist with a separately validated older route. See [Windows/WSL](windows-wsl.md).

**APUs and NPUs:** Shared-memory capacity, bandwidth, firmware allocation and kernel support are independent considerations. ROCm GPU detection does not establish NPU execution.

## Turn the answer into a decision

1. State whether this workflow has a documented route for this machine.
2. Name the narrowest blocking dependency or unknown.
3. Propose the smallest useful change: environment, backend, representation, sharding or hardware.
4. Give a test that settles the uncertainty.

For a working diffusion graph with a failing CUDA extension, isolate the custom node. Validate a maintained alternative and compare output/runtime. That symptom alone does not justify replacing the driver.

For a purchase, shortlist by workload rather than TFLOPS or capacity alone. Require a software route, usable per-device memory, bandwidth/interconnect, cooling/power and realistic maintenance. Check current prices after capability gates. A cheap accelerator requiring unavailable firmware, cooling or operators can have poor practical value.
