# Performance measurement and profiling

Evidence checked: 2026-10-30. Tool availability, counters, and profiler privileges depend on GPU, OS, driver, and tool release. A GPU's ROCm support does not imply that every profiler feature supports it.

## Contents

- [Define the experiment](#define-the-experiment)
- [Choose the observation tool](#choose-the-observation-tool)
- [Capture a useful trace](#capture-a-useful-trace)
- [Investigate the limiting resource](#investigate-the-limiting-resource)
- [Tune without losing correctness](#tune-without-losing-correctness)
- [Report reproducible results](#report-reproducible-results)

## Define the experiment

Write the performance question before choosing a profiler. Examples: reduce p95 inference latency at fixed request arrival rate; raise training samples/second at fixed global batch and loss behavior; reduce simulation wall time at fixed accuracy; fit a video job at the target resolution without offload stalls.

Capture a baseline with:

- Model/application revision, input distribution, dtype, kernel/backend selection, compile mode, and determinism settings.
- GPU SKU and architecture, per-device memory, partition mode, clocks/power policy, temperatures, and other active work.
- Driver, ROCm and component versions, framework wheel/container digest, Python, and compiler where relevant.
- CPU cores/NUMA binding, host-memory pressure, storage, and networking.

Separate cold start, model loading, kernel compilation/autotuning, warm-up, and steady execution. A faster second run might merely reuse caches. Keep both a realistic warm service test and a cold-start test when deployment latency matters.

GPU operations are asynchronous. Time completed work using framework events or synchronization at measurement boundaries. Avoid adding synchronization to every operation: that changes overlap and may destroy the behavior being studied. Count useful tokens/samples/iterations with consistent exclusions; record latency distributions, not only a mean.

## Choose the observation tool

| Question | First tool | Interpretation limit |
| --- | --- | --- |
| Is work reaching the intended GPU; is it throttling? | AMD SMI and application metrics | Utilization alone does not reveal useful efficiency |
| Is time lost in CPU work, waits, transfers, MPI, or GPU dispatch? | ROCm Systems Profiler or a short runtime trace | Instrumentation changes timing; remeasure without it |
| Which kernel dominates? | `rocprofv3`/framework trace | Longest single dispatch and largest total time are different rankings |
| Why is that kernel slow? | ROCm Compute Profiler | Counters may replay/serialize work and alter concurrency |
| Which instructions or stalls dominate? | Supported PC sampling or advanced thread trace | Architecture and driver support are narrower than general HIP support |
| Is movement between devices the limit? | TransferBench plus topology/collective tests | Isolated copy bandwidth is not application overlap |

The current stack centers on ROCprofiler-SDK; `rocprofv3`, Systems Profiler, and Compute Profiler serve different scopes. Old Omniperf/Omnitrace/ROCTracer recipes require version-aware migration, not mechanical executable renaming. [ROCm profiling overview](https://rocm.docs.amd.com/en/docs-10.1.0/components/profiling-tools-overview.html).

Check the tool's own support table before installation. Compute Profiler distinguishes counters from roofline support, while Systems Profiler has separate platform prerequisites. Do not infer discrete Radeon coverage from a nearby Ryzen or Instinct entry. [Compute Profiler supported hardware](https://rocm.docs.amd.com/projects/rocprofiler-compute/en/latest/quick-reference/rocprofiler-compute-at-a-glance.html#supported-hardware); [Systems Profiler installation](https://rocm.docs.amd.com/projects/rocprofiler-systems/en/latest/install/install.html).

## Capture a useful trace

On a supported native Linux stack, inspect the selected tools before running them:

```bash
rocprofv3 --version
rocprofv3 --help
rocprof-compute profile --help
```

Then profile a short, representative, restartable workload. This example assumes `workload.py` is the user's already-validated local reproduction:

```bash
rocprofv3 --runtime-trace --output-format rocpd -- python workload.py
```

For ROCprofiler-SDK 1.4.1, retain the `rocpd` database as the primary trace and use the matching conversion tools for other formats. Direct legacy output formats can omit newer records, including OMPT records. Check `rocpd --help` from the same installation before converting. [Versioned rocprofv3 guide](https://rocm.docs.amd.com/projects/rocprofiler-sdk/en/docs-10.1.0/how-to/using-rocprofv3.html); [rocpd output documentation](https://rocm.docs.amd.com/projects/rocprofiler-sdk/en/docs-10.1.0/how-to/using-rocpd-output-format.html).

Mark phases such as load, prefill, decode, forward, backward, optimizer, and checkpoint. Use ROCTx or the framework's supported annotations when it improves attribution. Record rank/PID and GPU identity for distributed traces; merge timestamps only after validating their clock basis.

Filter to a measured hotspot before collecting hundreds of counters:

```bash
rocprof-compute profile -n kernel-study -k selected_kernel -- ./validated_application
```

Replace `selected_kernel` with a name observed in the trace. This command can replay the application and run additional calibration work; use a reproduction that can safely execute repeatedly and writes disposable outputs. Inspect the generated output path and use the installed `analyze --help` to analyze it. Compute Profiler may serialize dispatches, so its kernel timings cannot substitute for the application's ordinary concurrency measurements. [Compute Profiler operation and replay model](https://rocm.docs.amd.com/projects/rocprofiler-compute/en/latest/quick-reference/rocprofiler-compute-at-a-glance.html).

Use scoped profiler permissions appropriate to the hardware. Do not add `--privileged`, disable container confinement, or lower host security settings merely because an example does so; first identify the specific denied capability or inaccessible performance counter.

## Investigate the limiting resource

| Observation | Hypothesis | Discriminating experiment |
| --- | --- | --- |
| Long GPU idle gaps | Input, CPU scheduling, synchronization, or compilation | Reuse resident synthetic input; compare CPU trace and first/warm run |
| Many tiny kernels | Launch overhead or lack of fusion | Compare eager/compiled or graph-enabled path with the same output check |
| Heavy memory traffic and little arithmetic | Bandwidth or redundant reads | Reuse data, change layout, fuse operations, measure bytes moved |
| High registers or local-memory traffic | Occupancy/resource pressure or spills | Compare tile/block variants and compiler resource reports |
| Long copies | Host staging, NUMA mismatch, or insufficient overlap | Separate pageable/pinned transfer tests and check placement |
| One rank always waits | Compute, data, or network imbalance | Per-rank step timings and pairwise transfers |
| Declining throughput over time | Thermal/power throttling, cache growth, or resource leak | Correlate clocks, temperature, memory, and completed work |

Use roofline analysis as a bound based on the relevant dtype and measured memory level. The arithmetic intensity of an entire application can conceal kernels with different bottlenecks. High occupancy is not itself the optimization goal; extra occupancy can come with more instructions, worse locality, or lower per-wave efficiency.

## Tune without losing correctness

Prefer changes in this order: eliminate CPU fallback and unnecessary transfers; correct data layout and batching; select a supported optimized library/kernel; enable justified compilation/graph paths; tune specific kernel shapes; then consider platform power/clock changes if authorized and operationally appropriate.

For GEMM, record dimensions, transposition, strides, epilogue, input/output/accumulation types, and workspace cap. Use the library's supported tuning path for that shape family and retain a fallback. A tuned solution is not a portable artifact across arbitrary GPU architectures or library revisions. [hipBLASLt tuning entry points](https://rocm.docs.amd.com/projects/hipBLASLt/en/latest/).

For each change, repeat numerical checks and end-to-end quality checks appropriate to the task. Quantization, different attention kernels, reduced accumulation precision, and reassociation can change results. Do not describe a change as faster unless it meets the same acceptance threshold. Restore diagnostic environment variables before final timing.

## Report reproducible results

Deliver the baseline, one-variable experiment, correctness result, speed/latency/memory delta, and uncertainty. Include at least several repetitions after warm-up when variance is material; state sample count and whether percentiles are request-weighted or run-weighted. Explain regressions as well as wins.

Keep the smallest useful trace, an exact invocation, the environment manifest, and the criterion for reverting. Avoid giant unrestricted production captures: they consume storage and can expose filenames, model data, and process details. Stop collecting once the remaining decision is resolved.
