# HIP programming and correctness

Evidence baseline: 2026-10-30; HIP documentation fetched as 7.16.0. Use the HIP version shipped by the chosen SDK, not a version number inferred from the umbrella release.

## Contents

- [Choose the implementation level](#choose-the-implementation-level)
- [Build the first correct kernel](#build-the-first-correct-kernel)
- [Manage memory and lifetime](#manage-memory-and-lifetime)
- [Use streams and graphs deliberately](#use-streams-and-graphs-deliberately)
- [Respect the target architecture](#respect-the-target-architecture)
- [Validate before tuning](#validate-before-tuning)

## Choose the implementation level

Prefer an existing library operation when it expresses the algorithm. Use HIP C++ for explicit control or an operation not covered efficiently by libraries. Use a framework custom operator when integration with tensor dispatch/autograd matters; use Triton or a maintained kernel collection only after checking target support. A hand-written kernel is a maintenance decision, not a prerequisite for using AMD GPUs.

Define an operator contract before implementation: input/output shapes and strides, dtype/accumulation, aliasing, device, memory ownership, deterministic requirements, valid value range and error tolerance. Include empty, non-contiguous and tail shapes if the interface permits them. Do not optimize a different contract from the one the application needs.

HIP exposes familiar grid/block/thread concepts and host/device functions. Use the [programming model](https://rocm.docs.amd.com/projects/HIP/en/latest/understand/programming_model.html) as the navigation entry; use the [runtime API](https://rocm.docs.amd.com/projects/HIP/en/latest/index.html) for exact signatures and supported features.

## Build the first correct kernel

The bundled [integer smoke kernel](../assets/hip-smoke/hip-smoke.hip) exercises device selection, allocation, host/device transfer, a tail-guarded launch, synchronization and host verification. It uses 257 elements so the final block is partial. It does not test floating-point matrix units or framework libraries.

After selecting a compatible SDK and confirming `hipcc` resolves to it:

```bash
# Example target only: replace with the measured and supported target.
ROCM_TARGET=gfx1100
hipcc --offload-arch="$ROCM_TARGET" -std=c++17 -O2 \
  assets/hip-smoke/hip-smoke.hip -o hip-smoke
./hip-smoke 0
```

Run on an allocated GPU with a job timeout. A machine without an AMD compiler can review source and prepare the build; it cannot claim GPU validation. See [build toolchains](build-toolchains.md) for CMake, architecture families and linking.

Check the return value of runtime calls. After a kernel launch, check launch status, then synchronize at an appropriate diagnostic boundary to observe execution faults. `hipGetLastError` consumes the error state; `hipPeekAtLastError` preserves it. A later copy can reveal an earlier asynchronous fault, so the failing source line may not be the actual cause. See [HIP error handling](https://rocm.docs.amd.com/projects/HIP/en/latest/how-to/hip_runtime_api/error_handling.html).

## Manage memory and lifetime

| Allocation/access choice | Use when | Verify |
| --- | --- | --- |
| Explicit device allocation | Working set belongs on GPU | Size, alignment, ownership, allocation failure |
| Ordinary host allocation | CPU owns/prepares data | Explicit transfer and host lifetime |
| Pinned/registered host memory | Transfers or mapped access justify pinning | Registration support, OS memory cost and transfer behavior |
| Managed/unified allocation | Supported migration/coherence semantics suit workload | Hardware, driver/HMM/XNACK, virtualized restrictions and measured faults |
| Peer access | One GPU consumes another GPU's data | Pairwise access, topology, remote bandwidth, lifetime |
| Stream-ordered allocation | Allocation lifetime follows stream work | Pool support, ordering, cross-stream dependencies |

Unified addressability, coherent access and physical placement are different properties. Do not assume a pointer accepted by both processors resides in fast local memory. A successful managed allocation does not prove page migration is available or efficient. Check runtime attributes and the [unified-memory requirements](https://rocm.docs.amd.com/projects/HIP/en/latest/how-to/hip_runtime_api/memory_management/unified_memory.html), including documented HMM/XNACK and SR-IOV restrictions.

Allocate reusable buffers outside hot loops where practical. Check multiplication overflow before computing bytes from dimensions. Keep pinned memory bounded. Preserve buffers until all dependent operations finish; a Python reference going out of scope or a host buffer being reused can race device execution when ownership is external.

Do not advertise host-memory oversubscription as extra VRAM. Measure transfers/page faults and end-to-end latency. Prefer explicit placement when it makes the algorithm's data movement predictable.

## Use streams and graphs deliberately

Treat a stream as an ordering mechanism. Use events for dependencies between streams; do not infer cross-stream ordering from submission order in unrelated threads. Avoid adding device-wide synchronizations to every production operation. Use them temporarily to isolate failures or at a measurement boundary.

Overlap requires suitable operations, available engines/resources, correct memory properties and independent work. Multiple streams alone do not create parallel speedup. Measure whether data transfer, host submission, compute or communication is critical. See [asynchronous execution](https://rocm.docs.amd.com/projects/HIP/en/latest/how-to/hip_runtime_api/asynchronous.html).

For HIP graphs, validate capture support for every library call and allocation behavior. Warm the required kernels first where the runtime demands it. Keep graph-referenced buffers alive and understand static-shape or pointer assumptions. Compare captured and eager results, graph creation cost and steady-state latency. A graph reduces suitable submission overhead; it does not remove memory capacity or unsupported kernels.

## Respect the target architecture

Do not hardcode a 32-lane NVIDIA warp or a universal 64-lane AMD wavefront. Use the programming model's supported query/abstraction and inspect the compiler target. Audit ballot widths, lane masks, shuffle collectives, barriers, subgroup assumptions and divergent control flow.

Check feature availability rather than copying numeric CUDA architecture tests. Device-side feature macros and host-side runtime properties serve different purposes; a host preprocessor branch cannot discover which GPUs will be present. See [HIP porting guidance](https://rocm.docs.amd.com/projects/HIP/en/latest/how-to/hip_porting_guide.html) and [hardware features](https://rocm.docs.amd.com/projects/HIP/en/latest/reference/hardware_features.html).

For performance, inspect coalescing, LDS use/bank conflicts, register pressure, spills, occupancy and vectorization. Maximal occupancy is not an objective by itself: more registers or larger tiles can improve useful work. Benchmark representative sizes instead of tuning only a convenient square matrix. Use [HIP performance guidance](https://rocm.docs.amd.com/projects/HIP/en/latest/how-to/performance_guidelines.html) to form hypotheses, then profile.

## Validate before tuning

Maintain an independent CPU or trusted-library reference. Test boundaries, tails, striding, alignment, large indices and supported dtypes. Check absolute/relative error and application-relevant invariants; exact equality is usually inappropriate for reordered floating-point reductions. Investigate nonfinite values and silent corruption before interpreting speed.

For custom autograd, validate gradients against a trusted implementation and, for small cases, numerical finite differences with suitable precision. For atomics/reductions, test contention and repeated runs. For random generation, test the intended distribution/reproducibility contract rather than identical vendor sequences.

Only after correctness passes, establish a synchronized warm baseline, vary one implementation choice and retain trace evidence. Preserve a fallback implementation for unsupported shapes or targets. See [performance](performance-profiling.md) and [validation](validation-workflows.md).
