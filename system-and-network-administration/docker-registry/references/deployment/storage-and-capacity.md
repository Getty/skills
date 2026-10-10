# Filesystem/object storage, redirects, and capacity planning

> Read when: choosing a storage backend or sizing a registry.

Choose the storage backend from durability, availability, concurrency, recovery, latency, and operational ownership requirements. Filesystem storage is a straightforward single-instance baseline. Object storage can support a shared backend, but its credentials, endpoint, consistency/performance characteristics, and redirect behavior become production dependencies.

The official cache guidance recommends filesystem storage for best cache performance and correctness; do not promote that guidance into a universal claim that no other backend can function. Test the chosen proxy/backend/version combination.

## Budget components

Budget unique compressed blobs, manifests/indexes, artifact attachments, upload staging, retained deleted/unreachable content, backend versioning, and temporary maintenance/backup space. Repository tag counts do not directly measure physical bytes because blobs can be shared. A filesystem can run out of inodes before bytes.

For S3-style storage, decide whether clients receive presigned blob redirects or the registry serves bytes itself. Redirects reduce registry data-plane load but require client reachability and safe URL handling. A successful push from inside a VPC can coexist with failed external pulls to an inaccessible object endpoint.

## Backend policy

Use a dedicated storage prefix/bucket, narrow permissions, encryption and key recovery appropriate to the data, and monitored lifecycle rules. Do not apply object-store expiry rules that delete registry objects independently of manifest reachability. Registry GC and object-store version retention are different layers; deleting the current object may not reclaim old versions or cost immediately.

Test large push/pull, simultaneous uploads, aborted uploads, backend outage, and a full restore. Record storage-driver options against the exact Distribution release. Do not assume options from an old v2 driver or another S3-compatible provider behave identically on the target.

## Primary sources

- [Distribution configuration](https://distribution.github.io/distribution/about/configuration/)
- [Distribution S3 storage driver](https://distribution.github.io/distribution/storage-drivers/s3/)
- [Distribution pull-through cache](https://distribution.github.io/distribution/recipes/mirror/)
- [Distribution garbage collection](https://distribution.github.io/distribution/about/garbage-collection/)
