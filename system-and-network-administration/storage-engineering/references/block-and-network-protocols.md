# Block access and storage transports

Evidence checked: 2026-10-21. Separate transport standards from a particular target's supported commands, availability design, security configuration, and operating-system support.

## Contents

- [Separate topology from the interface](#separate-topology-from-the-interface)
- [Compare transport families](#compare-transport-families)
- [Choose an ownership model](#choose-an-ownership-model)
- [Design multipath and failover](#design-multipath-and-failover)
- [Account for networking and security](#account-for-networking-and-security)
- [Validate a remote block service](#validate-a-remote-block-service)
- [Primary references](#primary-references)

## Separate topology from the interface

Treat a block service as an addressable range of sectors or logical blocks. The host may put a filesystem on it, give it to a VM, or let a database use it directly. The service does not inherently understand filenames, application transactions, or who may concurrently modify filesystem metadata.

| Term | Meaning | What it does not establish |
| --- | --- | --- |
| DAS | Direct-attached storage from a host's perspective | Device redundancy, host availability, or backup |
| NAS | File service exposed over a network | A particular disk layout or protection scheme |
| SAN | A network/fabric used to expose storage, commonly block devices | Safe concurrent filesystem mounting or automatic disaster recovery |
| Disaggregated storage | Compute and persistent storage can scale or fail independently | Independence from the network, control plane, or provider region |
| Hyperconverged storage | Compute nodes also provide storage resources | Adequate capacity during maintenance or independent failure domains |
| LUN / namespace | A presented logical storage unit | One physical disk, one failure domain, or one performance budget |

One physical system may serve block, file, and object interfaces. Identify the data path of the specific workload rather than assigning behavior based on the product's category.

## Compare transport families

| Family | Core mechanism | Typical decision criteria |
| --- | --- | --- |
| iSCSI | Carries SCSI commands over TCP/IP between initiator and target | Existing Ethernet, target interoperability, authentication, multipath, queueing, network isolation |
| Fibre Channel | Purpose-built storage fabric carrying protocols such as SCSI/FCP; NVMe/FC is another option | HBAs, switches, zoning, dual fabrics, operational skills and vendor support |
| NVMe/TCP | NVMe commands over TCP networks | Ordinary Ethernet reach, host/target support, CPU and network performance, authentication/security capabilities |
| NVMe/RDMA | NVMe transport using an RDMA-capable fabric | NIC/switch support, RDMA transport choice, congestion control and failure handling |
| Network block device / virtual block protocols | Export a block abstraction through software or a hypervisor | Exact flush, discard, authentication, reconnection, caching, and migration contracts |
| Storage-system client | A native driver/library accesses a distributed block image | Cluster-aware placement, client/cluster compatibility, locking and recovery support |

The iSCSI standard defines a SCSI transport over TCP; it does not prescribe the target's RAID, replication, or availability architecture. NVMe specifications separately define commands and transports. Check the current specification set instead of assuming every NVMe capability is implemented by every namespace or transport. [iSCSI RFC 7143](https://www.rfc-editor.org/rfc/rfc7143), [NVMe specifications](https://nvmexpress.org/specifications/)

Compare devices at the same boundary: host-visible I/O completion, application transaction commit, or replicated durable commit. A faster transport may leave the actual bottleneck unchanged if the target serializes flushes, the network is oversubscribed, or the application performs one synchronous operation at a time.

## Choose an ownership model

Select one explicit model before allowing multiple attachments:

1. **Single active writer:** one host owns the filesystem or database. A replacement must establish that the former owner cannot continue writing before activating the same storage.
2. **Read-only shared image:** multiple readers consume an immutable image. Specify how a new version is published and how readers switch. A concurrent writer invalidates the simplicity of this model.
3. **Cluster-aware filesystem:** cooperating hosts coordinate metadata and cache state using the filesystem's lock manager and fencing design. GFS2 is an example, not an instruction to place arbitrary filesystems on shared disks.
4. **Application-controlled raw block:** a specifically designed application coordinates access itself and has a documented support contract.

Never mount an ordinary ext4, XFS, or similar single-host filesystem read/write on independent machines merely because an API permits multi-attach. Each host can cache inconsistent metadata and overwrite another host's allocation decisions. Replicating blocks faithfully can replicate that corruption faithfully.

Distinguish filesystem locks from storage ownership. File locks do not protect an unaware host's block-level metadata cache. Likewise, network reachability is not proof that a previous writer has stopped. SCSI persistent reservations or NVMe reservations can support fencing, but reservation type, transport support, key management, reset behavior, and cluster integration must be verified. A reservation feature alone is not a complete cluster design.

For shared-disk clusters, include membership, distributed locking, fencing, and quorum in the same acceptance test. Red Hat's GFS2 documentation is a concrete example of why storage access can intentionally stop when membership and fencing are unsafe. [GFS2 administration](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/9/html-single/configuring_gfs2_file_systems/index)

## Design multipath and failover

Use multipathing to present several routes to the same logical device as one device. It can survive a path failure and, for supported target layouts, distribute work. It does not create a second copy of the data.

Draw two genuinely independent paths, including NIC/HBA, switch, cable, target port, controller, and power. Two VLANs on one switch or two sessions through one NIC may have one common failure point. Treat active/active and active/passive target ports according to their advertised access state; do not load-balance blindly across nonoptimized paths.

Record stable identities such as WWIDs or namespace identifiers. Confirm that multiple paths refer to the same underlying storage before combining them. Device names can change across reboot and discovery order.

Choose failure timing deliberately:

- Fast I/O errors may allow an application to fail over promptly, but require correct application recovery.
- Indefinite queueing can preserve access through a short outage, but can also freeze processes, shutdown, and failover.
- Aggressive path timeouts can turn congestion into repeated disconnect/reconnect cycles.
- Multiple timeout layers can exceed the claimed recovery objective even when each layer looks reasonable alone.

Test a single path loss, controller failover, all-path loss, restoration, host reboot, and stale initiator returning. Confirm no duplicate device appears and no obsolete writer regains access. Use the OS-specific supported multipath implementation; native NVMe multipathing and device-mapper multipath are related options with different configuration/support requirements. [Red Hat multipath guide](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/9/html/configuring_device_mapper_multipath/index)

## Account for networking and security

Budget front-end traffic, replica traffic, backfill/rebuild, backup, and client bursts separately. A nominal 10 Gbit/s link has a decimal line-rate ceiling of 1.25 GB/s before overhead; it is not 10 GB/s of application payload. Verify full end-to-end MTU rather than enabling jumbo frames at one endpoint. Tune only from measured loss, latency, CPU, queueing, and retransmission evidence.

For RDMA, specify whether the transport is InfiniBand, RoCE, or another supported option. Do not imply every RDMA network needs identical lossless-Ethernet settings. Validate the chosen vendor's congestion-management requirements, including behavior under congestion and partial failures.

Use target ACLs and initiator identity, network restriction, and appropriate encryption/authentication as separate controls. CHAP authentication for iSCSI does not itself encrypt all data traffic. A private VLAN or cloud network provides a routing/isolation boundary; it is not inherently transport encryption. Protect control-plane credentials because a storage administrator may be able to attach a volume elsewhere or destroy it.

## Validate a remote block service

Obtain explicit answers for attachment count, writer ownership, region/zone restrictions, durability acknowledgment, flush/FUA behavior, snapshots, discard, resize, encryption, and deletion lifecycle. Then test:

| Test | Required observation |
| --- | --- |
| Application crash and host power loss | Documented recovery without acknowledged-transaction loss beyond the promised model |
| Path and target failure | Bounded I/O behavior; no simultaneous unsafe writers |
| Reattach after host loss | Fencing completed before replacement activation; filesystem/application recovery verified |
| Snapshot during writes | Application-consistent or explicitly crash-consistent result, with coordinated multi-volume treatment |
| Expansion and thin allocation | Every layer sees the intended size; metadata and reserve monitoring works |
| Restore on another machine | Keys, configuration, boot order, target permissions, and application data are usable |

Do destructive fault injection only on an authorized disposable environment. For production, begin with read-only inventory and a reviewable maintenance plan.

## Primary references

- [RFC 7143: iSCSI](https://www.rfc-editor.org/rfc/rfc7143): transport and protocol semantics.
- [NVM Express specifications](https://nvmexpress.org/specifications/): command sets and transport-specific contracts; verify target feature support.
- [Linux writeback cache control](https://docs.kernel.org/block/writeback_cache_control.html): flush/FUA boundary.
- [Red Hat device-mapper multipath](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/9/html/configuring_device_mapper_multipath/index): supported multipath behavior and configuration.
- [Red Hat GFS2](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/9/html-single/configuring_gfs2_file_systems/index): cluster-aware shared-disk operation, locking, and fencing.
