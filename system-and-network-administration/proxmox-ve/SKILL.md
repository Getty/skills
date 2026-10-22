---
name: proxmox-ve
description: "Use when reading, auditing or changing a Proxmox VE host over CLI/SSH — qm/pct VM and container lifecycle, pvesm storage (ZFS, LVM-thin, dir), Proxmox Backup Server (PBS datastores, sync jobs, prune/GC/verify), vmbr bridges and VLANs, clustering, host maintenance, reading `qm config`/`pvesm status`/`zpool status` output."
---

# Proxmox VE

Proxmox VE (PVE) is a Debian host with KVM/QEMU (VMs) and LXC (containers), managed via `qm`, `pct`, `pvesm`, `pvecm` and the config under `/etc/pve/` (a cluster-wide synchronised FUSE filesystem, `pmxcfs`). Backups go through Proxmox Backup Server (PBS), a separate appliance.

## Working method

1. **Read first, then act.** The machine is the truth, docs can go stale. Starting point:
   `pveversion -v` · `qm list` / `pct list` · `pvesm status` · `zpool status -v` · `cat /etc/pve/storage.cfg` · `ip -br a` · `cat /etc/network/interfaces` · `pvecm status` (if clustered).
2. **VM/CT config is a file:** `qm config <vmid>` reads `/etc/pve/qemu-server/<vmid>.conf`, `pct config <vmid>` reads `/etc/pve/lxc/<vmid>.conf`. `qm config` also shows the `pending` block (changes that only take effect after stop/start).
3. **Reversible/read-only without asking.** Get confirmation **beforehand** for anything destructive (`qm destroy`, `pct destroy`, `zpool destroy`, deleting datastores/backups, `ifreload` with an uplink change, anything that interrupts a production service).
4. **Always address disks via `/dev/disk/by-id/`** — `nvme0n1`/`sdX` can swap after a reboot.
5. **Verify:** `qm status <vmid>`, `journalctl -u pve*`, `zpool status`, `pvesm status`, guest via `qm agent <vmid> ping`.

## Versions & repositories

| PVE | Base | PBS |
|---|---|---|
| PVE 8 | Debian 12 **bookworm** | PBS 3 |
| PVE 9 | Debian 13 **trixie** | PBS 4 |

From Debian 13/PVE 9 on, the **deb822** format (`.sources`) is the default; apt complains about the old single-line format (`.list`) — `apt modernize-sources` migrates it. Without a subscription: **disable the enterprise repo, add the no-subscription repo.**

**PVE 9 (trixie), setting up no-subscription:**
```
# Disable enterprise: add Enabled: no (or delete the file)
/etc/apt/sources.list.d/pve-enterprise.sources   # + line:  Enabled: no
/etc/apt/sources.list.d/ceph.sources             # same, if no Ceph subscription

# Create new: /etc/apt/sources.list.d/proxmox.sources
Types: deb
URIs: http://download.proxmox.com/debian/pve
Suites: trixie
Components: pve-no-subscription
Signed-By: /usr/share/keyrings/proxmox-archive-keyring.gpg
```
Then `apt update && apt full-upgrade`. The Debian base lives in `/etc/apt/sources.list.d/debian.sources`. PBS is analogous with URI `…/debian/pbs`, component `pbs-no-subscription`.

**PVE 8 (bookworm), single-line:** `/etc/apt/sources.list.d/pve-no-subscription.list` → `deb http://download.proxmox.com/debian/pve bookworm pve-no-subscription`; comment out the enterprise `.list`.

**Upgrade 8 → 9 (in-place, short path):** update to the last 8.4.x → `pve8to9 --full` and work through **all** findings → change `bookworm` → `trixie` in all repos (or `apt modernize-sources` + adjust the suite) → `apt update && apt dist-upgrade` → reboot → run `pve8to9` again. In a cluster, one node at a time, migrate the VMs away first. Always work via **console/IPMI**, not SSH (a network restart kills the session). The subscription "nag" dialog in the web UI is purely cosmetic.

## VM lifecycle (`qm`)

