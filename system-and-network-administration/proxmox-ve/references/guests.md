# Proxmox VE — Guests (`qm`, `pct`)

Read when creating, changing, starting, cloning, migrating or deleting a VM or container,
moving, growing or importing a disk, or using Cloud-Init or the QEMU guest agent.

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

**Live vs. offline disk move:** If the VM is running, PVE uses **drive-mirror** (QEMU) —
the move is uninterrupted, with a brief switchover at the end. If the VM is stopped, it is
a simple copy. The same applies to `qm migrate --with-local-disks` (online = drive-mirror).

**Cloud-Init** (assumes a template with a `cloud-init` disk):
`qm set <vmid> --ipconfig0 gw=172.16.0.1,ip=172.16.0.20/24 --sshkeys ~/.ssh/id_ed25519.pub --ciuser admin --nameserver 172.16.0.8`;
then `qm cloudinit update <vmid>`.

**Guest agent** (`--agent 1`, agent installed in the guest): `qm agent <vmid> ping` checks
reachability, `qm guest exec <vmid> -- <cmd>` runs commands in the guest without SSH,
`qm guest cmd <vmid> network-get-interfaces` returns guest IPs. Useful for VMs without SSH
access.

## Containers (`pct`)

| Task | Command |
|---|---|
| List / config | `pct list` · `pct config <vmid>` |
| Create | `pct create <vmid> local:vztmpl/<template>.tar.zst --hostname ct1 --memory 1024 --rootfs local-zfs:8 --net0 name=eth0,bridge=vmbr0,ip=dhcp --unprivileged 1` |
| Start/stop | `pct start/stop/shutdown` |
| Shell / command | `pct enter <vmid>` (shell) · `pct exec <vmid> -- <cmd>` |
| Autostart | `pct set <vmid> --onboot 1` |
| Templates | `pveam update` · `pveam available` · `pveam download local <template>` |

- **Unprivileged (default, recommended):** guest root ≠ host root thanks to UID/GID
  mapping. **Privileged** only when needed (e.g. certain mounts) — guest root == host
  root, a security risk.
- **Docker in LXC:** needs `--features nesting=1,keyctl=1` (unprivileged + nesting). Not
  officially recommended — Docker belongs in a **VM**.

## Common mistakes

- **`qm disk resize` with a negative value** → does not work, grow only. Shrinking only
  via re-creation/restore.
