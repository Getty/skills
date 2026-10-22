# Kubernetes recovery and workload patterns

Evidence checked: 2026-10-21. Recheck version-dependent shutdown, retention, snapshot, and operator behavior against the deployed versions.

## Contents

- [Select a pattern by application semantics](#select-a-pattern-by-application-semantics)
- [Recover safely after node failure](#recover-safely-after-node-failure)
- [Design the bootstrap path](#design-the-bootstrap-path)
- [Back up independent layers](#back-up-independent-layers)
- [Test the failure model](#test-the-failure-model)
- [Avoid capacity and upgrade traps](#avoid-capacity-and-upgrade-traps)
- [Primary references](#primary-references)

## Select a pattern by application semantics

Choose the smallest design that satisfies the workload's availability and recovery objectives. State which failure each extra replica addresses.

| Workload | Useful initial pattern | Required validation |
| --- | --- | --- |
| Single database with restart tolerance | One pod, durable block PVC, independent database backup | Fencing, restart time, recovery after interrupted writes |
| Database with tight availability target | Database-native replication across nodes, one volume per member | Leader election, replication acknowledgement, client reconnect, PITR |
| Stateless web tier with uploads | Object API plus database metadata | Upload completion, authorization, orphan cleanup, metadata/object consistency |
| Legacy application needing a shared tree | Managed file service or supported shared filesystem | Locks, rename, permissions, mount recovery, metadata latency |
| Build cache or reproducible index | Local scratch or cache with rebuild path | Cold-start duration and whether losing it blocks service |
| ML training data | Object source with local cache, or shared parallel/file storage | Small-file overhead, data-loader concurrency, checkpoint publication |
| VM disks managed in Kubernetes | Block backend with virtualization integration | Flush/barrier behavior, migration constraints, guest-aware backup |
| Batch outputs | Local work area followed by explicit object publication | Idempotent completion and durable upload before local deletion |

For databases, ask whether the database or storage layer is authoritative for replication and promotion. A StatefulSet creates stable identities and can create per-pod claims; it does not configure database replication. Set its PVC retention policy deliberately, including scale-down behavior, instead of assuming all deletions behave identically [R1].

For uploads, an object-native design can remove shared-filesystem scheduling constraints. Preserve the application's contract: write to a temporary object/key, confirm durable completion, then publish metadata or a manifest. Define what happens if either the database transaction or object upload succeeds alone. Use reconciliation for incomplete operations. A mounted object adapter requires a separate compatibility test; adding a mount path does not supply general POSIX semantics.

For legacy RWX, distinguish a genuinely distributed file service from one NFS gateway backed by a replicated block volume. The latter may preserve storage bytes during a node failure but still requires gateway failover, endpoint takeover, lock recovery, and client reconnection. Count these in RTO. A single shared directory can also become a shared corruption or permissions failure domain.

## Recover safely after node failure

Treat `NotReady` as an observation, not proof that a machine is powered off. A partitioned kubelet may be unable to contact the control plane while its workload still writes to storage.

Use this decision sequence:

1. Identify the volume, previous writer, attachment record, backend state, and current fault. Separate application failure, kubelet failure, host failure, storage-path failure, and control-plane partition.
2. Establish whether the old writer can still issue accepted writes. Use the supported fencing mechanism: power fencing, storage-side access revocation/reservations, or a proven backend lease/quorum protocol.
3. Confirm the fence actually took effect. Merely requesting a power-off or deleting an API object is insufficient evidence.
4. Detach or recover the volume using the driver's documented procedure; allow required recovery/replay.
5. Start the replacement within supported topology. Check application consistency and current write authority before admitting traffic.
6. Record lost acknowledgements, measured RPO/RTO, and any incomplete redundancy. Restore full redundancy before the next disruptive operation.

Kubernetes supports an out-of-service taint for certain non-graceful node shutdown recovery paths. Its documentation requires verifying that the node is shut down, not merely restarting, before invoking that path. Treat it as an operational action with a fencing prerequisite, not a generic fix for a stuck pod [R2, R3].

For a local PV, there may be nothing to attach to another node. Promote an application replica or restore a replacement volume. For a cloud volume, verify that its attachment scope includes the replacement node. For a distributed filesystem, inspect surviving metadata and data quorums as well as client reachability.

Force deletion can remove the controller's record while a process survives. Do not solve multi-attach errors by repeatedly forcing detach until something mounts. Preserve evidence and determine which writer owns the latest committed state.

## Design the bootstrap path

List everything needed to recreate service when the cluster is gone:

| Dependency | Store or reconstruct independently |
| --- | --- |
| Infrastructure definition | Network, compute, IAM, firewall, and storage topology declarations |
| Cluster identity/configuration | Version, node configuration, required CA and recovery material |
| Storage control metadata | Cluster IDs, pool maps, device mappings, provisioner configuration |
| Data-access credentials | Cloud API credentials, object credentials, encryption keys and KMS access |
| Software supply | Required images, charts, package mirrors and compatible binaries |
| Application definition | Manifests, operator CRDs/versions, configuration, schemas |
| Backup catalog | Backup identifiers, manifests, chains, timestamps, checksums, WAL/log ranges |
| Human procedure | Restore order, endpoint promotion, validation and escalation ownership |

Detect circular dependencies: a registry required to start storage cannot have its only copy on unavailable storage; a KMS needed to decrypt a volume cannot rely solely on that volume; a GitOps controller cannot fetch the only recovery instructions from a repository hosted inside the failed cluster. Keep a minimal bootstrap kit outside the fault domain, with appropriate secret protection.

For storage run inside Kubernetes, document which functions still work without Kubernetes and which need the operator or API. External storage can reduce some lifecycle coupling but introduces another system to operate. Make the tradeoff explicit.

## Back up independent layers

Protect at least three categories separately:

1. **Kubernetes control state:** etcd snapshots or the distribution's supported equivalent, plus the material required to decrypt and restore that state. etcd stores Kubernetes objects; it does not contain the ordinary bytes of mounted PVs [R4].
2. **Application data:** database-aware base backups and logs/PITR, or filesystem/object datasets captured at an appropriate consistency boundary.
3. **Storage and access metadata:** driver/backend identities, keys, bucket policies, share permissions, mappings, restore catalogs and off-cluster dependencies.

A control-plane restore can resurrect references to volumes that no longer exist. A volume restore can contain valid files but lack the Kubernetes objects and credentials needed to mount them. Build and test the mapping between restored logical claims and actual backend resources.

Use volume snapshots for rapid local recovery where available, and verify whether snapshot bytes remain in the source service, zone, account, or cluster. Export or back up to an independently protected destination when the required fault includes loss of that system. Kubernetes snapshot objects describe backend snapshots; the object itself is not a transportable backup [R5].

Restoring all resources from an old etcd snapshot also restores old configuration and possibly old secret references. Reconcile intended infrastructure and workloads carefully; prevent duplicate controllers or writers from using the same restored volume. Stage restore validation before reopening public traffic.

## Test the failure model

Agree on permitted tests and use disposable data or a staging environment for destructive failure injection. Define success in terms of observed application behavior, not merely green pods.

| Experiment | Evidence to collect |
| --- | --- |
| Restart one application pod | Committed data survives; client retries do not duplicate business operations |
| Lose a worker | Correct writer promotion; supported mount path; measured recovery time |
| Partition an old writer from control plane | It cannot produce accepted conflicting writes after promotion |
| Lose one storage replica/domain | Acknowledgement policy remains valid; degraded alerts and rebuild work |
| Exhaust capacity/inodes | Useful errors, bounded retries, no hidden success acknowledgements |
| Rotate or expire credentials | Existing and new data paths behave as expected; recovery access remains available |
| Recreate the cluster | Data restores without access to destroyed cluster state |
| Restore to another site | All needed bytes, keys, permissions, images, and catalog entries are available |

Write uniquely identifiable transactions before and during the test. Compare the acknowledged set with the recovered set. A successful filesystem mount proves much less than a successful application integrity check.

Test failback too. Returning to the old location requires choosing one authoritative dataset, reseeding stale replicas, fencing obsolete leaders, and coordinating endpoints. DNS changes alone do not synchronize data or revoke old writers.

## Avoid capacity and upgrade traps

Reserve enough free capacity and network budget to rebuild after the planned fault while serving normal load. Keep pod disruption budgets, storage quorum requirements, replica rebuild status, node drains, and provider maintenance windows aligned. A disruption budget protects only the operations within its scope; it cannot prevent a failed disk or lost site.

Before shrinking a node pool, check local data, replica placement, attachment limits, spare capacity, and whether replicas have genuinely moved. A node marked unschedulable may still hold necessary storage copies. Before upgrading a storage engine, verify on-disk and protocol compatibility and the permitted rollback path; a Helm rollback is not necessarily a data-format rollback.

Define alerts for backend degradation, missing replicas, failed backups, restore-test age, replication lag, capacity/inodes, mount errors, and application fsync/tail latency. A storage system can accept reads while no longer meeting the required write durability. Alert on that distinction.

## Primary references

- **R1:** [StatefulSet identity and PVC retention](https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/).
- **R2:** [Node shutdown behavior and non-graceful recovery](https://kubernetes.io/docs/concepts/cluster-administration/node-shutdown/).
- **R3:** [Non-graceful shutdown feature and prerequisite](https://kubernetes.io/blog/2023/08/16/kubernetes-1-28-non-graceful-node-shutdown-ga/).
- **R4:** [Operating and recovering etcd for Kubernetes](https://kubernetes.io/docs/tasks/administer-cluster/configure-upgrade-etcd/).
- **R5:** [Volume snapshot contract](https://kubernetes.io/docs/concepts/storage/volume-snapshots/).

The workload patterns, bootstrap inventory, and failure experiments are design guidance. Validate concrete behavior with the chosen application, distribution, CSI implementation, and backend.
