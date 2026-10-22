# Application storage patterns

Evidence reviewed: 2026-10-21. Treat the following as engineering patterns; validate each application's documented storage contract.

## Contents

- Split application state
- Databases and embedded stores
- Virtual machines and containers
- Uploads and collaborative files
- AI, analytics and artifacts
- Logs and streams
- Make the decision
- Primary references

## Split application state

Do not force all bytes into the same storage tier. Classify each dataset:

| Data class | Authority | Normal placement | Recovery requirement |
| --- | --- | --- | --- |
| Transactional state | Database or application leader | Storage satisfying its durability/latency contract | Consistent backup plus logs/replicas as supported |
| User assets | Committed object/file versions | Shared object or file service | Referenced versions plus business metadata |
| Reproducible cache | Upstream authoritative data | Local SSD/RAM or shared cache if justified | Recreate; prevent cache loss from becoming state loss |
| Scratch/staging | Running job until committed | Local/ephemeral space | Retry/checkpoint according to job economics |
| Configuration/secrets | Versioned configuration and secret authority | Independent bootstrap path | Restore access without depending on the broken storage |
| History/audit/backup | Explicit retained generations | Separate retention/security/failure domain | Verify discoverability, keys and restore |

Use one dataset owner and one publication protocol. If database rows reference object versions, retain the relationship during backup and restoration. “The database restored successfully” is insufficient if referenced files were deleted by a separate lifecycle policy.

## Databases and embedded stores

Separate database replication from volume replication:

- Database replication understands transactions, WAL/log positions and promotion state. It can often place independent database instances on separate local or provider volumes.
- Storage replication copies block/file changes and may provide a restartable disk image. It does not independently promote a database or prove application consistency.
- Combining both can be justified for additional failures, but multiply write traffic, space, latency and recovery interactions before accepting the design.

Never run independent ordinary database servers over the same live data directory unless the database explicitly implements that shared-storage architecture. A shared filesystem and a ReadWriteMany claim do not provide database cluster coordination.

For PostgreSQL, NFS is a documented option when its required behavior is satisfied. The documented client hard-mount requirement and server stable-storage/export behavior matter. Do not claim that all network filesystems are categorically invalid for databases. Conversely, a basic NFS copy test does not validate write durability or failure behavior.

For SQLite and similar embedded stores, investigate locking, shared-memory/WAL requirements and the access architecture. SQLite explicitly warns about direct network filesystem access and unreliable locking. Prefer moving queries through an application/database service, or choose an explicitly supported replication layer. Do not disable locking to make remote access “work.”

For backups, use the database's supported consistent physical/logical backup and log-retention procedure. A filesystem copy of a running database may mix incompatible points in time. A crash-consistent volume snapshot can be useful when the engine supports recovery, but “crash-consistent” and “application-consistent” are distinct claims.

Measure synchronous commit latency using representative durable transactions, not a sequential file write with synchronization disabled. Report p95/p99 under replication and rebuild.

## Virtual machines and containers

A VM disk can be a block device, logical volume, sparse image file, or network-served image. Track the complete layering: guest filesystem, guest cache, virtual controller, hypervisor image, host filesystem/storage target, physical persistence. A flush must reach a layer that actually protects acknowledged writes.

Snapshotting several VM disks requires a defined consistency boundary. Include guest/application quiescence if required, and account for external databases and services. Long snapshot chains and growing delta files can consume headroom and affect recovery.

A container image layer is reproducible content. Its writable container layer is tied to container lifecycle; it is not a durable data plan. Put state on explicitly managed volumes or external services. Bind mounts, named volumes, CSI volumes and application object APIs have different lifecycle and failure contracts.

For a small VM cluster, compare shared block/file storage, replicated host-local volumes and application-native replication. Live migration, HA restart and cross-site recovery are separate goals: shared disks may help migration while leaving the shared array as a common dependency.

## Uploads and collaborative files

For a web app running replaceable instances, object storage plus a metadata database is often a strong starting design. Use immutable keys, explicit upload completion, signed access where appropriate, and cleanup of abandoned uploads. Keep local working space for transcoding or processing, then publish the completed version.

