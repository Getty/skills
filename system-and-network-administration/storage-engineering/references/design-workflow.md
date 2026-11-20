# Design workflow checklists

Read this when producing a full storage design, recommendation or migration plan: it holds
the complete checklists behind the working method in SKILL.md.

## Establish the workload contract

Capture:

- Data classes: database state, user uploads, shared workspace, VM disks, container
  layers, logs, backups, immutable datasets, caches, scratch.
- Interface and required operations: filesystem path, block device, object API,
  append/log, database/query; random updates, atomic rename, locking, mmap, xattrs/ACLs,
  sparse files, range reads, listings.
- Concurrency: one writer, coordinated writers, independent writers, multi-tenant access;
  desired read visibility and transaction boundaries.
- Scale: live bytes, object/file count and size distribution, daily change rate, growth,
  working set, IOPS, bandwidth, latency percentiles.
- Recovery: named failures, tolerated lost acknowledged writes (RPO), recovery time (RTO),
  required service during maintenance and rebuild.
- Environment: OS/hypervisor, Kubernetes versions, hosts and independent sites, measured
  network RTT/bandwidth/loss, provider placement, operator skill and budget.

Distinguish a business target from an observed capability.

## Choose semantics before products

Produce a small candidate table: interface, data owner, writer model, persistence
boundary, failure domain, restore method, operational burden.

## Draw the failure and recovery design

For each named failure, state: readable data, permitted writers, surviving quorum, fencing
mechanism, recoverable copy, automatic/manual action, expected data loss, and return to
redundancy.

## Size normal, degraded, and recovery operation

Count protection overhead, free space, retained versions/snapshots, metadata, logs,
caches, and restore staging. Measure the bottleneck across disks, CPU, network, instance
caps, API requests, and application serialization.

## Deliver a testable decision

Include:

1. Recommended design and assumptions.
2. Access and write-acknowledgement guarantees.
3. Placement and failure matrix.
4. Capacity, latency, cost, and recovery budgets.
5. Backup/restore and failback ownership.
6. Deployment or migration stages, acceptance checks, and rollback limits.
7. Current sources for implementation-specific claims and unresolved facts.
