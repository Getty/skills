---
name: proxmox-ve
description: "Use when reading, auditing or changing a Proxmox VE host — qm and pct guests, pvesm storage (ZFS, LVM-thin), Proxmox Backup Server datastores, sync, prune and verify, vmbr bridges and VLANs, clustering, host maintenance."
---

# Proxmox VE

Proxmox VE (PVE) is a Debian host running KVM/QEMU VMs (`qm`) and LXC containers (`pct`),
with storage via `pvesm` and clustering via `pvecm`. Its config lives under `/etc/pve/`:
`pmxcfs`, a cluster-wide synchronised FUSE filesystem that turns read-only when a cluster
loses quorum. Backups go to Proxmox Backup Server (PBS), a separate appliance. Web UI/API
on `:8006` (`pveproxy`); root access via SSH key.

## Working method

1. **Read first, then act.** The machine is the truth, docs can go stale. Starting point:
   `pveversion -v` · `qm list` / `pct list` · `pvesm status` · `zpool status -v` ·
   `cat /etc/pve/storage.cfg` · `ip -br a` · `cat /etc/network/interfaces` ·
   `pvecm status` (if clustered).
2. **VM/CT config is a file:** `qm config <vmid>` reads `/etc/pve/qemu-server/<vmid>.conf`,
   `pct config <vmid>` reads `/etc/pve/lxc/<vmid>.conf`. `qm config` shows pending
   changes (effective only after stop/start) already applied — `--current` gives the
   running values, `qm pending <vmid>` both side by side. Editing the files
   under `/etc/pve/…` directly is possible, but prefer `qm set`/`pct set` (validation).
3. **Reversible/read-only without asking.** Get confirmation **beforehand** for anything
   destructive (`qm destroy`, `pct destroy`, `zpool destroy`, deleting datastores/backups,
   `ifreload` with an uplink change, anything that interrupts a production service).
4. **Verify:** `qm status <vmid>`, `journalctl -u pve*`, `zpool status`, `pvesm status`,
   guest via `qm agent <vmid> ping`.

## Traps

- **Disks by `nvme0n1`/`sdX`** (in pools, on replacement) → the names can swap after a
  reboot. Always address disks via `/dev/disk/by-id/`.
- **`qm stop` instead of `qm shutdown`** — `stop` is a hard power-off (filesystem risk in
  the guest). `shutdown` shuts down cleanly via ACPI.
- **`onboot` not set** → VMs/CTs do not start automatically after a host reboot.
  `qm set <vmid> --onboot 1 --startup order=…` for the start order (mail server/DB first).
- **`ifreload -a` remotely without a console** → locks you out on a bridge/uplink error.
  Check with `ifquery -c -a` first, keep a console ready.

## References

Read only the file the task needs.

| Task | File |
|---|---|
| VMs and containers: create, change, start/stop, clone, migrate, move/grow/import disks, destroy, Cloud-Init, guest agent, LXC privileged vs. unprivileged, Docker in LXC, CT templates | [references/guests.md](references/guests.md) |
| Storage: `pvesm` types and content types, `storage.cfg` examples, ZFS (layout, replace/resilver, properties, scrub, ARC), LVM-thin, dir, thin provisioning and discard/TRIM, HW RAID vs. ZFS | [references/storage.md](references/storage.md) |
| PBS: datastore, attaching PBS to PVE, `vzdump`, remote + sync job (off-site, core of 3-2-1), prune/GC/verify, restore (`qmrestore`, `proxmox-backup-client`), token/ACL, the `DatastoreAudit` trap (empty datastore list) | [references/pbs.md](references/pbs.md) |
| Networking: `/etc/network/interfaces`, `vmbr` bridges, VLAN-aware bridges and `tag=`, SDN, `e1000e` "Hardware Unit Hang" | [references/networking.md](references/networking.md) |
| Versions and apt: PVE/Debian/PBS mapping, deb822 `.sources`, no-subscription repos, `apt update` 401, upgrade 8 → 9 | [references/versions-and-repositories.md](references/versions-and-repositories.md) |
| Cluster and HA: `pvecm`, quorum, QDevice, `ha-manager` | [references/cluster.md](references/cluster.md) |

IP addresses, interface/storage names and VMIDs in this skill and its references are
examples — replace them with the host's actual values (first read `qm list`,
`pvesm status`, `cat /etc/network/interfaces`).
