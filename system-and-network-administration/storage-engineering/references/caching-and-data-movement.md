# Caching, tiers, gateways and data movement

Evidence reviewed: 2026-10-21. Check the selected client/server release before relying on cache or transfer behavior.

## Contents

- Define cache authority
- Choose a cache/write policy
- Design tiers and gateways
- Distinguish synchronization from replication
- Move large datasets
- Primary references

## Define cache authority

For every cache, name its upstream authority, fill path, eviction policy, validity rule and dirty-data policy. If losing the cache loses acknowledged writes, it is temporarily authoritative storage and must be protected accordingly.

| Layer | Common purpose | Failure to consider |
| --- | --- | --- |
| Application cache | Avoid repeated computation/lookup | Stale authorization or stale mutable state |
| OS page cache | Reuse file blocks | Buffered writes lost before durable commit |
| Client metadata cache | Reduce stat/list/lookup traffic | Stale names, attributes, permissions or negative results |
| Local SSD object cache | Reduce network and repeated dataset downloads | Eviction storms, disk exhaustion, unprotected write-back |
| Server/controller cache | Absorb writes and improve I/O | Power loss, controller failure, failed battery/capacitor |
| CDN/edge cache | Geographic read distribution | Stale mutable URLs, privacy leakage or missing invalidation |
| Distributed cache | Share hot data among workers | Membership/rebalance failures and mistaken authoritative use |

Separate capacity from correctness. A bigger cache can reduce misses; it cannot create missing file locks or make two independent write-back clients coherent.

## Choose a cache/write policy

| Policy | Acknowledge after | Benefit | Exposure |
| --- | --- | --- | --- |
| Read-through | Read fetched from authority, then cached | Simple demand loading | Cold-start latency, authority outages on misses |
| Read-ahead/prefetch | Predicted data arrives in advance | Sequential throughput and smoother pipelines | Wasted network/capacity for wrong predictions |
| Write-through | Required backing store commit | Clear durability boundary | Backing latency remains in write path |
| Write-back | Local cache/journal accepts write | Fast writes and intermittent operation | Dirty data must survive cache/host failure and drain safely |
| Write-around | Backing store commits; cache bypassed/invalidated | Avoid cache pollution | Read-after-write and stale-cache handling |
| Explicit staging | Application declares local draft then remote commit | Observable checkpoint/publication | App must not publish draft as durable state |

“Persistent cache” means the cache survives some restart or power scenarios; verify whether it survives disk/host failure and whether its metadata can be recovered. A durable local journal is still not a remote copy.

Estimate dirty backlog as accepted dirty bytes minus successfully committed bytes. If sustained incoming writes exceed drain throughput, no finite cache can sustain the workload indefinitely. Alert on both dirty-byte age and free space. Define backpressure before exhaustion.

Use immutable/versioned keys to make read caches easier to validate. When mutable objects are necessary, identify the invalidation/TTL/validator mechanism and its worst allowed staleness. Strong consistency at the origin does not eliminate stale SDK, gateway, application or CDN caches.

## Design tiers and gateways

Distinguish a cache (a replaceable copy), a tier (a placement class that may hold the only current copy), and an archive (retrieval may require an asynchronous restore). HSM can keep directory entries online while moving content to slower media. A file appearing in a listing does not prove immediate content availability.

For object archive classes, check restore delay, request cost, minimum duration, temporary restored-copy lifetime, and whether the reader retries rather than treating “archived” as missing. Do not infer that all storage classes containing “Glacier” require the same restore process.

For a file gateway to objects, establish:

- Whether writes are uploaded on write, flush, close, delay or background scan.
- What happens during WAN loss, gateway restart and local cache loss.
- Whether direct object changes require explicit cache refresh.
- Whether more than one gateway may write the same namespace.
- How file metadata maps to object metadata, and what raw API writes can invalidate.
- How to recover namespace/cache metadata and incomplete uploads.
- How local users authenticate and how their rights map to the remote service.

AWS File Gateway and rclone mount are useful examples of different gateway/cache contracts. Read their specific documentation rather than applying generic “S3 mount” assumptions. For rclone, choose VFS cache mode from the application's operations and understand the dirty-data upload path and limits.

## Distinguish synchronization from replication

| Method | Unit of work | Typical promise | Important limitation |
| --- | --- | --- | --- |
| Periodic file copy/sync | Whole files or changed byte ranges | Destination converges after a successful run | Intermediate multi-file state may be inconsistent |
| Bidirectional sync | Two namespaces plus conflict history | Offline edits can be exchanged | Conflicts and delete semantics need explicit resolution |
| Snapshot send/receive | Consistent filesystem/block generation | Recreate a source snapshot lineage | Not automatically application-consistent or portable |
| Storage replication | Blocks, objects or fragments | System-defined durable/visible copy behavior | Copies logical mistakes and has topology constraints |
| Database log replication | Ordered transactions/log records | Database-defined recovery/promotion state | Version/schema/role constraints |
| Backup | Retained recoverable generations | Restore history according to repository rules | Restore path, catalog and credentials must work |

A command that deletes destination-only files is not a backup policy. Bidirectional synchronization is particularly risky when one side is empty because of a mount failure: verify identities and mount presence before interpreting absence as deletion.

For snapshot streams, preserve required base snapshots until receivers advance safely. Loss of a shared base may force a full resend. For object copies, preserve required version history, metadata, tags, permissions and retention according to destination capabilities. Record source bucket/key/version to destination bucket/key/version mappings: ordinary S3 copies create new destination version IDs. Reconcile application references and restore catalogs before cutover. Copying only current bytes is a narrower migration.

## Move large datasets

1. Inventory bytes, number/size of objects, changes per second, ACLs, versions and metadata.
2. Determine whether files are mutable during transfer and how a consistent cut is obtained.
3. Measure useful throughput with representative file sizes and encryption/compression settings.
4. Seed the initial data through network or supported physical shipment.
5. Run incremental synchronization with observed backlog and integrity checks.
6. Drain writers or use supported transactional/log replication for the final boundary.
7. Verify destination state and switch authority exactly once.
8. Keep rollback copies until the reverse-change implications are resolved.

The lower bound for a transfer is bytes divided by useful throughput. Metadata operations, compression, source reads, destination commits, throttling and retries can dominate. For a live migration, catch-up requires drain throughput to exceed new transfer-equivalent change bytes.

Deduplication and compression can reduce transfer volume only when the tool understands the format and the data is compressible/repeated. Client-side encryption often reduces backend compression/deduplication effectiveness; account for where each operation occurs.

## Primary references

- [S3 CopyObject and destination version IDs](https://docs.aws.amazon.com/AmazonS3/latest/API/API_CopyObject.html).

- [rclone mount and VFS cache behavior](https://rclone.org/commands/rclone_mount/).
- [AWS Storage Gateway FAQ](https://aws.amazon.com/storagegateway/faqs/): gateway writer and cache model.
- [S3 changes not appearing in a file gateway](https://repost.aws/knowledge-center/storage-gateway-s3-changes-not-showing): explicit cache refresh behavior.
- [AWS archived objects](https://docs.aws.amazon.com/AmazonS3/latest/userguide/archived-objects.html).
- [IPFS persistence and pinning](https://docs.ipfs.tech/concepts/persistence/): cache retention versus persistent availability.
