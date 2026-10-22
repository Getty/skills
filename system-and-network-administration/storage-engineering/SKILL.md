---
name: storage-engineering
description: "Use when choosing, sizing or debugging storage — block vs file vs object, S3 vs a mounted directory, filesystems, NAS/SAN, NFS/SMB/iSCSI/NVMe-oF, RAID, replication, erasure coding, quorum and fencing, multi-site HA and DR, backups, Kubernetes CSI/PV/PVC, cloud disks, caching, migration, cost."
---

# Storage Engineering

Build a storage architecture from the application's access contract and the failures it must survive. Cover technologies broadly; use implementations to make methods concrete, and load their current documentation only when an implementation decision requires it.

## Operating rules

1. Separate **interface**, **implementation**, **placement**, and **service guarantee**. A mounted path may be local, networked, object-backed, cached, or transient. An S3 API says little by itself about durability, consistency, or geography.
2. Establish who owns each datum and each write. Trace a successful acknowledgement through application buffers, client caches, servers, journals, replicas, and durable media.
3. Treat availability, durability, integrity, consistency, recoverability, and security as different properties. Replication, snapshots, RAID, versioning, and backup solve different failure classes.
4. Name the failure domain for every protection claim: drive, controller, host, rack, power/network domain, site, region, account, operator, or provider.
5. Separate control-plane quorum from data placement and write acknowledgement. A witness stores votes, not necessarily recoverable user data. Never infer write availability from replica count alone.
6. Prove writer exclusion before failover. Restarting a pod, moving an IP, detaching a volume, or deleting an API object is not proof that the previous writer has stopped.
7. Treat examples and sizing formulas as conditional models. Do not invent SLAs, prices, zones, device guarantees, or achievable performance.
8. Prefer the smallest operationally supportable design that meets the stated failure and recovery targets. Consider application-native replication before adding another replicated storage layer.
9. Check current primary documentation for provider features, filesystem support, CSI behavior, release status, licenses, and destructive commands. Record service class, location, version, and verification date.
10. Keep actions proportional to the request. Use read-only investigation first; for formatting, restore overwrite, deletion, forced promotion, retention changes, or repair writes, establish the exact target, existing authorization, recoverable copy, and consequence before proceeding.

## Workflow

### 1. Establish the workload contract

Use the facts already provided; make explicit assumptions for unknowns and ask only questions that change the design. Capture:

- Data classes: database state, user uploads, shared workspace, VM disks, container layers, logs, backups, immutable datasets, caches, scratch.
- Interface and required operations: filesystem path, block device, object API, append/log, database/query; random updates, atomic rename, locking, mmap, xattrs/ACLs, sparse files, range reads, listings.
- Concurrency: one writer, coordinated writers, independent writers, multi-tenant access; desired read visibility and transaction boundaries.
- Scale: live bytes, object/file count and size distribution, daily change rate, growth, working set, IOPS, bandwidth, latency percentiles.
- Recovery: named failures, tolerated lost acknowledged writes (RPO), recovery time (RTO), required service during maintenance and rebuild.
- Environment: OS/hypervisor, Kubernetes versions, hosts and independent sites, measured network RTT/bandwidth/loss, provider placement, operator skill and budget.

Distinguish a business target from an observed capability. If the request is conceptual, teach the relevant distinction without requiring a full questionnaire.

### 2. Choose semantics before products

Read [taxonomy-and-selection.md](references/taxonomy-and-selection.md) and, for filesystem/object questions, [file-and-object-semantics.md](references/file-and-object-semantics.md).

Produce a small candidate table: interface, data owner, writer model, persistence boundary, failure domain, restore method, operational burden. Reject candidates that cannot meet required semantics before ranking cost or speed.

### 3. Draw the failure and recovery design

Read [distributed-consistency-and-ha.md](references/distributed-consistency-and-ha.md) for HA and [geo-replication-and-dr.md](references/geo-replication-and-dr.md) for multiple locations.

For each named failure, state: readable data, permitted writers, surviving quorum, fencing mechanism, recoverable copy, automatic/manual action, expected data loss, and return to redundancy. Include asymmetric partitions and a second failure during recovery. Show failback ownership explicitly.

### 4. Size normal, degraded, and recovery operation

Read [performance-and-sizing.md](references/performance-and-sizing.md). Count protection overhead, free space, retained versions/snapshots, metadata, logs, caches, and restore staging. Measure the bottleneck across disks, CPU, network, instance caps, API requests, and application serialization.

Use [storage_budget.py](scripts/storage_budget.py) for transparent capacity and transfer arithmetic. Treat its output as planning math, never a proof of quorum, placement, rebuild completion, or availability. Consult [capacity-and-recovery-models.md](references/capacity-and-recovery-models.md) for its assumptions.

### 5. Match the platform

- For Kubernetes, load [kubernetes-storage.md](references/kubernetes-storage.md) and [kubernetes-recovery-and-patterns.md](references/kubernetes-recovery-and-patterns.md).
- For virtual instances and provider-managed storage, load [cloud-lifecycle-and-topology.md](references/cloud-lifecycle-and-topology.md).
- For Hetzner, load [hetzner-storage.md](references/hetzner-storage.md); for alternatives, load [provider-service-matrix.md](references/provider-service-matrix.md).
- Recheck the exact region, resource type, attachment rules, backup inclusion, network path, and lifecycle before providing executable provisioning steps.

### 6. Deliver a testable decision

Use [architecture-brief.md](assets/architecture-brief.md) and [failure-matrix.csv](assets/failure-matrix.csv) as output templates when useful. Include:

