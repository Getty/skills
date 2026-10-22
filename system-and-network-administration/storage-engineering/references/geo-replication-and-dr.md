# Geographic Replication and Disaster Recovery

Evidence checked: 2026-10-21. Use this reference to compare one cluster spanning sites with independent site-local systems. Product-specific examples illustrate methods; verify supported topology, latency, and feature constraints against the deployed release.

## Contents

- [Define the disaster and service objective](#define-the-disaster-and-service-objective)
- [Choose a replication topology](#choose-a-replication-topology)
- [Make RPO and RTO measurable](#make-rpo-and-rto-measurable)
- [Reason about stretched clusters](#reason-about-stretched-clusters)
- [Plan regional applications](#plan-regional-applications)
- [Execute controlled failover and failback](#execute-controlled-failover-and-failback)
- [Assess independence and cost](#assess-independence-and-cost)
- [Primary references](#primary-references)

## Define the disaster and service objective

Name the event: one failed host, a lost rack, an inaccessible site, destruction of a site, provider control-plane outage, compromised credentials, corruption, or a regional dependency outage. A second location addresses only failures from which it is sufficiently independent.

State which operations must continue, which users must reach them, and whether the surviving site may operate with reduced durability or capacity. Separate “data survives” from “service accepts writes automatically.” A surviving copy is not useful within the RTO if encryption keys, DNS changes, images, secrets, or operators are unavailable.

## Choose a replication topology

| Method | Acknowledgement and movement | Appropriate use | Principal tradeoff |
| --- | --- | --- | --- |
| Synchronous remote replication | Wait for the required remote persistence boundary | Very small or zero acknowledged-write loss for a specified failure | Remote RTT and failure can enter the commit path |
| Asynchronous continuous log/block replication | Acknowledge locally, then transmit changes | Site-local write latency with a warm remote copy | Unreplicated acknowledged writes can be lost |
| Periodic snapshot/delta replication | Export a completed point-in-time state and its changes | Volume/filesystem recovery without continuous WAN writes | Recovery point follows the last complete usable transfer |
| Application-native physical replication | Replicate a database's recovery log or equivalent native representation | Transaction-aware failover and database recovery | Engine versions, promotion, retained logs, and replication topology matter |
| Logical replication / change data capture | Replicate selected logical changes | Selective migration, integration, or distributed ownership | Schema, ordering, omitted objects, conflicts, and transaction boundaries need explicit treatment |
| Object replication | Copy object versions and supported metadata between stores | Independent object endpoints and geographic copies | Per-object status and metadata/delete behavior may differ |
| Cascade / hub-and-spoke | Relay from an intermediate replica | Reduce origin fan-out or aggregate remote traffic | Relay lag and failure become additional dependencies |
| Backup shipping / offline transfer | Move independent recovery sets | Low-cost recovery or initial seeding of large datasets | Longer recovery and a finite data-loss window |
| Federation / regional ownership | Partition data ownership by region, tenant, or shard | Regional autonomy without global write latency on every operation | Cross-region moves and transactions require explicit protocols |

Choose the replication layer according to the data contract. Block replication reproduces changed blocks; it does not understand a business transaction spanning a database, uploaded objects, and a message queue. Native replication can preserve application semantics but also propagates valid destructive actions. Keep an independent historical recovery path.

## Make RPO and RTO measurable

Define **RPO** as the acceptable loss window for the specified incident and **RTO** as the elapsed time to restore the specified service. State whether the measurement begins at failure occurrence, detection, or declared disaster; use the business requirement consistently.

For asynchronous systems, a usual lag of two seconds is a measurement, not a hard two-second loss bound. A disconnected remote site can fall arbitrarily far behind while the source keeps acknowledging writes. A bounded policy requires lag detection plus defined behavior when the threshold is exceeded, such as restricting writes, changing the service promise, or escalating before the bound is breached. Measure bytes/transactions and durable/replayed positions as appropriate, not only a dashboard timestamp.

For snapshot replication, track the newest **completed and verified** recoverable snapshot. An hourly schedule can produce an older recovery point if jobs queue or transfers fail. A partially transferred snapshot is not automatically usable. Ceph RBD documents separate journal and snapshot mirroring modes, both asynchronous; snapshot-based failover depends on a completed delta set. [Ceph RBD mirroring](https://docs.ceph.com/en/tentacle/rbd/rbd-mirroring/)

Budget RTO as a critical path including detection, decision, fencing, promotion, recovery replay, compute provisioning, mount/attachment, credential availability, routing, cache warm-up, and application checks. Parallel steps need not be added twice, but none may be omitted. Include a cold-start case where provider capacity cannot immediately be allocated.

Estimate network catch-up using a simple model: with backlog B, effective transfer rate T, and ongoing source change rate C, ideal catch-up time is B/(T−C) when T>C. If T≤C, the backlog cannot shrink under those conditions. Treat this as a lower bound and account for read, compression, protocol, replay, and destination-write limits. Seed large datasets separately when that reduces recovery exposure.

## Reason about stretched clusters

A stretched cluster places one coordinated storage system across sites. It can present one namespace and automate some failures, but normal writes, metadata operations, or ownership decisions may depend on remote connectivity. Test the intended latency distribution and asymmetric partitions before considering this a substitute for site-local independence.

Prove all of the following for every site-loss scenario:

- The surviving side can establish the supported authority/quorum.
- Every required dataset has sufficient current replicas or fragments there.
- The old writer is excluded.
- Surviving clients can reach a working data path and supporting services.
- Reduced redundancy and restoration capacity are acceptable.

With ordinary majority voting, two sites alone cannot both independently hold a majority after either site disappears. A third independent witness may resolve ownership in a supported topology; it adds no missing data. A two-site EC stripe can also fail reconstruction despite a healthy remote witness. Evaluate data placement and voting separately.

**Version-specific example:** Ceph Tentacle documents cluster stretch mode with two data sites and a third-site tiebreaker monitor, including restrictions on replicas, monitors, and erasure-coded pools. The same documentation also describes individual stretch pools. These are distinct configuration mechanisms. An EC stretch design document under a development path is not evidence that the deployed release supports EC in cluster stretch mode. [Ceph stretch clusters](https://docs.ceph.com/en/tentacle/rados/operations/stretch-mode/)

## Plan regional applications

Compare three application models:

1. **Active-passive:** one write authority; the other site is a recovery destination. Define manual or automatic promotion and the data-loss decision.
2. **Active-active with disjoint ownership:** both sites serve users but each key/tenant/shard has one write authority. Route correctly and define ownership transfer.
3. **Concurrent writes to the same data:** use a globally coordinated transaction protocol, explicit conflict resolution, or an appropriate convergent data model. State which operations commute and which require coordination.

“Active-active” is insufficient as a specification. Two-way replication may mean independent primary datasets mirrored in opposite directions, rather than safe concurrent writers to the same blocks. Last-writer-wins can discard an update and depends on the implementation's ordering semantics. CRDT-style merging addresses selected data types and operations; it does not automatically preserve inventory, financial, or uniqueness invariants.

Maintain cross-resource recovery consistency. If a database references an object not yet copied to the recovery site, a successful database promotion can still produce missing content. Use immutable object identities, replication-state checks, ordering or outbox protocols, and a documented repair mechanism according to the application. Do not invent an atomic transaction across unrelated stores.

Amazon S3's documented bucket replication is asynchronous, and live rules do not automatically backfill pre-existing objects; a separate batch mechanism addresses existing objects. Check version, metadata, deletion, and account ownership policies. An object-replication feature does not create a filesystem or a complete regional application failover. [Amazon S3 replication](https://docs.aws.amazon.com/AmazonS3/latest/userguide/replication.html)

## Execute controlled failover and failback

Prepare an incident-specific sequence:

1. Establish incident scope and record the last verified recovery point.
2. Stop or fence the old write authority, or establish the supported protocol's exclusion evidence.
3. Select the authoritative copy and explicitly account for potentially missing acknowledged writes.
4. Promote, replay, and verify data before exposing writes.
5. Recover dependencies and application traffic; reconcile unknown client outcomes.
6. Keep the former site isolated from writes when it returns.
7. Re-seed or safely reconcile it from the current authority, then measure synchronization.
8. Perform any later failback as a separate controlled ownership transfer.

Preserve divergent histories when data-loss decisions are unresolved. A healthy network reconnect does not merge two independently modified block devices. Rehearse failback, because a design that survives the first incident can lose data during return to normal service.

## Assess independence and cost

Include cross-site transfer, API requests, retained logs, duplicate compute, spare capacity, restore egress, cold-tier retrieval, and operational staffing. A cheaper remote store can become expensive to restore at scale. Separate provider/account failure from geography; two regions in one account may share deletion authority, key administration, and billing suspension risk.

Use site-local storage plus explicit replication or backup when the workload tolerates an asynchronous recovery point and the team benefits from simpler failure boundaries. Consider a stretched or globally coordinated design when the semantics justify its latency and operational requirements. Make this a workload-based decision, not a blanket preference.

## Primary references

- [PostgreSQL standby replication](https://www.postgresql.org/docs/current/warm-standby.html): native log shipping, streaming, cascading, and synchronous modes.
- [Ceph RBD mirroring](https://docs.ceph.com/en/tentacle/rbd/rbd-mirroring/): asynchronous block-image replication.
- [CephFS snapshot mirroring](https://docs.ceph.com/en/tentacle/cephfs/cephfs-mirroring/): asynchronous filesystem snapshot replication; verify file-type and release limitations.
- [Ceph stretch clusters](https://docs.ceph.com/en/tentacle/rados/operations/stretch-mode/): supported stretched-topology mechanisms and constraints.
- [Ceph Object Gateway multisite](https://docs.ceph.com/en/tentacle/radosgw/multisite/): object-service replication across independent clusters.
- [Amazon S3 replication](https://docs.aws.amazon.com/AmazonS3/latest/userguide/replication.html): live and batch object replication.
