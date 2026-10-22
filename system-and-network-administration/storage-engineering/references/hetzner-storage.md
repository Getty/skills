# Hetzner storage: available building blocks and architecture choices

Evidence checked: 2026-10-21 against official Hetzner documentation and the official CSI repository. Product limits, encryption defaults, supported S3 actions, topology and driver capabilities can change. Recheck the linked source before provisioning or promising a capability.

## Contents

- [Distinguish the products](#distinguish-the-products)
- [Use Cloud Volumes deliberately](#use-cloud-volumes-deliberately)
- [Treat S3 compatibility as a feature matrix](#treat-s3-compatibility-as-a-feature-matrix)
- [Use Storage Box and Storage Share for the right contract](#use-storage-box-and-storage-share-for-the-right-contract)
- [Design Kubernetes storage](#design-kubernetes-storage)
- [Combine cloud, dedicated machines, and locations](#combine-cloud-dedicated-machines-and-locations)
- [Choose a concrete starting architecture](#choose-a-concrete-starting-architecture)
- [Primary references](#primary-references)

## Distinguish the products

| Building block | Access and ownership | Good starting use | Boundary to preserve |
| --- | --- | --- | --- |
| Cloud server root/local disk | Guest filesystem on instance storage | OS, application state with its own replication/backup, cache | Coupled to server lifecycle; verify rebuild, resize and deletion behavior |
| Cloud Volume | Managed network block device | Per-server or per-pod persistent dataset | Single attachment; not a shared file namespace |
| Dedicated server disks | Operator-controlled local disks | Storage nodes, databases, ZFS/RAID, predictable media layout | Operator owns disk failure, placement and restore design |
| Object Storage | S3-compatible bucket API | Objects, media, archives, supported backup software | Exact API compatibility and site protection must be checked |
| Storage Box | Remote file/backup protocols | Backup repositories and file transfer/sharing | File-service latency and single-host failure scope |
| Storage Share | Managed Nextcloud service | Human file sync and collaboration | Application-level collaboration service, not generic database storage |

Hetzner has both managed block and object storage. The relevant question is which contract and failure scope it provides, and which responsibilities remain with the operator. Do not describe its catalog as “only local disks,” or treat its products as interchangeable AWS replacements.

## Use Cloud Volumes deliberately

The official FAQ currently describes NVMe-backed network block storage with three copies on different physical servers, one attached cloud server at a time, a 10 GB–10 TB size range, and up to 16 attached Volumes per server. It supports growth rather than shrinking and does not directly attach to dedicated root servers [H1]. Treat those as dated limits; use the API/account limits when implementing.

Automatic creation/mounting can format a new Volume and create a guest mount; manual mode leaves that work to the operator [H2]. For an existing dataset, identify the device and filesystem before taking any formatting action. Capacity growth needs the appropriate guest filesystem expansion. Use mount points for filesystem growth commands when the filesystem's tooling requires them; do not blindly copy an illustrative device-path command.

The official Hetzner Cloud Python client documents that a Volume attaches only to a server in the same location [H17]. Before failover, compare the actual Volume and replacement server location and recheck the current attach contract; do not infer cross-location movement from a shared Cloud Network. A private network is not a block-storage migration feature.

The provider's three copies address specified hardware failures. They do not provide independent historical recovery or prove a separate-site copy. Hetzner's server Backups and Snapshots capture the server disk and explicitly exclude attached Volumes [H3]. The storage comparison currently lists no native Volume snapshots [H4]. Back up Volume data through the application or an appropriate file/block backup process, and test restoration to a newly created Volume.

Note an official-documentation inconsistency when evaluating databases: the storage comparison cautions against database use over network storage, while the dedicated Block Storage product page lists databases as a use case [H4, H16]. Do not turn either statement into a universal technical rule. Verify the database's durability requirements, flush behavior and measured latency on the selected setup; obtain provider clarification if a contractual guarantee is needed.

Separate deletion lifecycles. Hetzner documents server-bound Backups being removed with the server, while Snapshots are managed separately [H5]. Volumes are separately managed resources with explicit detach/delete operations [H6]. Check the actual console/IaC/CSI workflow: automation may delete data resources even when their API lifetime is otherwise independent.

## Treat S3 compatibility as a feature matrix

Object Storage is a stand-alone bucket service with location-specific endpoints. Current endpoints are documented for Falkenstein, Nuremberg and Helsinki [H7]. The FAQ states that a bucket's data resides in a single data center at the selected location and is erasure-coded across storage servers. It also states that objects have no default at-rest encryption; SSE-C is an available option [H8]. Recheck both claims before selecting a protection or encryption design.

The supported-actions page currently lists important exceptions to AWS parity, including native replication, notifications and several management features. It documents SSE-C as the supported server-side encryption mode, same-bucket-only `CopyObject`, and a limitation for conditional PUT/DELETE on versioned buckets. Versioning and Object Lock have their own documented procedures [H9].

Translate these capabilities into design consequences:

- For a second-site copy, verify a supported external replication/backup process rather than assuming S3 replication configuration works.
- For lock-based backup software, validate actual retention modes, credentials, version behavior and restore/prune operations with the selected client.
- For application concurrency, test the exact conditional request against the intended bucket configuration. A successful simple upload is not a compatibility test.
- For encryption, identify key custody, availability and restore requirements. Losing a customer-held key can make healthy stored bytes unusable.
- For moves/copies, inspect the exact operation and endpoints instead of assuming that every AWS CLI convenience command maps to a supported server-side action.

Object immutability as an access model means no arbitrary in-place byte editing of an object; it does not by itself mean WORM retention. A new PUT may replace the current value of a key. Configure and validate Object Lock separately when deletion prevention is required. An S3 filesystem adapter still needs application-semantic testing.

## Use Storage Box and Storage Share for the right contract

Storage Box exposes FTP/FTPS, SFTP/SCP, SSH-based rsync/BorgBackup, SMB/CIFS, and HTTPS/WebDAV, with protocol activation and connection-port distinctions documented in the access overview [H10]. Prefer an appropriately encrypted/authenticated transport. Do not invent an NFS export or root shell capability because the service has SSH access.

The Storage Box overview describes RAID-protected disks on one host, with checksums for corruption detection/correction [H11]. This can be a useful backup destination, but RAID on one host is not a distributed HA file cluster. For the fault model requiring loss of that host, location, account or administrator, retain another appropriately independent copy.

Storage Box snapshots are useful historical points with their own retention and capacity effects; confirm whether the credentials an attacker could obtain can alter them. Storage Share is a Nextcloud-based collaboration service [H12]. Select these according to the application contract, rather than taking “can mount it” as proof of safe database storage.

For a backup repository, verify the backup application's support for the chosen remote protocol, repository locking, atomic operations, resume behavior, consistency checks, and pruning. Transfer a realistic recovery sample to a clean machine. A directory listing alone does not validate a backup.

## Design Kubernetes storage

The official Hetzner CSI driver integrates Cloud Volumes and advertises RWO use [H13]. Pin a supported driver release and inspect its StorageClass, topology reporting, expansion, filesystem, attachment and snapshot support. The presence of a Kubernetes snapshot CRD or snapshot-related RBAC does not prove that the backend can take snapshots.

Choose among distinct patterns:

| Requirement | Candidate | Remaining responsibility |
| --- | --- | --- |
| One writable filesystem with restart tolerance | Cloud Volume through CSI | Data backup, detach/fencing, eligible replacement node |
| Highly available database | Database-native replicas on separate nodes and datasets | Quorum/promotion, client routing, replication policy, PITR |
| Shared uploads readable by many pods | Direct Object Storage integration | Object/metadata publication and API compatibility |
| Existing application needs RWX | Self-managed supported file service or another managed file offering | File semantics, server HA, locks, permissions and restore |
| Many workloads require distributed block/file/object | Dedicated storage nodes with an appropriate storage system | Full storage-cluster operations and capacity planning |

Do not mount one ext4/XFS block filesystem read-write on several nodes. Do not turn an S3 bucket or Storage Box into a database backend merely to obtain an RWX label. When using a replicated storage layer above Cloud Volumes, calculate duplicated redundancy and identify an additional failure that the extra layer actually covers.

## Combine cloud, dedicated machines, and locations

Cloud Networks are routed private networks; documented network zones constrain where a network and its subnets can span. Coupling to a dedicated-server vSwitch is supported only for the documented European network zone [H14]. Verify MTU, routing, firewalls, throughput and the exact link to each storage node. Connectivity does not establish acceptable synchronous-write latency.

Spread placement groups separate cloud VMs across physical hosts; they do not by themselves promise rack, data-center or region independence [H15]. Use such groups for host-level separation, and document broader placement requirements separately.

For geographically separate locations, compare site-local clusters with asynchronous DR against a stretched synchronous system. Quantify WAN RTT, jitter, recovery traffic, quorum/witness placement and what either site does during a partition. Avoid promising continued writes in both isolated sites for one strictly ordered dataset without a supported conflict/consensus design.

## Choose a concrete starting architecture

For a small service, begin with replaceable application instances, a clearly chosen database storage/replication strategy, object storage for bulk objects where the application supports it, and an independent backup destination. Add a self-managed shared filesystem only when the workload requires its semantics.

For several dedicated machines, compare application-native replication against a storage cluster before buying redundancy twice. For a mixed local/cloud environment, keep latency-sensitive writes near their authoritative storage and move backups, objects or application replication asynchronously where the requirements allow it.

For site disaster recovery, record four separate deliverables: recoverable data in another fault domain, access to keys and metadata, enough replacement compute/network capacity, and a tested promotion/restore/failback procedure. A remote bucket or additional VM alone satisfies only part of that plan.

## Primary references

- **H1:** [Cloud Volumes FAQ](https://docs.hetzner.com/cloud/volumes/faq/).
- **H2:** [Cloud Volumes overview](https://docs.hetzner.com/cloud/volumes/overview/).
- **H3:** [Server Backups/Snapshots overview](https://docs.hetzner.com/cloud/servers/backups-snapshots/overview/).
- **H4:** [Storage product comparison](https://docs.hetzner.com/storage/general/which-storage-is-right-for-me/).
- **H5:** [Backups/Snapshots FAQ](https://docs.hetzner.com/cloud/servers/backups-snapshots/faq/).
- **H6:** [Resource cancellation and deletion](https://docs.hetzner.com/general/billing-and-account-management/cancellation/cancellations-hetzner-console/).
- **H7:** [Object Storage overview and endpoints](https://docs.hetzner.com/storage/object-storage/overview/).
- **H8:** [Object Storage FAQ: placement, redundancy and encryption](https://docs.hetzner.com/storage/object-storage/faq/general/).
- **H9:** [Supported S3 actions and exceptions](https://docs.hetzner.com/storage/object-storage/supported-actions/).
- **H10:** [Storage Box protocol access](https://docs.hetzner.com/storage/storage-box/access/access-overview/).
- **H11:** [Storage Box overview](https://docs.hetzner.com/storage/storage-box/general/).
- **H12:** [Storage Box versus Storage Share](https://docs.hetzner.com/storage/storage-box/faq/storage-box-vs-storage-share/).
- **H13:** [Official Hetzner CSI driver](https://github.com/hetznercloud/csi-driver).
- **H14:** [Cloud Networks FAQ](https://docs.hetzner.com/networking/networks/faq/).
- **H15:** [Placement groups FAQ](https://docs.hetzner.com/cloud/placement-groups/faq/).
- **H16:** [Block Storage product page and database use cases](https://www.hetzner.com/cloud/block-storage/).
- **H17:** [Official Hetzner Cloud Python Volumes client](https://hcloud-python.readthedocs.io/en/latest/api.clients.volumes.html): same-location attachment contract.

Use the cited product contracts for facts. Treat the architecture choices and decision tables as engineering recommendations to be checked against workload measurements and the actual account topology.
