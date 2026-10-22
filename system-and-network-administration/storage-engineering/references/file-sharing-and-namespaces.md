# File sharing, distributed namespaces, and mounts

Evidence checked: 2026-10-21. Verify client/server versions, negotiated protocol dialects, filesystem support, and vendor support matrices for the actual workload.

## Contents

- [Define the required file contract](#define-the-required-file-contract)
- [Compare access mechanisms](#compare-access-mechanisms)
- [Make identities and caching explicit](#make-identities-and-caching-explicit)
- [Scale a namespace](#scale-a-namespace)
- [Understand object-backed filesystems](#understand-object-backed-filesystems)
- [Choose an architecture](#choose-an-architecture)
- [Validate before migration](#validate-before-migration)
- [Primary references](#primary-references)

## Define the required file contract

List the application's actual operations: random overwrite, append, atomic rename, hard links, symbolic links, `mmap`, file locks, directory enumeration, notifications, ACLs, case sensitivity, timestamps, sparse allocation, and synchronization. “Uses files” is insufficient to select a service.

A mount integrates a filesystem implementation into a process-visible namespace. It does not establish locality, POSIX completeness, stable performance, coherency between clients, or durability after host failure. FUSE is an implementation boundary for a userspace filesystem; it does not by itself establish whether the filesystem is coherent or suitable for a workload.

Distinguish local process concurrency from independent clients. Two local processes benefit from one kernel's shared caches. Two machines need an explicit protocol or distributed coordinator to maintain the necessary visibility and ownership rules. An application that works locally can fail remotely because it relied on undocumented timing or locking behavior.

## Compare access mechanisms

| Mechanism | Typical fit | Questions that determine suitability |
| --- | --- | --- |
| NFS | Unix/Linux shared directories, application files, home directories | Version, authentication, cache coherency, lock recovery, stable writes, server failover and mount-time failure policy |
| SMB | Windows and mixed-platform shares; supported enterprise applications | Dialect, identity/ACL mapping, leases, durable/persistent handles, signing/encryption, supported clustering |
| SSHFS/SFTP | Convenient authenticated remote access and modest transfer workflows | Reconnect behavior, caching, available protocol extensions, lock/rename semantics, latency and maintenance status |
| WebDAV | HTTP-based document/resource access | Client buffering, server locks, conditional updates, authentication, directory/property translation |
| Distributed/parallel filesystem | Many clients and servers sharing one namespace | Metadata scalability, data placement, network assumptions, client compatibility, failure recovery |
| Synchronization software | Offline local copies and eventual distribution | Conflict policy, scan lag, delete propagation, permissions and version retention |
| Object-to-file gateway | Legacy path access to remote objects | Which filesystem operations are emulated; cache authority, writeback completion, concurrent clients and API bypass |

NFSv4 integrates protocol-level state, locking, and security mechanisms that differ from NFSv3's design. NFSv4.1 includes sessions and parallel-access facilities; support is negotiated and implementation dependent. pNFS can separate metadata coordination from direct data-server access. It does not inherently replicate data or make arbitrary WAN latency disappear. [NFSv4](https://www.rfc-editor.org/rfc/rfc7530.html), [NFSv4.1](https://www.rfc-editor.org/rfc/rfc8881.html)

Modern SMB offers capabilities including Multichannel, Direct/RDMA, encryption, and failover features in supported combinations. Confirm both endpoints and the share configuration; do not infer persistent-handle or transparent-failover behavior from the label “SMB 3.” A supported SQL Server or Hyper-V over SMB design does not establish that every database is safe on every SMB share. [Microsoft SMB overview](https://learn.microsoft.com/en-us/windows-server/storage/file-server/file-server-smb-overview)

## Make identities and caching explicit

Map user identity through the full chain. Numeric UID/GID assumptions, NFSv4 name mapping, Windows SIDs, POSIX ACLs, SMB ACLs, and container user IDs can produce different access results for the same apparent username. Test effective permissions from the real service identity.

Do not treat NFS `AUTH_SYS` client-supplied identity as equivalent to strong user authentication. Root squashing limits one class of access but is not a substitute for an authentication design. Where required and supported, use Kerberos or another documented secure mode, with explicit integrity/confidentiality settings. Verify time synchronization, DNS, and credential renewal as availability dependencies.

Separate caching from correctness. File and directory attributes, data, negative lookups, delegations, and SMB leases each affect visibility. NFS close-to-open behavior is not a promise that every already-open file on another client instantly reflects arbitrary writes. Disabling caches indiscriminately can amplify metadata traffic without solving application coordination. [Linux NFS client manual](https://man7.org/linux/man-pages/man5/nfs.5.html)

Specify how locks behave after client crash, server restart, lease expiry, and network partition. Decide whether an application retries, aborts, or requires fencing. Configure NFS timeout policy knowingly: soft timeout behavior can return errors in situations where an application assumes persistent writes, while hard retry can block processes through an outage. Test the actual failure path rather than selecting a mount option solely to avoid a visible hang.

When exporting the same data through NFS and SMB, verify cross-protocol lock coordination, ACL translation, case handling, and notifications. Accessing a backing directory directly can bypass the coordination layer of a distributed service. Do not assume “the files look identical” makes mixed access safe.

## Scale a namespace

Identify where names, inode attributes, allocation maps, locks, and data blocks live. A gateway bottleneck and a metadata bottleneck require different remedies.

| Architecture | Scaling opportunity | Remaining constraint |
| --- | --- | --- |
| Single file server | Simple ownership and operations; scale up network/cache/device capacity | One server's limits and an explicitly designed failover path |
| Clustered file service over shared storage | Several service nodes with coordinated ownership or access | Shared backend, quorum/fencing, protocol recovery, common control-plane failures |
| Metadata service plus distributed data servers | Direct parallel data paths; metadata/data resources scale separately | Hot directories/inodes, metadata service availability, distributed locking and rebalancing |
| Sharded independent namespaces | Strong operational isolation and predictable shard boundaries | Cross-shard rename, discovery, balancing, and application-visible placement |
| Federated namespace | One naming view over several independent services | A single directory tree does not imply shared atomicity, consistent snapshots, or uniform latency |

CephFS uses metadata servers to coordinate a namespace while clients reach distributed RADOS data directly. Lustre and BeeGFS represent parallel filesystems with separate metadata and data roles. Evaluate metadata-heavy workloads independently from bulk bandwidth; millions of tiny files may be limited by lookup, create, lock, and stat operations even when the data network is mostly idle. [CephFS architecture](https://docs.ceph.com/en/latest/cephfs/), [BeeGFS architecture](https://doc.beegfs.io/latest/architecture/overview.html), [Lustre introduction](https://www.lustre.org/getting-started-with-lustre/)

Treat labels such as “POSIX-compatible” as a reason to run the required operation tests, not a substitute for them. Review supported clients, crash recovery, direct-I/O behavior, and known limitations in the selected release. Ceph's `latest` documentation is explicitly a development branch; pin production implementation decisions to release documentation.

## Understand object-backed filesystems

Distinguish two different systems:

- A gateway maps each external object to something resembling a file and approximates missing operations.
- A filesystem uses an object store as its data backend and adds its own authoritative metadata engine, chunk layout, locking, and consistency protocol.

The second can provide richer file semantics, but its files may be chunked, encoded, or encrypted into internal objects. Reading the bucket directly may expose neither original names nor whole files. JuiceFS is a representative split between file data in object storage and namespace metadata in a separate engine. Restore both coherently, preserve keys and configuration, and verify metadata availability as well as object durability. [JuiceFS architecture](https://juicefs.com/docs/community/architecture/)

Ask where an acknowledged write lives when local writeback caching is enabled. A cache loss before upload can change the RPO even when the remote object store is highly durable. Never permit independent object edits behind a filesystem unless its design explicitly supports them.

## Choose an architecture

Prefer an application-supported file protocol when existing software needs shared filesystem operations. Consider an object API when immutable uploads, media, archives, or independently addressable blobs dominate. Consider local working copies plus synchronization for offline human workflows, with a conflict policy; synchronization is not a distributed lock service for live database files.

For a small environment, one adequately protected file server plus tested restore may be more achievable than a distributed filesystem that nobody can operate. If continued service after host failure is required, specify and test the redundant service nodes, authoritative data copies, fencing, identity, client reconnection, and repair capacity. A second DNS name alone supplies none of those guarantees.

## Validate before migration

Test concurrent rename/read, overwrite and truncation, append, lock contention, process crash, client reconnect, server restart, quota exhaustion, and permission changes. Include filenames that differ only by case, Unicode normalization, long paths, symlinks, and large sparse files if relevant. Verify backup/restore of ACLs and metadata. Run tests from the actual OS, container runtime, and application version.

Record expected versus observed behavior and any compatibility workaround. If a workaround changes application semantics, make that tradeoff explicit rather than silently accepting a passing “file copied successfully” test.

## Primary references

- [RFC 7530](https://www.rfc-editor.org/rfc/rfc7530.html), [RFC 8881](https://www.rfc-editor.org/rfc/rfc8881.html), and [Linux NFS manual](https://man7.org/linux/man-pages/man5/nfs.5.html): protocol versus client behavior.
- [Microsoft SMB overview](https://learn.microsoft.com/en-us/windows-server/storage/file-server/file-server-smb-overview) and [feature descriptions](https://learn.microsoft.com/en-us/windows-server/storage/file-server/smb-feature-descriptions): negotiate and verify capabilities by version.
- [SSHFS upstream](https://github.com/libfuse/sshfs), [WebDAV RFC 4918](https://www.rfc-editor.org/rfc/rfc4918.html), [Syncthing synchronization](https://docs.syncthing.net/users/syncing.html): access and synchronization families.
- [CephFS](https://docs.ceph.com/en/latest/cephfs/), [BeeGFS](https://doc.beegfs.io/latest/architecture/overview.html), [Lustre](https://www.lustre.org/getting-started-with-lustre/), [JuiceFS](https://juicefs.com/docs/community/architecture/): representative namespace/data architectures.
