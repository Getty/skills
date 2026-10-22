# Distributed Storage System Families

Evidence checked: 2026-10-21. Use this reference to identify architectural families before comparing products. Examples indicate a method; they are not an endorsement, a support commitment, or a statement that every edition provides every capability.

## Contents

- [Classify the architecture](#classify-the-architecture)
- [Compare representative families](#compare-representative-families)
- [Read implementation examples correctly](#read-implementation-examples-correctly)
- [Separate management from the data path](#separate-management-from-the-data-path)
- [Choose a family from the workload](#choose-a-family-from-the-workload)
- [Primary references](#primary-references)

## Classify the architecture

For each candidate, draw or describe five separate roles: client interface, namespace/metadata authority, data placement, replication or coding, and lifecycle orchestration. Determine which roles can fail independently and which must be recovered together.

“Distributed” can mean a distributed data plane, distributed metadata, a single server with remote disks, a failover pair, multiple independent services behind a namespace, or an application that replicates its own state. These arrangements have different semantics and operational responsibilities. “Software-defined” describes how control is implemented; it is not a consistency or durability guarantee.

## Compare representative families

| Family | Data path and authority | Typical fit | Main design question |
| --- | --- | --- | --- |
| NAS or file-server failover pair | Clients use NFS/SMB; an active service owns the filesystem | Shared files with established file protocol semantics | Does failover preserve protocol state, locks, identities, and a healthy independent backing store? |
| Shared block array with clustered consumers | Several initiators reach a LUN; consumers coordinate ownership | Virtualization or cluster-aware filesystems/databases | What prevents simultaneous unsafe writers, and what fails with the array? |
| Replicated block volumes | Replicate block changes among storage nodes; attach a logical volume to a consumer | VM disks and application volumes | How do promotion, fencing, attachment, and degraded writes work? |
| Unified distributed storage | Shared placement/protection substrate exposes block, file, and object services | Several storage interfaces under one operational platform | Which control planes and performance budgets are shared? |
| Scale-out distributed filesystem | Metadata and file data are served across nodes | Concurrent file access and large namespaces | Which operations serialize through metadata, and what does client caching guarantee? |
| Parallel/HPC filesystem | Clients perform parallel I/O across storage targets | Large scientific datasets and high-throughput computation | Does workload concurrency justify network, tuning, and operations complexity? |
| Large-file analytics filesystem | Replicated/coded blocks with a dedicated namespace service | Streaming/batch data processing | Are its write, append, and metadata semantics compatible with the application? |
| Distributed object store | Object API routes keys to replicated/coded data and metadata | Blobs, artifacts, backups, and API-native applications | Which consistency, S3 operations, versioning, and geographic guarantees are implemented? |
| Filesystem built over an object store | A filesystem service adds metadata and chunk mapping over object payloads | File semantics with object-backed data capacity | How are metadata and object data jointly protected and recovered? |
| Application-native replicated state | Database/log/application controls replication and consistency | Transactional or domain-specific state | Can the application own failover more effectively than transparent storage replication? |
| Federation or global namespace | Route to independently owned backends/regions | Regional autonomy, migration, or heterogeneous systems | Is the namespace merely routing, or does it enforce shared consistency? |

Treat **hyperconverged** versus **dedicated storage nodes** as deployment choices orthogonal to these families. Hyperconvergence combines compute and storage failure/load domains; dedicated nodes allow separate lifecycle and capacity planning but add network dependency and infrastructure. Neither is inherently more available without a failure model.

## Read implementation examples correctly

### Unified substrate: Ceph

Ceph exposes RBD block devices, CephFS files, and Object Gateway APIs over its RADOS substrate. Its monitors, OSDs, filesystem metadata services, and gateways have distinct roles. An internal RADOS object is not itself an S3 object contract; client-facing semantics come from the selected service. Sharing one substrate can consolidate operations while correlating outages or resource contention. [Ceph architecture](https://docs.ceph.com/en/tentacle/architecture/)

For metadata scaling, CephFS supports multiple active metadata ranks. More active ranks do not automatically accelerate one serial client's operations, and active capacity does not replace standby capacity for failure recovery. Use that distinction as a general lesson for distributed namespace designs. [CephFS multiple metadata servers](https://docs.ceph.com/en/tentacle/cephfs/multimds/)

### Replicated block: DRBD/LINSTOR and Longhorn

Treat DRBD as a block replication mechanism and LINSTOR as a resource-management layer that can provision and orchestrate storage resources. Distinguish controller metadata availability from the replicated volume's data path, and select the actual backend and redundancy arrangement explicitly. [LINSTOR guide](https://linbit.com/drbd-user-guide/linstor-guide-1_0-en/)

Longhorn illustrates Kubernetes-managed per-volume controllers and replicas. Its documentation distinguishes V1 and V2 data engines, whose prerequisites and resource behavior differ. Do not transfer engine-specific transport or performance claims to all Longhorn configurations. Replicated block storage still needs a filesystem or raw-block consumer, and an RWX file-sharing layer has its own service path. [Longhorn architecture](https://longhorn.io/docs/1.13.0/concepts/)

### File and analytics systems

Lustre is a parallel filesystem with metadata services, object storage services/targets, and clients. Treat its HPC-oriented architecture as a candidate for measured parallel I/O demand, not a default shared directory for a few small application servers. [Lustre overview](https://www.lustre.org/about/)

HDFS illustrates a large-file, streaming-oriented distributed filesystem with distinct namespace and data-node roles. Its interface and write model should be evaluated explicitly; the word “filesystem” does not establish full interchangeability with a general-purpose mounted POSIX filesystem. [HDFS architecture](https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-hdfs/HdfsDesign.html)

### Object stores and filesystems over objects

OpenStack Swift illustrates proxy-based object access with placement rings and per-policy protection choices. Garage illustrates another distributed object-store design and publishes an API compatibility matrix. Check each project's own current documentation and test required calls; do not use one vendor's comparison table as authoritative evidence about another vendor. [Swift architecture](https://docs.openstack.org/swift/latest/overview_architecture.html), [Garage internals](https://garagehq.deuxfleurs.fr/documentation/design/internals/), [Garage S3 compatibility](https://garagehq.deuxfleurs.fr/documentation/reference-manual/s3-compatibility/)

JuiceFS illustrates a filesystem that separates file metadata into a metadata engine and file payload into managed objects. It can provide filesystem semantics because it supplies additional coordination and metadata, not merely because objects are exposed through a mount. Protect both parts. Do not assume the underlying object keys are ordinary user filenames or modify managed chunks behind the filesystem. [JuiceFS architecture](https://juicefs.com/docs/community/architecture/)

Distinguish that model from a thin S3 mount adapter that maps file calls onto existing bucket operations. Both may use FUSE; FUSE alone says nothing about locking, rename atomicity, durability, or multi-client cache coherence.

### Application-native storage

A database can replicate logs and maintain transaction-aware recovery directly. PostgreSQL is one example with streaming and log-shipping standby mechanisms. This can avoid forcing all applications onto one shared filesystem, but it introduces engine-specific backup, promotion, and version requirements. [PostgreSQL standby replication](https://www.postgresql.org/docs/current/warm-standby.html)

Do not automatically replicate every database volume three times beneath three application replicas. Quantify whether both protection layers add independent benefits or mostly duplicate writes, capacity, and failure coupling. Conversely, do not remove a layer until its hardware-failure and recovery role is accounted for.

## Separate management from the data path

For each candidate, answer:

1. Can established I/O continue when the management API is unavailable?
2. Can a new client connect, resolve metadata, or obtain credentials in that state?
3. Can failed replicas be rebuilt or a new volume be provisioned?
4. Which catalog/controller database must survive to reassemble existing bytes?
5. Can the orchestrator start without the storage service it is supposed to recover?

A Kubernetes operator or CSI driver automates lifecycle; it does not by itself define data durability. An object gateway can make access scalable while remaining dependent on one metadata service. A stateless frontend is only as independent as the state it requires.

## Choose a family from the workload

Start with the smallest architecture that meets access semantics, failure tolerance, growth, and operational constraints. For immutable artifacts, consider an object API. For shared application files, evaluate file semantics and concurrent writers. For databases, compare native replication with volume-level protection. For ephemeral compute, keep authoritative data outside instance-local lifecycle unless the application deliberately rebuilds it.

Compare candidates with the same workload, acknowledgement boundary, topology, backup scope, and recovery objective. Include required host privileges, kernel/client support, license/edition, maintenance state, upgrade path, observability, and staffed expertise. Verify changing project facts before recommending a specific implementation.

## Primary references

- [Ceph architecture](https://docs.ceph.com/en/tentacle/architecture/) and [CephFS metadata scaling](https://docs.ceph.com/en/tentacle/cephfs/multimds/).
- [LINSTOR guide](https://linbit.com/drbd-user-guide/linstor-guide-1_0-en/) and [Longhorn architecture](https://longhorn.io/docs/1.13.0/concepts/).
- [Lustre overview](https://www.lustre.org/about/) and [HDFS architecture](https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-hdfs/HdfsDesign.html).
- [Swift architecture](https://docs.openstack.org/swift/latest/overview_architecture.html), [Garage internals](https://garagehq.deuxfleurs.fr/documentation/design/internals/), and [Garage API compatibility](https://garagehq.deuxfleurs.fr/documentation/reference-manual/s3-compatibility/).
- [JuiceFS architecture](https://juicefs.com/docs/community/architecture/) and [PostgreSQL standby replication](https://www.postgresql.org/docs/current/warm-standby.html).

Some linked “latest,” “stable,” or development documentation paths can move. Re-resolve the installed release before generating deployment commands or asserting feature availability.
