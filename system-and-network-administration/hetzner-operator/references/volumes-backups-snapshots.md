# Cloud Volumes, Backups and Snapshots

Reviewed: 2026-10-04. Read for disk growth, server replacement, image recovery and backup coverage reviews. For database consistency, also read [database recovery](database-recovery.md). For Storage Box snapshots, use [Storage Box/Share](storage-box-share.md); they are a different mechanism.

## Establish the protection boundary

| Mechanism | Captures | Lifecycle |
|---|---|---|
| Cloud Backup | Server's local disk | Automatic daily images, seven rotating slots per server. |
| Cloud Snapshot | Server's local disk | Customer-created image retained until deletion. |
| Attached Cloud Volume | Separate network block device | Neither covered by the server images nor supplied with native Hetzner Volume Backups/Snapshots. Arrange its own backup. |

Sources: [Backup/Snapshot overview](https://docs.hetzner.com/cloud/servers/backups-snapshots/overview/), [Volume overview](https://docs.hetzner.com/cloud/volumes/overview/).

Inspect actual mount points rather than assuming `/srv`, a container path or the database directory resides on the root disk. A root image can contain an empty mount-point directory while all useful data lives on an excluded Volume.

## Operate Volumes deliberately

Volumes replicate blocks across three physical servers. They support one attached server at a time; expansion is possible, shrinking is not, and filesystem growth is a separate guest operation. They cannot be attached to dedicated servers. These capabilities provide storage availability and flexible capacity, not historical recovery. [Volume FAQ](https://docs.hetzner.com/cloud/volumes/faq/)

A Volume and its attached server must be in the same location. Detaching permits later reattachment; deleting destroys the data and requires the Volume to be detached and unprotected. Use delete protection for valuable datasets. [Official Python SDK: Volumes](https://hcloud-python.readthedocs.io/en/stable/api.clients.volumes.html)

Before changing storage:

```bash
lsblk -o NAME,SIZE,FSTYPE,UUID,MOUNTPOINTS,MODEL,SERIAL
findmnt --target /srv
df -hT
```

Match the block-device serial, stable by-id path or filesystem UUID to the actual Volume ID. Verify the application path, mount options, partition/LVM/encryption layers, free space, retention and most recent restore test. Do not assume `/dev/sdb` is the desired disk.

For a new empty Volume, Hetzner's automatic mode can format and mount it; manual mode leaves those steps to the operator. Existing data disks must not pass through an initialization routine that reformats them. [Creating a Volume](https://docs.hetzner.com/cloud/volumes/getting-started/creating-a-volume/)

For growth, enlarge the provider resource, wait for the action to succeed, rescan if needed, and grow each applicable guest layer in order. Use the filesystem's own documentation: ext4 and XFS have different tools and argument requirements. Validate both block-device size and usable filesystem size. Shrinking or moving location requires a replacement/copy workflow; keep the original until the copied application has been verified.

For reattachment, stop writers, unmount cleanly, detach, attach to the replacement in the same location, mount the verified filesystem and validate permissions before starting services. Establish exclusive ownership; do not design two concurrently writing database servers around one single-attachment Volume. Add service dependencies so a missing mount cannot silently redirect writes onto the root disk.

## Understand image lifecycle and geography

Backups are deleted with their server; Snapshots survive server deletion. Convert a required Backup to a Snapshot and enable deletion protection before removing the server. Live image capture has no guaranteed data consistency; Hetzner recommends powering down. Replacement servers must match the image architecture. Images can create servers in other locations, but restore portability is separate from storage placement. Backups stay in the source location, normally a different data center; Hillsboro and Singapore are same-data-center exceptions. Snapshots use another location within the network zone when possible; Ashburn, Hillsboro and Singapore remain in their source location. The placement is assigned, not customer-selectable. Recheck the location table before making disaster-recovery or residency commitments. [Backup/Snapshot FAQ](https://docs.hetzner.com/cloud/servers/backups-snapshots/faq/)

## Restore as a controlled cutover

1. Record image ID/time, CPU architecture, source disk size, Volumes, addresses, network membership and external dependencies. Record which application state is absent from the image.
2. Prefer a new isolated recovery server while diagnosing. Rebuilding an existing server overwrites its local disk. [Restore choices](https://docs.hetzner.com/cloud/servers/backups-snapshots/overview/)
3. Prevent the recovery instance from contacting production databases, running scheduled jobs, advertising duplicate identities or processing queues until its state has been inspected.
4. Restore external data to a compatible recovery point; do not blindly combine an old application image with a newer database schema or unrelated Volume contents.
5. Check boot, mounts, users, service health and an application transaction. Confirm a restored clone does not unintentionally reuse credentials or network identity that should be rotated.
6. Measure elapsed restoration time and actual data loss. Cut traffic over only after validating the recovered service; retain the prior instance/data according to the rollback plan.

Avoid periodic image-only protection for applications whose required recovery interval is shorter than the image schedule. Add application-aware backups, retention and independent recovery copies instead of increasing confidence based solely on a green image status.
