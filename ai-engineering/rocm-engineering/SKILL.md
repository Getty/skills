---
name: rocm-engineering
description: "Use when running, building or debugging GPU workloads on AMD hardware with ROCm — Instinct, Radeon or Ryzen APU graphics on Linux, Windows or WSL; amdgpu, TheRock, rocminfo, amd-smi, HIP, HIPIFY, porting CUDA code, PyTorch, JAX, ONNX, vLLM, SGLang, llama.cpp, Ollama, ComfyUI, training, quantization, Triton/AITER, RCCL, Kubernetes, HSA_OVERRIDE_GFX_VERSION; choosing an AMD GPU, checking whether a GPU/OS/driver/framework combination is supported, or when a ROCm install, kernel or multi-GPU job fails or runs slow."
metadata:
  researched: "2026-10-30"
---

# AMD ROCm Engineering

Build a reproducible GPU workflow with a stated support boundary, numerical checks, measured performance, and a recovery path. Answer capability questions directly; for execution requests, continue from discovery through the verification that the available machine permits.

## Start with the workload and exact stack

1. Identify the task: assess feasibility, choose hardware, install, run an application, develop kernels, port CUDA, improve performance, or recover a failed deployment.
2. Reuse known context. Obtain only missing facts that affect the decision: exact GPU SKU and count, runtime `gfx` target, per-device memory, native Linux/Windows/WSL/VM/container, OS and kernel, driver, ROCm distribution and version, framework and Python ABI, model or application revision, dtype, workload sizes, topology, service objective and downtime constraints.
3. Run [the inventory helper](scripts/rocm_inventory.py) for available local metadata. Treat missing tools and incomplete virtualized visibility as unknowns. It never decides official support. Read [compatibility](references/compatibility.md) before choosing a release or proposing a purchase.
4. Load only the relevant references below. Treat commands with placeholders as templates until values have been verified.
5. Record proposed and observed combinations separately using [the stack record](assets/stack-record.yaml). Do not silently replace a working stack with the newest release.

## Apply the support test

Determine the intersection of **hardware + OS/kernel + driver/firmware + SDK/artifact + framework/runtime + required operator/backend**. A GPU listed in one matrix is not proof that every framework or datatype works on that GPU.

For each material claim, report one of:

- **Vendor validated:** an applicable AMD matrix/recipe explicitly lists the combination and scope.
- **Upstream supported:** the owning project documents the combination; AMD validation may be narrower.
- **Preview:** the source explicitly labels the relevant artifact or feature preliminary.
- **Community/experimental:** a reproducible route exists without the relevant support commitment.
- **Unsupported in this scope:** an explicit restriction or a required incompatible dependency blocks this route.
- **Unverified:** the available evidence cannot settle the exact combination.

Record runtime verification independently: not run, enumeration passed, primitive passed, application passed, or workload-qualified. Successful execution does not change the vendor-support label. A missing matrix row usually means **not validated/unverified**, not a proof of technical impossibility.

Check current primary sources whenever the answer depends on releases, supported SKUs, installation commands, packaging, quantization kernels, OS parity, partitioning or prices. Use [sources and maintenance](references/sources-maintenance.md). Inspect page version, release status and footnotes; resolve conflicts by scope instead of combining unrelated rows.

The researched baseline is **2026-10-30**, when AMD's current production documentation identifies **ROCm Core SDK 10.1.0**. TheRock packaging and legacy ROCm packaging differ. Preserve this as dated context, not a perpetual latest-version assertion. See [release notes](https://rocm.docs.amd.com/en/latest/about/release-notes.html) and [the transition guide](https://rocm.docs.amd.com/en/latest/about/transition-guide-TheRock.html).

## Work through the smallest complete path

