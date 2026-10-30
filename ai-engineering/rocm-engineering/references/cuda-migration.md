# CUDA migration and dependency audits

Evidence baseline: 2026-10-30. Treat portability as a set of source, binary, library, numerical and deployment decisions.

## Contents

- [Audit before translating](#audit-before-translating)
- [Map dependencies](#map-dependencies)
- [Use HIPIFY as one migration stage](#use-hipify-as-one-migration-stage)
- [Handle Python and compiled extensions](#handle-python-and-compiled-extensions)
- [Prove the port](#prove-the-port)

## Audit before translating

Start from a known working application and test corpus. Record the intended AMD hardware/OS and the application's numerical and performance contract. Classify each dependency as maintained AMD backend, source-portable, manually replaceable, vendor-binary-only, or unresolved.

Search the actual source tree with `rg`, excluding generated/vendor directories as appropriate:

```bash
rg -n 'cuda|cuDNN|cudnn|cublas|nccl|TensorRT|tensorrt|nvcc|NVRTC' src CMakeLists.txt pyproject.toml
rg -n '__CUDA_ARCH__|warpSize|__shfl|__ballot|asm\b|\.ptx|\.cubin|\.fatbin' src
rg -n 'CUDAExtension|CUDA_HOME|TORCH_CUDA_ARCH_LIST|sm_[0-9]+|compute_[0-9]+' . \
  -g '!build/**' -g '!vendor/**' -g '!third_party/**'
```

Adjust paths to the project; missing paths are not evidence of absence. Inspect dependency lock files and release-wheel contents too. A Python package with no CUDA source may depend on a binary that contains it.

Write a porting table: dependency/call site, required feature, candidate AMD route, source evidence, conversion effort, test and unresolved blocker. Do not estimate the whole project from the percentage of names HIPIFY can rewrite.

## Map dependencies

| Existing dependency | Candidate AMD route | Boundary to inspect |
| --- | --- | --- |
| CUDA runtime/kernel code | HIP runtime and compiler | API coverage, launch/memory/stream behavior |
| cuBLAS/cuBLASLt | hipBLAS/hipBLASLt or rocBLAS | Algorithms, epilogues, layouts, accumulation and workspace |
| cuFFT/cuRAND/cuSOLVER/cuSPARSE | Matching HIP/ROC libraries | Exact API and data/precision coverage |
| CUB/Thrust | hipCUB/rocPRIM/rocThrust | Templates, backend configuration and performance |
| cuDNN operations | Framework ROCm implementation, MIOpen or applicable DNN interface | No assumed binary/API equivalence |
| NCCL integration | RCCL behind compatible APIs where supported | Version, transport, stream and topology behavior |
| TensorRT engine/plugin | Rebuild using a supported inference backend | Serialized engines and plugins are not portable model files |
| CUDA-specific FlashAttention/quantization | Supported AMD kernel/backend | Operator version, GPU, shape, dtype and model integration |
| Inline PTX or architecture intrinsics | New portable algorithm or AMD-specific implementation | Semantics, subgroup width, memory model |
| CUDA-only binary wheel | Maintained ROCm wheel or source build | ABI, target code objects and licensing/access to source |

Use [HIPIFY's API coverage](https://rocm.docs.amd.com/projects/HIPIFY/en/latest/index.html) and the relevant library's own documentation. Similar library names do not promise complete parity. Some projects maintain their own portability layer; use it before introducing a second one.

## Use HIPIFY as one migration stage

Prefer an isolated branch/worktree and inspect the generated diff. `hipify-clang` performs syntax-aware translation and needs the appropriate parse/include context; `hipify-perl` uses replacement rules and can work with less setup. For PyTorch-related code, inspect the project's existing HIP transformation before invoking a general tool. See [HIPIFY](https://rocm.docs.amd.com/projects/HIPIFY/en/latest/index.html) and [HIP porting](https://rocm.docs.amd.com/projects/HIP/en/latest/how-to/hip_porting_guide.html).

First run the installed tool's help and examination mode where available. Translate a small vertical slice: allocation, one kernel, result verification, build integration. Review macros, nested headers, conditional compilation and generated source. Keep a portable host interface so unsupported kernels can fall back or fail clearly.

Do not globally replace `cuda` with `hip`. Names can be part of a framework API, user configuration, serialized data, or a backend-independent interface. Do not translate PTX text as though it were C++ source. Treat proprietary libraries without an AMD implementation as architectural blockers requiring a different route.

Audit semantic traps:

- Hardcoded warp/lane masks, subgroup reductions and divergence assumptions.
- Undefined cross-thread ordering, atomics and cache-coherence assumptions hidden by one device.
- Default-stream semantics, event lifetime and asynchronous host-buffer reuse.
- Layout/stride, alignment, indexing width and address-space assumptions.
- Texture/surface, cooperative launch, IPC, graph and memory-management feature coverage.
- Host/compiler ABI, C++ standard library, link flags, RDC and symbol visibility.

Use [build toolchains](build-toolchains.md) for target and linker issues and [HIP programming](hip-programming.md) for runtime contracts.

## Handle Python and compiled extensions

On HIP PyTorch, `torch.cuda` and `device='cuda'` are expected API names. Branch on `torch.version.hip` when backend-specific behavior is necessary. Do not use the existence of `torch.cuda` or its availability alone to identify NVIDIA. See [PyTorch HIP semantics](https://docs.pytorch.org/docs/2.14/notes/hip.html).

Rebuild extensions against the exact installed framework and compatible compiler. Check whether its build scripts support HIP automatically or require project-specific configuration. `TORCH_CUDA_ARCH_LIST` is not a generic AMD target switch. Use the actual build system's documented AMD target mechanism, such as `PYTORCH_ROCM_ARCH` where applicable, and inspect the build log/code objects.

Keep CPU-only and ROCm/CUDA wheels out of the same environment unless the project explicitly supports that arrangement. A stale cached extension can mask a corrected source change. Rebuild only the affected cache after recording its provenance; do not delete unrelated environments.

## Prove the port

1. Verify compiler/runtime/device access with the bundled HIP check.
2. Test each migrated operator against a trusted reference over the application's shapes and dtypes.
3. Test the assembled application, including saved-model loading, preprocessing, postprocessing and errors.
4. For training, verify gradients, a meaningful parameter update, checkpointing and resumed execution.
5. Test multi-GPU communication separately before interpreting application scaling.
6. Compare performance with equivalent precision, quality, input lengths and concurrency. Include host overhead and transfers.

Publish the supported subset and remaining blockers. “Compiles” means code generation/linking succeeded; “runs” means execution completed; “correct” means it met an explicit numerical contract; “qualified” includes the real workload and operating conditions. Preserve these distinctions in the handoff.
