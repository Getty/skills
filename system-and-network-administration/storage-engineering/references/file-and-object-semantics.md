# File paths, object APIs, and the real access contract

Evidence reviewed: 2026-10-21. Apply provider, bucket, client, OS, and filesystem version scope to every capability.

## Contents

- Start with the application contract
- Compare operations
- Explain the acknowledgement boundary
- Distinguish three ways to put files on objects
- Adapt applications deliberately
- Validate semantics
- Primary references

## Start with the application contract

Ask what the application does, not merely whether it accepts a path. The same path syntax can reach an ext4 disk, an NFS server, an SMB share, a FUSE object mount, an in-memory filesystem, or an object-backed distributed filesystem. A successful mount only establishes a namespace entry.

“POSIX-like” is insufficient for critical state. Name the required operations, atomicity scope, visibility, locking, durability, and failure behavior. Windows applications may depend on share modes, byte-range locks, ACL inheritance, reparse points, alternate streams, or rename/open-handle rules that differ from Unix conventions.

## Compare operations

| Operation/property | Local filesystem over owned block storage | Network/shared filesystem | General-purpose S3-style object API |
| --- | --- | --- | --- |
| Namespace | Files and directories with filesystem metadata | Shared file namespace, with server/client caching | Bucket and object keys; slash-delimited prefixes often simulate folders |
| Random byte updates | Supported by ordinary file I/O, subject to filesystem rules | Often supported, with remote latency and coherency rules | Usually replace/create objects; range GET is not random range PUT |
| Append | File append primitives; atomicity depends on operation and system | Protocol and multi-client semantics need checking | No universal append operation; service-specific extensions exist |
| Rename | Namespace operation; same-filesystem replacement can be atomic | Supported under protocol/server rules; cross-share moves may become copies | Commonly copy plus delete; not a universal atomic rename |
| Multi-file update | Not automatically one transaction | Not automatically one transaction | Multiple keys are not automatically one transaction |
| Locks | Local advisory/mandatory/application locks according to OS | Protocol locks, leases, reconnect and server recovery | No general POSIX file locks; conditional requests and external coordination instead |
| Durability | Buffer flush and persistent media contract | Client flush plus server stable-storage contract | Successful API commit under the service contract |
| Visibility | File-operation semantics, including open handles | Cached metadata/data; verify close-to-open or stronger guarantees | Provider consistency contract; separate SDK/CDN/mount caches |
| Permissions | UID/GID/mode, ACLs, xattrs according to OS | Identity mapping, server ACLs, authentication | Credentials, policies, bucket/object controls; not chmod equivalence |
| Sparse files/mmap | Filesystem and device dependent | Client and server dependent | No general promise; mounts may emulate at significant cost |
| Failure response | I/O errors, read-only transitions, partial operations | Timeouts, hangs, stale handles, reconnect/lock loss | HTTP failures, retries, conditional conflicts and uncertain request outcomes |
| Repeated listing | Directory enumeration/metadata operations | Network metadata work | Paginated API calls with request/cost considerations |

Do not label object storage inherently eventually consistent. AWS S3 documents strong object read-after-write consistency, including overwrites and deletes; that does not imply cross-object transactions or synchronous replication to another region. Other compatible providers must be checked independently.

Do not label all S3 operations universally incapable of rename or append. AWS directory buckets using S3 Express One Zone support service-specific RenameObject and append operations. Those capabilities do not imply arbitrary POSIX mutation, apply to every bucket type, or generalize to another S3 endpoint. Azure Data Lake hierarchical namespace and Google Cloud Storage hierarchical namespace also add specific namespace operations; verify their API and client scope.

## Explain the acknowledgement boundary

Distinguish:

1. The application accepts bytes in its own buffer.
2. The OS/client accepts a write into memory.
3. A local gateway or write-back cache journals the data.
4. A storage server accepts the request.
5. The configured durable replicas/fragments acknowledge it.
6. An independent backup or remote DR copy receives it.

A successful step is not proof that all later steps have happened. Identify the step that a user-visible success actually represents.

For a local atomic publication pattern, an application can write a temporary file, synchronize its data, rename within the same filesystem, and synchronize the affected directory entries as required by the platform. That is a design pattern whose exact implementation must follow the OS/filesystem contract. Atomic rename concerns visibility; it is not by itself a power-loss durability guarantee. Cross-filesystem moves have different behavior. Check all error returns, including flush and close.

For network files, a client's fsync depends on server stable-storage behavior and the full stack. A remote mount with a dishonest volatile acknowledgement can defeat a correct database. An NFS client timeout also does not prove the server did not execute an operation.

