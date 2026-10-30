# Environment controls and controlled experiments

Evidence baseline: 2026-10-30. Variable names can persist while semantics, defaults or applicability change. Read the component's selected-version reference before use.

## Select a control by the problem

| Control family | Examples | Appropriate purpose | Boundary |
| --- | --- | --- | --- |
| Runtime device visibility | `ROCR_VISIBLE_DEVICES`, `HIP_VISIBLE_DEVICES` | Select allocated devices before process startup | Selection is not tenant security |
| Compatibility device visibility | `CUDA_VISIBLE_DEVICES`, `GPU_DEVICE_ORDINAL` | Interoperate with a documented framework/scheduler | Multiple masks can filter/reindex the same list |
| Compiler/SDK discovery | `ROCM_PATH`, `HIP_PATH`, `HIPCXX` | Select a coherent toolchain | Runtime wheel loading can be independent |
| Extension targets | `PYTORCH_ROCM_ARCH` where supported | Build required device code | Build-system specific; not a hardware override |
| Launch serialization | `AMD_SERIALIZE_KERNEL`, `AMD_SERIALIZE_COPY`, `HIP_LAUNCH_BLOCKING` | Locate asynchronous faults | Changes timing and concurrency |
| HIP logging | `AMD_LOG_LEVEL`, `AMD_LOG_MASK` | Narrow runtime evidence | Can expose arguments/paths and add overhead |
| Collective diagnostics | `NCCL_DEBUG`, `NCCL_DEBUG_SUBSYS` | Inspect RCCL initialization/transport | NCCL names are normal on AMD |
| Collective transport/algorithm | `NCCL_*` settings documented by RCCL | Test an evidenced communication hypothesis | No universal fast configuration |
| Managed-memory behavior | `HSA_XNACK` on eligible paths | Configure supported fault/migration behavior | Depends on GPU, driver, code and virtualization |
| Architecture override | `HSA_OVERRIDE_GFX_VERSION` | A narrowly evidenced compatibility experiment | Does not add instructions, kernels or support |
| Queue/CU controls | Documented queue/CU masks | Specific profiling or workload experiment | No guaranteed quota or adversarial isolation |

Primary references: [ROCm controls](https://rocm.docs.amd.com/en/docs-10.1.0/reference/environment-variables/index.html), [HIP controls](https://rocm.docs.amd.com/projects/HIP/en/latest/reference/env_variables.html), [GPU isolation](https://rocm.docs.amd.com/en/latest/reference/system-optimization/gpu-isolation.html), and [RCCL controls](https://rocm.docs.amd.com/projects/rccl/en/latest/api-reference/env-variables.html).

## Choose devices without confusing indices

On applicable Linux ROCr paths AMD recommends `ROCR_VISIBLE_DEVICES`; on Windows, use the documented HIP selection route. A process usually sees a reindexed logical list after filtering. Map its visible index to the scheduler's assigned physical device before comparing logs or sending work.

Set a mask once at the appropriate launch boundary. Do not layer a shell mask, container mask, scheduler mask and application mask without tracing each mapping. For a known two-device allocation, use one process per assigned GPU. If the scheduler exposes exactly one device to each process, local visible index zero can be correct even when the global rank is larger; the bundled distributed helper makes that mapping explicit.

Use visibility variables for cooperative selection. Enforce real isolation with the supported OS/container/VM/partition mechanisms and scheduling policy. Do not call a CU mask a hard power, memory or compute quota. See [Kubernetes/virtualization](kubernetes-virtualization.md).

## Debug one hypothesis

Capture the clean environment and error first. Use command-scoped settings rather than adding an experiment to a shell profile or every container image. For a small failing Python reproduction:

```bash
AMD_SERIALIZE_KERNEL=3 AMD_SERIALIZE_COPY=3 python reproduce.py
```

This serializes relevant work to help attribute the fault. It is not a repair. If the failure disappears, investigate races, lifetime or timing changes instead of declaring the issue solved. Remove these controls before performance measurement and preserve the unsynchronized reproduction.

For RCCL, use the minimal log scope described in [multi-GPU networking](multi-gpu-networking.md). For a release-note workaround, record the affected version/SKU/symptom and the condition for removing it. A workaround for one protocol on one architecture should not become a fleet-wide tuning default.

Keep logs local until reviewed. The inventory helper lists relevant variable **names** that are set, not values. A detailed report may need deliberate values, but a wholesale environment dump can expose credentials or private endpoints. Store only the relevant, sanitized settings in the stack record.

## Treat architecture overrides as experiments

If a device is not validated, first identify whether the blocker is package target omission, unsupported instructions, absent library kernels, driver support or framework policy. A build with the correct architecture may be the meaningful experiment. A misleading architecture override can make an incompatible binary load and fail later or produce incorrect output.

Require a specific source explaining the exact device/release combination and a rollback. Keep the override limited to one fresh process. Verify runtime identity, operator numerics and the complete intended workload. Label results experimental even when they pass. Do not prescribe a random `gfx` value or propagate a workaround to another GPU family.

## Distinguish build settings from runtime state

An environment variable set after import may be too late. Frameworks, runtimes and compilers can consume settings once during initialization or cache configuration. Restart the relevant process to test a change and identify whether a clean build directory or targeted cache rebuild is required.

Resolve compiler headers/libraries and application-loaded libraries independently. Avoid permanent `LD_LIBRARY_PATH` combinations that accidentally mix SDK generations. Use a dedicated environment and the selected release's installation guidance. See [build toolchains](build-toolchains.md) and [upgrades](upgrades-reproducibility.md).

Record each accepted control with its purpose, owner/component, version, measured effect and removal condition. A setting without a tested explanation is technical debt, not tuning.
