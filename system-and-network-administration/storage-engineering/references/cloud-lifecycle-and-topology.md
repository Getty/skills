# Cloud storage lifecycle and topology

Evidence checked: 2026-10-21. Use this as a provider-independent design procedure; verify every lifecycle and topology contract for the actual service, region, account, instance family, and API version.

## Contents

- [Separate lifetime from physical location](#separate-lifetime-from-physical-location)
- [Build a lifecycle matrix](#build-a-lifecycle-matrix)
- [Map the actual failure domains](#map-the-actual-failure-domains)
- [Design replacement and relocation](#design-replacement-and-relocation)
- [Operate with a limited managed-storage catalog](#operate-with-a-limited-managed-storage-catalog)
- [Model control dependencies and cost](#model-control-dependencies-and-cost)
- [Primary references](#primary-references)

## Separate lifetime from physical location

Classify cloud storage along independent axes: the API the application sees, the resource that owns its lifetime, its attachment or network scope, its data-protection mechanism, and the administrator responsible for recovery.

| Storage form | Application view | Lifecycle questions |
| --- | --- | --- |
| Instance-local disk | Block device or mounted filesystem | Does data survive reboot, stop/start, host replacement, resize, rebuild, deletion? |
| Persistent network block volume | Block device, usually formatted by guest | Is deletion independent from instance lifetime; what deletion flags apply? |
| Managed file service | Shared namespace over file protocol | Does share deletion remove all snapshots; which networks can reach it? |
| Object service | API over keys and objects | Who can delete versions, buckets, policies, or encryption keys? |
| Snapshot/image | Captured state used to create another resource | Which disks are included; where are snapshot bytes stored; how quickly can they be read? |
| External backup repository | Backup-specific objects/files and catalog | Can it restore without the original account, cluster, keys, or vendor control plane? |

Do not equate “local” with “lost on every reboot.” Providers can preserve an instance's local root disk across normal power cycles, while still coupling it to that instance or host. Conversely, “persistent volume” means a resource may outlive compute, not that every deletion workflow will retain it.

AWS illustrates the distinction: instance store is temporary host-attached storage, while EBS is independently persistent block storage with attachment scoped to an Availability Zone [C1, C2]. Google distinguishes durable Hyperdisk/Persistent Disk from Local SSD and makes instance-family compatibility explicit [C3]. Re-derive the contract for Hetzner and every other provider instead of copying AWS assumptions.

## Build a lifecycle matrix

Fill this matrix from current provider documentation, infrastructure code, and a non-production verification before describing a workload as replaceable:

| Event | Root disk | Data volume | File/object service | Backup and keys |
| --- | --- | --- | --- | --- |
| Reboot | Exact persistence contract | Attachment/mount behavior | Client retry/session recovery | Availability independent of reboot |
| Stop/start | Host migration or data-retention contract | Attachment preserved or recreated | Credentials/network still valid | Retention continues |
| Instance deletion | Delete/retain behavior | Delete-on-termination or independent deletion | Explicit/implicit cleanup policies | Server-bound backups may be removed |
| Rebuild/reimage | Usually replacement of OS contents; verify | Formatting and attachment effects | Identity/configuration changes | Backup of pre-rebuild state exists |
| Resize or machine-family change | Disk/network limits and compatibility | Driver and performance limits | Endpoint path unchanged or reconfigured | Restore to target family possible |
| Zone/location failure | Replacement elsewhere possible? | Can existing volume attach there? | Service-class failure scope | Independent copy and keys reachable |
| Account/project deletion | Resource deletion scope | Same | Same | Independent administrator/account needed? |

Do not fill unknown cells with “probably persists.” State the uncertainty and either check the API/contract or design a controlled test. Infrastructure-as-code can deliberately destroy resources that the underlying provider would otherwise retain. Review lifecycle flags, state ownership, module cleanup scripts, Kubernetes reclaim policies, and user interface deletion options together.

Keep durable data resources separately identifiable from ephemeral workers. Use stable resource IDs and filesystem identifiers rather than assuming `/dev/sdb` always names the same volume. Recreating compute should attach or restore the intended dataset, not create an empty directory that accidentally allows the service to start without data.

## Map the actual failure domains

Distinguish host, enclosure, rack, power domain, storage cluster, network fabric, data center, availability zone, region, provider account, and administrative credential. Physical geography and API naming do not always match.

For each stored copy, record:

- Where the data is physically protected, to the extent the provider documents it.
- Which domains share networking, identity, control plane, billing, encryption keys, and operators.
- Which failures are covered by the documented service class, and which require another copy.
- Whether the surviving copy remains reachable by clients and can accept safe writes.

Do not translate a location into an AWS-style multi-AZ region without evidence. A provider network spanning two cities supplies connectivity, not cross-city storage replication. An anti-affinity or spread placement rule for VMs does not necessarily place their managed volume replicas in separate zones.

Compare service classes, not just service names. EFS offers Regional and One Zone forms with different protection scopes [C4]. Google exposes zonal and regional/HA block options with distinct provisioning and failover behavior [C5]. Azure redundancy choices similarly change copy placement and recovery characteristics [C6]. A generic “cloud filesystem” label omits the decision that matters.

Separate data survival from service continuity. A volume can retain all data while the regional attachment API is unavailable. A surviving replica can remain unusable because the only KMS, DNS zone, VPN gateway, or database leader-election service is down.

## Design replacement and relocation

For replacement within a supported attachment domain:

1. Confirm whether the old writer is still active; fence it using the supported mechanism.
2. Stop or quiesce writes where possible and confirm backend detach completion.
3. Start compatible compute with enough CPU, memory, networking and disk bandwidth.
4. Attach by verified identity, unlock as necessary, mount without reformatting, and allow filesystem/application recovery.
5. Validate state and then redirect traffic.

For movement beyond the attachment domain, choose a data-transfer mechanism: snapshot copy and new volume, application replication, file replication, object replication, or backup restore. A new VM in a remote region cannot be assumed to attach the old block device. Define a cutover watermark and a single authoritative writer.

Include data-transfer duration in RTO. Snapshot restore may expose a volume before every block is locally initialized; verify first-read latency and any prewarming/initialization options. Test the application after cold restore, not only an already warmed benchmark. If the destination lacks capacity for the required instance or disk class, a perfect backup alone will not meet the service deadline.

For autoscaling, decide which state is disposable. Cache and scratch capacity can grow with workers if loss is tolerable. Stateful shards need a membership and redistribution protocol. Scaling a deployment does not create more independent copies of a shared single-writer volume.

## Operate with a limited managed-storage catalog

When a provider lacks the exact managed service required by the application, compare these choices explicitly:

| Choice | What it solves | Work that remains |
| --- | --- | --- |
| Use available managed block | Durable per-instance/volume data | Shared access, application failover, independent backup |
| Run an NFS/SMB gateway | Shared file protocol for existing software | Gateway HA, locks, backend protection, performance, upgrades |
| Run distributed storage on dedicated nodes | Control of replication, placement, interfaces | Quorum, recovery, hardware lifecycle, spare capacity, on-call expertise |
| Replicate inside the application | Application-aware failover and consistency | Leader election, bootstrap/reseed, backups, client routing |
| Refactor bulk data to object APIs | Shared object access decoupled from worker lifetime | Upload/publication semantics and application changes |
| Use another provider's managed service | Outsource an unavailable capability | WAN latency, egress, identity, dependency and restore complexity |

Avoid using a distributed storage cluster merely to make a small application “cloud native.” Compare expected downtime and recovery labor against operational complexity. Conversely, do not hide a critical single file server behind an HA load balancer and call the storage highly available.

For self-managed storage, dedicated machines may provide more predictable media and network access than small VMs, but budget hardware failure replacement and control-plane hosting. If using managed block volumes as backing disks for another replicated storage layer, calculate compounded write amplification, copy count, network traffic and common-mode failure before claiming additional resilience.

## Model control dependencies and cost

Record data-plane and control-plane requirements separately. Existing mounted volumes may remain usable while create/attach operations fail; object requests may require online authentication or keys. Design recovery without assuming that all provider APIs will be healthy during the outage being mitigated.

Calculate cost from the complete workload:

`provisioned storage + replicas + snapshots/backups + requests + data transfer + provisioned IOPS/throughput + required compute/network + operations`

Include minimum sizes, retained noncurrent object versions, multipart remnants, snapshot growth, idle volumes, cross-zone traffic, restore egress and temporary double capacity during migration. Prices and free-transfer rules are time-sensitive; fetch them for the actual source/destination pair rather than embedding old figures.

Evaluate portability with a restore rehearsal. An S3-compatible client may still depend on unsupported conditional writes, object lock, IAM policy elements or replication features. A filesystem image may depend on kernel features unavailable on the replacement host. A cloud snapshot is only as portable as its export/restore path.

## Primary references

- **C1:** [AWS instance store](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/InstanceStorage.html).
- **C2:** [AWS EBS volumes and attachment scope](https://docs.aws.amazon.com/ebs/latest/userguide/ebs-volumes.html).
- **C3:** [Google Cloud disk choices](https://docs.cloud.google.com/compute/docs/disks).
- **C4:** [EFS filesystem types and interfaces](https://docs.aws.amazon.com/efs/latest/ug/whatisefs.html).
- **C5:** [Regional Persistent Disk and Hyperdisk HA in GKE](https://docs.cloud.google.com/kubernetes-engine/docs/how-to/persistent-volumes/regional-pd).
- **C6:** [Azure Storage overview and redundancy options](https://learn.microsoft.com/en-us/azure/storage/common/storage-introduction).

The lifecycle matrix and design procedures are engineering analysis, not claims that every provider exposes identical behavior.
