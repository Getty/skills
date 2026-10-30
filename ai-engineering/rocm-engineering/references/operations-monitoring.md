# Operations, monitoring, and reliability

Evidence checked: 2026-10-30. Examples below target native Linux unless explicitly marked otherwise. Telemetry coverage is a per-platform capability; unavailable metrics must remain unavailable rather than being converted into zero.

## Contents

- [Build an operational identity](#build-an-operational-identity)
- [Collect bounded telemetry](#collect-bounded-telemetry)
- [Monitor useful service behavior](#monitor-useful-service-behavior)
- [Interpret reliability signals](#interpret-reliability-signals)
- [Operate Windows and WSL within their scope](#operate-windows-and-wsl-within-their-scope)
- [Manage changes and incidents](#manage-changes-and-incidents)

## Build an operational identity

Track physical board identity separately from logical GPU/partition identity and process-visible index. Use the available stable UUID/BDF/partition fields and retain their mapping after reboot, driver change, partitioning, or virtualization changes. Label measurements with GPU SKU, architecture, driver and firmware, ROCm/framework version, workload/image revision, and relevant partition mode.

Start with [the passive inventory helper](../scripts/rocm_inventory.py); enable runtime probes only when useful and authorized by the task. Inventory should not need root, install packages, alter permissions, reset devices, or dump all environment variables. Avoid exporting serials, hostnames, process command lines, or job payloads unnecessarily in public incident reports.

Record who owns each lifecycle: host kernel/driver, ROCm userspace, framework environment/container, scheduler/operator, firmware, and model. A wheel update can change kernels without a driver update; a driver update affects all users of that host.

## Collect bounded telemetry

Prefer AMD SMI for current stacks. ROCm's TheRock transition removed ROCm SMI from the Core SDK; old `rocm-smi` commands belong to their original release context. [Transition guide](https://rocm.docs.amd.com/en/docs-10.1.0/about/transition-guide-TheRock.html).

On native Linux with AMD SMI installed, start with short one-shot queries:

```bash
timeout 15s amd-smi version
timeout 15s amd-smi list --json
timeout 15s amd-smi metric --json
timeout 15s amd-smi process --json
```

Inspect `amd-smi <subcommand> --help` before using version-sensitive flags. Preserve timeout, permission, unsupported, and command-not-found outcomes as distinct states. `process` can expose other users' workload metadata; restrict collection and sharing accordingly. For long-lived monitoring, use the supported AMD SMI API/exporter with typed fields and error handling instead of parsing a human terminal table. AMD itself recommends its library interfaces for robust telemetry integrations. [AMD SMI 27.1.0 CLI](https://rocm.docs.amd.com/projects/amdsmi/en/docs-10.1.0/how-to/amdsmi-cli-tool.html).

Choose collection intervals against the event of interest. Subsecond polling is not automatically more informative if sensors are cached or updated less frequently. Separate a short diagnostic trace from the ordinary service scrape interval and measure monitoring overhead.

## Monitor useful service behavior

| Layer | Signals | Operational interpretation |
| --- | --- | --- |
| Application | Request errors, queue depth, p50/p95/p99 latency, completed work, model readiness | Whether users receive correct useful output |
| Framework | Allocated/reserved memory, compilation/cache events, OOM, rank failures | Whether the workload fits and executes as designed |
| GPU | Utilization, clocks, power, temperatures, memory pressure | Saturation, imbalance, and throttling hypotheses |
| Fabric | Link errors, retries, collective duration, NIC throughput | Communication degradation or topology mismatch |
| Host | CPU pressure, NUMA locality, RAM, disk latency, network | Bottlenecks outside the GPU |
| Reliability | Corrected/uncorrected errors, resets, page retirement, device disappearance | Whether work should be retried, quarantined, or serviced |

Do not use GPU utilization as the sole capacity signal. A saturated memory-bound kernel and a productive compute-bound kernel can show similar utilization. A stalled service can occupy VRAM while completing no requests. Couple telemetry to completed useful work and correctness outcomes.

For Kubernetes, the AMD Device Metrics Exporter exposes Prometheus-compatible metrics and integrates with operator configuration. Pin an exporter version compatible with the node stack; the retrieved operator page mixes newer example images with an older historical requirements table, so that table alone does not validate a new ROCm release. Verify the exporter's own release guidance and observed metrics. [Metrics Exporter](https://instinct.docs.amd.com/projects/gpu-operator/en/latest/metrics/exporter.html).

Keep the scrape endpoint internal, constrain access, and avoid high-cardinality labels such as unrestricted process arguments or request IDs. Define alerts from a baseline, hardware limits, and workload SLOs rather than one universal temperature or error-count threshold.

## Interpret reliability signals

Distinguish corrected from uncorrected errors, cumulative counters from interval rates, and preserved hardware counters from values reset by a reboot or driver reload. Correlate an error with timestamp, GPU identity, workload, kernel messages, and any CPER/AFID record available. Missing ECC capability or telemetry does not prove error-free memory.

AMD SMI exposes ECC/RAS information where supported; CPER records provide structured error context, while AFIDs identify documented AMD conditions. Consult the matching platform documentation before classifying severity or clearing records. [AMD SMI RAS guide](https://rocm.docs.amd.com/projects/amdsmi/en/docs-10.1.0/conceptual/ras.html).

On uncorrected errors, unexplained resets, or repeated corrupted results, preserve evidence and stop admitting affected work according to the service policy. Distinguish workload defects from a persistent device fault using the smallest validated reproduction and a known-good peer system. A successful reset is not proof of repaired hardware. Run stress tests or error injection only as explicit maintenance/qualification work on the affected scope.

## Operate Windows and WSL within their scope

Do not apply Linux `/dev/kfd` or DRM/sysfs expectations to WSL. AMD SMI 27.1.0 documents an experimental WSL backend using the Windows driver path; it is opt-in at build time and disabled by default. Thus a generic installed AMD SMI package is not proof that WSL telemetry is available. Some query classes, including ECC, partitions, and fabric, have no supported WSL equivalent. [WSL backend prerequisites and limitations](https://rocm.docs.amd.com/projects/amdsmi/en/docs-10.1.0/how-to/amdsmi-wsl-mode.html).

Native Windows and WSL monitoring support do not imply the same management commands as native Linux. Capability-detect supported queries and use the relevant Windows driver/system tools for missing host observations. Avoid `amd-smi event` under the documented ROCm 10.1.0 WSL limitation; it can hang. Keep timeouts around diagnostic queries and terminate only the tool process you started when necessary. [ROCm 10.1.0 known issues](https://rocm.docs.amd.com/en/docs-10.1.0/about/release-notes.html#rocm-known-issues).

## Manage changes and incidents

Before changing a driver, firmware, partition profile, power policy, or node image, record the prior state and affected users/jobs. Use a canary node or isolated workload, run numerical and application acceptance checks, compare performance, then expand. Keep downgrade feasibility explicit: a userspace rollback may be easy while firmware or kernel-driver rollback may require a maintenance reboot.

For an incident, capture a bounded time window and the smallest failing case, identify the failing layer, apply one justified change, and rerun the same acceptance criterion. Preserve kernel messages before resets when access permits. Never clear RAS counters, unload drivers, reset every GPU, or kill all GPU processes as an evidence-collection step.

Readiness should test that the correct model/backend is loaded and can perform useful work. Liveness should detect a stuck process without repeatedly restarting a service during a legitimate long initialization. After a service stop, verify worker processes and GPU allocations are released before restarting; distinguish an orphaned worker from a genuine allocator leak.