1. **Select a route.** Prefer an applicable published recipe and a pinned environment. Use a fresh virtual environment, dedicated container, or separate SDK prefix where that isolates change. For a source build, establish why released artifacts are insufficient.
2. **Inspect before altering.** Determine which layer owns the failure. Resolve host driver/device access before reinstalling Python; resolve framework/backend mismatch before changing firmware.
3. **Establish correctness in stages.** Check device visibility, kernel execution, representative library operations, the application's critical path, then scale. A package import or enumeration command alone is insufficient.
4. **Measure a baseline.** Record warmup, first-use compilation, workload shape, numerical tolerance, latency distribution, throughput, per-device peak memory and power/thermal state as applicable.
5. **Change one cause at a time.** State the hypothesis, expected observation, cost and rollback. Retest the affected correctness and performance gates.
6. **Finish the requested work.** Preserve exact commands/configuration and observed outputs. If no AMD GPU or relevant OS is available, provide checked preparation and explicitly leave hardware qualification unperformed.

For disruptive driver, firmware, partition or shared-service actions, respect the user's existing authorization and scheduling constraints. Prepare a concrete change and recovery plan before seeking genuinely missing permission. Do not add approval steps to routine read-only discovery or already authorized work.

## Keep these invariants

- Treat `torch.cuda` as PyTorch's normal GPU API on HIP builds; verify `torch.version.hip`. Do not rename device strings to `rocm` or `hip`.
- Do not infer CUDA binary compatibility from HIP source/API similarity. Audit extensions, PTX, binary wheels, attention and quantization backends individually.
- Distinguish Instinct, Radeon, integrated Radeon graphics, and the Ryzen NPU. CPU/platform branding is not a GPU support entry.
- Separate native Windows from WSL and Linux. Use the applicable matrix and artifact route; historical Linux-only claims and blanket feature parity are unreliable.
- Budget memory per logical device. Cards, dies, partitions and host RAM do not automatically form one fast allocation space. Verify the application's sharding/placement mechanism.
- Treat datatype storage, hardware arithmetic, kernel availability and model quality as separate checks.
- Use environment masks for device selection; they do not provide adversarial tenant isolation or guaranteed quotas.
- Do not install kernel drivers inside ordinary containers or use `--privileged`, world-writable devices, global ABI symlinks, ISA overrides, or disabled security features as generic fixes.
- Use `HSA_OVERRIDE_GFX_VERSION` only as an evidenced experiment, with a fresh process and numerical verification. It does not create vendor support or hardware features.
- Do not add every tuning variable from a forum post. Remove diagnostic serialization before timing. Treat compiler/kernel caches as versioned artifacts.
- Read release-specific known issues before qualification, including correctness failures. “No crash” does not establish correct computation.
- Avoid fabricated benchmarks, invented package URLs, guessed image tags, assumed CUDA kernel replacements, and fit promises based only on weight size.

## Reference map

### Platform and planning

| Need | Read |
| --- | --- |
| ROCm layers, naming and adjacent stacks | [Architecture and ecosystem](references/architecture-ecosystem.md) |
| Workload possibilities and blocking dependencies | [Capability map](references/capability-map.md) |
| Exact support, releases and documentation scope | [Compatibility](references/compatibility.md) |
| Instinct, Radeon, APU, PCIe and memory hardware | [Hardware](references/hardware.md) |
| Weights, KV cache, training and per-device capacity | [Memory and capacity](references/memory-capacity.md) |
| Native Linux installation and host readiness | [Linux installation](references/linux-installation.md) |
| Native Windows, WSL and distinct artifacts | [Windows and WSL](references/windows-wsl.md) |
| Docker/Podman and userspace dependencies | [Containers](references/containers.md) |
| Pin, migrate, upgrade, roll back and reproduce | [Upgrades and reproducibility](references/upgrades-reproducibility.md) |

### AI applications