| Task | Command |
|---|---|
| List / status | `qm list` · `qm status <vmid>` |
| Read config | `qm config <vmid>` (`--current` without pending) |
| Create | `qm create <vmid> --name web --memory 4096 --cores 2 --net0 virtio,bridge=vmbr0 --scsihw virtio-scsi-single --scsi0 local-zfs:32` |
| Change | `qm set <vmid> --memory 8192 --net0 virtio,bridge=vmbr0,tag=65` |
| Start/stop | `qm start` · `qm shutdown` (ACPI, clean) · `qm stop` (**hard**, like pulling the plug) · `qm reboot` |
| Autostart | `qm set <vmid> --onboot 1 --startup order=1,up=30` |
| Clone | `qm clone <vmid> <newid> --name clone --full` |
| Migrate | `qm migrate <vmid> <node> --online` (running) · `--with-local-disks` (storage migration) |
| Move disk | `qm disk move <vmid> scsi0 <storage> --delete` (alias `qm move-disk`) |
| Grow disk | `qm disk resize <vmid> scsi0 +10G` (**grow only**) |
| Import disk | `qm disk import <vmid> disk.qcow2 <storage>` |
| Delete | `qm destroy <vmid> --purge` (**get confirmation**) · `qm unlock` for a stuck lock |

**Live vs. offline disk move:** If the VM is running, PVE uses **drive-mirror** (QEMU) — the move is uninterrupted, with a brief switchover at the end. If the VM is stopped, it is a simple copy. The same applies to `qm migrate --with-local-disks` (online = drive-mirror).

**Cloud-Init** (assumes a template with a `cloud-init` disk): `qm set <vmid> --ipconfig0 gw=172.16.0.1,ip=172.16.0.20/24 --sshkeys ~/.ssh/id_ed25519.pub --ciuser admin --nameserver 172.16.0.8`; then `qm cloudinit update <vmid>`.

**Guest agent** (`--agent 1`, agent installed in the guest): `qm agent <vmid> ping` checks reachability, `qm guest exec <vmid> -- <cmd>` runs commands in the guest without SSH, `qm guest cmd <vmid> network-get-interfaces` returns guest IPs. Useful for VMs without SSH access.

## Containers (`pct`)

`pct list` · `pct config <vmid>` · `pct create <vmid> local:vztmpl/<template>.tar.zst --hostname ct1 --memory 1024 --rootfs local-zfs:8 --net0 name=eth0,bridge=vmbr0,ip=dhcp --unprivileged 1` · `pct start/stop/shutdown` · `pct enter <vmid>` (shell) · `pct exec <vmid> -- <cmd>` · `pct set <vmid> --onboot 1`.

- **Unprivileged (default, recommended):** guest root ≠ host root thanks to UID/GID mapping. **Privileged** only when needed (e.g. certain mounts) — guest root == host root, a security risk.
- **Docker in LXC:** needs `--features nesting=1,keyctl=1` (unprivileged + nesting). Not officially recommended — Docker belongs in a **VM**. Templates: `pveam update` · `pveam available` · `pveam download local <template>`.

## Storage (`pvesm`)

`pvesm status` (type, active, total/used/avail) · `pvesm list <storage>` (volumes) · config in `/etc/pve/storage.cfg`. Types: **`dir`** (directory, qcow2/raw), **`lvmthin`** (thin, snapshots), **`zfspool`** (thin, snapshots, compression), **`nfs`/`cifs`**, **`pbs`** (backup), `rbd`/`cephfs`, `btrfs`. Content types per storage: `images` (VM disks), `rootdir` (CT), `iso`, `vztmpl`, `backup`, `snippets`.

- **Thin provisioning** (lvmthin, zfspool): space is only allocated when used. To give deleted blocks back, set `discard=on` on the disk (`scsi`/`virtio-scsi`) **and** run `fstrim` in the guest — otherwise the volume only grows.
- PBS as storage: `pvesm add pbs <id> --server pbs.host --datastore store1 --username backup@pbs --password <pw> --fingerprint <sha256>`.

**ZFS (short form, details → `references/storage.md`):** `zpool status -v` (health, errors, resilver), `zpool list -v` (usage per vdev), `zfs list -o name,used,avail,refer,mountpoint`. Replace a disk: `zpool replace <pool> <old-by-id> /dev/disk/by-id/<new>` → follow the resilver in `zpool status`. Important properties: `ashift=12` (4K, **settable only at creation**), `compression=lz4`/`zstd`, `atime=off`. Scrub monthly: `zpool scrub <pool>`.

