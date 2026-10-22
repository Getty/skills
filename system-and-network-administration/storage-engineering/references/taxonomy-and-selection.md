# Storage taxonomy and selection

Evidence reviewed: 2026-10-21. Treat this as a method map, not a claim that every product implements every method.

## Contents

- Classify the service on independent axes
- Recognize the interface families
- Recognize implementation and placement families
- Match the workload
- Run the selection process
- Primary references

## Classify the service on independent axes

Describe a candidate as a tuple, for example: “single-writer block volume; network attached; provider replicated within one location; filesystem owned by one VM; independently backed up.” Calling it “cloud storage” loses almost all useful information.

| Axis | Questions to resolve |
| --- | --- |
| Application interface | Bytes/blocks, files/directories, objects, records/queries, append log, or memory addresses? |
| Physical location | Same process, host, enclosure, LAN, fabric, data center, WAN, or offline medium? |
| Authority | Which copy is authoritative, and which is a cache, replica, staging area, or backup? |
| Concurrency | One writer, coordinated cluster writers, independently mergeable writes, or conflict-prone shared mutation? |
| Consistency | When are writes visible; what is atomic; what survives a crash? |
| Protection | Checksums, redundant fragments, copies, retained history, offline/independent recovery? |
| Placement | Which named drive/host/rack/site/account failures leave sufficient data and control services? |
| Lifecycle | Which stop/reboot/delete/recreate operations retain the data? |
| Management | Local administration, software-defined cluster, managed service, appliance, or outsourced backup? |
| Economics | Allocated versus used bytes, requests, throughput/IOPS, retrieval, network, replicas, operational labor? |

Keep availability and persistence independent. A RAM cache may be highly available but disposable. An unplugged backup disk may preserve data while providing no online access. A provider volume may survive a VM deletion but still be unavailable outside its location.

## Recognize the interface families

| Family | What the application sees | Typical strengths | Main compatibility boundary |
| --- | --- | --- | --- |
| Block | An addressable device or virtual disk | Existing filesystems, databases, VM disks, low-level control | Filesystem ownership and write ordering remain above it |
| File | Paths, directories, handles, metadata | Legacy applications, shared workspaces, ordinary file tools | Exact locks, rename, cache, ACL and durability semantics vary |
| Object | Named/versioned blobs plus metadata through an API | Immutable assets, datasets, backups, direct client transfers | General-purpose object APIs do not provide the complete file-operation contract |
| Record/database | SQL, document, key/value, graph, time-series, vector or transactional operations | Querying, indexes, coordinated updates, constraints | Backup/replication and schema contracts belong to the database |
| Append log/stream | Ordered records, offsets and retention | Ingestion, event history, replay | Ordering scope, retention and acknowledgement differ from arbitrary file access |
| Memory/byte addressable | Process or device memory mappings | Very low latency, specialized persistence | Volatility, persistence ordering and software compatibility must be explicit |
| Archive | Retrieval jobs, tape catalogs, offline media | Long retention, offline isolation, low media cost | Restore time and reader/catalog availability dominate |

An API may expose several families. Ceph can underpin block, file, and object services; that does not make all three interfaces semantically equivalent. An “object-backed filesystem” can implement stronger file behavior by adding metadata coordination. Its metadata service then becomes part of availability and recovery.

Treat a bucket mount and a filesystem built on objects as distinct designs. A lightweight mount translates operations onto existing object keys; a full filesystem may maintain inodes and chunks whose raw bucket contents are not meaningful original files.

## Recognize implementation and placement families

Use this checklist to avoid reducing the answer to “NAS or S3.”