| Need | Read |
| --- | --- |
| Builds, semantics, compile and custom extensions | [PyTorch](references/pytorch.md) |
| JAX, TensorFlow, ONNX and backend alternatives | [Framework interoperability](references/frameworks-interop.md) |
| vLLM, SGLang, llama.cpp, Ollama and serving | [LLM inference](references/llm-inference.md) |
| Full training, LoRA/QLoRA, optimizer state and distribution | [Training and fine-tuning](references/training-finetuning.md) |
| ComfyUI, Diffusers, image/video pipelines and nodes | [Diffusion and video](references/diffusion-video.md) |
| Dtypes, SDPA, FlashAttention, Triton, CK and AITER | [Quantization and attention](references/quantization-attention.md) |

### Development and operation

| Need | Read |
| --- | --- |
| HIP kernels, memory/streams and numerics | [HIP programming](references/hip-programming.md) |
| Port a CUDA application or extension | [CUDA migration](references/cuda-migration.md) |
| CMake, targets, ABI/linking and TheRock source builds | [Build toolchains](references/build-toolchains.md) |
| Scientific computing, OpenMP and Fortran | [HPC and libraries](references/hpc-libraries.md) |
| Data science, CuPy/Julia, media decode, direct GPU I/O and redistribution | [Data, media and adjacent ecosystems](references/data-media-ecosystems.md) |
| RCCL, P2P, xGMI, NUMA, RDMA and topology | [Multi-GPU and networking](references/multi-gpu-networking.md) |
| Kernel and end-to-end latency/throughput | [Performance and profiling](references/performance-profiling.md) |
| Selection, debugging and runtime controls | [Environment controls](references/environment-controls.md) |
| Operator, device plugins, scheduling and partitioning | [Kubernetes and virtualization](references/kubernetes-virtualization.md) |
| Health, RAS, thermals, services and incidents | [Operations and monitoring](references/operations-monitoring.md) |
| Diagnose errors through an evidence ladder | [Troubleshooting](references/troubleshooting.md) |
| Qualify a release, migration or deployment | [Validation workflows](references/validation-workflows.md) |
| Refresh moving claims and choose primary evidence | [Sources and maintenance](references/sources-maintenance.md) |

## Reusable checks and records

Run helpers from this skill directory or use absolute paths. They do not install software or upload data.

| Resource | Contract |
| --- | --- |
| [rocm_inventory.py](scripts/rocm_inventory.py) | Passive metadata by default; optional bounded utility probes; no support verdict or raw logs |
| [torch_smoke.py](scripts/torch_smoke.py) | Requires HIP PyTorch/GPU; matrix/CPU comparison, FP32 autograd, optional SDPA; worker timeout |
| [distributed_smoke.py](scripts/distributed_smoke.py) | Allocated GPUs and `torchrun`; RCCL-backed all-reduce versus exact sums; process-group timeout |
| [memory_budget.py](scripts/memory_budget.py) | Explicit weights/KV and independent shard counts; estimate only |
| [HIP program](assets/hip-smoke/hip-smoke.hip) and [CMake project](assets/hip-smoke/CMakeLists.txt) | Original small kernel, host reference, API error checks; build for the observed target |
| [Stack record](assets/stack-record.yaml) | Hardware, versions, evidence, support and validation as separate fields |
| [Benchmark record](assets/benchmark-record.json) | Comparable workload, quality, environment and performance observations |

Example local checks:

```bash
python3 scripts/rocm_inventory.py
python3 scripts/rocm_inventory.py --probe-runtime --timeout 15
python3 scripts/torch_smoke.py --device 0 --dtype float32 --sdpa
```

Read the relevant reference before GPU work, distributed jobs or a source build. Test required dtypes/operators separately; a tiny smoke cannot certify production behavior.

## Deliver an actionable result

Lead with feasibility for this exact stack. Include the implemented or proposed route, cited support evidence, commands/configuration, checks actually executed, remaining uncertainty and rollback where applicable. For purchases, compare usable capacity, required kernels, topology, cooling/power and ownership effort. For performance claims, use a recorded workload and quality threshold.

Keep public examples generic. Omit personal hostnames, credentials, internal addresses, proprietary prompts and unsanitized dumps from reusable documentation. Use other installed domain skills when they add depth; this skill remains usable without them.