For object uploads, buffer locally or use the provider's multipart protocol, then publish only after the commit succeeds. A timed-out completion can have an uncertain outcome: inspect the exact key/version/checksum or use conditional/idempotent operations before deciding whether to repeat or compensate. Successful upload into one location is not proof of remote replication completion.

## Distinguish three ways to put files on objects

| Approach | How it works | Suitable uses | Hidden responsibility |
| --- | --- | --- | --- |
| Direct object API | App names immutable/versioned objects and uses PUT/GET/range requests | Web uploads, artifacts, datasets, backup objects | App handles publication, references, pagination, retry and authorization |
| Object-key mount/gateway | File operations are translated or emulated over keys, often with cache | Read-heavy tools, bulk ingest, compatible legacy workflows | Unsupported calls, local dirty data, cache coherence, request amplification |
| Full filesystem backed by objects | A metadata system implements namespace/coordination; data uses object chunks | Workloads needing a richer shared namespace over object capacity | Metadata availability/backup, chunk integrity, compaction and client compatibility |

Mountpoint for S3 explicitly provides a subset of file semantics. Its documented behavior is an example of an honest adapter, not a universal limitation of every FUSE implementation.

JuiceFS illustrates the third model: user filenames and object chunks are linked through separate metadata. Losing that metadata can make otherwise intact bucket bytes unusable. Editing the underlying chunk bucket using ordinary S3 file-management tools is not equivalent to editing files through the filesystem.

With gateways, define whether raw API writers may modify the same data. Without a documented coherency mechanism, direct bucket edits can bypass namespace state, locks, cached attributes, and filesystem metadata.

## Adapt applications deliberately

For an object-native upload workflow:

1. Reserve an application record or upload identifier.
2. Upload to a unique immutable key, using constrained credentials or a signed request.
3. Verify completion, expected length and a suitable checksum.
4. Commit the database reference and object version.
5. Publish the record only after the required data is durable.
6. Reconcile abandoned objects and incomplete application records after crashes.

Database and object commits are two separate operations unless a supported system coordinates them. Use explicit pending/ready states, an outbox or reconciliation job; do not claim a distributed transaction from a successful PUT.

For a dataset, write immutable chunks first and atomically/conditionally publish a manifest pointer last. Readers use one manifest generation. Preserve old chunks until all retained manifests and readers no longer need them. This converts many mutable-file operations into a small coordination problem, but correctness depends on the selected conditional-write or catalog service.

For a legacy application that needs locks, mmap or arbitrary updates, prefer a compatible filesystem service or validate a full filesystem implementation. Do not enable a larger local cache and assume it has acquired missing cross-client coordination.

## Validate semantics

Test only on disposable data. Include:

- Two clients racing to create or replace the same item.
- Atomic publish visibility while readers run.
- A process crash before and after flush/close.
- Client disconnection while a write or rename is outstanding.
- Stale open handles and cached listings after remote change.
- Lock recovery and old-writer behavior after reconnect.
- Required ACL, xattr, link, timestamp, case, Unicode and sparse-file behavior.
- A gateway restart with unflushed data.
- An ambiguous API timeout followed by safe reconciliation.
- Restore of metadata together with the matching data generation.

A successful “copy, read, delete” test proves very little about database or concurrent workspace correctness.

## Primary references

- [Linux rename(2)](https://man7.org/linux/man-pages/man2/rename.2.html): atomic namespace replacement and filesystem boundaries.
- [Linux fsync(2)](https://man7.org/linux/man-pages/man2/fsync.2.html): file and directory durability distinction.
- [AWS S3 consistency](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html): provider-specific consistency.
- [Mountpoint semantics](https://github.com/awslabs/mountpoint-s3/blob/main/doc/SEMANTICS.md): an explicitly limited file adapter.
- [S3 directory-bucket rename](https://docs.aws.amazon.com/AmazonS3/latest/userguide/directory-buckets-objects-rename.html) and [append](https://docs.aws.amazon.com/AmazonS3/latest/userguide/directory-buckets-objects-append.html): scoped exceptions.
- [Azure hierarchical namespace](https://learn.microsoft.com/en-us/azure/storage/blobs/data-lake-storage-namespace) and [GCS hierarchical namespace](https://docs.cloud.google.com/storage/docs/hns-overview): service-specific namespace features.
- [JuiceFS architecture](https://juicefs.com/docs/community/architecture/): metadata/data split.
- [Apache Iceberg specification](https://iceberg.apache.org/spec/): atomic catalog metadata publication as a concrete design.
