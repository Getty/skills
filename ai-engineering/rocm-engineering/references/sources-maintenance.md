# Sources, provenance and maintenance

Research baseline: **2026-10-30**. Current AMD production pages observed during authoring identify **ROCm Core SDK 10.1.0**. This is a dated baseline; reevaluate moving claims for the actual task. Individual references carry the narrower component/version scope.

## Contents

- [Choose the source that owns the claim](#choose-the-source-that-owns-the-claim)
- [Use the primary-source registry](#use-the-primary-source-registry)
- [Resolve conflicts and selectors](#resolve-conflicts-and-selectors)
- [Refresh only what changes the decision](#refresh-only-what-changes-the-decision)

## Choose the source that owns the claim

| Claim | Strongest source | Evidence that is insufficient alone |
| --- | --- | --- |
| GPU/OS/driver/SDK qualification | Selected-version AMD matrix and footnotes | A compiler target, product advertisement or successful import |
| Framework/runtime artifact | Owning project's installer/release plus AMD recipe where applicable | Search snippet, guessed wheel URL or similar image tag |
| Operator/quantization support | Engine/library backend matrix, source and tests at the relevant revision | Another engine supporting the same format |
| API behavior | Versioned API docs and implementation | General tutorial or old CUDA analogy |
| Production maturity | Released support documentation | `main`, `develop`, nightly, proposal or open PR |
| Bug/workaround | Applicable release note or reproducible issue with version context | Unscoped forum export line |
| Performance | Reproducible measurements on equivalent workloads | Peak specs or a vendor number with different precision/batch |
| Hardware value | Current configuration/pricing plus qualified workload | Memory or TFLOPS alone |

Treat official engineering blogs as evidence for the setup they actually tested, not a wider compatibility contract. Treat upstream issues as symptom/reproduction evidence, not proof that a proposed fix landed in a particular release.

## Use the primary-source registry

The following entry points and the more specific sources linked throughout the references were used to construct this skill. Live `latest` pages can change; capture the observed page version/date when using them. Repository branches are development sources unless pinned to a release.

### Platform, hardware and distribution

| Source | Purpose |
| --- | --- |
| [ROCm release notes](https://rocm.docs.amd.com/en/latest/about/release-notes.html) | Release features, known/resolved issues, component boundaries |
| [Compatibility selector](https://rocm.docs.amd.com/en/latest/compatibility/compatibility-matrix.html) | Exact family/SKU/platform qualification |
| [TheRock transition](https://rocm.docs.amd.com/en/docs-10.1.0/about/transition-guide-TheRock.html) | Legacy/Core SDK package and path changes |
| [ROCm installation](https://rocm.docs.amd.com/en/latest/install/rocm.html) | Selected hardware/platform installation branches |
| [Driver compatibility](https://instinct.docs.amd.com/projects/amdgpu-docs/en/latest/compatibility/compatibility-matrix.html) | Independent kernel-driver lifecycle |
| [GPU specifications](https://rocm.docs.amd.com/en/latest/reference/gpu-specs.html) | Product/architecture identification, not complete workload support |
| [RDNA3.5 optimization](https://rocm.docs.amd.com/en/latest/reference/system-optimization/rdna3-5.html) | Shared-memory APU system considerations |
| [TheRock](https://github.com/ROCm/TheRock) | Build/release tooling, pinned-source workflows |
| [TheRock supported GPUs](https://github.com/ROCm/TheRock/blob/main/SUPPORTED_GPUS.md) | Build/artifact coverage distinct from production qualification |
| [Windows development status](https://github.com/ROCm/TheRock/blob/main/docs/development/windows_support.md) | Component-level Windows build scope |
| [Microsoft WSL commands](https://learn.microsoft.com/en-us/windows/wsl/basic-commands) | Host-side WSL inventory and lifecycle |
| [Ryzen AI](https://ryzenai.docs.amd.com/en/latest/) | Separate NPU stack routing |

### Frameworks, inference and creative workloads

| Source | Purpose |
| --- | --- |
| [AMD PyTorch installation](https://rocm.docs.amd.com/projects/ai-ecosystem/en/latest/frameworks/pytorch/install.html) | Published architecture-specific framework artifacts |
| [PyTorch HIP semantics](https://docs.pytorch.org/docs/2.14/notes/hip.html) | CUDA-named APIs on HIP, allocator/backend behavior |
| [JAX installation](https://docs.jax.dev/en/latest/installation.html) | PJRT/plugin and platform installation contracts |
| [AMD TensorFlow route](https://rocm.docs.amd.com/projects/ai-ecosystem/en/latest/frameworks/tensorflow/install.html) | Current AMD build scope |
| [ONNX Runtime ROCm provider](https://onnxruntime.ai/docs/execution-providers/ROCm-ExecutionProvider.html) | Historical provider removal boundary |
| [AMD ONNX Runtime](https://rocm.docs.amd.com/projects/ai-ecosystem/en/latest/inference/onnxruntime.html) | Current MIGraphX plugin packaging/registration |
| [vLLM GPU installation](https://docs.vllm.ai/en/latest/getting_started/installation/gpu/) | Upstream AMD runtime requirements |
| [AMD vLLM recipe](https://rocm.docs.amd.com/projects/ai-ecosystem/en/latest/inference/vllm.html) | AMD published artifact tuple |
| [vLLM quantization](https://docs.vllm.ai/en/latest/features/quantization/) | Engine-specific hardware/backend coverage |
| [SGLang AMD](https://docs.sglang.io/docs/hardware-platforms/amd_gpu) | Upstream AMD features and kernels |
| [AMD SGLang recipe](https://rocm.docs.amd.com/projects/ai-ecosystem/en/latest/inference/sglang.html) | Validated recipe and artifact-version scope |
| [llama.cpp build](https://github.com/ggml-org/llama.cpp/blob/master/docs/build.md) | HIP/Vulkan build routes and switches |
| [Ollama GPU support](https://docs.ollama.com/gpu) | Application-level device/backend coverage |
| [bitsandbytes installation](https://huggingface.co/docs/bitsandbytes/installation) | Current library build/target scope; not every engine's integration |
| [PEFT quantization](https://huggingface.co/docs/peft/developer_guides/quantization) | Adapter-training integration constraints |
| [AITER](https://github.com/ROCm/aiter) | AMD kernel integration and architecture requirements |
| [FlashAttention](https://github.com/Dao-AILab/flash-attention) | Backend-specific implementation scope |
| [AMD ComfyUI](https://rocm.docs.amd.com/projects/ai-ecosystem/en/latest/inference/comfy.html) | Current AMD creative workflow |
| [ComfyUI upstream](https://github.com/Comfy-Org/ComfyUI/blob/master/README.md) | Application setup and current backend paths |
| [Diffusers memory](https://huggingface.co/docs/diffusers/optimization/memory) | Offload/tiling implications |
| [AMD xDiT](https://rocm.docs.amd.com/projects/ai-ecosystem/en/latest/inference/xdit.html) | Explicitly scoped distributed diffusion recipe |

### Development, profiling and operations

| Source | Purpose |
| --- | --- |
| [HIP](https://rocm.docs.amd.com/projects/HIP/en/latest/index.html) | Runtime, language, errors, streams and memory |
| [HIPIFY](https://rocm.docs.amd.com/projects/HIPIFY/en/latest/index.html) | Translation coverage and limitations |
| [Clang HIP](https://clang.llvm.org/docs/HIPSupport.html) | Compiler targets/linking; inspect released compiler applicability |
| [CMake HIP architectures](https://cmake.org/cmake/help/latest/variable/CMAKE_HIP_ARCHITECTURES.html) | Native CMake target configuration |
| [ROCm controls](https://rocm.docs.amd.com/en/docs-10.1.0/reference/environment-variables/index.html) | Versioned environment behavior |
| [HPC SDK](https://rocm.docs.amd.com/en/docs-10.1.0/components/hpc-sdk/index.html) | Scientific library distribution boundaries |
| [RCCL](https://rocm.docs.amd.com/projects/rccl/en/latest/index.html) | Collectives and current repository location |
| [Open MPI ROCm](https://docs.open-mpi.org/en/v5.0.x/tuning-apps/networking/rocm.html) | MPI transport build/runtime scope |
| [rocprofv3](https://rocm.docs.amd.com/projects/rocprofiler-sdk/en/docs-10.1.0/how-to/using-rocprofv3.html) | Tracing commands and options |
| [Compute Profiler](https://rocm.docs.amd.com/projects/rocprofiler-compute/en/latest/quick-reference/rocprofiler-compute-at-a-glance.html) | Kernel analysis and replay implications |
| [AMD SMI WSL](https://rocm.docs.amd.com/projects/amdsmi/en/docs-10.1.0/how-to/amdsmi-wsl-mode.html) | Experimental opt-in management scope |
| [GPU Operator](https://instinct.docs.amd.com/projects/gpu-operator/en/latest/) | Released operator configuration, DRA/device plugin and partitioning |
| [CDI](https://instinct.docs.amd.com/projects/container-toolkit/en/latest/container-runtime/cdi-guide.html) | Device injection and runtime configuration |
| [Slurm GRES](https://slurm.schedmd.com/gres.conf.html) | Scheduler GPU autodetection/accounting dependencies |

### Data, media and redistribution

| Source | Purpose |
| --- | --- |
| [AMD Data Science 26.07](https://rocm.docs.amd.com/projects/datascience/en/docs-26.07/index.html) | Separate toolkit and its compatibility matrix |
| [CuPy installation](https://docs.cupy.dev/en/stable/install.html) | Experimental AMD route and packaging limitations |
| [AMDGPU.jl](https://amdgpu.juliagpu.org/stable/) | Julia array/kernel/library integration |
| [numba-hip](https://github.com/ROCm/numba-hip) | Current AMD Numba backend project, not a blanket maturity claim |
| [Media components](https://rocm.docs.amd.com/en/docs-10.1.0/components/media-libs.html) | rocDecode, rocJPEG and RPP scope |
| [hipFile](https://rocm.docs.amd.com/projects/hipFile/en/docs-10.1.0/) | Direct GPU I/O, backend checks and fallbacks |
| [Component licenses](https://rocm.docs.amd.com/en/docs-10.1.0/about/license.html) | Per-component license/notice discovery |

## Resolve conflicts and selectors

AMD's current pages use multiple selectors. Extracted text may include hidden branches for several GPUs, OSes and versions. Do not join the first OS list to the next GPU list and call it a row. Resolve the selector state through an accessible official table/artifact or a documented source representation; if it cannot be determined, report the combination unverified.

Read the page itself instead of relying on cached search snippets. Check redirects, banners and version selectors. A `develop` page can carry an upcoming version number; a project's `latest` documentation can point to a release candidate. The umbrella SDK and component versions also need not match.

When a matrix, installer and upstream release differ, preserve separate scopes. Select an artifact that actually exists and is documented for the task. Never synthesize a Docker tag from newer version numbers, assume the latest upstream Torch is the version used by an AMD server image, or use an old wheel URL because it appears in a popular tutorial.

## Refresh only what changes the decision

Recheck before a new deployment, a support-sensitive recommendation, a driver/framework upgrade, a platform transition or a proposed workaround. Prioritize the exact GPU/OS tuple, artifact provenance, required kernels and relevant known issues; do not reread unrelated libraries for a narrow task.

Maintain a claim record containing the claim, source URL, page/release version, access date, relevant selector/footnote, applicability and local test status. Use [the stack record](../assets/stack-record.yaml). If offline, distinguish dated verified evidence from present uncertainty and avoid claiming a current latest version.

Update one authoritative reference for each topic, then adjust routing or examples that depend on it. Validate local links, code syntax, helper behavior and a representative task after substantive changes. Preserve generic/public examples; do not incorporate a particular user's hostnames, addresses or private configuration into this reusable skill.
