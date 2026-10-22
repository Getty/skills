# VLANs and port configuration

## VLAN database

```
configure
vlan database                      # 1.x only; on 2.x/CBS use "vlan 10,65-67" directly in config mode
 vlan 10,65,66,67
 default-vlan vlan 66              # change default/native VLAN 1 → takes effect after save + reboot
exit
interface vlan 10
 name HQ
show vlan
show vlan tag 10                   # membership of one VLAN
```
`show vlan` lists per VLAN which ports are members but not the mode — use `show interfaces switchport giN` for tagged/untagged/PVID detail.

## Port modes

| Mode | Untagged VLAN | Tagged VLANs | Typical use |
|---|---|---|---|
| `access` | `switchport access vlan N` (one) | none | end devices |
| `trunk` | `switchport trunk native vlan N` (default 1) | `switchport trunk allowed vlan add 10,65` | uplinks to routers/switches/hypervisors |
| `general` | `switchport general allowed vlan add N untagged` + `switchport general pvid N` | `switchport general allowed vlan add 10,65 tagged` | hybrid ports, VoIP, fine control (acceptable-frame-type, ingress filtering) |
| `customer` | QinQ | | provider edge |

```
interface gi22
 description hv1 trunk
 switchport mode trunk
 switchport trunk native vlan 66
 switchport trunk allowed vlan add 10,65
 switchport trunk allowed vlan remove 1
interface gi6
 description IoT downstream
 switchport mode access
 switchport access vlan 10
 spanning-tree portfast
interface range gi13-15
 switchport mode access
 switchport access vlan 66
interface gi19
 switchport mode general
 switchport general allowed vlan add 66 untagged
 switchport general allowed vlan add 10 tagged
 switchport general pvid 66
 switchport general acceptable-frame-type all        # tagged-only | untagged-only | all
 switchport general ingress-filtering disable        # default enabled
show interfaces switchport gi22
show interfaces status ; show interfaces description ; show interfaces configuration
```
Changing mode with `switchport mode` resets the VLAN membership of that port; re-add allowed VLANs afterwards. `no switchport trunk native vlan` removes the native VLAN (all traffic tagged).

## Link aggregation

```
interface range gi25-26
 channel-group 1 mode auto        # LACP; "on" = static
interface Po1
 switchport mode trunk
 switchport trunk allowed vlan add 10,66
show interfaces port-channel ; show lacp port-channel
```
Member ports inherit the Po's VLAN config; configure VLANs on `PoN`, not on members.

## Spanning tree, storm control, security

```
spanning-tree mode rstp              # global: stp | rstp | mst
spanning-tree priority 4096          # make this switch root (multiples of 4096)
interface gi6
 spanning-tree portfast
 spanning-tree bpduguard enable
 storm-control broadcast enable
 storm-control broadcast level 10    # percent or kbps depending on version
 port security max 5 ; port security mode lock   # MAC limiting (syntax varies)
show spanning-tree ; show spanning-tree detail ; show spanning-tree interface gi1
```
Uplinks to routers without STP should not be `portfast`; ports facing other switches must not have bpduguard.

## PoE (P/MP/PP models)

```
show power inline                    # budget, per-port status/class/consumption
show power inline gi5
interface gi5
 power inline never                  # auto | never | static (2.x: "power inline auto/never")
 power inline limit 15400            # mW (1.x) or "power inline limit-mode"
 power inline priority critical
```
PoE power-cycling a device: `power inline never` → `power inline auto` (no dedicated "power cycle" on 1.x).

## Port basics

`shutdown` / `no shutdown`, `speed 1000|100|10|auto`, `duplex full|auto`, `negotiation`, `flowcontrol auto|on|off`, `mdix auto`, `description`, `mtu 9000` (jumbo, global `port jumbo-frame` on 1.x — needs reboot). `show interfaces counters giN` shows errors/CRC per port (they are not logged to syslog).
