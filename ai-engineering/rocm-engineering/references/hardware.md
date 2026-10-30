# AMD hardware, memory and topology

Evidence baseline: 2026-10-30; current AMD ROCm documentation identifies Core SDK 10.1.0. Use this file to interpret a system and plan measurements. Obtain a fresh SKU-specific support verdict from [compatibility.md](compatibility.md).

## Contents

- [Separate the device families](#separate-the-device-families)
- [Identify the real target](#identify-the-real-target)
- [Budget memory per logical device](#budget-memory-per-logical-device)
- [Evaluate an APU](#evaluate-an-apu)
- [Inspect the whole server](#inspect-the-whole-server)
- [Choose hardware from the workload](#choose-hardware-from-the-workload)

## Separate the device families

| Family | Design context | Questions that matter |
| --- | --- | --- |
| Instinct / CDNA | Compute accelerators and HPC/AI systems | HBM per logical device, fabric, precision throughput, cooling, firmware and virtualization support |
| Radeon / RDNA | Graphics plus compute | Exact ROCm qualification, VRAM, display contention, supported framework kernels, board cooling |
| Radeon PRO / AI PRO | Workstation or professional product lines | Exact SKU and driver branch; professional branding alone does not establish every feature |
| Ryzen APU | CPU and integrated GPU sharing system resources | Memory mapping limits, RAM bandwidth, kernel fixes, CPU competition and sustained power |
| Ryzen AI NPU / XDNA | A separate neural accelerator | NPU compiler, operator coverage, quantization and deployment runtime |

ROCm GPU execution and Ryzen AI NPU execution are separate paths. AMD's [Ryzen AI documentation](https://ryzenai.docs.amd.com/en/latest/) provides the NPU deployment stack. An “AI” CPU name does not mean an arbitrary PyTorch HIP operation can execute on its NPU. If a product includes CPU, GPU and NPU, identify which processor runs each stage.

## Identify the real target

Representative architecture mappings from AMD's [GPU specifications](https://rocm.docs.amd.com/en/latest/reference/gpu-specs.html):

| Example device | Architecture / LLVM target |
| --- | --- |
| MI100 | CDNA / `gfx908` |
| MI210, MI250, MI250X | CDNA2 / `gfx90a` |
| MI300A, MI300X, MI325X | CDNA3 / `gfx942` |
| MI350X, MI355X | CDNA4 / `gfx950` |

Use the same primary table for Radeon and Ryzen mappings. Do not derive a `gfx` ID from a product number or assume all cards in one commercial series share it. These examples identify hardware; they do not confer current support.

For native Linux, collect targeted read-only observations:

```bash
lspci -nnk
uname -r
rocminfo
```

If installed, inspect `amd-smi --help` and use supported read-only listing/topology queries. Match physical PCI addresses, logical devices and partition identifiers. Preserve target suffix information such as XNACK or SRAM ECC where the build or execution path depends on it. `rocminfo` is not a universal native-Windows diagnostic; use that platform's supported HIP device query.

An enclosure can contain more execution devices than its physical board count suggests. In particular, inspect the logical-device presentation of multi-die accelerators before dividing a model or assigning ranks. Do not use total board memory as the maximum size of one allocation without verifying the runtime's memory pools.

## Budget memory per logical device

Use a per-device budget:

`weights + activations + KV cache + gradients/optimizer + temporary workspaces + runtime reserve`

Remove terms that do not apply. Account for checkpoint loading peaks and temporary unquantized tensors. A model file's compressed size does not prove its loaded footprint. Quantized weights can leave activations, scales, metadata and selected layers in higher precision.

Distinguish these situations:

- **One large device:** large allocations may fit directly; bandwidth and compute still determine speed.
- **Several discrete devices:** memory is distributed. The application must shard or explicitly transfer work; capacity is not a transparent shared pool.
- **A physically shared-memory APU:** CPU and GPU consume the same system memory and bandwidth. Mapping and allocation policies still limit what the application can use.
- **A partitioned accelerator:** each logical partition has a defined resource view. Query the configuration instead of treating it as the original whole device.

For a hypothetical 160 GiB aggregate installation made from several cards, derive feasibility from the largest per-rank allocation and communication pattern. Report the number as aggregate capacity until a sharding design is verified. Pipeline offload, tensor parallelism and independent replicas solve different problems.

Estimate communication cost separately from capacity. Run the intended peer-to-peer or collective path on the actual topology. A second GPU can improve throughput for independent requests even when tightly coupled model parallelism scales poorly.

## Evaluate an APU

AMD's [RDNA3.5 optimization guide](https://rocm.docs.amd.com/en/latest/reference/system-optimization/rdna3-5.html) describes GTT/TTM mappings, firmware reservations and additional kernel requirements for Ryzen AI Max. Mapping limits are not additional physical memory. The documented TTM page limit uses pages, so convert using the actual page size. Apply the guide to the matching architecture and kernel; do not transfer settings blindly to a discrete card or another APU generation.

Record total installed RAM, memory channels, effective memory speed, available host RAM at idle, firmware GPU reservation, framework-reported memory and actual peak allocation. Leave capacity for the OS, CPU preprocessing, file cache and other applications. A successful large allocation with swap activity may be unusable for the intended latency.

Measure both cold and warm runs. Include tokenization/data loading and CPU activity when those are part of production. Test sustained load on the intended power profile; short bursts do not establish long-run thermal behavior. On a shared-memory system, an experiment that changes GPU memory reservation must also record the host-memory consequences.

Treat persistent TTM/GTT or firmware changes as configuration work: capture the prior value, confirm the units, compute a conservative target, explain the reboot requirement where applicable, and provide the exact reversal. Do not maximize every memory limit by default.

## Inspect the whole server

Before blaming ROCm, check electrical, mechanical and platform constraints:

1. Confirm board form factor, slot width, power connectors, PSU headroom and chassis airflow. A passive accelerator needs a suitable forced-air design.
2. Record negotiated PCIe generation and width under a representative workload, PCIe switches and CPU root complexes.
3. Record CPU NUMA placement and host-memory locality. Compare data loading and transfer rates with sensible affinity.
4. Inspect firmware recommendations for the exact OEM system, including MMIO allocation and IOMMU mode.
5. Read kernel logs for driver initialization, PCIe/AER and GPU reset errors, limiting collection to the relevant period.
6. Validate one GPU first, then peer traffic, then the whole application.

AMD's [BAR addressing guide](https://rocm.docs.amd.com/en/latest/reference/system-optimization/bar-access-limits.html) explains how physical address limits can block peer DMA. Above-4G decoding, resizable BAR, IOMMU and address-space placement are related configuration questions with different purposes. Do not prescribe a universal “disable IOMMU” fix; virtualization and DMA correctness can require it.

Firmware changes must follow the OEM's supported update and recovery process. Do not treat another board's firmware or a consumer-card tuning guide as interchangeable.

## Choose hardware from the workload

Use a decision table with workload size, supported precision/backend, memory per GPU, bandwidth-sensitive phases, communication, power/cooling and software maintenance. For inference, distinguish prompt processing from token generation and throughput from interactive latency. For training, include optimizer state and checkpoint/restart behavior. For HPC, check numerical accuracy and the required FP64/communication path.

Compare measured results with the same model revision, precision, context lengths, batch/concurrency, output length and acceptance criteria. Do not compare sparse peak throughput to dense workload throughput or rank devices solely by nominal memory. Record the cost of engineering missing software support alongside hardware cost.