**Hardware RAID + ZFS = discouraged.** ZFS needs direct disk access (SMART, no cache layer in between) for bit-rot protection. On a HW-RAID controller ZFS only sees one virtual disk and cannot repair on errors; double caching looms. Either put the controller in **IT/HBA mode** (pass-through disks) and use ZFS, **or** use HW RAID with `ext4`/`LVM` without ZFS features.

## Networking

`/etc/network/interfaces` (ifupdown2). Apply without a reboot: `ifreload -a` — **be careful with running services/remote sessions** (the uplink can drop briefly; work via console). Check: `ifquery -a`, `ip -br a`.

- **Linux bridge `vmbr0`:** `auto vmbr0` / `iface vmbr0 inet static` / `bridge-ports eno1` / `bridge-stp off` / `bridge-fd 0` (+ `address`/`gateway` for the host IP).
- **VLAN-aware bridge:** `bridge-vlan-aware yes` + `bridge-vids 2-4094`; the VLAN is then set per NIC on the guest via `tag=<vlan>` (`--net0 virtio,bridge=vmbr0,tag=65`). Without VLAN-aware: separate interfaces `eno1.65`/`vmbr0.65`.
- **SDN** (`Datacenter → SDN`, `pvesh`/`/etc/pve/sdn/`) for zone/VXLAN-based overlays — only when needed.
- **Intel `e1000e` "Detected Hardware Unit Hang":** old, known driver bug — the NIC hangs under load. Workaround: turn offloading off — `ethtool -K <if> tso off gso off gro off`, persistent via `post-up /usr/sbin/ethtool -K <if> tso off gso off gro off` in `interfaces`. Prefer `igb` NICs where possible.

## PBS, security & maintenance

- **PBS** (datastore, `vzdump` backup, remote + sync for off-site, prune/GC/verify, restore, token/ACL) → **`references/pbs.md`**. Rule of thumb: a sync job to a second PBS is the core of the 3-2-1 rule.
- **Cluster (`pvecm`):** `pvecm status` / `pvecm nodes`; `pvecm add <ip>` adds a node. Quorum required (≥ 3 nodes or a QDevice), otherwise `/etc/pve` becomes read-only.
- **HA (`ha-manager`):** `ha-manager status`; needs a cluster with quorum. Only touch briefly, don't enable without a reason.
- **Access:** web UI/API on `:8006` (`pveproxy`), root via SSH key. Changing the VM config directly in `/etc/pve/…` is possible, but prefer `qm set`/`pct set` (validation).

## References

| Topic | File |
|---|---|
| PBS: create a datastore, vzdump backup, remote + sync job (off-site), prune/GC/verify schedules, restore (`qmrestore`, `proxmox-backup-client`), token/ACL, the `DatastoreAudit` trap | `references/pbs.md` |
| Storage details: ZFS (pool/vdev layout, replace/resilver, properties, scrub, ARC), LVM-thin, dir, `storage.cfg` examples, discard/TRIM, HW RAID | `references/storage.md` |

## Common mistakes

- **`qm stop` instead of `qm shutdown`** — `stop` is a hard power-off (filesystem risk in the guest). `shutdown` shuts down cleanly via ACPI.
- **`onboot` not set** → VMs/CTs do not start automatically after a host reboot. `qm set <vmid> --onboot 1 --startup order=…` for the start order (mail server/DB first).
- **Enterprise repo active without a subscription** → `apt update` aborts with 401. Disable the enterprise repo (`.sources`/`.list`), add no-subscription.
- **Single-line repos on trixie** → apt warns; `apt modernize-sources`.
- **ZFS on HW RAID** → no bit-rot protection, no direct SMART data. HBA/IT mode or ext4/LVM.
- **`qm disk resize` with a negative value** → does not work, grow only. Shrinking only via re-creation/restore.
- **`ifreload -a` remotely without a console** → locks you out on a bridge/uplink error. Check with `ifquery -c -a` first, keep a console ready.
- **Disks in pools by `nvme0n1`/`sdX`** → swapped after a reboot. Always `/dev/disk/by-id/`.
- **PBS token without `DatastoreAudit`** → the API/UI datastore list stays empty even though backups run (see `references/pbs.md`).

IP addresses, interface/storage names and VMIDs above are examples — replace them with the host's actual values (first read `qm list`, `pvesm status`, `cat /etc/network/interfaces`).
