# Performance, capacity, and recovery sizing

Evidence checked: 2026-10-21. Treat all numerical examples below as arithmetic illustrations, not measured product performance or an SLA.

## Contents

- [Describe a measurable workload](#describe-a-measurable-workload)
- [Use consistent units and equations](#use-consistent-units-and-equations)
- [Budget protected capacity](#budget-protected-capacity)
- [Budget the degraded state](#budget-the-degraded-state)
- [Benchmark the intended contract](#benchmark-the-intended-contract)
- [Locate the bottleneck](#locate-the-bottleneck)
- [Include operating cost](#include-operating-cost)
- [Primary references](#primary-references)

## Describe a measurable workload

Record a workload vector before choosing devices or providers:

| Dimension | What to measure |
| --- | --- |
| Operations | Read/write/delete/list/stat/rename proportions; random versus sequential; overwrite versus append |
| Size distribution | I/O sizes, object/file sizes, total object/file count, directory fanout |
| Concurrency | Clients, processes, independent streams, actual in-flight operations |
| Durability | Buffered writes, synchronous commits, group commit, replication acknowledgment |
| Working set | Hot bytes and metadata, cache hit rate, reuse distance, cold-start demand |
| Service objective | Useful throughput and operation/transaction latency percentiles at the intended load |
| Lifecycle | Growth, retention, snapshots, compaction, ingest bursts, rebuild and restore windows |

Measure median and tail latency, not just an average. Define a specific target such as “p99 transaction commit below the stated limit at the expected offered load.” A raw device latency percentile is not automatically an application transaction percentile. Include errors, timeouts, and retries; exclude none silently from reported performance.

## Use consistent units and equations

Use decimal GB/TB for `10^9`/`10^12` bytes and binary GiB/TiB for `2^30`/`2^40` bytes. Use lower-case `b` for bits and upper-case `B` for bytes. Preserve the provider's billing units separately from OS display units.

For fixed-size operations measured at the same layer:

`throughput_bytes_per_second = IOPS × bytes_per_operation`

Thus 20,000 operations/s at 8 KiB per operation equals 156.25 MiB/s of those operations' payload. It does not include replica writes, protocol overhead, metadata, or read-modify-write work. For mixed sizes, use the actual size distribution.

For a stable queue measured at one boundary, Little's law gives:

`mean_in_flight ≈ completed_operations_per_second × mean_latency_seconds`

Do not substitute p99 latency into this mean-value relationship. Increasing queue depth can increase throughput until another limit is reached, while making tail latency worse. A serial synchronous writer cannot use a device's high-depth benchmark IOPS without application concurrency or batching.

A 10 Gbit/s link provides a theoretical 1.25 GB/s decimal line-rate ceiling before protocol and other traffic. WAN throughput also depends on loss, congestion control, and the bandwidth-delay product. More disks cannot repair a client network bottleneck.

## Budget protected capacity

Separate raw bytes, protected logical capacity, allocated bytes, referenced data, and application-visible free space. A simplified planning envelope is:

`payload_budget ≈ raw_capacity × protection_efficiency × (1 - operational_headroom) - additional_reserves`

Use `1/r` for `r` full replicas, or `k/(k+m)` for ideal erasure coding with `k` data and `m` parity fragments. Account separately for metadata, small-object packing, padding, imbalance, snapshots, journals, allocator behavior, and implementation limits. For local arrays, compute each vdev/RAID group's actual geometry; heterogeneous drive sizes can leave unusable capacity.

Example: 60 TB raw with three copies gives an ideal 20 TB logical ceiling. Reserving 25% of that protected envelope leaves 15 TB before other overheads. This is a capacity estimate; it says nothing by itself about whether copies are placed in independent hosts or whether another failure can be tolerated.

Do not automatically credit compression or deduplication. Measure representative data; encrypted or already-compressed content may yield little saving. Include deduplication indexes, memory, CPU, and recovery complexity. Track logical versus physical usage so a workload change cannot silently consume the reserve.

For snapshots, estimate changed blocks over retention intervals, not snapshot count alone. For thin pools, monitor metadata as well as data. For log-structured systems, reserve room for compaction and garbage collection. For file services, track inodes or metadata limits and quotas in addition to bytes.

## Budget the degraded state

The useful capacity and throughput during failure may be lower than the healthy configuration. Calculate what remains after losing the largest planned failure domain and whether the placement rule can still be satisfied. Spare bytes on two surviving hosts cannot create a third host required by a three-host replica rule.

Define both restoration of service and restoration of protection. An application may resume quickly while data remains under-replicated for hours. Include this exposure period in the design and alerts.

The absolute transfer floor is:

`recovery_time_seconds >= bytes_that_must_move / effective_recovery_bytes_per_second`

Moving 8 TiB at an actually sustained 500 MiB/s has a transfer-only floor of about 4.66 hours. Real recovery adds detection, scheduling, scanning, random reads, metadata, checksums, competing foreground traffic, remote retrieval, and possible retries. Erasure-code repair may read more bytes than it reconstructs; use the scheme's actual repair path.

Choose a repair bandwidth budget that still meets application latency requirements. A configuration that rebuilds quickly only when users stop working does not meet an always-on availability objective. Verify restore rate separately from backup ingest rate, especially for compressed archives, tiny files, and cold storage.

## Benchmark the intended contract

Use the real application benchmark where possible. Supplement it with a small set of discriminating tests, not a single “disk speed” number:

| Experiment | What it isolates |
| --- | --- |
| Small random reads, several realistic queue depths | Working-set/cache effect, device latency, concurrency scaling |
| Small synchronized writes | Durable acknowledgment latency, flush path, replication cost |
| Large sequential read/write | Streaming path, network and device bandwidth |
| Create/stat/list/delete many small files | Metadata path, namespace contention, request overhead |
| Cold start versus warm run | Cache dependence and startup capacity |
| Sustained writes beyond temporary caches | Steady-state flash/array/provider behavior |
| One planned failure plus repair | Actual degraded SLO and repair interference |
| Restore representative data | End-to-end recovery objective |

Use tools such as fio or Microsoft's DiskSpd with explicit workload parameters. fio's requested depth may differ from achieved depth; inspect its distribution. A synchronous engine is not made asynchronous merely by increasing `iodepth`. Direct I/O and synchronization are separate concepts: bypassing a page cache does not by itself prove power-loss durability. [fio documentation](https://fio.readthedocs.io/en/latest/fio_doc.html), [DiskSpd](https://github.com/microsoft/diskspd)

For synthetic writes, use only clearly identified disposable files or devices with sufficient free space and explicit authorization. Never point a copied random-write example at a production block device. Record tool version, command/job file, filesystem/mount settings, cache policy, data pattern, duration, warmup, queue depth, host load, and environment.

Avoid all-zero data for a compressed/deduplicated target unless that pattern is the workload. Avoid interpreting sparse-file reads as device reads. Do not drop caches on a production machine simply to manufacture a “cold” run; use an isolated test and state the cache boundary. Include an arrival-rate-oriented test when a closed-loop benchmark hides latency by reducing offered load during stalls.

## Locate the bottleneck

Correlate timestamps across application, host, network, storage target, and distributed backend. Inspect CPU saturation, TLS/checksum/compression cost, NUMA locality, memory pressure, queues, retries, packet loss, and actual device reads/writes. Account for noisy neighbors and per-instance/per-volume limits independently in a cloud environment.

Treat utilization percentages cautiously. Modern SSDs and arrays process operations in parallel; a device reported busy nearly all the time is not necessarily at its maximum throughput. Conversely, low device utilization does not exclude a metadata lock or synchronous acknowledgment bottleneck. Kernel disk counters can combine/split requests and count different work than application operations. [Linux I/O statistics](https://docs.kernel.org/admin-guide/iostats.html), [sysstat iostat manual](https://github.com/sysstat/sysstat/blob/master/man/iostat.in)

## Include operating cost

Budget capacity, replicas/EC overhead, snapshots and noncurrent versions, request charges, minimum retention, retrieval, inter-zone/region transfer, public egress, compute nodes, licenses, support, energy, and staff time. An apparently inexpensive object store can be unsuitable for a latency-sensitive small-operation workload; a high-performance cluster can be wasteful for seldom-read archives.

Compare complete architectures at the same durability, RPO/RTO, retention, and workload. Present a range based on growth and restore/egress scenarios rather than a single optimistic monthly figure. Verify current provider prices separately; this reference deliberately contains no price claims.

## Primary references

- [fio manual](https://fio.readthedocs.io/en/latest/fio_doc.html): workload definition, depth, direct I/O, and synchronization.
- [Microsoft DiskSpd](https://github.com/microsoft/diskspd): Windows storage workload generation.
- [Linux I/O statistics](https://docs.kernel.org/admin-guide/iostats.html) and [sysstat iostat](https://github.com/sysstat/sysstat/blob/master/man/iostat.in): measurement boundaries.
- [Microsoft file-server performance guidance](https://learn.microsoft.com/en-us/windows-server/administration/performance-tuning/role/file-server/): workload and hardware constraints.
- [Linux thin provisioning](https://docs.kernel.org/admin-guide/device-mapper/thin-provisioning.html): shared allocation and metadata capacity.
- [OpenZFS pool status](https://openzfs.github.io/openzfs-docs/man/master/8/zpool-status.8.html): rebuild progress is an estimate; use release-matched tools.
