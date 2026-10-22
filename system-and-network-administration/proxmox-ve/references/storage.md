# Proxmox VE — Storage details

`/etc/pve/storage.cfg` defines all storages cluster-wide. `pvesm status` (overview), `pvesm list <storage>` (volumes), `pvesm scan <type>` (e.g. `pvesm scan zfs`, `pvesm scan nfs <server>`). **Always use `/dev/disk/by-id/` for disks** — kernel names (`sdX`, `nvmeXn1`) can swap after a reboot.

## storage.cfg — examples

```
dir: local
    path /var/lib/vz
    content iso,vztmpl,backup

zfspool: local-zfs
    pool rpool/data
    content images,rootdir
    sparse 1                 # thin

lvmthin: data
    thinpool data
    vgname pve
    content images,rootdir

pbs: pbs-store
    server pbs.host
    datastore store1
    username backup@pbs
    fingerprint 64:d3:...:fe
    content backup
```
Content types: `images` (VM disks), `rootdir` (CT rootfs), `iso`, `vztmpl`, `backup`, `snippets`. Storage via CLI: `pvesm add zfspool <id> --pool <pool>/<ds> --content images,rootdir --sparse 1`; `pvesm set <id> --disable 1`; `pvesm remove <id>` (only removes the PVE attachment, not the data).

## ZFS

**Reading:**
```
zpool status -v            # health, DEGRADED/FAULTED, resilver/scrub progress, error counters
zpool list -v              # capacity per vdev, FRAG, CKPOINT
zpool iostat -v 2          # live latency/throughput
zfs list -o name,used,avail,refer,mountpoint
zfs get compressratio,compression,atime,recordsize <dataset>
```
The vdev layout **cannot** be changed afterwards (redundancy level is fixed): mirror (recommended on a small setup, easier to extend/replace), raidz1/2/3. A `special`/`log`/`cache` vdev can be added; a `special` (metadata) vdev without redundancy takes the whole pool down with it on failure.

**Replacing a disk / resilver:**
```
zpool status                                   # identify the DEGRADED disk by by-id
zpool replace <pool> <old-by-id> /dev/disk/by-id/<new>
zpool status <pool>                            # follow the resilver
# Hot-Spare: zpool add <pool> spare /dev/disk/by-id/<x>
zpool offline/online <pool> <dev>              # take offline/online selectively
```
**Properties** (on pool/dataset): `ashift=12` (4K sectors) — **settable only at pool creation**, fixed afterwards; `compression=lz4` (cheap, practically always on) or `zstd`; `atime=off` (fewer writes); `recordsize` (default 128K; DB/VM often 16K–64K); `xattr=sa`. Set with: `zfs set compression=zstd atime=off <dataset>`.

**Scrub & maintenance:** `zpool scrub <pool>` (monthly; checks all data against checksums, repairs from redundancy). Error counters after a fixed problem: `zpool clear <pool>`. Snapshots: `zfs snapshot <ds>@name`, `zfs rollback`, `zfs send | zfs recv` (replication).

**ARC (RAM cache):** ZFS uses a lot of RAM. On PVE, limit it via `/etc/modprobe.d/zfs.conf` → `options zfs zfs_arc_max=<bytes>`, then `update-initramfs -u` + reboot. Current state: `arcstat` / `cat /proc/spl/kstat/zfs/arcstats`.

## LVM-thin & dir

- **lvmthin:** thin-provisioned, supports snapshots, local (not shared). Display: `lvs -a`, `vgs`, `pvs`. Create a thin pool: `lvcreate --type thin-pool -n data -l 90%FREE pve`.
- **dir:** plain directory; VM disks as `qcow2` (snapshots) or `raw`. Flexible, but no native thin/snapshot except via qcow2. Handy for ISOs, templates, dump backups on a single disk.

## Thin provisioning & TRIM/discard

With `lvmthin`/`zfspool`/qcow2 the volume only grows with data actually written. Deleted blocks are given back **only** if:
1. the disk runs with `discard=on` (`qm set <vmid> --scsi0 <storage>:vol,discard=on,ssd=1`, controller `virtio-scsi-single`), **and**
2. the guest issues TRIM (`fstrim -av`, systemd timer `fstrim.timer`, or automatically on Windows).

Without both, the volume stays bloated. After large deletions/disk moves: run `fstrim -av` in the guest (or `qm guest exec <vmid> -- fstrim -av`).

## Hardware RAID vs. ZFS

ZFS expects **direct** access to individual disks (SMART, no RAID controller cache in between) so it can detect bit rot via checksums and **repair** from redundancy. On a HW-RAID controller (disks presented as one virtual drive) ZFS only sees a black box: no self-healing, double/conflicting caching, possibly masked disk errors. Therefore:

- **Recommended:** controller in **IT/HBA/JBOD mode** (disks passed through individually) → ZFS does the RAID.
- **If HW RAID has to stay:** put `ext4`/`xfs` + LVM (or `dir` storage) on it — **without** ZFS features/checksums; the controller provides redundancy and battery-backed cache. Do not build a ZFS pool on a RAID volume.
