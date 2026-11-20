# Proxmox VE — Networking

Read when changing `/etc/network/interfaces`, a `vmbr` bridge, VLANs or SDN, or when a NIC
hangs under load.

`/etc/network/interfaces` (ifupdown2). Apply without a reboot: `ifreload -a` — **be careful
with running services/remote sessions** (the uplink can drop briefly; work via console).
Check: `ifquery -a`, `ip -br a`.

- **Linux bridge `vmbr0`:** `auto vmbr0` / `iface vmbr0 inet static` / `bridge-ports eno1` /
  `bridge-stp off` / `bridge-fd 0` (+ `address`/`gateway` for the host IP).
- **VLAN-aware bridge:** `bridge-vlan-aware yes` + `bridge-vids 2-4094`; the VLAN is then
  set per NIC on the guest via `tag=<vlan>` (`--net0 virtio,bridge=vmbr0,tag=65`). Without
  VLAN-aware: separate interfaces `eno1.65`/`vmbr0.65`.
- **SDN** (`Datacenter → SDN`, `pvesh`/`/etc/pve/sdn/`) for zone/VXLAN-based overlays —
  only when needed.
- **Intel `e1000e` "Detected Hardware Unit Hang":** old, known driver bug — the NIC hangs
  under load. Workaround: turn offloading off — `ethtool -K <if> tso off gso off gro off`,
  persistent via `post-up /usr/sbin/ethtool -K <if> tso off gso off gro off` in
  `interfaces`. Prefer `igb` NICs where possible.
