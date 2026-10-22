---
name: cisco-ios-router
description: Use when reading, auditing or changing a classic Cisco IOS 15.x router (ISR 900 C921/C926/C927/C931, ISR G2 1900/2900/3900, 800 series; "c900-universalk9" images) — interfaces and SVIs on the built-in switch ports, ACLs and reflexive ACLs, NAT/port forwards, zone-based firewall, static routes with IP SLA failover, DHCP/DNS/NTP, SSH/VTY hardening, licenses (ipbasek9/securityk9), config archive/rollback, IOS upgrades. Most CLI also applies to IOS-XE (ISR 1100/4000, Catalyst) — differences are noted.
---

# Cisco IOS (classic 15.x) routers

## Modes and grammar

```
Router>            user EXEC            enable → Router#
Router#            privileged EXEC       configure terminal → Router(config)#
Router(config)#    global config         interface Gi4 → Router(config-if)#, line vty 0 4 → (config-line)#
end / Ctrl-Z       back to Router#       exit = one level up
```
- `show …` works from any mode with `do show …` inside config. Filters: `show run | include ip route`, `| exclude`, `| begin interface`, `| section interface Vlan`, `show run interface Gi4`, `show run | section ^ip access-list`.
- Commands abbreviate (`sh ip int br`), `?` lists options, Tab completes. `no <cmd>` removes; `default interface Gi0` resets an interface.
- Changes are live immediately but **not saved**: `write memory` (= `copy running-config startup-config`). Reload without saving = revert.
- Long output: `terminal length 0` (per session) turns off `--More--` paging.

## Working method

1. Read: `show version` (image, uptime, config-register, license), `show inventory`, `show ip interface brief`, `show run`, `show ip route`, `show license`, `show archive`.
2. Remote change safety net: `reload in 10` before risky edits (firewall, NAT, VTY, interfaces), `reload cancel` after verifying. Or `archive` + `configure replace flash:archive-N force` to roll back.
3. Apply in config mode; verify with the matching `show` (see references); then `write memory`.
4. Record in the host document what changed and why.

## Map of references

| Topic | File |
|---|---|
| CLI access: SSH v2 setup, VTY/console hardening, users, legacy SSH clients, `reload in` safety net, archive/rollback, config-register, file system, IOS upgrade | references/cli-and-access.md |
| ISR 900 platform: ports Gi0-3 switch / Gi4-5 WAN, licensing (ipbasek9, securityk9 RTU), EoL dates, ROMMON | references/isr900-platform.md |
| Interfaces, VLANs on built-in switch ports, SVIs, sub-interfaces, DHCP server, DNS, NTP | references/interfaces-vlan-dhcp.md |
| ACLs: standard/extended/named, wildcard masks, editing by sequence, reflexive ACLs, `established`, VTY `access-class` | references/acl.md |
| NAT: overload/PAT, static port forwards, inside/outside vs NVI, translation tables | references/nat.md |
| Zone-based firewall (needs securityk9): zones, class-maps, policy-maps, self zone, port forwards through ZBFW | references/zbfw.md |
| Routing: static/floating routes, IP SLA + track failover, PBR, CEF checks | references/routing.md |
| Management plane: logging, NTP server/ACLs, SNMP, CDP/LLDP, HTTP off, service defaults, login block | references/management-services.md |

## Common mistakes

- Forgetting `write memory`; the change vanishes on the next power cut, and the next admin sees a config that never matched reality.
- Applying an inbound ACL on the WAN interface without `evaluate`/`established` rules or a stateful firewall → replies to the router's own DNS/NTP/SSH sessions are dropped. Outbound ACLs never see router-originated traffic, so reflexive ACLs never create entries for it.
- Adding `deny` lines to a numbered ACL: numbered ACLs cannot be edited in place on old IOS; re-enter as a named ACL (`ip access-list extended NAME`) with sequence numbers.
- `switchport` commands on Gi4/Gi5 (routed WAN ports) or `ip address` on Gi0-3 (switch ports): the ISR 900 has both kinds; IPs for the switch side live on `interface VlanN`.
- Locking yourself out with `transport input ssh` + broken `login local`/missing username, or `access-class` without your own subnet. Always keep the console path and use `reload in`.
- Trying ZBFW/IPsec/VPN without `securityk9` active → commands accepted partially or rejected; check `show license` first (`Active, In Use`).
- `ip nat inside source list … overload` without `ip nat inside/outside` on the interfaces → no translations, `show ip nat translations` empty.
- Assuming CDP/LLDP show the switch behind a dumb media converter or a modem; `show mac address-table` on the ISR switch ports and ARP are the fallback.

Addresses, interface names and ACL names in the references are illustrative (`203.0.113.10`, `LAN-INTERN`, `Vlan66`); substitute your own.
