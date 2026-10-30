# Compatibility decisions and support evidence

Evidence baseline: checked 2026-10-30. AMD's current production documentation identifies ROCm Core SDK 10.1.0. Treat every version below as a dated observation and refresh the relevant source before selecting a new installation. This file defines an engineering decision process; it is not a replacement support matrix.

## Contents

- [Build the compatibility tuple](#build-the-compatibility-tuple)
- [Assign an evidence status](#assign-an-evidence-status)
- [Read the right matrix](#read-the-right-matrix)
- [Decide what is actually possible](#decide-what-is-actually-possible)
- [Handle unsupported configurations](#handle-unsupported-configurations)
- [Report a useful verdict](#report-a-useful-verdict)

## Build the compatibility tuple

Record these fields before proposing installation commands, purchase advice, an upgrade, or an explanation of a failure:

| Layer | Required evidence | Why it changes the answer |
| --- | --- | --- |
| Device | Exact commercial SKU, PCI device ID, observed `gfx` target, GPU count | A family name or a similar ISA does not establish SKU qualification. |
| Memory and topology | Memory per logical device, partitions, interconnect, PCIe layout | Determines whether the actual allocation or parallel strategy fits. |
| Execution environment | Native Linux, native Windows, WSL2, VM, container | These have different driver and tooling paths. |
| Host | Distribution and point release, running kernel, CPU architecture | A distribution's marketing name alone is insufficient. |
| Driver and firmware | Running module or Windows driver version; firmware where required | Installed packages need not equal the driver currently loaded. |
| ROCm | Release stream, precise runtime and compiler versions, install source | Legacy packages, Core SDK, nightly artifacts and distro packages are distinct. |
| Framework | Version, wheel or container origin, Python ABI, architecture coverage | A working HIP runtime does not ensure a usable framework build. |
| Workload | Model or application revision, operators, precision, extensions, parallelism | Support can fail at a single kernel or dependency. |
| Service objective | Correctness tolerance, throughput, latency, uptime, recovery needs | A successful demo may not satisfy the intended use. |

Leave absent fields explicitly unknown. For a broad overview, explain the alternatives without blocking on a questionnaire. For a concrete deployment, resolve the fields that can change the proposed commands.

## Assign an evidence status

Use a separate status for the platform, framework and required feature. Do not compress all three into one unsupported/supported Boolean.

| Status | Minimum evidence | Permitted conclusion |
| --- | --- | --- |
| AMD-qualified | Exact relevant row or release note, including footnotes | AMD documents this combination within the stated scope. |
| Upstream-supported | Framework/runtime upstream documents this backend and target | That project supports the path; AMD qualification still needs a separate check. |
| Locally validated | Reproducible test record on the exact tuple | These specific tests passed on this system. |
| Preview / experimental | Explicit preview label or development-only implementation | Evaluate in isolation with a fallback and expected maintenance. |
| Community-enabled | Reproducible community build or workaround, without official qualification | May be useful, but support and repeatability must be established locally. |
| Unknown | Missing or contradictory evidence | Investigate the missing layer; do not infer impossibility. |
| Known limitation | Specific documented exclusion or reproduced failure | State exactly which feature, build and environment are affected. |

TheRock's development GPU table explicitly separates artifact build success, sanity testing and release readiness. A published wheel alone does not establish runtime functionality, and its development roadmap is not the released ROCm qualification matrix. Consult [TheRock GPU support](https://github.com/ROCm/TheRock/blob/main/SUPPORTED_GPUS.md) for development status and keep that evidence separate from production support.

## Read the right matrix

Start with the [current compatibility selector](https://rocm.docs.amd.com/en/latest/compatibility/compatibility-matrix.html), then use the corresponding [release notes](https://rocm.docs.amd.com/en/latest/about/release-notes.html). The current unified documentation covers Instinct, Radeon and Ryzen families. Earlier releases have separate Radeon/Ryzen matrices; retrieve the historical version when maintaining one of those stacks.

Select the exact hardware and environment before reading a table. Text extraction can flatten conditional columns, merged cells and hidden selector panels. Do not turn a flat list of operating systems into a claim that every listed GPU supports all of them. If the selector result cannot be recovered, use explicit SKU rows and footnotes in the release notes, an official machine-readable source, or state that the specific combination remains unverified.

Check driver/runtime compatibility in the separate [AMD GPU driver matrix](https://instinct.docs.amd.com/projects/amdgpu-docs/en/latest/compatibility/compatibility-matrix.html). AMD documents a compatibility window rather than requiring matching driver and ROCm version numbers. The exact supported pair and mutual hardware coverage govern the decision; a slogan such as “new driver works with everything” does not.

Check the framework's own installation page after the platform matrix. Treat AMD-tested containers, upstream stable wheels, nightly wheels and source builds as different artifacts. Read component limitations for native Windows and WSL independently. Use the specific artifact's architecture targets; a system-wide SDK cannot add missing kernels to a previously built wheel.

## Decide what is actually possible

Answer each requested capability through a short evidence chain:

1. Identify the backend the application can use: HIP, Vulkan, DirectML, OpenCL, a framework's ROCm backend, or a separate NPU runtime.
2. Establish whether the required build exists for the OS, Python ABI and GPU target.
3. Check the exact operator path: attention, quantized GEMM, convolution, collective communication, media codec, or custom extension.
4. Estimate memory per device and host memory before downloading a large model.
5. Run a representative correctness test followed by a small performance test.
6. Expand the workload only after the basic path succeeds.

Examples of appropriate conclusions:

- “The platform is qualified; this third-party CUDA extension still needs an AMD backend.”
- “The application has a Vulkan route. That can be evaluated independently of whether ROCm supports this SKU.”
- “The runtime enumerates the GPU, but the requested quantized attention kernel is unverified.”
- “The package exists for this architecture; execution on this exact device has not been tested.”

## Handle unsupported configurations

Prefer a supported OS/kernel combination or a compatible published build when that resolves the problem at low cost. Offer a source build when the missing piece is genuinely absent from the binary and the source supports the target. Do not promise that recompilation can implement an unsupported hardware instruction or port a CUDA-only dependency automatically.

For older Radeon or Instinct hardware, distinguish historical support, current compiler targeting and the availability of current math-library kernels. A source release retaining an ISA target is not proof that every framework ships usable kernels for it.

Treat `HSA_OVERRIDE_GFX_VERSION` and patched libraries as experiments with a precise hypothesis. An identity override does not change physical capabilities. Require a clean baseline, exact source provenance, numerical tests, a rollback, and a record of the override. Do not install an override globally or recommend one simply because a similarly named GPU worked for someone else.

Avoid generic absolute statements such as “ROCm only runs on Linux,” “all AMD GPUs work,” “a Docker image fixes the driver,” or “the NPU becomes a HIP GPU.” Resolve the relevant layers instead.

## Report a useful verdict

Return: exact tuple, support status per layer, primary evidence with access date, required changes, one reproducible validation procedure, remaining uncertainty, and a fallback. When buying hardware, name the workload assumptions and the maintenance burden; verify present support and availability before making a concrete recommendation.

Keep a support decision small enough to review. A useful table has one row per candidate configuration, with separate columns for qualification, application coverage, memory feasibility and operational constraints. A list of advertised TFLOPS is not a compatibility analysis.
