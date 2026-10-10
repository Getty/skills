# Select storage by workload and recovery needs

Reviewed: 2026-10-04. Read this file when choosing a storage product or reviewing a proposed architecture. Load the product-specific reference only after selecting a candidate. Recommendations below are engineering guidance; linked product capabilities are documented by Hetzner.

## Match the interface first

| Requirement | Candidate | Boundary that changes the design |
|---|---|---|
| Operating system, application working set, latency-sensitive database | Cloud server local disk, or suitable dedicated-server disks | Keep an independent recovery path; local storage is coupled to its compute host. Cloud architecture documents local NVMe storage and migration behavior. [Architecture](https://docs.hetzner.com/cloud/servers/technical-concepts/architecture/) |
| Additional filesystem capacity with an independently attachable disk | Cloud Volume | Network block storage, attached to one Cloud server at a time; no attachment to dedicated servers. [Volume FAQ](https://docs.hetzner.com/cloud/volumes/faq/) |
| Application objects, downloadable artifacts, backup repositories | Object Storage | S3 API and object semantics; suitability depends on object sizes and request pattern. [Object Storage FAQ](https://docs.hetzner.com/storage/object-storage/faq/general/) |
| Encrypted file backups or a remote file repository | Storage Box | File protocols and a restricted command environment; its underlying RAID is on one host. [Storage Box overview](https://docs.hetzner.com/storage/storage-box/general/) |
| Human file sharing, synchronization, groups and collaboration | Storage Share | Managed Nextcloud service with browser/client workflows. [Storage Share overview](https://docs.hetzner.com/storage/storage-share/general/) |
| Rebuild a Cloud server's local disk | Cloud Backup or Snapshot | Disk image protection excludes attached Volumes. [Backup/Snapshot overview](https://docs.hetzner.com/cloud/servers/backups-snapshots/overview/) |

Do not infer equivalent filesystem behavior from the fact that a client can mount a remote service. For a database, verify the application's required durability, locking, write ordering and failure handling on the actual backend. Prefer a documented application storage integration over a filesystem adapter introduced solely to imitate a local disk.

## Establish the decision inputs

Record the following before selecting a plan:

- Working-set size, growth, file/object count, object-size distribution and retention.
- Required synchronous write latency, sequential bandwidth, concurrency and peak duration.
- Whether multiple writers need shared state, or whether one writer with replicas is sufficient.
- Recovery point objective (acceptable lost work) and recovery time objective (acceptable outage).
- Which failures must be survived: process, VM, disk, host, location, account compromise or accidental deletion.
- Where clients run and how private-only servers reach remote storage endpoints.
- Required encryption, key recovery, access isolation and migration portability.

A cheap capacity tier may be a poor transaction tier. Conversely, expensive low-latency disks can waste money on archives that are never read. Separate active data, replaceable caches and recovery copies before optimizing capacity.

## Workload patterns

**PostgreSQL:** Start with a measured local-disk design when write latency matters. Consider Volumes when independent capacity and reattachment are valuable, then measure transaction latency under realistic concurrent load. Put logical dumps or physical backups and WAL archives in a separate repository. Treat a standby and a backup as separate deliverables: replication can propagate unwanted changes. Read [database recovery](database-recovery.md).

**Forgejo and registries:** Inventory repositories, database, LFS, attachments, packages, registry manifests/blobs, queues, configuration and secrets separately. Keep latency-sensitive metadata near the application. Move supported blob classes to S3 only after exercising that application's exact S3 operations. Coordinate backup boundaries across all stores; a successful VM image alone proves little about external state.

**Model weights and AI workloads:** Treat downloaded weights as versioned source artifacts and stage the active model on appropriate local storage. Keep irreplaceable fine-tuning data, checkpoints and configuration in a recoverable repository. Measure first-start downloads separately from steady-state inference. Avoid turning every model-file read into a remote object request without a demonstrated reason.

**Backups:** Choose the restore workflow before the destination. A Storage Box suits file-oriented backup tools; S3 suits tools with an object backend. Store encryption recovery material independently. Retain an independently controlled copy when account loss or malicious deletion is in scope. Read [Storage Box/Share](storage-box-share.md) and [Object Storage](object-storage.md).

## Compare performance and total cost

Use the same application dataset, transaction mix, concurrency, duration and time window for comparisons. Capture p50/p95/p99 latency, throughput, errors, CPU pressure and storage queueing. Separate warm-cache results from cold reads. Run synthetic write tests only against a clearly identified disposable file or disposable resource; never point a generic benchmark at a production block device.

Consult the live [Volume limits](https://docs.hetzner.com/cloud/volumes/overview/) before interpreting results: published IOPS and throughput are ceilings, including distinct sustained and burst values. Do not convert them into a database throughput guarantee. For Object Storage, include the minimum billable object size, retained versions, incomplete uploads and account-wide base charge in estimates. [Object Storage billing](https://docs.hetzner.com/storage/object-storage/overview/)

Compare **compute + storage + backup retention + traffic + restoration capacity + operations**, using current prices in the requested currency/tax context. Include migration cost, recovery testing and the capacity needed while old and new copies coexist. A smaller VM plus a Volume is not automatically cheaper than a larger VM with enough local disk.

## Finish with a reviewable decision

Return the chosen product per data class, rejected alternatives with the actual tradeoff, measured or unmeasured performance assumptions, backup ownership, restore order and a migration/rollback outline. Mark unknown capacity, latency and recovery time as unknown. Do not present provider redundancy as application-level recovery or promise cross-location protection without checking where every copy actually resides.
