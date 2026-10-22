# Architecture Recipes

Evidence checked: 2026-10-21. Treat these recipes as illustrative starting points with explicit assumptions, not availability guarantees. Substitute measured workload, topology, failure behavior, and current provider contracts before implementing.

## Contents

- [Use the recipes](#use-the-recipes)
- [One reliable workstation or NAS](#one-reliable-workstation-or-nas)
- [Two physical servers and an independent witness](#two-physical-servers-and-an-independent-witness)
- [Three hosts with local storage](#three-hosts-with-local-storage)
- [Replaceable cloud VM with persistent block storage](#replaceable-cloud-vm-with-persistent-block-storage)
- [Small Hetzner application and database deployment](#small-hetzner-application-and-database-deployment)
- [Legacy application requiring shared NFS files](#legacy-application-requiring-shared-nfs-files)
- [Site-local clusters with asynchronous DR](#site-local-clusters-with-asynchronous-dr)
- [Local compute with cloud artifacts](#local-compute-with-cloud-artifacts)
- [Primary references](#primary-references)

## Use the recipes

For the chosen design, complete a workload contract, dependency map, placement table, and failure matrix. State who owns writes, where acknowledgements become durable, which copies survive each event, how traffic finds the surviving service, and how historical data is restored. Include maintenance and a failure during repair.

Select the smallest design that satisfies the actual RPO/RTO and operational capacity. A well-tested restore from a simple system can meet a modest objective more reliably than an unfamiliar cluster with an untested promotion procedure.

## One reliable workstation or NAS

**Assume:** one user or a small team; a machine outage lasting several hours is tolerable; files need local or LAN filesystem semantics.

Use suitable local media, a supported filesystem, optional mirrors/parity for device failures, periodic integrity checking, and versioned backups to an independent destination. Add an offline or independently administered copy when production credentials must not be able to destroy all recovery points. Include permissions, application exports, and encryption keys.

**Failure:** disk redundancy may preserve service during a member failure, but the motherboard, operating system, enclosure, or shared power can still stop the whole service. A snapshot on that same pool does not survive every pool failure.

**Recovery:** replace/rebuild the host or pool, restore verified data and identities, and check client access. Choose this over a cluster when the tolerated downtime makes host failover unnecessary. Integrity checking and repair depend on the actual implementation; [OpenZFS scrub](https://openzfs.github.io/openzfs-docs/man/master/8/zpool-scrub.8.html) is one example.

## Two physical servers and an independent witness

**Assume:** the workload needs one authoritative writer and automatic failover is valuable; a third small, independently reachable system can participate in the supported design.

Use two data-bearing servers with a supported replicated-block or application-replication design. Add the product's supported witness/quorum mechanism and effective stale-writer exclusion. Separate the witness from shared host, storage, and power dependencies where the failure model requires it. A witness contributes authority, not a third payload copy.

**Failure:** after one data server is lost, the surviving current copy may serve if the protocol and fencing conditions permit it. Its subsequent loss can destroy the only current payload. A partition or witness-link transition may require the service to stop rather than promote an uncertain copy.

**Recovery:** prove ownership, re-seed the returning node, and restore redundancy before claiming normal protection. Choose manual promotion or a single server with tested restore when independent fencing/witness dependencies cannot be provided. See [DRBD quorum](https://linbit.com/drbd-user-guide/drbd-guide-9_0-en/) and [Pacemaker fencing](https://clusterlabs.org/projects/pacemaker/doc/3.0/Pacemaker_Explained/html/fencing.html).

## Three hosts with local storage

**Assume:** several workloads need storage that can move between hosts; local disks and a measured LAN are available; the team can operate a storage cluster.

Place replicas across actual hosts and design metadata/voting services independently. Reserve CPU, memory, network, and free space for repair while applications run. Select block, file, or object access according to the consumers; do not acquire unused interfaces solely because one platform offers them.

**Failure:** behavior follows the selected system's data and authority policies. Three hosts do not establish a universal “two may fail” or “one may fail” contract. With one replica per host and three required replicas, a lost host cannot be replaced by free space on the remaining two hosts alone.

**Recovery:** supply another eligible host, rebuild, verify placement and health, and test backups separately. Prefer application-native replication when only one database needs HA and a general storage cluster would add more operational dependencies than it solves. [Ceph placement](https://docs.ceph.com/en/tentacle/rados/operations/crush-map/) illustrates explicit failure-domain rules.

## Replaceable cloud VM with persistent block storage

**Assume:** one writable application filesystem; the provider supports a separately managed persistent volume and an eligible replacement VM.

Keep VM creation/configuration reproducible. Define volume deletion independently from VM replacement, identify the filesystem reliably, and mount it only after confirming the old writer is excluded. Back up the application data rather than assuming that a VM image includes every attached volume.

**Failure:** VM loss can be recoverable without restoring all bytes, but volume attachment topology, stale attachment, provider APIs, keys, and replacement compute capacity can delay service. This is restart tolerance; it does not automatically provide uninterrupted application availability or site-level recovery.

**Recovery:** create an eligible VM, attach/mount without formatting, recover the application, and validate its data. If the volume is lost, restore to a new one. Choose direct application replication when the required recovery time or failure scope exceeds this pattern. Read [cloud lifecycle and topology](cloud-lifecycle-and-topology.md).

## Small Hetzner application and database deployment

**Assume:** three application/database nodes, a modest service, application support for object storage, and a requirement to survive a selected node failure.

Keep application instances replaceable where practical. Give each database replica its own dataset on appropriate local disks or provider volumes; choose the database's synchronous/asynchronous policy, promotion authority, and client routing deliberately. Store suitable uploads/artifacts through an object API. Keep application-aware backups and required logs in an independently recoverable destination.

**Failure:** the remaining database nodes must satisfy the selected replication and authority contract; three app replicas do not compensate for one database writer with no recovery plan. Shared provider location, network, identity, or storage dependencies may affect all nodes. Object access and database references need coordinated publication and recovery.

**Recovery:** replace a node, rejoin it from the current authority, and rehearse full restoration into new resources. Prefer one database with tested backups when node HA is unnecessary. Add a shared filesystem only for an actual filesystem requirement. Use [Hetzner storage](hetzner-storage.md) for verified product capabilities and limitations; do not infer AWS feature parity.

## Legacy application requiring shared NFS files

**Assume:** the application requires concurrent file access and its documented locking/cache semantics work with the selected NFS version and implementation.

Provide an NFS service with an appropriate durable backend. If server HA is required, select a supported failover design that addresses file handles, client recovery, locks/state, identity mapping, and exclusion of the old server. A single NFS server on replicated block storage still has a server/service availability boundary.

**Failure:** data can survive while clients stall because the export service is unavailable. A new IP route or restarted Pod does not by itself restore NFS state correctly. Test actual client behavior during failure and recovery.

**Recovery:** transfer service ownership safely, validate handles and locks, then confirm application-level writes. Retain separate file/application backups. Choose a single well-managed file server with restore if its downtime is acceptable; consider application changes to object storage only when its access pattern can change. Read [file sharing and namespaces](file-sharing-and-namespaces.md).

## Site-local clusters with asynchronous DR

**Assume:** normal writes should remain site-local; a measured nonzero data-loss window and explicit disaster declaration are acceptable.

Operate independent local storage/application systems. Replicate supported logs, snapshots, or objects to the recovery site and keep historical backups. Track the newest usable recovery point, not just the last transfer start. Keep recovery compute, keys, catalog, and routing prerequisites available.

**Failure:** a WAN outage need not stop local writes, but remote lag grows. Site loss can discard acknowledged changes not yet durable at the recovery site. Promotion requires exclusion of the former writer and an explicit recovery-point decision.

**Recovery:** promote and validate, then re-seed the old site before a separate failback. Prefer periodic backup shipping if the permitted RPO/RTO makes a warm standby unnecessary. [Ceph RBD mirroring](https://docs.ceph.com/en/tentacle/rbd/rbd-mirroring/) illustrates asynchronous volume replication; [geographic DR](geo-replication-and-dr.md) covers the decision framework.

## Local compute with cloud artifacts

**Assume:** local jobs process large immutable or versioned datasets; outputs can be published through an API; WAN interruption should not corrupt authoritative data.

Keep hot working sets and scratch data near compute. Fetch inputs by immutable identity, verify them, and cache them locally. Upload outputs to new identities, validate completion, then publish the manifest or database reference. Preserve local-only outputs until remote durability is established. Keep separate backups for irreplaceable local state.

**Failure:** a warm cache may allow some work while WAN access is unavailable; a cold cache or missing credentials may stop new jobs. A write-back cache contains authoritative changes until successfully flushed, so it is not freely disposable.

**Recovery:** re-fetch reproducible inputs and reconcile incomplete output publication. Avoid synchronous remote filesystems for latency-sensitive local writes unless measurements and semantics justify them. Prefer a simple download/process/upload workflow before adding a distributed cache service. Read [caching and data movement](caching-and-data-movement.md).

## Primary references

- [OpenZFS integrity checking](https://openzfs.github.io/openzfs-docs/man/master/8/zpool-scrub.8.html).
- [DRBD replication and quorum](https://linbit.com/drbd-user-guide/drbd-guide-9_0-en/) and [Pacemaker fencing](https://clusterlabs.org/projects/pacemaker/doc/3.0/Pacemaker_Explained/html/fencing.html).
- [Ceph failure-domain placement](https://docs.ceph.com/en/tentacle/rados/operations/crush-map/) and [RBD mirroring](https://docs.ceph.com/en/tentacle/rbd/rbd-mirroring/).
- [PostgreSQL standby replication](https://www.postgresql.org/docs/current/warm-standby.html) and [PITR](https://www.postgresql.org/docs/current/continuous-archiving.html).
- [Hetzner official storage comparison](https://docs.hetzner.com/storage/general/which-storage-is-right-for-me/) and the more detailed source map in [Hetzner storage](hetzner-storage.md).
