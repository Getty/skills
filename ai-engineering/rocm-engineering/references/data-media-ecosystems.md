# Data science, media, storage and adjacent ecosystems

Evidence baseline: 2026-10-30. Use this reference when the task extends beyond neural models or direct HIP kernels. Each ecosystem has its own compatibility and packaging contract.

## Data science and array programming

The [AMD Data Science toolkit](https://rocm.docs.amd.com/projects/datascience/en/docs-26.07/index.html), observed at release 26.07, is a separate collection built on ROCm. Its catalog includes hipDF, hipGRAPH, hipRAFT, hipVS, hipMM, dask-hip, hip-ucxx and rocOpt. Use its [own matrix](https://rocm.docs.amd.com/projects/datascience/en/docs-26.07/about/compatibility-matrix.html) rather than assuming every GPU supported by Core SDK supports each toolkit component.

For a dataframe, graph, vector-search or distributed-data task:

1. Identify the actual operation, input format, data size, precision and correctness contract.
2. Select the maintained component and exact artifact/version for that operation.
3. Check missing APIs, CPU fallbacks, data-transfer cost and interaction with the rest of the pipeline.
4. Run a representative end-to-end case including parse/load, transformations and output materialization.
5. Compare with a tuned CPU baseline at the same quality; a small GPU kernel time is not the pipeline runtime.

Do not assume a CUDA-oriented data science package becomes AMD-compatible because both implement dataframe or array abstractions. A compatible public API can have a different supported subset, memory manager and binary dependency graph.

[CuPy's current installation guide](https://docs.cupy.dev/en/stable/install.html) explicitly labels its ROCm route experimental and contains separate source-build, wheel and limitation notes. Its fetched 14.2 documentation refers to ROCm 7.x and older AMD wheel packaging, so it cannot by itself certify a Core SDK 10.1 environment. Select the actual supported distribution, verify `cupy.show_config()`, run representative operations and inspect CPU/GPU transfer boundaries. Do not install `cupy-cuda*` wheels as an AMD route or copy its historical package list into a new Core SDK setup.

## Other languages and portability layers

| Existing environment | Candidate entry point | What to verify |
| --- | --- | --- |
| Julia arrays/custom kernels | [AMDGPU.jl](https://amdgpu.juliagpu.org/stable/) | Julia/package/compiler/ROCm tuple, library coverage, synchronization and scalar fallback |
| Numba-oriented Python kernels | [ROCm numba-hip](https://github.com/ROCm/numba-hip) | Actual released backend status, Numba/LLVM compatibility and supported APIs |
| C/C++/Fortran scientific application | [HPC and libraries](hpc-libraries.md) | Existing offload/portability framework, compiler and target support |
| Other host language | A maintained binding or a narrow C ABI around HIP/library operations | Ownership, device/stream lifetime, error propagation and binary ABI |

Treat these as discovery routes. For Numba in particular, do not equate an installed generic `numba` package with a working AMD backend or reuse obsolete `numba.roc` instructions without checking the project. For Julia, a `ROCArray` path and custom kernels need their own tests; identical array syntax does not imply identical execution.

With FFI, keep allocation ownership explicit and avoid exposing unstable C++ ABI across language boundaries when a stable wrapper is possible. Never allow a host garbage collector to release a buffer still used asynchronously by the GPU. Confirm device-side compilation separately from the host binding.

## Media decode and preprocessing

ROCm 10.1's [media catalog](https://rocm.docs.amd.com/en/docs-10.1.0/components/media-libs.html) includes rocDecode for video decoding, rocJPEG for JPEG decoding, and RPP for image/computer-vision primitives with applicable HIP/CPU backends. Their existence does not establish every codec/profile/resolution on every GPU.

For a media pipeline, inventory codec, profile, bit depth, chroma subsampling, resolution, frame rate, batch size and output color/layout. Check the chosen library's hardware support and fallback behavior. Decoding, colorspace conversion, resizing, augmentation, inference and encoding are different stages with separate acceleration paths.

Measure throughput and memory across the entire pipeline. A decoder producing device memory is useful only if the next stage can consume it with the correct layout, synchronization and ownership. Validate frame order, timestamps, color range and image quality. Include corrupt/unsupported inputs and backpressure behavior.

Neural video generation spends substantial work in model operations; a hardware codec block does not automatically accelerate denoising. Conversely, training on compressed media can be input-bound even when GPU model kernels are fast. Use phase-level evidence from [diffusion/video](diffusion-video.md) and [profiling](performance-profiling.md) to choose which part to change.

## Storage and direct GPU I/O

[hipFile 0.5.0](https://rocm.docs.amd.com/projects/hipFile/en/docs-10.1.0/) provides the AMD Infinity Storage I/O path. It has explicitly documented [fastpath and fallback backends](https://rocm.docs.amd.com/projects/hipFile/en/docs-10.1.0/reference/hipFile-io-backends.html) and a [system compatibility check](https://rocm.docs.amd.com/projects/hipFile/en/docs-10.1.0/how-to/checking-system-compatibility.html). Successful I/O does not prove the CPU-staging path was bypassed.

Check GPU, kernel/driver, storage device, filesystem, network/RDMA path where relevant, alignment, file/buffer registration and supported I/O mode. Verify the actual selected backend with its documented statistics. Compare checksums and data correctness before interpreting bandwidth.

Use a dedicated disposable dataset for write benchmarks. Include opening/registration, cache effects, block size, concurrency, CPU utilization and end-to-end model/data-loading time. Do not extrapolate local NVMe behavior to NFS, an object store or remote KV-cache service. Adding an I/O library alone does not move an application's cache to a new tier; the application must implement the lifecycle and failure handling.

## Rendering and alternative backends

For Blender or another renderer, inspect the application's exact HIP/graphics backend, features and device requirements. A working ML stack does not establish ray-tracing support, viewport integration or rendering correctness. Use the application's representative scenes and image comparisons.

OpenCL, Vulkan and DirectML are distinct routes. Check installed runtime/driver, application support, extensions, dtype and operator coverage. They may provide a useful alternative when a ROCm path is unavailable, but that does not establish feature or performance parity with HIP. A compatibility/translation layer is another explicitly scoped experiment, not a generic guarantee that CUDA programs run unchanged.

## Distribution and licensing records

When shipping containers or binaries, preserve component versions, source origins, license/notice files and any separately distributed binary terms. AMD's [license inventory](https://rocm.docs.amd.com/en/docs-10.1.0/about/license.html) states that component licenses are separate; the documentation repository's license is not the license for every bundled dependency. Model weights, datasets and third-party extensions add their own distribution conditions. Resolve actual artifact terms instead of describing the whole stack as one license.

Record which libraries are bundled and which the target system supplies. A deployment that works on a build machine can depend accidentally on its driver libraries, global Python environment or local SDK. Verify the final distributable on the intended clean environment and retain a reproducible dependency manifest.
