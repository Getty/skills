# Architecture and ecosystem

Evidence baseline: 2026-10-30. Use this map to find the responsible layer; use the exact release matrix to establish support.

## Read the stack from the application downward

| Layer | Responsibility | Evidence to collect | Typical failure boundary |
| --- | --- | --- | --- |
| Model/application | Graph, shapes, custom operators, workflow, scheduler | Revision, model format, dtype, flags, input | Unsupported operator, placement, excessive context |
| Framework/runtime | Dispatch, compiler, allocator, serving | Wheel/image provenance, backend, Python ABI, plugins | CPU/CUDA artifact, extension mismatch |
| Compute libraries | GEMM, convolution, attention, collectives, FFT/sparse | Dispatched kernel and component version | Missing target, shape/dtype, numerical regression |
| Language/runtime | HIP APIs, launches, streams, memory | HIP version, code objects, return codes | Invalid device function, launch error, allocation fault |
| OS-facing runtime | Queues, memory, discovery | Applicable ROCr/Windows/WSL path and access | Device hidden, permissions, runtime/driver mismatch |
| Driver/firmware | Initialization, scheduling, mappings, recovery | Loaded driver, kernel, firmware, boot logs | Initialization failure, reset, device fault |
| Hardware | Compute, memory, links, cooling, power | Exact SKU, logical devices, topology, thermals | Capacity, throttling, PCIe, hardware fault |

This is a diagnostic model, not a claim that every OS implements every layer identically. Start at the first boundary that fails. Reinstalling everything destroys evidence and changes several variables at once.

ROCm includes compilers, runtimes and libraries; HIP is one interface within it. Applications may consume ROCm through PyTorch without containing HIP source. Current documentation separates Core SDK, AI integration, HPC and infrastructure guidance. See [AMD's overview](https://rocm.docs.amd.com/en/latest/about/what-is-rocm.html).

## Distinguish similar names

| Name | Identifies | Does not establish |
| --- | --- | --- |
| ROCm release | Coordinated SDK/artifact context | Identical version numbers for every component |
| HIP | C++ API, kernel language and runtime | Execution of arbitrary NVIDIA binaries |
| ROCr/HSA | Lower-level runtime concepts on applicable paths | A need to write HSA for ordinary ML work |
| amdgpu/KFD | Linux kernel/display/compute components | Python wheel or userspace version |
| TheRock | Build/release system and artifact organization | Production status of every development artifact |
| `gfx` target | Compiler/runtime ISA identity | Exact SKU, capacity or support commitment |
| CDNA/RDNA | Architecture families | Uniform performance or library coverage |
| Instinct/Radeon/PRO | Product families | One firmware, virtualization or support contract |
| Ryzen AI | CPU/GPU/NPU platform branding | ROCm execution on its NPU |

HIP APIs resemble CUDA, but compilation targets an ISA and runtime. Read [HIP](https://rocm.docs.amd.com/projects/HIP/en/latest/index.html) and [HIPIFY](https://rocm.docs.amd.com/projects/HIPIFY/en/latest/index.html) before estimating portability.

## Map components to work

Use rocBLAS/hipBLAS/hipBLASLt for dense algebra; rocFFT/hipFFT for FFT; rocSPARSE/hipSPARSE for sparse work; rocSOLVER/hipSOLVER for solvers; rocRAND/hipRAND for RNG; and rocPRIM/hipCUB/rocThrust for parallel primitives. MIOpen and framework-dispatched kernels handle neural operations. RCCL provides collectives; rocSHMEM addresses a different communication model. Treat this as navigation, not API equivalence. Follow the [component catalog](https://rocm.docs.amd.com/en/latest/about/what-is-rocm.html) to the selected API.

Identify what the application actually loads. It can combine libraries, generated kernels and CPU work. Changing a BLAS setting cannot fix an attention kernel; a fast GEMM cannot predict token-generation throughput.

Separate inventory, telemetry, tracing and kernel analysis. `rocminfo` enumerates agents; AMD SMI observes/manages supported hardware; ROCprofiler tools attribute execution. See [profiling](performance-profiling.md) for release-specific tools rather than assuming historical utilities still ship.

## Identify adjacent stacks

An AMD application may use Vulkan compute, DirectML, OpenCL or graphics APIs instead of ROCm. Evaluate each as a distinct backend with its own device/precision support. Its success is not proof that ROCm works on the same host.

For Ryzen NPU work, identify the Ryzen AI software and provider. For rendering, inspect the renderer's HIP/Vulkan/DirectX backend. For codecs, inspect media APIs separately from neural video generation. A video decoder block does not inherently accelerate a diffusion denoiser. Read [framework alternatives](frameworks-interop.md), [HPC libraries](hpc-libraries.md) and [data/media ecosystems](data-media-ecosystems.md).

## Explain results at the right layer

Prefer: “The driver exposes the GPU, HIP executes correctly and PyTorch FP16 works; this quantized serving path lacks the selected engine's required kernel.” State the exact functioning and blocked parts.

Avoid “AMD works,” “ROCm is broken,” or “CUDA-only” without identifying the dependency. Record whether a remedy changes hardware, environment, library, representation or application. Retest that boundary and its consuming workload.

Across distribution changes, use [the transition guide](https://rocm.docs.amd.com/en/latest/about/transition-guide-TheRock.html) and [upgrades](upgrades-reproducibility.md). A pinned container with a new host driver is still a changed combination.
