# Kubernetes storage: contracts, scheduling, and lifecycle

Evidence checked: 2026-10-21. Match Kubernetes, CSI driver, sidecar, kernel, and storage-system versions before implementing features. Treat the current documentation URLs as moving references.

## Contents

- [Model the layers](#model-the-layers)
- [Choose the access contract](#choose-the-access-contract)
- [Schedule where the data can exist](#schedule-where-the-data-can-exist)
- [Control the lifecycle](#control-the-lifecycle)
- [Trace a failed operation](#trace-a-failed-operation)
- [Select an implementation family](#select-an-implementation-family)
- [Primary references](#primary-references)

## Model the layers

Draw the complete path before recommending a StorageClass:

`application → container mount or device → node client → storage service → media and replicas`

Identify the owner of every transition. Kubernetes coordinates claims, placement, attachment, and mounts; the backend determines where bytes reside and which failures they survive. A CSI driver adapts those operations to a backend. An operator reconciles the lifecycle of a storage system or database. None of these labels alone establishes durability.

| Object or component | Use it to describe | Do not infer |
| --- | --- | --- |
| PersistentVolumeClaim (PVC) | Namespaced request for capacity and access | A separately backed-up dataset |
| PersistentVolume (PV) | Cluster resource representing storage | Physical redundancy or cross-site access |
| StorageClass | Provisioner and provisioning policy | That every driver implements every parameter |
| CSI controller | Backend provisioning, attachment, expansion, snapshots when supported | That existing reads always require its API |
| CSI node plugin | Node-side publish, mount, device operations | That another node already holds a replica |
| Storage operator | Reconciliation of storage daemons, resources, upgrades | Freedom from storage administration |
| StatefulSet | Stable workload identity and per-instance storage association | Database replication or leader election |

Separate control-plane health from data-plane health. A failed CSI controller may prevent new attachments while existing mounts continue working; an unavailable storage server can interrupt I/O even when every Kubernetes API object appears healthy. Confirm the actual implementation before attributing an outage to either layer.

## Choose the access contract

Use the Kubernetes access modes precisely [K1, K2]:

| Mode | Requested access scope | Design consequence |
| --- | --- | --- |
| `ReadWriteOnce` (RWO) | Read-write from one node | Several pods on that node can still use the volume |
| `ReadWriteOncePod` (RWOP) | Read-write by one pod across the cluster | Requires compatible CSI implementation and sidecars |
| `ReadOnlyMany` (ROX) | Read-only access from many nodes | Enforce read-only behavior in the mount/backend too |
| `ReadWriteMany` (RWX) | Read-write access from many nodes | Application must still coordinate concurrent changes |

Treat access modes as API and scheduling contracts, not a transaction protocol. RWO is not a database mutex. RWX does not make concurrent database processes sharing one data directory safe. RWOP improves workload exclusivity but does not replace backend fencing after a partition or protect writers outside Kubernetes.

`volumeMode: Filesystem` presents a directory; `volumeMode: Block` presents a raw device [K1]. The latter requires an application designed to manage a raw block device. It does not mean object storage, replicated storage, or automatically faster end-to-end service. Choose based on the application's I/O contract and measure the complete path.

For shared files, verify locking, atomic namespace operations, permissions, identities, cache behavior, and recovery after disconnection. For object-native applications, use an SDK/API and credentials directly; a PVC is not required merely because the process runs in Kubernetes. A bucket provisioner or object-storage custom resource manages a different contract from a file/block PVC.

## Schedule where the data can exist

Treat placement as the intersection of constraints:

1. Where can this storage be attached or reached?
2. Where can the pod run given CPU, GPU, architecture, affinity, and taints?
3. Where are surviving storage replicas and their required quorum?
4. Which failure domains must remain independent?

For topology-constrained storage, use `WaitForFirstConsumer` when supported so provisioning considers pod placement. Avoid `nodeName` for that workflow because it bypasses the scheduler; use scheduling constraints instead. Explicitly review `allowedTopologies`, PV node affinity, and driver-provided topology keys [K3]. Do not invent zone labels that imply stronger physical independence than the provider documents.

Local PVs bind workload placement to the node holding the data. They can be appropriate for a database that replicates across nodes, for rebuildable indexes, or for scratch workloads. A node failure then requires application failover, node recovery, or restore. A dynamically provisioned local directory remains local storage; dynamic provisioning does not add replication.

`hostPath` exposes a path from the selected host and brings host-access risks. An identically named directory on another node is not the same dataset. `emptyDir` is tied to pod lifetime and is suitable for temporary work; distinguish container restart from pod replacement. Memory-backed `emptyDir` also competes for memory [K4].

Place both workload replicas and storage replicas across the intended domains. Pod anti-affinity without storage placement can leave all copies on one machine; storage replication without sufficient schedulable compute can preserve bytes while the application remains unavailable.

## Control the lifecycle

Write an explicit lifecycle policy before enabling automatic provisioning:

| Event | Required decision |
| --- | --- |
| PVC deleted | Retain backend data or delete it; inspect the actual PV reclaim policy |
| StatefulSet scaled down or removed | Determine PVC retention policy and owner references separately |
| Node replaced | Detach/fence safely, then attach only within supported topology |
| Capacity increased | Grow backend, then device/partition/filesystem as applicable |
| StorageClass changed | Determine which changes affect new volumes versus existing volumes |
| Snapshot deleted | Follow snapshot deletion policy and backend retention behavior |
| Cluster destroyed | Preserve data, credentials, restore catalog, and independent backup as required |

Use `Retain` for data that must survive claim deletion, while accepting that manual reclamation is then needed. A `Delete` reclaim policy can remove the actual backend volume. Finalizers coordinate lifecycle operations; removing them to clear a stuck object can orphan data or bypass cleanup. Diagnose the owner and backend state first [K1, K3].

Check both the StorageClass expansion setting and the driver's capabilities. Expansion may need node-side filesystem work; shrinking is usually a migration to a new volume rather than a reverse expansion operation. Do not edit PV capacity to impersonate a completed storage resize.

CSI snapshots require the snapshot API/controller machinery and backend support. `readyToUse` means the backend snapshot can be used; it does not establish application consistency, separate-site survival, or successful restoration. For multiple database volumes, coordinate writes and snapshot boundaries or use database-aware backup. Distinguish `VolumeSnapshot`, `VolumeSnapshotContent`, and `VolumeSnapshotClass` ownership and retention [K5].

Clones are new volumes from an existing dataset where supported; verify source/target size, mode, namespace and backend restrictions. They are useful for tests or migration but may share a physical failure domain with the source [K6].

## Trace a failed operation

Start with read-only evidence, scoped to the affected namespace and resource:

```sh
kubectl get storageclass
kubectl get pvc -n WORKLOAD_NAMESPACE
kubectl describe pvc CLAIM_NAME -n WORKLOAD_NAMESPACE
kubectl describe pod POD_NAME -n WORKLOAD_NAMESPACE
kubectl get volumeattachments
kubectl get csidrivers
kubectl get events -n WORKLOAD_NAMESPACE --sort-by=.metadata.creationTimestamp
```

Resolve placeholders before running. Inspect only relevant driver logs; redact tokens, endpoint credentials, tenant paths, and application data when sharing evidence.

| Symptom | Investigate first |
| --- | --- |
| PVC Pending | Provisioner health, missing class, topology, quota, backend capacity, first consumer |
| Pod Pending with bound PVC | PV node affinity, attach limits, pod constraints, unavailable eligible nodes |
| Multi-attach error | Previous node/writer state, fencing, detach completion, backend attachment record |
| Mount failure | Filesystem support, device identity, permissions, network/authentication, node-plugin logs |
| Slow mount | Large ownership changes, metadata traversal, replay/recovery, remote service latency |
| Running pod with I/O errors | Backend health, network, filesystem errors, exhausted space/inodes, lost quorum |
| Stuck termination | Unmount blockers, unreachable node, CSI failure, finalizer dependency |

Do not equate deleting a pod with stopping its process on an unreachable machine. For force-detach and non-graceful shutdown procedures, read `kubernetes-recovery-and-patterns.md`.

## Select an implementation family

Choose a backend separately from its Kubernetes integration:

| Family | Representative example | Operational responsibility |
| --- | --- | --- |
| Provider-managed block | Cloud volume CSI | Attachment/topology, data backup, application HA |
| Provider-managed file | NFS/SMB CSI | Share permissions, semantics, service-class topology |
| Distributed storage cluster | Rook-managed Ceph | OSDs, monitors, placement, capacity, recovery, upgrades |
| Per-volume replicated block | Longhorn | Replica scheduling, engine lifecycle, rebuild and backup paths |
| Replicated block management | LINSTOR/DRBD with CSI | Storage pools, replication, quorum/fencing, controller recovery |
| Local provisioning | Local PV/local CSI family | Node-bound data and application-level resilience |

Rook manages Ceph and exposes its block, file, or object interfaces; these are distinct services over a shared storage foundation [K7]. Longhorn and LINSTOR represent different replicated-block designs; inspect each version's data engine and access implementation rather than treating their checkboxes as interchangeable [K8, K9]. Avoid stacking three-way storage replication beneath three database replicas without explaining the additional failure coverage and capacity/write cost.

## Primary references

- **K1:** [Kubernetes Persistent Volumes](https://kubernetes.io/docs/concepts/storage/persistent-volumes/).
- **K2:** [ReadWriteOncePod enhancement and design](https://github.com/kubernetes/enhancements/blob/master/keps/sig-storage/2485-read-write-once-pod-pv-access-mode/README.md).
- **K3:** [StorageClasses](https://kubernetes.io/docs/concepts/storage/storage-classes/).
- **K4:** [Volume types, local, hostPath, emptyDir](https://kubernetes.io/docs/concepts/storage/volumes/).
- **K5:** [Volume snapshots](https://kubernetes.io/docs/concepts/storage/volume-snapshots/).
- **K6:** [CSI volume cloning](https://kubernetes.io/docs/concepts/storage/volume-pvc-datasource/).
- **K7:** [Rook Ceph documentation](https://rook.io/docs/rook/latest/Getting-Started/intro/).
- **K8:** [Longhorn documentation](https://longhorn.io/docs/latest/).
- **K9:** [LINSTOR guide](https://linbit.com/drbd-user-guide/linstor-guide-1_0-en/).

Use these sources for product/API contracts. Treat architecture recommendations and failure-analysis tables above as engineering guidance requiring verification against the selected deployment.