| Method group | Methods to recognize | What it changes |
| --- | --- | --- |
| Direct media | HDD, SATA/SAS SSD, NVMe, removable USB, optical, tape, persistent memory | Latency, endurance, access pattern, replacement and portability |
| Local organization | Partitions, volume managers, pooling, thin provisioning, local filesystems | Allocation and administration; pooling alone supplies no redundancy |
| Local protection | Mirrors, parity RAID, nested RAID, copy-on-write, checksums, scrub, spare drives | Device-failure tolerance and integrity inside one system |
| Block networks | iSCSI, Fibre Channel, NVMe over TCP/RDMA/FC, multipath | Remote device access and path redundancy; not shared-filesystem safety |
| File networks | NFS, SMB, pNFS, NFS over RDMA, SMB Direct | Shared namespace, identity and protocol-level coordination |
| User-space and gateways | FUSE/WinFsp, SSHFS, WebDAV, file/object gateway | Compatibility and caching; the gateway adds its own failure boundary |
| Distributed storage | Sharding/striping, replication, EC, placement maps, replicated metadata | Scale and protection across machines |
| Cluster filesystems | Shared-disk filesystems with distributed locks; shared-nothing filesystems | Who coordinates metadata and concurrent block ownership |
| Storage layout | Scale-up arrays, scale-out clusters, hyperconverged and disaggregated storage | Compute/storage coupling, operational complexity, contention |
| Replication | Synchronous, asynchronous, semi-synchronous, chain/cascade, log shipping, snapshot shipping | Write latency, acknowledged durability and lag |
| Multi-site | Stretched quorum, site-local clusters with DR, application replication, regional sharding, active-active | Partition behavior, geography and authority |
| Caches and tiers | Read-through, write-through, write-back, CDN, burst buffers, hot/cold tiering, HSM | Data locality, acknowledgement and recall latency |
| History/recovery | Snapshots, clones, full/incremental/differential backup, PITR, immutable/offline copies | Recovery from deletion, corruption and compromise |
| Data motion | File sync, rsync-style deltas, block snapshot streams, API copies, export/import, physical seeding | Migration consistency, transfer volume and downtime |
| Specialized | HPC parallel filesystems, object-backed analytics tables, content addressing, P2P, GPU direct I/O, zoned devices | Workload-specific access and deployment requirements |

Do not confuse striping with protection, deduplication with backup, compression with guaranteed capacity, multipath with independent replicas, or a global namespace with geographically local durable data.

## Match the workload

| Workload | Usually evaluate first | Reject or qualify |
| --- | --- | --- |
| Transaction database | Local or network block; validated file service; database-native replication | Generic bucket mounts; independent database processes writing one data directory |
| User-upload web application | Object API plus metadata database and optional CDN | Local-only uploads when instances are replaceable |
| Legacy shared workspace | Managed/shared file service or distributed filesystem | Object API unless the app can change; sync clients as automatic locking substitutes |
| VM disks | Block storage or explicitly supported virtual disk file service | Uncoordinated multi-mount; assuming a crash snapshot is an app-consistent backup |
| Training data/model artifacts | Immutable object datasets plus local caching; parallel filesystem if measured need | Millions of tiny remote opens without measuring metadata/request overhead |
| Backup repository | Repository-compatible file/object target with independent retention and keys | Treating a production snapshot in the same account as the only recovery path |
| Scratch/cache | Local instance disk, temporary block or RAM when affordable | Paying for cross-site synchronous replicas for reproducible bytes by habit |
| Offline branch/site | Local authority with explicit synchronization/merge policy | A mandatory low-latency WAN round trip for every ordinary operation |
| Multi-region business records | Application/database topology with clear write ownership | Stretching a generic filesystem simply to avoid defining conflicts |

These are starting hypotheses. A database vendor may support particular NFS deployments, and an object-native database may deliberately use object storage. Decide from the application's documented contract, not its category label.

## Run the selection process

1. Split authoritative, reproducible and historical data. A single application may need three different storage methods.
2. List operations whose failure would corrupt behavior, such as conditional create, atomic publish, fsync, file locking or cross-record transaction.
3. Define one or two realistic failure targets and business RPO/RTO. Add maintenance/rebuild headroom.
4. Eliminate semantic mismatches. Compare two or three remaining designs on measured latency and total cost.
5. Draw the ownership path from application to media and the dependency graph needed to restore.
6. Verify provider facts and software support. Validate a representative application operation, a realistic failure, and a restore.
7. Document what is intentionally not protected and what would justify adding another layer later.

For a three-machine design, explicitly ask whether those are independent physical hosts or VMs on unknown placement, whether every node stores a full copy, where metadata/votes live, and whether the surviving machines have enough capacity and I/O for recovery.

## Primary references

- [Linux filesystem documentation](https://docs.kernel.org/filesystems/index.html): local filesystem and interface families.
- [Ceph architecture](https://docs.ceph.com/en/latest/architecture/): one distributed substrate with distinct service interfaces.
- [AWS S3 overview](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html): object API and bucket-type distinctions.
- [JuiceFS architecture](https://juicefs.com/docs/community/architecture/): separate file metadata and object data.
- [Kubernetes storage overview](https://kubernetes.io/docs/concepts/storage/): orchestration vocabulary; load the dedicated Kubernetes references for details.