For collaborative file applications, inspect locking, rename, large-file edits, conflict handling, identity and version history. A file synchronization product may provide offline copies with conflict resolution; a network filesystem provides remote operations under another consistency model. Choose the behavior users need.

If legacy code requires a shared upload directory, evaluate a managed file service or an operated NAS/DFS with HA appropriate to the target. A single NFS VM on a durable volume has durable data but still has a server/endpoint outage path. A second NFS server over the same disk needs supported failover, lock recovery and fencing.

For multiple sites, separate read caching from write ownership. Route writes to the owner, partition ownership by tenant/dataset, or use an application conflict-resolution protocol. “Active-active files everywhere” is not a conflict policy.

## AI, analytics and artifacts

For model files and immutable datasets, compare:

| Access pattern | Candidate | Key measurement |
| --- | --- | --- |
| Download once, reuse on a worker | Object store plus local SSD cache | Cold-start time, cache hit ratio, eviction and aggregate egress |
| Many workers reading large shards | Parallel object range reads or parallel filesystem | Aggregate throughput, network fan-out, data loader CPU |
| Millions of small opens/stat calls | Packed indexed shards or optimized metadata filesystem | Operations per sample and metadata latency |
| Shared mutable checkpoints | Application-supported checkpoint protocol and storage | Commit consistency, partial checkpoint cleanup, restore speed |
| Cross-site dataset distribution | Immutable versions plus manifests and regional caches | Initial seeding, incremental lag and independent access |

A GPU does not make object storage inherently too slow; insufficient pipelining, serialization, tiny objects, CPU decoding or repeated cold downloads may be the bottleneck. Likewise, GPUDirect Storage changes the data path for supported stacks, not the durability or application transaction model.

For analytics tables on objects, use a table format/catalog protocol supported by the engine. Apache Iceberg exemplifies immutable data/metadata files with an atomic catalog pointer update. Protect the catalog as well as object bytes; avoid generic bucket sync that cannot preserve a consistent table generation. Verify format-version compatibility before upgrades.

A registry or artifact store may keep both blobs and metadata. Follow its supported storage driver and garbage-collection procedure. Share objects by digest only if the application's authorization and metadata model allow it. Never delete apparently unused blobs by listing alone while uploads or references can still be in flight.

## Logs and streams

Choose between local files with shipping, immutable object segments, or a replicated log service according to ordering, ingest throughput, acknowledgement and replay requirements.

Define ordering scope: per producer, partition, tenant or global. A distributed log may acknowledge after a configurable replica rule; that does not make unlimited retention or backup automatic. Object storage is useful for archived segments, but frequent small appends may require buffering or a service-specific append API.

For agents or unattended services, constrain spool growth during disconnection. Decide when to stop accepting work, shed reproducible logs, or block producers. A local queue acknowledged before replication creates a local failure exposure even when its destination is highly durable.

## Make the decision

Return a table per dataset: interface, owner, writer model, location, ack boundary, retention, recovery source and cache policy. This catches accidental use of the same storage for production state, working data and the only backup.

Reject an extra replicated layer unless it contributes a named failure protection, migration need, or operation that the application layer cannot supply more simply.

## Primary references

- [PostgreSQL filesystem and NFS requirements](https://www.postgresql.org/docs/current/creating-cluster.html#CREATING-CLUSTER-FILESYSTEM).
- [PostgreSQL replication solution comparison](https://www.postgresql.org/docs/current/different-replication-solutions.html).
- [SQLite over a network](https://www.sqlite.org/useovernet.html).
- [SQLite appropriate use cases](https://www.sqlite.org/whentouse.html).
- [Kubernetes volumes](https://kubernetes.io/docs/concepts/storage/volumes/).
- [Apache Iceberg specification](https://iceberg.apache.org/spec/).
- [NVIDIA GPUDirect Storage overview](https://docs.nvidia.com/gpudirect-storage/overview-guide/index.html).
