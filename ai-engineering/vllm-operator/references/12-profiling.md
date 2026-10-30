# 12 — Profiling Without Disrupting Operations

## Choose the tool for the question

Metrics show trends; distributed traces show request paths; a kernel profile
shows GPU/CPU execution and synchronization. Do not immediately capture a
multi-gigabyte trace on a fully loaded rented instance. Start with a hypothesis:
“CPU tokenization is limiting,” “TP communication dominates,” “graph fallback,”
or “prefill displaces decode.” [S10–S11](28-sources.md)

For the PyTorch profiler, the consulted documentation describes `--profiler-config`:

```json
{
  "profiler": "torch",
  "torch_profiler_dir": "/protected-local-volume/profiles",
  "torch_profiler_with_stack": false,
  "torch_profiler_record_shapes": false,
  "torch_profiler_with_memory": false
}
```

Check the **exact field names locally** before startup. This is an example
structure, not proof of testing on every release. Newer versions use the
structured profiler-configuration path; do not blindly copy old environment-
variable instructions. Start the server accordingly; the official benchmark
CLI can request a bounded profiling run with `--profile`. Make profiler
start/stop endpoints reachable internally only. [S11, S16](28-sources.md)

## A controlled experiment

Preserve a working baseline. Warm up the model, graphs, and kernels without
the profiler. Capture very few representative requests, then stop immediately.
Bound storage for profile files beforehand; flushing traces can take a long
time and generate substantial IO. Afterward, measure the same load **without**
the profiler. Do not present profiled latency as normal production latency.

Enable stacks, shapes, and memory tracking only when needed for the question.
They increase data volume and overhead and can reveal sensitive structures or
file paths. Treat profiling artifacts as internal operational data.

## What to look for in the timeline

| Pattern | Hypothesis | Counter-test |
|---|---|---|
| Large GPU idle gaps between steps | CPU, IPC, sampling, tokenization, or synchronization | Host profiler and small constant prompts |
| Heavy H2D/D2H traffic per step | Offload or unsuitable data paths | No offload or a smaller model |
| Many short launches and CPU gaps | Launch/graph issue | Supported graph configuration versus eager |
| Dominant collectives | TP/EP topology or very small batches | Compare single GPU, PP, and replicas |
| Large prefill blocks with stuttering decode | Batched-token budget/mixed load | Smaller chunks, separate workload classes |
| Unexpected recompilation | Changing shapes/configurations/cache paths | Fixed workload class and compilation logs |

CUDA operations launch asynchronously. A host timer around Python code may
measure only enqueue time, not actual kernel duration. Synchronizing for
measurement changes execution in turn. Interpret results using appropriate
GPU timelines rather than simply wrapping a forward pass in `time.time()`
and deriving absolute performance promises.

Nsight Systems is useful for CPU/GPU/communication timelines; deeper kernel
analysis requires appropriate permissions, drivers, and host tools. These are
often missing on rented instances. Do not enable privileged containers without
controls. Specialized NVTX/layer-tracing paths can be constrained by CUDA Graphs;
do not interpret graphs as “computation that disappeared.” [S11](28-sources.md)

## Abort criteria and handover

Abort on disk pressure, a severe latency regression, OOM, sustained export
backlog, or missing isolation. Disable profiler flags/endpoints afterward.
The handover includes the question, a relevant excerpt, a testable interpretation,
an alternative explanation, and the profiler-free control experiment.
A hundred-page trace file without findings is not a completed optimization.