1. Recommended design and assumptions.
2. Access and write-acknowledgement guarantees.
3. Placement and failure matrix.
4. Capacity, latency, cost, and recovery budgets.
5. Backup/restore and failback ownership.
6. Deployment or migration stages, acceptance checks, and rollback limits.
7. Current sources for implementation-specific claims and unresolved facts.

For troubleshooting, use [operations-and-troubleshooting.md](references/operations-and-troubleshooting.md): preserve evidence, narrow the failing layer, change one cause at a time, verify application behavior.

## Reference router

Read only the rows relevant to the current problem. All references are direct children of this skill.

| Need | Reference |
| --- | --- |
| Complete technology map and first selection | [taxonomy-and-selection.md](references/taxonomy-and-selection.md) |
| Mounted path versus API; POSIX, rename, locks, fsync | [file-and-object-semantics.md](references/file-and-object-semantics.md) |
| S3 operation, compatibility, multipart, versions, event handling | [object-storage-and-s3.md](references/object-storage-and-s3.md) |
| Drives, controllers, volume managers, local filesystems | [local-media-and-filesystems.md](references/local-media-and-filesystems.md) |
| DAS/NAS/SAN, iSCSI, FC, NVMe-oF, multipath | [block-and-network-protocols.md](references/block-and-network-protocols.md) |
| NFS, SMB, distributed namespaces and object-backed filesystems | [file-sharing-and-namespaces.md](references/file-sharing-and-namespaces.md) |
| RAID, copies, EC, checksums and failure-domain placement | [data-protection-and-placement.md](references/data-protection-and-placement.md) |
| Consistency, votes, leases, fencing, partitions and two-node designs | [distributed-consistency-and-ha.md](references/distributed-consistency-and-ha.md) |
| WAN replication, stretched clusters, DR, active-active and failback | [geo-replication-and-dr.md](references/geo-replication-and-dr.md) |
| Architecture families and implementation examples | [distributed-system-families.md](references/distributed-system-families.md) |
| Backup methods, immutable/offline copies, PITR and restore | [backup-and-restore.md](references/backup-and-restore.md) |
| Kubernetes storage contracts and CSI lifecycle | [kubernetes-storage.md](references/kubernetes-storage.md) |
| Kubernetes application patterns and cluster recovery | [kubernetes-recovery-and-patterns.md](references/kubernetes-recovery-and-patterns.md) |
| Instance/volume lifetime, placement and cloud control planes | [cloud-lifecycle-and-topology.md](references/cloud-lifecycle-and-topology.md) |
| Hetzner Cloud/dedicated/Volumes/Box/Share/Object Storage | [hetzner-storage.md](references/hetzner-storage.md) |
| AWS, Azure, GCP and other provider capability families | [provider-service-matrix.md](references/provider-service-matrix.md) |
| Database, VM, uploads, artifact, AI and analytics patterns | [application-storage-patterns.md](references/application-storage-patterns.md) |
| Cache authority, tiers, gateways, synchronization and transfer | [caching-and-data-movement.md](references/caching-and-data-movement.md) |
| Performance measurement, queueing, rebuilds and cost | [performance-and-sizing.md](references/performance-and-sizing.md) |
| Calculator inputs, formulas, limitations and worked examples | [capacity-and-recovery-models.md](references/capacity-and-recovery-models.md) |
| Read-only investigation and operational runbooks | [operations-and-troubleshooting.md](references/operations-and-troubleshooting.md) |
| Identity, encryption, tenant isolation, retention and deletion | [security-and-tenancy.md](references/security-and-tenancy.md) |
| Tape/HSM, HPC, content-addressed storage, memory and emerging methods | [specialized-storage.md](references/specialized-storage.md) |
| Small-server, limited-cloud, hybrid and multi-site architectures | [architecture-recipes.md](references/architecture-recipes.md) |
| Conversion, cutover, semantic tests and recovery acceptance | [migration-and-validation.md](references/migration-and-validation.md) |
| Evidence discipline, capability lookup and terminology | [sources-and-glossary.md](references/sources-and-glossary.md) |

## Diagnostic shortcuts

- **“It is mounted, so it is a normal disk.”** Identify the implementation and operation-level contract; load filesystem/object semantics.
- **“Two/three copies means HA.”** Inspect data placement, voters, quorum thresholds, fencing, endpoint ownership, and spare capacity.
- **“We can mount one ext4/XFS/NTFS volume on several servers.”** Stop independent writers unless the complete filesystem/application coordination model supports them.
- **“RWO means exactly one pod.”** Distinguish node-based access from supported ReadWriteOncePod enforcement; inspect actual CSI capabilities.
- **“S3 means eventual consistency/no rename.”** Resolve provider and bucket type. AWS general-purpose, directory, table, and vector buckets have different contracts.
- **“A snapshot is our backup.”** Identify shared failure domains, app consistency, independent retention, and an actual restore path.
- **“A second data center solves disasters.”** Determine which copy is current, who can promote it, which side may write during a partition, and how failback avoids divergence.
- **“A new VM can attach the disk immediately.”** Verify location constraints, old-writer exclusion, control-plane reachability, mount recovery, credentials, and application startup.
- **“Self-hosted storage is cheaper.”** Include replicas, traffic, idle headroom, operators, recovery time, replacements, upgrades, and tested backups.

## Scope boundaries

Explain architecture across vendors without pretending to implement every product. Route deep database replication, filesystem internals, platform security, or provider provisioning to their corresponding expertise after settling the storage contract. Do not treat SQL/KV/vector APIs, messaging logs, block devices, shared files, and S3 as interchangeable persistence interfaces. Use current primary evidence for capabilities, and label proposed designs as engineering judgments.
