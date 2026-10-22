# Local media, volume layers, and filesystems

Evidence checked: 2026-10-21. Treat the architecture as durable knowledge; verify filesystem features against the installed OS, kernel, on-disk format, tooling, and support policy before changing a system.

## Contents

- [Map the storage stack](#map-the-storage-stack)
- [Choose media by workload and failure behavior](#choose-media-by-workload-and-failure-behavior)
- [Follow an acknowledged write](#follow-an-acknowledged-write)
- [Select a filesystem family](#select-a-filesystem-family)
- [Account for allocation and retention](#account-for-allocation-and-retention)
- [Apply an operational decision procedure](#apply-an-operational-decision-procedure)
- [Primary references](#primary-references)

## Map the storage stack

Identify physical devices, transport, controller, logical-volume layer, encryption, filesystem, mount, and application separately. Record the owner and recovery procedure of each layer. A typical stack is application → filesystem → encrypted logical volume → RAID/device mapper → drives. ZFS integrates pooling and filesystem functions, so applying an additional opaque RAID layer changes what it can observe and repair.

Distinguish these independent properties:

| Property | Question to answer |
| --- | --- |
| Medium | Is the data on rotating disks, NAND flash, persistent memory, or volatile RAM? |
| Attachment | Is the device local PCIe/SATA/SAS/USB, or remotely presented block storage? |
| Allocation | Are bytes reserved now, allocated on first write, compressed, or shared with snapshots? |
| Failure boundary | Which disks share a controller, enclosure, cable, host, power feed, or firmware defect? |
| Persistence | What survives reboot, sudden power loss, host loss, and deletion of the containing VM? |
| Namespace | Which component supplies names, permissions, locks, and atomic operations? |

Never derive physical location or durability from a path such as `/data`. A mount can hide local, network, userspace, or synthetic storage. `tmpfs` consumes volatile memory/swap resources and is not durable storage merely because it exposes ordinary files.

## Choose media by workload and failure behavior

| Medium or interface | Useful characteristics | Inspect before selecting |
| --- | --- | --- |
| CMR HDD | Economical bulk capacity; efficient large sequential transfers | Random seek demand, vibration, startup power, rebuild duration, controller error timeouts |
| SMR HDD | High-density sequential or append-oriented storage | Device-managed versus host-managed operation; sustained rewrites and rebuild performance; supported storage-stack use |
| SATA/SAS SSD | Low mechanical latency; existing drive-bay compatibility | Sustained writes after cache exhaustion, endurance, power-loss protection, firmware, thermal behavior |
| NVMe SSD over PCIe | High parallelism and direct host attachment | PCIe lanes, CPU/NUMA placement, cooling, endurance, namespace capabilities; NVMe does not imply enterprise durability |
| USB enclosure or bridge | Portable disks, offline copies, convenient expansion | Cable/power resets, shared hubs, bridge flush/discard/SMART behavior, stable device identities, cooling |
| Tape or offline removable media | Disconnected retention and economical large archives | Sequential access, catalog/key preservation, restore equipment, media migration and tested retrieval time |

Separate interface from medium: SATA can carry an SSD or HDD; M.2 is a form factor; an NVMe protocol label says little about NAND quality. Read the actual drive's warranty workload, TBW/DWPD interpretation, and power-loss guarantees. Account for replication, filesystem copy-on-write, database WAL, compaction, and garbage collection when estimating host and physical writes. Avoid an assumed universal amplification factor.

Treat a disk's health report as evidence, not a promise of remaining lifetime. Correlate increasing errors, latency, wear, temperature, and resets with backups and pool health. A quiet device may still fail abruptly.

## Follow an acknowledged write

Locate every volatile cache: application buffer, OS page cache, hypervisor, host controller, device DRAM, and remote target. Successful `write()` may only mean that the kernel accepted bytes. A durable transaction requires the application's synchronization operation and correct propagation through the complete stack.

Linux provides cache flush and Force Unit Access mechanisms for that propagation. A preflush orders previously completed writes onto nonvolatile storage; FUA makes the associated request complete after durable placement. A device, bridge, or virtual target that falsely reports these semantics can invalidate filesystem and database recovery assumptions. Do not disable barriers or set an unsafe synchronous-write policy to make a benchmark attractive. [Linux cache-control documentation](https://docs.kernel.org/block/writeback_cache_control.html)

Distinguish device power-loss protection from a UPS. A UPS covers some upstream power failures; it cannot substitute for protection against cable removal, controller reset, firmware bugs, or a host failure. Verify which data and internal mapping metadata the device's protection covers.

For ZFS, distinguish RAM ARC and optional L2ARC read caching from the intent log. A separate log device changes where eligible synchronous intent records are stored; it is not a universal write-throughput accelerator. Loss of a cache device and loss of an authoritative pool/special device have different consequences. Check the exact topology before adding a “cache SSD.”

## Select a filesystem family

Choose by semantics, operational support, recovery tools, and workload evidence. Avoid treating a feature checkbox as an architectural guarantee.

| Family | Representative strengths | Boundary to verify |
| --- | --- | --- |
| ext4 | General-purpose Linux filesystem; journaling and broad tooling | Journal mode and application durability; filesystem metadata checksums are not blanket checksums of ordinary file contents |
| XFS | Scalable Linux filesystem, metadata journaling, allocation groups, workload-dependent reflink features | Kernel/tool feature support and recovery procedure; metadata recovery does not restore an application transaction |
| OpenZFS | Integrated pools, checksums, snapshots, send/receive, configurable redundancy | Vdev failure rules, special/log-device topology, memory and operational needs; checksums detect damage but repair needs a valid copy |
| Btrfs | Copy-on-write, subvolumes, snapshots, checksums, compression, send/receive | Data and metadata profiles are distinct; review current status and per-profile restrictions rather than treating every RAID profile as equally mature |
| NTFS | Windows integration, access control, journaling, mature ecosystem | Application-specific backup, sparse/compressed files, Windows sharing semantics and cross-platform translation |
| ReFS | Integrity features and useful virtualization/storage operations | OS edition/version, supported workloads, file-data integrity configuration, underlying redundancy, tooling compatibility |
| APFS | Apple-platform integration, encryption, snapshots, space-sharing containers | Case sensitivity, per-volume quotas/reserves, snapshot retention, recovery on compatible macOS |
| exFAT/FAT | Interchange with devices and operating systems | Permissions, crash recovery, filenames, limits, and suitability for the workload; portability is not server resilience |

As checked on the evidence date, the Btrfs project's introduction still labels RAID5/6 experimental and not production-ready. Recheck before recommending those profiles. Microsoft documents optional file-data integrity streams in ReFS; automatic correction relies on an alternate valid copy in supported deployments. APFS volumes sharing one container compete for its free capacity unless quota/reservation policy controls them. [Btrfs](https://btrfs.readthedocs.io/en/latest/Introduction.html), [ReFS](https://learn.microsoft.com/en-us/windows-server/storage/refs/refs-overview), [APFS](https://support.apple.com/guide/disk-utility/file-system-formats-dsku19ed921c/mac)

## Account for allocation and retention

Use LVM or comparable volume management to separate physical devices from logical allocations. A linear volume spanning devices adds capacity but does not create redundancy. Striping, mirroring, parity, snapshots, and thin provisioning are separate choices with separate failure rules.

For thin pools, monitor both data and metadata consumption, growth rate, reserve capacity, and what happens when either reaches its limit. Provisioned logical capacity can exceed physical capacity; it cannot make concurrent writes fit. Snapshot retention and clone divergence consume space even when an application's apparent dataset size remains constant. An origin and its local snapshot share failure domains.

Inspect logical and physical sector sizes, filesystem block size, RAID stripe layout, and supported direct-I/O alignment. Do not reformat a populated device to chase alignment gains without a migration plan. Physical 4 KiB sectors exposed as 512-byte logical sectors are not the same configuration as native 4 KiB logical sectors.

Treat TRIM/discard/UNMAP as deallocation hints through a verified chain. They may improve reuse and thin-pool accounting; they do not constitute a universal secure-erasure guarantee. Encryption keys, snapshots, replicas, backups, controller remapping, and flash overprovisioning affect deletion assurance. Use a medium-appropriate sanitization procedure when deletion assurance is actually required.

## Apply an operational decision procedure

1. Identify whether the workload needs durable local state or only rebuildable scratch/cache.
2. Specify peak working set, latency, sustained write rate, growth, and tolerated host outage.
3. Draw shared controllers and power boundaries before selecting a protection scheme.
4. Verify application/filesystem support, sync semantics, and restore tooling.
5. Budget snapshots, metadata, repair headroom, and temporary migration capacity.
6. Validate power-loss/restart recovery on a disposable equivalent setup; benchmark steady state and degraded operation.
7. Keep independent, restorable copies even when local redundancy and checksums are enabled.

## Primary references

- [Linux block writeback cache control](https://docs.kernel.org/block/writeback_cache_control.html): flush/FUA semantics.
- [Linux thin provisioning](https://docs.kernel.org/admin-guide/device-mapper/thin-provisioning.html): allocation and metadata dependencies.
- [Red Hat LVM management](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/9/html/configuring_and_managing_logical_volumes/index): supported volume-management procedures; edition/version specific.
- [ext4 high-level design](https://docs.kernel.org/filesystems/ext4/overview.html) and [XFS logging design](https://docs.kernel.org/filesystems/xfs/xfs-delayed-logging-design.html): implementation boundaries.
- [OpenZFS hardware guidance](https://openzfs.github.io/openzfs-docs/Performance%20and%20Tuning/Hardware.html): controllers, drives, power, and USB considerations.
- [Btrfs introduction](https://btrfs.readthedocs.io/en/latest/Introduction.html), [ReFS overview](https://learn.microsoft.com/en-us/windows-server/storage/refs/refs-overview), and [Apple filesystem formats](https://support.apple.com/guide/disk-utility/file-system-formats-dsku19ed921c/mac): feature families and version caveats.
