# Proxmox VE — Cluster and HA

Read when the host is part of a cluster (`pvecm status` lists members), when adding a
node, or before touching HA.

- **Cluster (`pvecm`):** `pvecm status` / `pvecm nodes`; `pvecm add <ip>` adds a node.
  Quorum required (≥ 3 nodes or a QDevice), otherwise `/etc/pve` becomes read-only.
- **HA (`ha-manager`):** `ha-manager status`; needs a cluster with quorum. Covered only
  briefly here — don't enable it without a reason.
