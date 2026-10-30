# Multi-GPU execution and networking

Evidence checked: 2026-10-30. Resolve the actual ROCm, RCCL, framework, driver, and firmware releases before applying this guide. A working single-GPU program does not establish collective or inter-node correctness.

## Contents

- [Choose the execution model](#choose-the-execution-model)
- [Map the physical topology](#map-the-physical-topology)
- [Validate in increasing scope](#validate-in-increasing-scope)
- [Bring up network communication](#bring-up-network-communication)
- [Interpret and tune collectives](#interpret-and-tune-collectives)
- [Handle mixed and partitioned devices](#handle-mixed-and-partitioned-devices)

## Choose the execution model

| Goal | Initial design | Cost to measure |
| --- | --- | --- |
| Serve independent requests or run independent jobs | One replica/process per GPU | Per-replica model memory and queue balance |
| Train a model that fits on one GPU | Data parallelism | Gradient synchronization and input throughput |
| Train a model that does not fit | Explicit parameter/optimizer sharding or pipeline/tensor parallelism supported by the framework | Communication, temporary all-gather buffers, checkpoint reconstruction |
| Serve a model too large for one GPU | Supported tensor or pipeline parallelism | Per-token collectives, layer transfers, uneven KV placement |
| Accelerate a scientific simulation | Domain decomposition or an application-supported distributed solver | Halo exchange, load imbalance, collective reductions |

Treat every GPU's memory as an allocation domain. Adding card capacities describes total physical memory, not the maximum single allocation. Explicit sharding also consumes communication buffers and may leave uneven free memory. A coherent address space, peer access, unified memory, and an application-managed distributed tensor are different capabilities.

RCCL supplies AMD GPU collectives over supported PCIe/xGMI and network paths. Its API and configuration retain many `nccl*`/`NCCL_*` names; that naming is not evidence that NVIDIA CUDA is in use. [RCCL documentation](https://rocm.docs.amd.com/projects/rccl/en/latest/index.html), observed version 2.30.7.

## Map the physical topology

On native Linux, start with bounded, read-only commands available on the target:

```bash
amd-smi list --json
amd-smi topology --json
lspci -tv
numactl --hardware
```

Record physical GPU identity, logical device/partition identity, PCIe attachment, CPU NUMA node, NIC locality, link type, and negotiated link width/speed under load. Cross-check runtime enumeration inside the intended container and scheduler allocation. Do not assume host GPU 0 becomes process GPU 0 after visibility filtering.

For transfer measurements use a release-compatible [TransferBench](https://rocm.docs.amd.com/projects/TransferBench/en/latest/) or RVS workload. Measure every relevant pair in both directions, small and large buffers, and simultaneous transfers. Topology weights describe relative distance; they are not measured GB/s. A GPU pair can have functional communication through a host-staged path while direct peer transfer is unavailable.

Map slow pairs to PCIe switches, cross-socket links, NUMA placement, IOMMU configuration, and shared NICs before changing firmware. Do not disable IOMMU or ACS globally as a generic performance recipe; preserve device isolation and follow the system vendor's documented configuration.

## Validate in increasing scope

1. Run the single-GPU smoke workload on each intended logical device independently. Detect one bad device before involving collectives.
2. Run two local ranks with an exact expected reduction result, then all local ranks. Confirm every rank selects a unique intended device and reports the same world size.
3. Run a correctness-enabled RCCL test across a range of message sizes and dtypes. Cover the collective the application actually uses, including all-gather or reduce-scatter when relevant.
4. Run two nodes with one rank each, then one rank per GPU, then the target node count. Retain the first failing topology and smallest failing message.
5. Exercise the real workload, restart it, and repeat checkpoint save/restore or serving readiness. Passing a reduction does not validate an entire training or inference stack.

From the skill directory, the bundled integration check is:

```bash
torchrun --standalone --nproc-per-node=2 scripts/distributed_smoke.py
```

It requires an already working ROCm PyTorch environment and two allocated GPUs. Enforce an external scheduler/job wall-time limit: a process-group timeout cannot guarantee recovery from a driver hang. It checks a known result; it is neither a throughput benchmark nor a comprehensive RCCL qualification. See [the script](../scripts/distributed_smoke.py) for its options and timeout behavior.

For large sweeps, use the RCCL tests matching the deployed library. The old `ROCm/rccl-tests` repository now identifies itself as deprecated and points to `ROCm/rocm-systems`; follow the current project's build instructions and pin a commit instead of silently building an obsolete checkout. [Repository migration notice](https://github.com/ROCm/rccl-tests).

**ROCm 10.1.0 correctness caveat:** AMD lists incorrect MI350-series all-reduce results with RCCL's LL protocol and gives `NCCL_PROTO=LL128,Simple` as a workaround. Apply it only to an affected stack, repeat correctness tests, and recheck the issue on upgrade. Never accept a higher throughput score that fails validation. [Pinned release notes](https://rocm.docs.amd.com/en/docs-10.1.0/about/release-notes.html#rocm-known-issues).

## Bring up network communication

Separate the launch/rendezvous path from the payload transport. A reachable rendezvous address does not prove GPU-direct RDMA or even the intended NIC is in use. For each node record interface names, addresses appropriate to that job, RDMA device/port, firmware, MTU, and the selected transport reported in logs. Do not embed deployment addresses in reusable skill material.

Useful discovery commands, where the corresponding packages exist:

```bash
ip -brief address
rdma link
ibv_devinfo
ucx_info -v
```

Use ROCm-aware MPI/UCX only when the application or test needs MPI. RCCL is not automatically made GPU-aware by installing an arbitrary MPI package. In Open MPI 5.0.x, the documented ROCm transport is UCX, which must itself be built with ROCm support. Other Open MPI releases have their own support contracts. [Open MPI 5.0.x ROCm guide](https://docs.open-mpi.org/en/v5.0.x/tuning-apps/networking/rocm.html).

Check NIC driver/RDMA libraries and GPU-memory registration support for the exact platform. Expose only required network and GPU devices to containers. Compare host and container runs if NIC enumeration differs. Prove connectivity with host buffers and GPU buffers separately; working TCP sockets can hide an absent RDMA path. RoCE fabric configuration, loss behavior, congestion controls, and switch policy belong to the network design, not a universal RCCL environment-variable block.

## Interpret and tune collectives

Enable scoped logs for the failing reproduction, not every service permanently:

```bash
NCCL_DEBUG=INFO NCCL_DEBUG_SUBSYS=INIT,NET,GRAPH torchrun --standalone --nproc-per-node=2 scripts/distributed_smoke.py
```

Inspect the installed library's [environment-variable reference](https://rocm.docs.amd.com/projects/rccl/en/latest/api-reference/env-variables.html) before setting names or defaults. Distinguish socket-interface selection from RDMA HCA selection. `NCCL_SOCKET_IFNAME` affects the socket path; it is not a blanket instruction to use a particular RDMA device. Change one transport, algorithm, or protocol parameter at a time and retain the unmodified baseline.

Compare algorithm bandwidth and normalized bus bandwidth only under the benchmark's definitions. Neither is automatically a physical-link measurement. Report ranks, GPUs, topology, message sizes, dtype, warm-up, repetitions, validation status, and transport. For production, evaluate time in collectives and time to complete useful work; a faster isolated reduction can coexist with worse compute/communication overlap.

Use [RCCL troubleshooting](https://rocm.docs.amd.com/projects/rccl/en/latest/how-to/troubleshooting-rccl.html) to collect library paths, topology, versions, and logs. Adapt legacy `/opt/rocm` examples to the selected install prefix. Avoid replacing a production library with a development build until a small isolated reproduction justifies that experiment.

## Handle mixed and partitioned devices

Match ranks to the actual exposed logical devices. Partition changes invalidate cached device counts, UUID mappings, topology assumptions, and memory estimates. Re-enumerate before scheduling work.

For mixed AMD GPUs, verify compiled code objects and collective support for every architecture. Balance layers or tasks using measured capacity and speed; the smallest device or slowest link can limit the group. Prefer separate replicas or pools when heterogeneous tensor parallelism adds complexity without measured benefit. Combining AMD and NVIDIA within one distributed application requires an explicitly supported cross-vendor communication design; neither a shared Python API nor a mixed node proves that design exists.
