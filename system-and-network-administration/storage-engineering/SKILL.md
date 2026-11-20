---
name: storage-engineering
description: "Use when choosing, sizing or debugging storage — block vs file vs object, S3 vs a mounted directory, filesystems, NAS/SAN, NFS/SMB/iSCSI/NVMe-oF, RAID, replication, erasure coding, quorum and fencing, multi-site HA and DR, backups, Kubernetes CSI/PV/PVC, cloud disks, caching, migration, cost."
---

# Storage Engineering

Design storage from the application's access contract and the failures it must survive.
Once the storage contract is settled, hand deep database replication, filesystem
internals, platform security or provider provisioning to their own expertise.

## Rules and traps

1. **Separate interface, implementation, placement and guarantee.** A mounted path may be
   local, networked, object-backed, cached or transient; an S3 API says little about
   durability, consistency or geography. SQL/KV/vector APIs, messaging logs, block
   devices, shared files and S3 are not interchangeable persistence interfaces.
2. **Find the owner of each datum and each write.** Trace an acknowledgement through
   application buffers, client caches, servers, journals, replicas and durable media.
3. **Name the property and the failure domain of every protection claim.** Availability,
   durability, integrity, consistency, recoverability and security differ; replication,
   snapshots, RAID, versioning and backup cover different failure classes. Domains: drive,
   controller, host, rack, power/network, site, region, account, operator, provider.
4. **Quorum is not placement.** Separate control-plane votes from data placement and write
   acknowledgement; a witness stores votes, not necessarily recoverable user data. Never
   infer write availability from replica count alone.
5. **Prove writer exclusion before failover.** A restarted pod, moved IP, detached volume
   or deleted API object does not prove the previous writer has stopped. One ext4/XFS/NTFS
   volume mounted on several servers corrupts: stop independent writers unless the full
   filesystem and application coordination model supports them.
6. **Claim only what evidence supports.** Examples and sizing formulas are conditional
   models; never invent SLAs, prices, zones, device guarantees or achievable performance.
   Verify provider features, filesystem support, CSI behavior, release status, licenses
   and destructive commands in current primary docs, loaded when a decision depends on
   them; record service class, location, version and verification date; label designs as
   engineering judgments.
7. **Prefer the smallest operationally supportable design** meeting the stated failure and
   recovery targets; consider application-native replication before another replicated
   layer.
8. **Act in proportion to the request.** Investigate read-only first. Before formatting,
   restore overwrite, deletion, forced promotion, retention changes or repair writes,
   establish the exact target, existing authorization, recoverable copy and consequence.

## Working method

Checklists per step: [design-workflow.md](references/design-workflow.md).

1. **Workload contract.** Use the facts given, state assumptions for unknowns, ask only
   questions that change the design. For a conceptual question, teach the distinction
   without a full questionnaire.
2. **Semantics before products** — [taxonomy](references/taxonomy-and-selection.md), plus
   [file/object semantics](references/file-and-object-semantics.md) for path-vs-API
   questions. Reject candidates that miss required semantics before ranking cost or speed.
3. **Failure and recovery** — [HA](references/distributed-consistency-and-ha.md),
   [multi-site](references/geo-replication-and-dr.md). Include asymmetric partitions, a
   second failure during recovery, and explicit failback ownership.
4. **Normal, degraded and recovery sizing.** Execute
   [storage_budget.py](scripts/storage_budget.py) for capacity and transfer arithmetic:
   planning math, never proof of quorum, placement, rebuild completion or availability.
5. **Platform** — for Kubernetes read both Kubernetes entries below. Recheck the exact
   region, resource type, attachment rules, backup inclusion, network path and lifecycle
   before giving executable provisioning steps.
6. **Testable decision** — when useful, fill
   [architecture-brief.md](assets/architecture-brief.md) and
   [failure-matrix.csv](assets/failure-matrix.csv).

Troubleshooting: preserve evidence, narrow the failing layer, change one cause at a time,
verify application behavior.

## Reference router

Read only the entries the problem needs.

- [A common belief to check ("mounted = disk", "3 copies = HA", "snapshot = backup")](references/diagnostic-shortcuts.md)
- [Complete technology map and first selection](references/taxonomy-and-selection.md)
- [Mounted path versus API; POSIX, rename, locks, fsync](references/file-and-object-semantics.md)
- [S3 operation, compatibility, multipart, versions, event handling](references/object-storage-and-s3.md)
- [Drives, controllers, volume managers, local filesystems](references/local-media-and-filesystems.md)
- [DAS/NAS/SAN, iSCSI, FC, NVMe-oF, multipath](references/block-and-network-protocols.md)
- [NFS, SMB, distributed namespaces and object-backed filesystems](references/file-sharing-and-namespaces.md)
- [RAID, copies, EC, checksums and failure-domain placement](references/data-protection-and-placement.md)
- [Consistency, votes, leases, fencing, partitions and two-node designs](references/distributed-consistency-and-ha.md)
- [WAN replication, stretched clusters, DR, active-active and failback](references/geo-replication-and-dr.md)
- [Architecture families and implementation examples](references/distributed-system-families.md)
- [Backup methods, immutable/offline copies, PITR and restore](references/backup-and-restore.md)
- [Kubernetes storage contracts and CSI lifecycle](references/kubernetes-storage.md)
- [Kubernetes application patterns and cluster recovery](references/kubernetes-recovery-and-patterns.md)
- [Instance/volume lifetime, placement and cloud control planes](references/cloud-lifecycle-and-topology.md)
- [Hetzner Cloud/dedicated/Volumes/Box/Share/Object Storage](references/hetzner-storage.md)
- [AWS, Azure, GCP and other provider capability families](references/provider-service-matrix.md)
- [Database, VM, uploads, artifact, AI and analytics patterns](references/application-storage-patterns.md)
- [Cache authority, tiers, gateways, synchronization and transfer](references/caching-and-data-movement.md)
- [Performance measurement, queueing, rebuilds and cost](references/performance-and-sizing.md)
- [Calculator inputs, formulas, limitations and worked examples](references/capacity-and-recovery-models.md)
- [Read-only investigation and operational runbooks](references/operations-and-troubleshooting.md)
- [Identity, encryption, tenant isolation, retention and deletion](references/security-and-tenancy.md)
- [Tape/HSM, HPC, content-addressed storage, memory and emerging methods](references/specialized-storage.md)
- [Small-server, limited-cloud, hybrid and multi-site architectures](references/architecture-recipes.md)
- [Conversion, cutover, semantic tests and recovery acceptance](references/migration-and-validation.md)
- [Evidence discipline, capability lookup and terminology](references/sources-and-glossary.md)
