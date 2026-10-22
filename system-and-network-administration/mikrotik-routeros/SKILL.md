---
name: mikrotik-routeros
description: Use when working on a MikroTik RouterOS 7 device (RouterBOARD, CCR, CRS, hAP, CHR) over CLI/SSH, WinBox terminal, REST API or .rsc exports — reading or changing firewall filter/NAT, bridge VLAN filtering, static routes and WAN failover, DHCP server/DNS, WireGuard, users/services, or doing export/backup/import/reset. Also when interpreting an existing "/export" dump or "print" output.
---

# MikroTik RouterOS 7

RouterOS is one menu tree with one grammar. Learn the verbs once; every subsystem (`/ip/firewall`, `/interface/bridge`, `/ip/route`, …) reads and writes the same way.

## CLI grammar

| Verb | Example |
|---|---|
| print | `/ip/firewall/filter/print` · `print detail` · `print terse` (one item per line, script-friendly) · `print where chain=input` · `print count-only` · `print stats` |
| add / set / remove | `/ip/address/add address=10.0.0.1/24 interface=bridge` · `set [find comment="x"] disabled=yes` · `remove [find dynamic=no && list=old]` |
| find | `[find where address~"^10\\."]` returns stable internal ids (`*1`, `*A`), usable inside any verb |
| enable / disable / move | `move [find comment="drop all"] destination=[find comment="accept wg"]` |
| export | `/ip/firewall/export` from any menu; `terse`, `show-sensitive`, `file=name` (→ `name.rsc`) |

- `/ip firewall filter` and `/ip/firewall/filter` are equivalent. `/` goes to root, `..` one level up, `?` lists options, Tab completes.
- `print` index numbers (`0 1 2`) are positional and change between calls; internal `*id`s are stable. Scripts use `[find …]`, never numbers.
- `!` negates a matcher (`in-interface=!bridge`), lists are comma-separated without spaces, values with spaces need quotes.
- Non-interactive: `ssh user+ct@router '/ip/route/print terse'` (`+ct` = no colors, no terminal detection). Password users need `-o PubkeyAuthentication=no`; see skill `network-device-ssh-cli` for a driver.

## Working method

1. **Read first**: `/system/resource/print`, `/system/routerboard/print`, `/system/package/print`, then `/export` (or the menu you will touch). v6 and v7 differ (routing tables, `wifi` vs `wireless`, `/routing/rule`); match the docs to the running version.
2. **Safe mode for anything remote**: `Ctrl+X` → prompt shows `<SAFE>`. If the session drops, all changes since roll back. `Ctrl+X` again commits, `Ctrl+D` discards. Use it for firewall, bridge VLAN, addresses, routes, services.
3. **Order matters** in firewall chains, NAT, DNS static, mangle. New rules append at the end; use `place-before=[find …]` or `move`.
4. **Verify**: `print stats` on firewall rules, `/ip/firewall/connection/print`, `/log/print`, `/tool/torch`, `/ping … count=4`, `/tool/traceroute`.
5. **Persist**: changes apply immediately, nothing to commit. Take `/export file=` and `/system/backup/save name=` before and after (references/config-backup-api.md).

## Map of references

| Topic | File |
|---|---|
| print/find operators, scripting, scheduler, undo history, users/groups/policies, services, logging, diagnostics | references/cli-and-scripting.md |
| Firewall filter: chains, matchers, actions, baseline rule set, interface lists, RAW, bruteforce lists | references/firewall-filter.md |
| NAT: srcnat/masquerade vs src-nat, dst-nat port forwards, hairpin, netmap, conntrack clearing | references/nat.md |
| Bridge VLAN filtering: pvid, tagged/untagged, CPU port, ingress filtering, management VLAN, lockout-safe order | references/bridge-vlan.md |
| Routing: static routes, distance, check-gateway, recursive failover, ECMP, routing tables/rules, blackhole | references/routing.md |
| DHCP server (pools, networks, option sets, static leases), DHCP client, DNS cache/static/regexp/FWD | references/dhcp-dns.md |
| WireGuard interface/peers, site-to-site, road warrior, firewall rules, multi-WAN quirks | references/wireguard.md |
| Export/import, binary backup, reset-configuration, REST API, upgrade | references/config-backup-api.md |

## Common mistakes

- Enabling `vlan-filtering=yes` before the bridge VLAN table carries the management VLAN to the bridge itself (CPU port) → lockout. Configure the table, then enable filtering last, inside safe mode.
- A drop rule above the `connection-state=established,related` accept → all existing sessions die. Order: accept established/related → drop invalid → policy → drop.
- `action=masquerade` on a static public IP: on link flap RouterOS purges those connections; use `action=src-nat to-addresses=<ip>` for static IPs and `masquerade` only for dynamic ones.
- Editing NAT without clearing affected entries: `/ip/firewall/connection/remove [find dst-address~"…"]`, otherwise old translations persist until timeout.
- Trusting `/export` as a backup: it hides passwords/keys unless `show-sensitive`, and never contains user passwords, certificates or SSH keys.
- Assuming a `group=read` user is harmless: it can still `print` WireGuard private keys, PPP secrets and SNMP communities.
- Using `dst-port=` without `protocol=` → error "protocol must be specified".

Addresses, interface names, usernames and file paths in the references are illustrative (`172.16.x.x`, `ops`, `~/router.txt`); substitute your own.
