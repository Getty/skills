# Provider service families and portability

Evidence checked: 2026-10-21. This is a capability map, not a price ranking or promise that every product exists in every region. Recheck product availability, service class, maturity, limits and API support for the target deployment.

## Contents

- [Map a requirement before choosing a product](#map-a-requirement-before-choosing-a-product)
- [Current service-family map](#current-service-family-map)
- [Compare contracts rather than labels](#compare-contracts-rather-than-labels)
- [Translate an AWS design to a different provider](#translate-an-aws-design-to-a-different-provider)
- [Validate portability](#validate-portability)
- [Primary references](#primary-references)

## Map a requirement before choosing a product

Describe the requirement as an interface plus a failure/recovery contract:

- “A writable filesystem for one database instance with durable fsync and tested promotion” is more useful than “something like EBS.”
- “A shared namespace with the application's locking and rename behavior” is more useful than “RWX storage.”
- “An object repository with verified conditional writes, retention, encryption and an independent restore path” is more useful than “S3 compatible.”

Then identify the managed product, the application's own replication feature, or the system the operator must run. Do not assume that using a lower-cost provider requires recreating every hyperscaler service; the application may need only a small subset of those capabilities.

## Current service-family map

| Provider | Durable block family | Shared file family | Object family | What to inspect next |
| --- | --- | --- | --- | --- |
| AWS | EBS | EFS; FSx variants | S3 and its distinct bucket/storage classes | AZ scope, multi-attach constraints, filesystem variant, single-zone versus regional protection [P1–P4] |
| Microsoft Azure | Managed Disks; Elastic SAN for appropriate workloads | Azure Files; Azure NetApp Files; Managed Lustre for parallel workloads | Blob Storage, including Data Lake features where configured | Redundancy option, protocol, hierarchical namespace, client and region support [P5] |
| Google Cloud | Hyperdisk; Persistent Disk for supported machine series | Filestore; specialized options selected by workload | Cloud Storage | Instance compatibility, zonal/regional block type, Filestore tier and object location/class [P6–P8] |
| Hetzner | Cloud Volumes; operator-controlled dedicated disks | Storage Box for its supported file/backup protocols; Storage Share for Nextcloud collaboration; self-managed file service where needed | Hetzner Object Storage | Single attachment, volume-backup gap, one-DC bucket placement, exact S3 exceptions [P9] |
| OVHcloud | Public Cloud Block Storage | Managed File Storage using NFS and Kubernetes integration | S3-compatible Object Storage; distinguish older Swift-based offerings | Class/region and maturity; roadmap features are not deployed guarantees [P10–P12] |
| Scaleway | Block Storage | File Storage for supported Instances | S3-compatible Object Storage | Instance/zone support, attachment/access mechanism, shared-filesystem semantics and service maturity [P13–P15] |
| DigitalOcean | Volumes Block Storage | Network File Storage | S3-compatible Spaces | Actual region/tier support, VPC access, snapshot and Kubernetes integration [P16, P17] |

Treat products in a row as different contracts, not drop-in substitutes. For example, AWS FSx comprises ONTAP, OpenZFS, Windows File Server and Lustre offerings; select the particular filesystem and deployment type [P3]. Likewise, “object” does not mean all S3 features are implemented, and a provider-native object API may require different authentication or client operations.

Do not repeat old assumptions that smaller providers have no managed file services. Current official documentation lists file offerings at OVHcloud, Scaleway and DigitalOcean. Verify where and how the selected service is usable; a product announcement or roadmap is weaker evidence than a supported provisioning contract for the target region.

## Compare contracts rather than labels

Use this worksheet for every serious candidate:

| Axis | Questions that change the architecture |
| --- | --- |
| Interface | Raw block, filesystem protocol/version, object API and feature subset? |
| Consistency | What becomes visible after success; how are concurrent changes resolved? |
| Durability | Which replicas/media must acknowledge; which failures are documented? |
| Availability | Can existing clients continue I/O during backend/control-plane failure? |
| Placement | Host, rack, data center, zone, region, account and key-management scope? |
| Lifecycle | Behavior on stop, restart, deletion, snapshot removal, cluster teardown? |
| Shared access | Single attachment, multi-attach, shared namespace, application-safe concurrent writers? |
| Recovery | Snapshot/export, independent backup, cross-region copy, cold-restore speed, failback? |
| Performance | Read/write tail latency, fsync, metadata rate, throughput, IOPS, burst limits? |
| Security | Identities, access boundaries, key custody, audit, retention and deletion controls? |
| Economics | Allocated capacity, request/egress costs, extra replicas, provisioned performance, operator time? |

A provider SLA is not a measurement of your application RTO, a durability percentage is not a backup policy, and multi-zone data protection is not protection against a compromised administrator deleting every copy. Translate each requirement to a testable mechanism.

Evaluate protocol access from the actual client environment. An NFS service reachable within one provider network may require routed connectivity for local machines. A service called File Storage may use an attachment mechanism or restrictions different from an ordinary public NFS endpoint. A private endpoint improves network exposure control; it does not automatically provide encryption, identity correctness, or site redundancy.

## Translate an AWS design to a different provider

Extract the behavior the application depends on rather than copying resource names:

| Existing dependency | Functional requirement | Candidate translation |
| --- | --- | --- |
| One EBS-backed server | Persistent single-writer block data | Another managed volume plus its attach/fence/backup workflow |
| EFS-mounted application replicas | Shared file namespace and supported concurrency | Verified managed file service, or self-managed HA file architecture |
| S3 SDK for uploads | Shared object access and publication | Compatible object service after exact request/response tests |
| S3 events trigger processing | Reliable change notification and replay | Supported provider events, an application queue/outbox, or reconciliation polling |
| Cross-region object replication | Independent second-site object copy | Verified native replication or external copy/backup with lag and deletion rules |
| Managed database failover | Database-aware promotion and client continuity | Another managed database or an operator-owned database replication design |
| Snapshot-based recovery | Point-in-time recoverable dataset | Provider snapshots where supported or application/file backup with measured restore |

The translation may change application code and operating procedures. If a destination lacks conditional writes required by a lock or manifest protocol, replacing them with “upload then check” is not equivalent. If the application depends on a managed HA file service, replacing it with one VM serving NFS transfers availability and repair responsibilities to the operator.

Select the translation whose ongoing operational burden is realistic for the team. Include upgrade handling, monitoring, restore drills, hardware replacement, credential recovery and emergency diagnosis. Model both cost and recovery effort at the expected scale, including a realistic failure during maintenance.

## Validate portability

Run a disposable compatibility suite against the exact service and configuration:

1. Exercise actual application operations: object conditions/versioning, file locks and atomic operations, or block flush/recovery.
2. Confirm error handling, retries, pagination, timeouts, multipart resume and idempotency where relevant.
3. Read the data from the intended replacement compute and another required location.
4. Restore after removing access to the original system's catalog and credentials, using the documented recovery materials.
5. Verify the backup's retention and deletion protection with least-privilege test credentials.
6. Benchmark cold start and degraded/recovery states as well as steady state.

Record unresolved capabilities as unknown rather than filling a comparison cell with a checkmark. Attach evidence date, service class, region, API/driver version and observed test outcome to the final decision.

## Primary references

- **P1:** [AWS EBS volumes](https://docs.aws.amazon.com/ebs/latest/userguide/ebs-volumes.html).
- **P2:** [Amazon EFS](https://docs.aws.amazon.com/efs/latest/ug/whatisefs.html).
- **P3:** [Amazon FSx filesystem families](https://aws.amazon.com/fsx/).
- **P4:** [Amazon S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html).
- **P5:** [Azure storage services](https://learn.microsoft.com/en-us/azure/storage/common/storage-introduction).
- **P6:** [Google Cloud disk options](https://docs.cloud.google.com/compute/docs/disks).
- **P7:** [Filestore overview](https://docs.cloud.google.com/filestore/docs/overview).
- **P8:** [Google Cloud storage strategy and service options](https://docs.cloud.google.com/architecture/storage-advisor).
- **P9:** [Hetzner storage comparison](https://docs.hetzner.com/storage/general/which-storage-is-right-for-me/); read `hetzner-storage.md` for feature-specific evidence.
- **P10:** [OVHcloud block classes](https://docs.ovhcloud.com/en/guides/storage-and-backup/block-storage/block-storage-the-right-storage-class).
- **P11:** [OVHcloud managed File Storage](https://www.ovhcloud.com/en/public-cloud/file-storage/).
- **P12:** [OVHcloud object storage and legacy Swift distinction](https://docs.ovhcloud.com/en/guides/storage-and-backup/object-storage/s3-getting-started-with-object-storage).
- **P13:** [Scaleway Block Storage](https://www.scaleway.com/en/docs/block-storage/).
- **P14:** [Scaleway File Storage](https://www.scaleway.com/en/docs/file-storage/).
- **P15:** [Scaleway Object Storage](https://www.scaleway.com/en/docs/object-storage/).
- **P16:** [DigitalOcean storage catalog](https://docs.digitalocean.com/products/storage/).
- **P17:** [DigitalOcean Network File Storage](https://docs.digitalocean.com/products/nfs/).

The comparison procedure and translation examples are original engineering guidance. Product-specific cells are dated observations from the listed primary sources.
