# Distributed Consistency and High Availability

Evidence checked: 2026-10-21. Use this reference when a design promises safe failover, multiple writers, quorum, or uninterrupted access. Specify observable behavior before selecting a consensus or replication mechanism.

## Contents

- [Define the data contract](#define-the-data-contract)
- [Separate quorum from data protection](#separate-quorum-from-data-protection)
- [Locate the acknowledgement boundary](#locate-the-acknowledgement-boundary)
- [Control ownership and fence stale writers](#control-ownership-and-fence-stale-writers)
- [Design two-node and two-site systems](#design-two-node-and-two-site-systems)
- [Handle partitions and ambiguous outcomes](#handle-partitions-and-ambiguous-outcomes)
- [Validate failover](#validate-failover)
- [Primary references](#primary-references)

## Define the data contract

Ask what the application must observe, at which API, and across which clients:

| Contract | Question to answer | Do not infer |
| --- | --- | --- |
| Atomic operation | Can a read observe a partially applied update? | Atomicity of an object update does not imply a transaction across several objects |
| Linearizable operation | Does each completed operation appear at one point between invocation and response, respecting real-time order? | Linearizable reads alone do not make a workflow transactional |
| Serializable transactions | Is the effect equivalent to some serial transaction order? | Serializability alone does not necessarily preserve real-time ordering |
| Read-your-writes / session guarantees | Does this session observe its accepted writes? | Other sessions or regions need not immediately see them |
| Eventual consistency | Do replicas converge after updates stop and communication resumes? | No bounded staleness follows without an explicit bound |
| Causal consistency | Are causally dependent updates observed in a compatible order? | Concurrent updates can still require reconciliation |
| Durable acknowledgement | Which failures may occur without losing a successful write? | Success from an API need not mean every replica has persisted it |

Define these contracts independently for data, metadata, listing, locks, and caches. A coherent server cannot correct a client's unsupported cache assumptions. An application may require a stronger cross-file transaction than any mounted filesystem promises.

Treat the consistency/availability tradeoff during a partition as a question about required operations. A system can reject writes, serve explicitly stale reads, or continue conflict-producing writes; the acceptable choice depends on the workload. Avoid reducing an entire product to a universal “CP” or “AP” label without stating the operation and failure model.

## Separate quorum from data protection

For ordinary majority voting with N voters, quorum is floor(N/2)+1. Three voters require two; five require three. Two voters normally cannot lose either voter and still form a majority. This arithmetic assumes the protocol's membership rules and a connected surviving majority; an odd number does not guarantee a majority exists under every multi-way partition.

Raft is one example of a replicated-log consensus protocol that uses elections, log ordering, and membership rules to preserve safety. Do not treat “a majority replied” as an implementation of consensus. The log's persistence and state-machine semantics remain part of the guarantee. [Raft paper](https://raft.github.io/raft.pdf)

Count **control-plane voters** separately from **payload replicas/fragments**. A witness may contribute to ownership decisions while holding none of the application payload. A storage controller can retain quorum while the required data copies are inaccessible. Conversely, all data disks can be healthy while loss of metadata quorum stops serving requests. For an etcd-backed design, apply its documented majority and membership behavior; adding a member can change the required quorum before that member becomes useful. [etcd FAQ](https://etcd.io/docs/v3.6/faq/)

Read/write quorum schemes use read threshold R, write threshold W, and replica count N. The familiar R+W>N overlap condition is useful only under its assumptions. Concurrent operations, sloppy quorums, changing membership, stale responses, and reconciliation rules prevent that inequality alone from proving linearizability. Dynamo illustrates a design that combines versioning, decentralized replication, and conflict resolution to favor availability in selected conditions. Do not equate that historical system with every current managed service carrying a similar name. [Dynamo paper](https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf)

## Locate the acknowledgement boundary

Trace a write through application buffers, OS page cache, filesystem/journal, block layer, controller/device cache, replication transport, remote cache, remote durable media, and application replay. Specify which stages have completed when success is returned.

Distinguish these acknowledgements:

- Accepted into local memory.
- Persisted locally, queued for remote transmission.
- Received by a remote process or OS cache.
- Persisted on the required remote replicas.
- Applied remotely so dependent reads can observe the result.

Use the actual API's flush/fsync or transaction-commit contract. Ensure storage layers propagate flushes and ordering appropriately, and verify power-loss protection or cache configuration. A benchmark that acknowledges RAM writes measures a different promise from a test of durable transactions.

For an illustrative implementation, DRBD distinguishes asynchronous, memory-synchronous, and disk-synchronous replication modes. Verify the selected mode and supported quorum behavior in the deployed release; the word “replicated” does not identify the acknowledgement boundary. [DRBD replication modes and quorum](https://linbit.com/drbd-user-guide/drbd-guide-9_0-en/)

## Control ownership and fence stale writers

Require one of these explicit models:

1. One authoritative writer, with safe transfer of ownership.
2. A cluster-aware filesystem or database coordinating concurrent access.
3. An application protocol that accepts concurrency and reconciles conflicts.

Attaching the same block device to two machines does not make ordinary filesystems multi-writer safe. A floating IP, load balancer, or Kubernetes reschedule changes client routing; it does not prove that the former writer stopped writing.

Use a mechanism that actually excludes the stale owner: power fencing, storage/fabric access revocation, reservations, or a correctly enforced lease/generation scheme. A fencing token is useful only if the resource rejects stale tokens. A lease requires well-defined expiry, pause, and clock assumptions; merely writing an expiry timestamp into a database is insufficient.

Pacemaker's fencing guidance distinguishes reliable isolation from assuming an unreachable node is dead. Its fence mechanism must remain effective when the target cannot cooperate and must account for shared power and network dependencies. [Pacemaker fencing](https://clusterlabs.org/projects/pacemaker/doc/3.0/Pacemaker_Explained/html/fencing.html)

Do not prescribe an external power fence for every distributed product indiscriminately. Some systems implement sufficient exclusion at the storage protocol itself. Identify and test the actual enforcement boundary, including application behavior after I/O suspension or errors.

## Design two-node and two-site systems

For two data nodes, compare a third independent witness, a supported fencing arrangement, or deliberate manual failover. A witness does not add another full data copy. If only one current data copy remains, explain what additional failure would lose it and whether degraded writes remain permitted.

For majority voters divided across two sites, an unequal allocation makes one site necessary for a majority, while an equal allocation loses the majority on either full site failure. A supported third-site arbiter can break an ownership tie, but cannot reconstruct missing payload or provide absent compute capacity. Other protocols and manual operating policies exist; do not promise symmetric automatic failover from generic two-site voting alone.

Treat witness placement and connectivity as part of the failure matrix. Test losing either data node, either site, only the witness, each link, and combinations occurring during recovery. A witness hosted on a surviving VM that depends on the failed storage cluster is circular protection.

## Handle partitions and ambiguous outcomes

Classify a timed-out write as **unknown**, not automatically failed. The server may have committed it before the response was lost. Retry with a protocol-supported idempotency mechanism, conditional update, transaction identifier, or application reconciliation; otherwise a retry can duplicate an effect.

Distinguish data-plane reachability from control-plane reachability. Test asymmetric partitions where A can contact B differently from B contacting A, and cases where clients reach both isolated sides. Also test a stalled process that resumes after its lease or ownership has expired. A clean shutdown test does not exercise these states.

Avoid lowering quorum, promoting a stale copy, or using force flags simply to make a health indicator green. First establish the authoritative history and which acknowledged writes could be discarded. Preserve competing copies and logs until reconciliation is decided.

## Validate failover

For every scenario, record: expected writer, accepted/stalled/rejected operations, possible stale reads, maximum acknowledged-data loss, detection delay, exclusion mechanism, promotion conditions, and rejoin behavior. During a controlled test, retain transaction IDs and verify that successful writes remain present, rejected operations are handled, and ambiguous operations are reconciled.

Test failback as a separate change. Rejoining an old primary must not resurrect an independent writer or overwrite the current authoritative history. Measure application recovery, including reconnects and cache invalidation, rather than reporting only the leader-election duration.

## Primary references

- [Raft paper](https://raft.github.io/raft.pdf): consensus and replicated-log safety.
- [etcd FAQ](https://etcd.io/docs/v3.6/faq/): quorum and operational membership implications.
- [Amazon Dynamo paper](https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf): availability-oriented replication and reconciliation.
- [DRBD user guide](https://linbit.com/drbd-user-guide/drbd-guide-9_0-en/): acknowledgement modes and implementation-specific quorum.
- [Pacemaker fencing](https://clusterlabs.org/projects/pacemaker/doc/3.0/Pacemaker_Explained/html/fencing.html): stale-writer exclusion.
