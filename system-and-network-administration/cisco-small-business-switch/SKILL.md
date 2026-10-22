---
name: cisco-small-business-switch
description: Use when reading, auditing or configuring a Cisco Small Business managed switch over its CLI or web UI — Sx300/Sx500 (SG300-xx, SF300-xx, SG500) on firmware 1.x, and the same CLI family on Sx350/Sx550/CBS250/CBS350 (2.x/3.x) — VLANs and access/trunk/general ports, management VLAN and IP, SSH/users, LLDP/CDP/MAC-table lookups, PoE, port mirroring, SNTP/syslog/SNMP, saving config, firmware and boot-code upgrades. These switches are NOT Catalyst IOS: the CLI looks similar but differs in details.
---

# Cisco Small Business switches (Sx300 / Sx500 / Sx350 / CBS)

Marketed as "Cisco Small Business", the firmware is the Linksys-derived "Cisco SB" OS. It imitates IOS syntax (`configure`, `interface gi1`, `show running-config`) but has its own commands, its own web UI as the primary interface, and legacy SSH. Do not assume Catalyst behaviour.

## Grammar and quirks

- Modes: `switch>` (level 1, read-only), `switch#` (level 15), `switch(config)#`, `switch(config-if)#`, `switch(config-vlan)#`. `enable` prompts for the level-15 password; a privilege-15 user lands in `#` directly.
- Interface names: `gi1`…`gi28`, `fa1`…, `te1`, `Po1`; ranges `interface range gi1-4,gi7`; on stacked/newer models `gi1/0/1` (unit/slot/port).
- Paging: `terminal datadump` (per session) disables `More:` prompts. Filters `| include|exclude|begin` exist on 1.4+/2.x.
- Login is in-band for SSH: the SSH session opens, then the switch prints `User Name:` / `Password:` itself. Commands given on the ssh command line are ignored — drive it interactively (skill `network-device-ssh-cli`).
- Nothing persists until `copy running-config startup-config` (or `write`). A reload without saving reverts everything.
- `show running-config` is the fastest way to learn the exact CLI for something you clicked in the web UI.

## Working method

1. Read: `show version`, `show system`, `show system mode` (1.4+/2.x; L2 "switch" vs L3 "router" — on 1.3 only via web UI Administration → System Mode), `show bootvar`, `show ip interface`, `show vlan`, `show interfaces status`, `show lldp neighbors`, `show running-config`.
2. Change in small steps on the CLI; for anything touching the management VLAN/IP or the uplink port, have console access or `reload in` armed (1.4+/2.x: `reload in 10`, `reload cancel`; check `reload ?`). On 1.3.x there is no `reload in` — the console is the only safety net.
3. Verify with `show interfaces switchport giN`, `show vlan`, `show mac address-table`.
4. `copy running-config startup-config` → answer `Y`.
5. Document in the host file.

## Map of references

| Topic | File |
|---|---|
| Access: console, web UI, SSH server/keys, users and privilege levels, management ACLs, system mode L2/L3, IP and default gateway, save/backup/restore/reset, legacy SSH client options | references/cli-and-access.md |
| VLANs, port modes (access/trunk/general), PVID/native, allowed lists, port ranges, LAG/LACP, spanning-tree, storm control, PoE | references/vlan-ports.md |
| Monitoring and discovery: interface status/counters, LLDP/CDP, MAC table, port mirroring, logging/syslog, SNTP, SNMP, CPU | references/monitoring-discovery.md |
| Firmware images and boot code, upgrade path, EoL status, where firmware still exists | references/firmware-eol.md |

## Common mistakes

- Forgetting `copy running-config startup-config`; the web UI shows a blinking "Save" reminder, the CLI does not.
- `set system mode router` (switch → L3) reboots the switch and **deletes the startup configuration**. Back up first; L2 mode is enough when a router does inter-VLAN routing.
- Changing the management VLAN's IP or the PVID of the uplink over SSH → lockout. Use console or `reload in`.
- Expecting Catalyst commands: no `switchport trunk encapsulation`, no `vlan database` on 2.x (but required on 1.x), `show mac address-table` (1.4+/2.x) / `show bridge address-table` (1.3) both need privilege 15 — a level-1 user gets "% Unrecognized command" (verified on SG300-28PP 1.3.5.58).
- Treating the general mode like trunk: `general` ports need `switchport general allowed vlan add N tagged|untagged` **and** `switchport general pvid N`; trunk ports use `switchport trunk allowed vlan add` + `native vlan`.
- Upgrading firmware 1.3 → 1.4 without first loading the intermediate boot code: the switch refuses or bricks. Read references/firmware-eol.md.
- Sx300 line is out of support (2023); no security fixes. Treat as an L2 access switch behind a real firewall, restrict management to the admin VLAN.

Port numbers, VLAN ids, addresses and usernames in the references are illustrative (`gi22`, VLAN 66, `172.16.0.99`, `ops`); substitute your own.
