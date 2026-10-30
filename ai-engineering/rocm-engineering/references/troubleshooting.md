# Troubleshooting by failing layer

Evidence checked: 2026-10-30. Diagnose the smallest failing boundary before changing the stack. Installation, device discovery, a trivial tensor operation, and a real workload are separate acceptance gates.

## Contents

- [Preserve a minimal evidence record](#preserve-a-minimal-evidence-record)
- [Walk the evidence ladder](#walk-the-evidence-ladder)
- [Map symptoms to discriminating checks](#map-symptoms-to-discriminating-checks)
- [Use scoped diagnostic controls](#use-scoped-diagnostic-controls)
- [Distinguish memory and numerical failures](#distinguish-memory-and-numerical-failures)
- [Handle hangs and regressions](#handle-hangs-and-regressions)
- [Escalate with a reproducible case](#escalate-with-a-reproducible-case)

## Preserve a minimal evidence record

Collect exact GPU SKU/PCI ID/gfx target, physical and logical device mapping, OS/kernel or Windows/WSL version, driver/firmware, ROCm component versions, framework version/build, and installation provenance. Record the first complete error, the command that produced it, and the last known-good configuration. For containers include image digest and passed devices; for distributed jobs include ranks and transport.

Use [the inventory helper](../scripts/rocm_inventory.py) before asking for broad logs. It should remain bounded and report missing capabilities explicitly. Redact credentials, internal addresses, model inputs, and irrelevant process details before publishing. Do not erase caches, uninstall packages, reset GPUs, or change permissions merely to obtain a cleaner report.

## Walk the evidence ladder

1. **Support contract:** establish the exact combination in [compatibility.md](compatibility.md), including framework/component restrictions and known issues. Mark a missing entry as unknown or unsupported according to source wording.
2. **Hardware/host:** does the OS enumerate the expected device, and is the correct driver bound? On native Linux inspect PCI and kernel messages when permitted; on Windows inspect the installed driver and device status.
3. **Runtime access:** can the intended user/process access the runtime's device interface? Native Linux KFD/DRM and WSL's Windows-backed interface are different paths.
4. **Library loading:** does the process load the intended HIP and dependent libraries? Check actual resolved paths rather than only the shell's reported default version.
5. **Framework build:** does the selected interpreter import a HIP-enabled framework and enumerate the intended device? Check the environment inside the container or job.
6. **Numerical kernel:** run a small verified operation with synchronization and a known result.
7. **Application:** reproduce the smallest failing operator/model/input. Add compilation, custom nodes/extensions, quantization, or optimized attention individually.
8. **Distribution and scale:** add additional GPUs, nodes, larger batches, longer contexts, and concurrency only after the smaller case works.

At each boundary keep the successful evidence and first failure. Stop reinstalling the entire system once the defect is isolated to one custom extension.

## Map symptoms to discriminating checks

| Symptom | First useful checks | Common misleading response |
| --- | --- | --- |
| No runtime GPU | Host enumeration, driver binding, platform-specific device interface, permission groups and current login session | Treating every missing device as a missing toolkit |
| `torch.cuda.is_available()` is false | `torch.__file__`, `torch.__version__`, `torch.version.hip`, wheel provenance, visibility settings | Installing CUDA because the API is named `cuda` |
| No binary/kernel image for device; invalid device function | Exact gfx target, packaged code objects, extension build flags | Spoofing architecture globally |
| Missing shared object or undefined symbol | Actual loaded paths, wheel/container dependencies, compiler/ABI compatibility | Appending every ROCm directory to `LD_LIBRARY_PATH` |
| Import works; first kernel fails | Synchronize the small operation, confirm runtime/driver compatibility and dtype support | Declaring success from import alone |
| GPU out of memory | Per-device capacity, real allocations, workspace/KV/activation memory, other processes | Adding all cards' VRAM as one pool |
| Host process killed | Host OOM/cgroup limits, RAM pressure, logs, pinned-memory demand | Assuming a GPU OOM because the job uses a GPU |
| NaN, black image, unstable loss, wrong reduction | Dtype, numerical range, kernel/backend choice, reference result, current known issues | Treating a completed execution as correct |
| Collective timeout | Missing rank, wrong mapping, first rank's exception, rendezvous, NIC/transport | Tuning RCCL algorithms before checking a crashed worker |
| Container fails but host works | Devices, groups, mounts, userspace libraries, runtime limits | Launching every container privileged |
| Large speed regression | Cold/warm state, backend selection, clocks, NUMA, thread count, precision, concurrency | Blaming the GPU model without a matched baseline |

PyTorch retains the CUDA-facing API on HIP builds; use its HIP version field and the actual computation path to identify the backend. Follow [pytorch.md](pytorch.md) for the framework-specific procedure.

## Use scoped diagnostic controls

Inspect a small allowlist of relevant variables: visible-device masks, selected ROCm/HIP paths, dynamic-library paths, and explicit application/backend controls. Do not dump the full environment. Conflicting masks can filter an already-remapped device list; start an isolated reproduction with a deliberate, documented selection.

For trusted local binaries, inspect linkage using platform tools such as `readelf -d` and the loader's diagnostics; use `ldd` only on trusted binaries. On Windows inspect DLL resolution and the selected environment. Do not copy arbitrary shared libraries into system directories as a repair.

HIP logging and synchronization controls can help localize an asynchronous failure. Consult the installed release's [ROCm environment-variable reference](https://rocm.docs.amd.com/en/docs-10.1.0/reference/environment-variables/index.html), enable only the required log categories for a short run, and remove diagnostic settings before benchmarking. Synchronization can change timing and hide a race; a passing synchronized run narrows the hypothesis but does not establish a fix.

Treat `HSA_OVERRIDE_GFX_VERSION`, SDMA changes, forced protocols, allocator changes, and unusual compiler flags as scoped experiments with a recorded reason and rollback. Architecture spoofing cannot add missing instructions or supply absent framework kernels. Preserve the original environment and avoid placing experimental overrides in shell startup files or shared images.

## Distinguish memory and numerical failures

For GPU memory, record allocated/reserved framework memory and process/device totals. Separate a true model-capacity limit from fragmentation, graph-capture pools, retained tensors, growing KV cache, and other processes. Reduce one dimension at a time: batch, context, resolution/frame count, or concurrency. A successful smaller case identifies pressure without proving the original workload fits.

CPU offload and managed memory exchange capacity pressure for transfer, page migration, and host-memory costs; measure those costs. See [llm-inference.md](llm-inference.md), [training-finetuning.md](training-finetuning.md), and [diffusion-video.md](diffusion-video.md) for workload-specific budgets.

For wrong results, preserve a reference input/output and compare one operation at a time. Try an explicitly supported higher-precision or simpler backend as a diagnostic baseline. Record input, output, and accumulation dtype separately. Check release-specific correctness advisories before long training runs. The MI350 LL all-reduce advisory is covered in [multi-gpu-networking.md](multi-gpu-networking.md); do not convert its workaround into a universal performance setting.

## Handle hangs and regressions

Use process-level time limits for disposable reproductions. Preserve the point of last progress and available telemetry before terminating only the reproduction you started. A kernel-driver hang may not be recoverable by killing a Python process; coordinate any device reset or reboot with the affected workloads rather than issuing it as the next generic command.

For WSL, consult [windows-wsl.md](windows-wsl.md) and [operations-monitoring.md](operations-monitoring.md). Missing native Linux interfaces and unsupported telemetry commands are not evidence that the GPU itself is defective.

Bisect changes across application, framework/wheel, custom kernels, userspace ROCm, and host driver separately. Reuse a fixed input and explicit correctness/performance criterion. Prefer a known-good isolated environment or image to overwriting the working baseline. When testing an upstream development build, label it as an experiment and retain its commit and dependency manifest.

For collective issues, use [RCCL's troubleshooting evidence](https://rocm.docs.amd.com/projects/rccl/en/latest/how-to/troubleshooting-rccl.html) plus the staged tests in this skill. For performance issues, follow [performance-profiling.md](performance-profiling.md); for repeated errors or resets, follow [operations-monitoring.md](operations-monitoring.md).

## Escalate with a reproducible case

Provide the exact failing command, minimized source or framework snippet, input shape/dtype, environment manifest, error/trace, expected versus actual result, reproduction frequency, and a tested comparison. State whether the failure occurs on host, container, VM, WSL, one GPU, several GPUs, or multiple nodes.

Separate verified facts from hypotheses and workarounds. Include what the workaround changes and which correctness/performance checks pass afterward. Stop once the user has a concrete supported resolution or a clearly isolated limitation with a viable alternative; do not continue speculative tuning indefinitely.
