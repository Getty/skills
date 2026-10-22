# Storage operations and evidence-led troubleshooting

Evidence checked: 2026-10-21. Treat commands as platform-specific inspection examples, not a universal script. Confirm available versions and target identifiers before use. Read-only inspection may require privileges, wake disks, access a network mount, or add load.

## Contents

- [Establish incident scope](#establish-incident-scope)
- [Capture a read-only baseline](#capture-a-read-only-baseline)
- [Follow the failing layer](#follow-the-failing-layer)
- [Investigate exhaustion](#investigate-exhaustion)
- [Preserve recovery options](#preserve-recovery-options)
- [Define steady-state operations](#define-steady-state-operations)
- [Close the incident with evidence](#close-the-incident-with-evidence)
- [Primary references](#primary-references)

## Establish incident scope

Identify the affected application and precise error, first occurrence, recent changes, and current user impact. Distinguish unavailable data, slow operations, stale reads, permission failures, full capacity, and confirmed corruption. Establish whether writes still succeed elsewhere and whether there is one authoritative writer.

Draw the actual dependency path: application → mount/driver → host/device or network endpoint → backend data and metadata services → media. Include identity, DNS, time, encryption keys, orchestration, and provider control planes. Preserve timestamps with timezone and record clock differences before correlating events.

Determine what can be safely changed within the existing authorization. During suspected data loss or split brain, preserve evidence and valid copies before trying to make the dashboard green. Avoid restarting all nodes, clearing error counters, force-importing pools, or recreating volumes as an initial diagnostic step.

## Capture a read-only baseline

Collect only what discriminates between current hypotheses. Keep secrets, customer paths, and access keys out of shared logs.

### Linux

Use commands appropriate to installed components:

```bash
lsblk -o NAME,TYPE,SIZE,FSTYPE,MOUNTPOINTS,RO,MODEL,SERIAL
findmnt -o TARGET,SOURCE,FSTYPE,OPTIONS
df -hT
df -i
cat /proc/mdstat
pvs
vgs
lvs -a -o lv_name,vg_name,lv_size,lv_attr,data_percent,metadata_percent
iostat -xz 1 5
pidstat -d 1 5
journalctl -k --since '-1 hour' --no-pager
```

Interpret logical volume and physical device counters at their own layers; summing both can double-count work. Inspect process-level I/O alongside application latency. `iostat` busy time is not a universal saturation percentage for parallel SSDs or arrays, and counters can reset after reboot or device reattachment. [Kernel counters](https://docs.kernel.org/admin-guide/iostats.html), [iostat upstream manual](https://github.com/sysstat/sysstat/blob/master/man/iostat.in)

For a verified device identity, inspect `smartctl -x DEVICE` or `nvme smart-log DEVICE` and, where useful, `nvme error-log DEVICE`. These are query forms; do not substitute format, sanitize, reset, or firmware commands. Health data can be incomplete behind a USB bridge, RAID controller, hypervisor, or provider abstraction. Vendor-specific raw attributes need the relevant interpretation.

For ZFS, use `zpool status -v`, `zpool iostat -v 1 5`, and `zfs list` as appropriate. For multipath, inspect `multipath -ll` if installed. For NFS, inspect `nfsstat -m` and client/server statistics. Select installed tools rather than installing a new monitoring stack during an urgent outage without a reason.

### Windows

Start with Disk Management or the following inspection commands where the Storage module is available:

```powershell
Get-Disk
Get-Partition
Get-Volume
Get-PhysicalDisk
Get-PhysicalDisk | Get-StorageReliabilityCounter
Get-SmbConnection
Get-SmbMultichannelConnection
```

Record physical disk identity, health/operational status, pool/virtual-disk state, and free capacity. Reliability counters depend on the storage provider and may be absent; an empty wear value is not zero wear. Inspect System and relevant storage/SMB event logs around the incident. Use Performance Monitor or an appropriately scoped trace for latency and queues, noting localized counter names. [Physical disks](https://learn.microsoft.com/en-us/powershell/module/storage/get-physicaldisk?view=windowsserver2025-ps), [reliability counters](https://learn.microsoft.com/en-us/powershell/module/storage/get-storagereliabilitycounter?view=windowsserver2025-ps), [SMB connections](https://learn.microsoft.com/en-us/powershell/module/smbshare/get-smbconnection?view=windowsserver2025-ps)

### macOS

Inspect Disk Utility with all devices visible, and distinguish physical device, APFS container, volume, and snapshot. Query `diskutil list`, `diskutil apfs list`, and `diskutil info IDENTIFIER` for resolved identifiers. Inspect Activity Monitor and relevant logs for pressure or I/O symptoms. Distinguish free, allocated, purgeable, and snapshot-retained space; they are not interchangeable numbers. Use the installed `diskutil` manual before invoking a repair or resize operation. [Apple Disk Utility information](https://support.apple.com/en-euro/guide/disk-utility/dskutl1005/mac)

## Follow the failing layer

| Symptom | Discriminating evidence | Next direction |
| --- | --- | --- |
| One process is slow; device is quiet | Locks, process state, application trace, per-operation timing | Application serialization, metadata locks, remote acknowledgment, or CPU |
| Latency rises under writes | Queue depth, flush latency, free space, cache exhaustion, replica lag | Steady-state media, sync policy, compaction, replication or throttling |
| All clients lose one share | Server/service health, backend status, network path, identity services | Shared service dependency; avoid changing every client independently |
| One client sees stale content | Mount options, leases/caches, protocol, application open handles | Visibility contract or client behavior; compare controlled close/reopen |
| Resets/timeouts in kernel or event logs | Cable/controller/NIC errors, device identity, correlated hosts | Transport, power, firmware, target overload, or driver |
| Healthy network but blocked filesystem | Quorum, leases, fencing, distributed locks, all-path state | Intentional safety stop or unresolved ownership |
| Access denied after migration | Effective service identity, ACL/SID/UID mapping, key policy | Authorization and translation, not necessarily missing data |
| Missing mount but application still writes | Actual source of mountpoint, boot dependencies, local directory contents | Writes may be landing on root disk instead of intended storage |
| Reported corruption | End-to-end checksums, replica disagreement, hardware logs, app validation | Preserve known-good copies; choose recovery boundary before repair |

Use one controlled change at a time and define the observable success/failure signal. A reboot that temporarily clears a symptom is evidence about state, not proof of the original cause. Correlate provider incidents without assuming all unexplained latency is the provider's fault.

## Investigate exhaustion

Check more than the `df` byte total:

- Free blocks, reserved blocks, inodes, directory/metadata limits, user/project quotas, and open-file/process limits.
- Deleted files still held open; identify the owning process before deciding how to release them.
- Snapshots, clones, noncurrent object versions, incomplete multipart uploads, and retention policies.
- Thin-pool data and metadata, compaction reserve, journal/WAL growth, temporary files, and failed cleanup jobs.
- Allocation imbalance: one full device or placement group can block writes while aggregate capacity looks adequate.
- A missing mount, changed container mapping, or incorrect namespace that redirected writes to another filesystem.

Use targeted directory scans after establishing their load impact. Avoid recursively walking an unhealthy network mount or a huge namespace when service-level metrics already locate the problem. Do not delete database logs or filesystem metadata merely because they are large.

## Preserve recovery options

For failing hardware or suspected corruption, distinguish filesystem repair from data recovery. Repair may discard structures to regain mountability; it may not maximize recoverable data. A forensic image or provider snapshot may preserve a recovery point, but snapshots can share failing media or capture only crash consistency. Choose the method according to the incident and available valid copies.

Before replacement, record serial/WWID, slot, pool membership, and whether redundancy can survive another loss. Never identify the target solely by an unstable `/dev/sdX` name. Before force attach/import or promoting a replica, prove that obsolete writers are fenced and establish which copy is authoritative.

Before restoring, preserve the current state when feasible, identify the desired recovery point, and isolate a trial restore. Recover data together with metadata/catalogs, encryption keys, access policies, application configuration, and logs needed for replay. Validate consistency through the application. Reconnection success or a mounted directory is not a completed restore.

## Define steady-state operations

Monitor user-visible latency/error rates, bytes and metadata headroom, under-replication/degraded states, repair progress, quorum/membership, device errors/wear, network loss, backup age, replica lag, and restore-test age. Express alerts as an actionable failure or a time-to-exhaustion estimate where possible.

Schedule scrubs, health checks, backups, firmware/OS/storage upgrades, and restore drills with concurrency limits. Scrubbing can detect latent corruption and repair from a valid redundant copy; it does not supply historical data or replace backups. Check the supported upgrade path and compatibility across all clients before changing an on-disk format or protocol feature.

For each component, document the maintainer, replacement procedure, credentials/key recovery, expected failure behavior, and spare-capacity policy. Verify maintenance with one node unavailable; otherwise routine upgrades may consume the entire fault budget.

## Close the incident with evidence

Report cause as confirmed, likely, or unresolved. State the observed data-loss boundary, current protection level, recovered functionality, remaining degraded capacity, and repair completion criteria. Include the command/configuration change and rollback where relevant. Retain a small reproducible test and monitoring improvement that would detect recurrence; do not broaden changes beyond the demonstrated cause.

## Primary references

- [Linux I/O statistics](https://docs.kernel.org/admin-guide/iostats.html) and [sysstat](https://sysstat.github.io/): host measurement boundaries.
- [smartmontools upstream](https://github.com/smartmontools/smartmontools) and [nvme-cli upstream](https://github.com/linux-nvme/nvme-cli): device-health query tooling; use installed version documentation.
- [OpenZFS pool status](https://openzfs.github.io/openzfs-docs/man/master/8/zpool-status.8.html): pool health and approximate repair progress.
- [Windows physical disks](https://learn.microsoft.com/en-us/powershell/module/storage/get-physicaldisk?view=windowsserver2025-ps), [reliability counters](https://learn.microsoft.com/en-us/powershell/module/storage/get-storagereliabilitycounter?view=windowsserver2025-ps), and [SMB connections](https://learn.microsoft.com/en-us/powershell/module/smbshare/get-smbconnection?view=windowsserver2025-ps): read-only inspection interfaces.
- [Apple disk information](https://support.apple.com/en-euro/guide/disk-utility/dskutl1005/mac): device/container/volume and space reporting.
- [Linux NFS client manual](https://man7.org/linux/man-pages/man5/nfs.5.html): mount and timeout semantics.
