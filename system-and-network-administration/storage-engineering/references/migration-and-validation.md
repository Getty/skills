# Migration and Validation

Evidence checked: 2026-10-21. Use this reference when changing devices, filesystems, storage protocols, providers, replication layouts, or application storage models. Treat the migration as a change in data authority and semantics, not only a byte transfer.

## Contents

- [Classify the migration](#classify-the-migration)
- [Inventory what must survive](#inventory-what-must-survive)
- [Choose the transfer and consistency boundary](#choose-the-transfer-and-consistency-boundary)
- [Plan copy, catch-up, and cutover](#plan-copy-catch-up-and-cutover)
- [Define rollback after new writes](#define-rollback-after-new-writes)
- [Run semantic probes](#run-semantic-probes)
- [Validate recovery and finish](#validate-recovery-and-finish)
- [Primary references](#primary-references)

## Classify the migration

| Migration | What changes | Required validation |
| --- | --- | --- |
| Block copy / volume replacement | Device or provider beneath a filesystem/application | Complete consistent image, geometry/size, identifiers, encryption, durability, attachment behavior |
| File copy / filesystem conversion | Namespace representation or filesystem features | File data plus names, ownership, metadata, links, permissions, and application behavior |
| Object-store migration | Endpoint, API implementation, bucket policies, or object layout | Payload, versions, metadata, retention, request semantics, identity and encryption |
| Application-native migration | Database engine/version/topology or data model | Logical/physical compatibility, schema and omitted objects, ordering, transaction boundaries |
| File-to-object conversion | Access contract and application code | Publication, addressing, concurrency, updates, listing, deletion, and cross-store consistency |
| Repartitioning / protection change | Placement, sharding, replica count, or EC layout | Reachable current data throughout movement, remaining fault tolerance, repair capacity |

A transparent block move may preserve filesystem semantics while changing flush latency or failure behavior. A file-to-S3 move requires explicit application redesign unless a suitable additional filesystem layer supplies the missing semantics. A mount adapter alone does not establish equivalence.

## Inventory what must survive

Record the authoritative source, destination, workload owners, write paths, data size/count, churn, largest objects, and acceptable downtime. Include hidden dependencies and a recoverable pre-migration point.

| Scope | Inventory beyond payload bytes |
| --- | --- |
| Block | Partition layout, filesystem identity/UUIDs, boot dependencies, volume labels, encryption headers/keys, trim/thin allocation assumptions, snapshot/clone lineage |
| Files | UID/GID or SID mappings, ACLs, xattrs, timestamps, hard links, symlinks, sparse extents, special files, case behavior, Unicode naming, alternate streams where relevant |
| Objects | Every required version and delete marker, tags, content type/cache headers, user metadata, encryption and keys, checksums, retention/legal holds, lifecycle, ownership, policies |
| Applications | Schema, extensions/plugins, sequences/counters, roles, credentials, jobs, logs, transaction IDs, external object references, queues, compatibility requirements |
| Operations | Monitoring, backup catalog, restore tooling, endpoint/DNS behavior, connection pools, retained old copies, and cancellation/deletion automation |

Mark unsupported features and choose an explicit conversion, archival, or application-change policy. Do not silently drop metadata because the destination cannot represent it. A raw clone can duplicate identifiers; avoid exposing two indistinguishable devices or duplicated server identities to automation.

For object migration, distinguish copying current objects from preserving history. A convenience “sync” operation may omit versions or delete markers. Ordinary S3 copies allocate destination version IDs; keep a source bucket/key/version to destination bucket/key/version mapping and update application references or restore catalogs accordingly. Server-side copy can alter system metadata, and endpoint compatibility controls whether cross-bucket or multipart operations work at all. [Amazon S3 copy documentation](https://docs.aws.amazon.com/AmazonS3/latest/userguide/copy-object.html) illustrates why metadata and operation choice require inspection.

## Choose the transfer and consistency boundary

Prefer a documented native migration/backup/replication mechanism for live application state. A filesystem snapshot can provide a stable source, but confirm that all relevant volumes and application recovery logs are included. An ordinary live directory copy can combine different points in time.

For file copying, explicitly select the metadata preservation features required by the inventory. Do not assume a generic archive flag preserves every ACL, xattr, hard link, or sparse-file property. Rsync documents distinct options and distinguishes its ordinary size/time quick check from stronger content checking. Verify the exact versions and options on both ends. [rsync manual](https://download.samba.org/pub/rsync/rsync.1)

For database logical migration, list objects excluded by the replication mechanism. For example, PostgreSQL's documented logical replication restrictions include schema/DDL and sequence state, which require separate handling for a writable cutover. [PostgreSQL logical replication restrictions](https://www.postgresql.org/docs/current/logical-replication-restrictions.html)

For incremental streams, preserve the required base snapshot, lineage, logs, and metadata until completion is verified. A missing common ancestor can require a new full transfer. Retain the source snapshot for the duration needed by the specific send/receive protocol rather than pruning it according to an unrelated schedule.

## Plan copy, catch-up, and cutover

1. **Prepare:** verify capacity, credentials, encryption, compatibility, recovery access, and explicit acceptance criteria. Keep the destination isolated from production writes.
2. **Seed:** copy a consistent baseline and retain an inventory of objects/files and verification results. Throttle against actual workload latency and failure-repair reserves.
3. **Track changes:** use a documented log/change mechanism or repeated consistent deltas. Define treatment of creates, updates, deletes, renames, and permission changes.
4. **Catch up:** measure outstanding changes and destination replay, not only transfer bandwidth. If effective catch-up throughput cannot exceed incoming churn, arrange a write pause or change the transfer approach.
5. **Quiesce:** stop new source writes, drain background jobs/queues as needed, and capture the final consistent boundary. Include out-of-band clients and scheduled jobs.
6. **Finish and verify:** transfer/replay the final tail, verify the destination at that boundary, and account for unknown or in-flight client operations.
7. **Transfer authority:** fence or revoke the source writer through the appropriate service/storage mechanism. DNS changes and load-balancer routing alone do not stop old clients from writing.
8. **Enable destination traffic:** start the intended write authority, reconnect clients, invalidate incompatible caches, and check application outcomes.
9. **Observe:** retain source evidence and the agreed rollback/reconciliation path until acceptance criteria are met.

Do not improvise dual writes as a low-downtime shortcut. A write can succeed on one backend and fail on the other; retries, ordering, deletes, and concurrent writers then diverge. Use a documented application protocol with durable change capture, idempotency, reconciliation, and clearly owned authority if dual operation is genuinely required.

## Define rollback after new writes

Before the destination accepts writes, rollback can often mean abandoning the destination and reopening the unchanged source after verifying authority. Once destination-only writes exist, returning traffic to the old source can discard them.

Choose the later rollback policy before cutover: supported reverse replication, application reconciliation, an explicit export of the destination tail, or restoration to a newly selected authoritative system. Document unsupported reverse schema changes and the point after which forward repair is safer. Preserve both histories when conflicts remain unresolved.

Keep old data read-only or otherwise fenced while retained. An accidentally resumed scheduler or old application process can create a second writer without any administrator intentionally initiating rollback. Delete old resources only after acceptance, backup/restore validation, and the retention decision are complete.

## Run semantic probes

Run bounded probes in a disposable or isolated representative environment. Select probes that address actual migration risks; do not fault-inject into production by default. Record each expected outcome before running it.

| Probe | Observe | Acceptance question |
| --- | --- | --- |
| Durable write followed by abrupt process/host loss | Successful, failed, and unknown writes; replay behavior | Do acknowledged operations survive the promised failure boundary? |
| Client/network partition during a write | Timeouts, retries, duplicate effects, recovery | Can clients reconcile unknown outcomes without corrupting or duplicating data? |
| Old owner resumes after failover | Rejected writes, tokens/leases, fencing | Is stale write authority effectively excluded? |
| Concurrent writers and stale locks | Lock acquisition, expiry, release, cache coherence | Does the real application retain its required coordination semantics? |
| Atomic publication / rename | Readers during replace/publish; directory and object behavior | Do readers see only permitted old/new states, including after a crash? |
| Conditional update conflict | Two writers using the same expected version | Does the required precondition reject the stale update? |
| Copy/checksum comparison | Known-content bytes at source and destination | Are algorithms and comparison boundaries compatible, rather than assuming ETag equals MD5? |
| Metadata and naming round trip | ACLs, links, case collisions, Unicode, timestamps | Are required attributes preserved or explicitly converted? |
| List/read-after-write and cache expiry | Multiple clients, new/deleted objects, cached names | Does visibility satisfy the actual application contract? |
| Full/reduced-capacity destination | Error propagation, cleanup, repair reserve | Does failure remain controlled without silently losing accepted writes? |

A single successful upload or mount is insufficient validation of a storage interface. If a feature is unsupported, redesign the workflow and test the new contract instead of masking the failure with retries.

## Validate recovery and finish

Compare counts, sizes, content hashes where meaningful, sampled and high-risk metadata, and application invariants. Distinguish compressed/encrypted representations from logical contents when selecting hashes. Record explained differences rather than accepting matching totals as full proof.

Restore a destination backup into clean resources and run representative application reads and writes. Check keys, roles, external object references, log continuity, and recovery timing. Confirm that new backups protect the new authority and old retention policies cannot unexpectedly delete the only required lineage.

Finish with a migration record: authoritative endpoint, cutover boundary, validation evidence, known differences, retained source resources, rollback/reconciliation limit, and ownership of remaining cleanup. Keep throughput benchmarks subordinate to correctness and recoverability.

## Primary references

- [rsync manual](https://download.samba.org/pub/rsync/rsync.1): copy comparison and metadata controls.
- [Amazon S3 copy documentation](https://docs.aws.amazon.com/AmazonS3/latest/userguide/copy-object.html): object-copy semantics and metadata considerations.
- [S3 CopyObject API](https://docs.aws.amazon.com/AmazonS3/latest/API/API_CopyObject.html): destination version IDs and response handling.
- [PostgreSQL logical replication restrictions](https://www.postgresql.org/docs/current/logical-replication-restrictions.html): migration exclusions requiring separate handling.
- [PostgreSQL PITR](https://www.postgresql.org/docs/current/continuous-archiving.html): consistent recovery-chain requirements.
- [Ceph RBD mirroring](https://docs.ceph.com/en/tentacle/rbd/rbd-mirroring/): replicated-image promotion and synchronization model.
- [Pacemaker fencing](https://clusterlabs.org/projects/pacemaker/doc/3.0/Pacemaker_Explained/html/fencing.html): effective exclusion of an old owner.
