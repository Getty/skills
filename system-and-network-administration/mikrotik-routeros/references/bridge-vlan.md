# Bridge VLAN filtering (`/interface/bridge`)

Two models exist; know which one a router uses before touching it:

1. **VLAN on a physical/trunk interface, no bridge filtering** (router-on-a-stick): `/interface/vlan/add interface=ether1 vlan-id=65 name=vlan65` and put addresses on `vlan65`. Tagging is done elsewhere (a managed switch). Simple, no lockout risk. Several bridges *without* `vlan-filtering` per segment are the same model.
2. **Bridge VLAN filtering**: one bridge, ports get `pvid`, a VLAN table says which VLAN is tagged/untagged on which port, and `/interface/vlan` on the *bridge* gives the router an IP in a VLAN. Needed when the router itself is the switch (hardware offload on CRS/RB with switch chip).

## Concepts

- **pvid** on a bridge port: untagged ingress frames get this VLAN. Bridge itself also has a `pvid` (default 1) — that is the CPU port's untagged VLAN.
- **`/interface/bridge/vlan`** entries: `vlan-ids`, `tagged=` ports, `untagged=` ports. Checked on *egress*: a VLAN not listed for the egress port is dropped. Ports with the same pvid are added dynamically as untagged.
- **CPU port** = the bridge interface name itself in `tagged=`/`untagged=`. Management traffic must reach it.
- **`ingress-filtering=yes`** on a port: drop frames whose VLAN is not allowed on that ingress port. **`frame-types=admit-only-vlan-tagged | admit-only-untagged-and-priority-tagged | admit-all`** limits what a port accepts (requires ingress-filtering).
- One VLAN id per access port entry; multiple `vlan-ids` only for pure trunk entries.

## Lockout-safe order (do this in safe mode, or via serial/MAC-telnet)

```
/interface/bridge/add name=bridge1 vlan-filtering=no
/interface/bridge/port
add bridge=bridge1 interface=ether1 comment=trunk               # tagged trunk to switch
add bridge=bridge1 interface=ether2 pvid=10 comment=access-hq
add bridge=bridge1 interface=ether3 pvid=66 comment=access-admin
/interface/bridge/vlan
add bridge=bridge1 tagged=bridge1,ether1 vlan-ids=66 comment="admin/mgmt: router listens here"
add bridge=bridge1 tagged=ether1 untagged=ether2 vlan-ids=10
add bridge=bridge1 tagged=bridge1,ether1 vlan-ids=65
/interface/vlan
add interface=bridge1 vlan-id=66 name=vlan66-admin
add interface=bridge1 vlan-id=10 name=vlan10-hq
/ip/address
add address=172.16.0.8/24 interface=vlan66-admin
add address=172.16.8.2/22 interface=vlan10-hq
/interface/bridge/port
set [find interface=ether1] ingress-filtering=yes frame-types=admit-only-vlan-tagged
set [find interface=ether2] ingress-filtering=yes frame-types=admit-only-untagged-and-priority-tagged
# --- last step, verify table first:
/interface/bridge/vlan/print
/interface/bridge/set bridge1 vlan-filtering=yes
```
If management should only work tagged, also `/interface/bridge/set bridge1 frame-types=admit-only-vlan-tagged ingress-filtering=yes` — this removes the dynamic untagged CPU entry for pvid 1.

## Verification

```
/interface/bridge/vlan/print            # CURRENT-TAGGED / CURRENT-UNTAGGED include dynamic entries (D flag)
/interface/bridge/port/print
/interface/bridge/host/print where vid=66   # MAC table with VLAN
/interface/bridge/print                 # vlan-filtering, pvid, ether-type, hw offload
/interface/bridge/port/print where !hw   # ports without hardware offload (CPU-switched)
```
`ether-type=0x8100` default; `0x88a8` for QinQ service tags. Hardware offload with vlan-filtering works only on switch-chip models listed in the docs; otherwise the CPU switches and throughput drops.

## Typical failures

- Router unreachable right after `vlan-filtering=yes`: the CPU port is not in the management VLAN entry (`tagged=bridge1,…`), or the bridge pvid mismatch. Safe mode reverts; else serial console / reset.
- Trunk to a switch works only for one VLAN: VLAN table entry has `tagged=ether1` for one id but not the others.
- Hosts in different access ports see each other although they should not: single entry with several `vlan-ids` and `untagged=ether2,ether3`.
- DHCP works but routing does not: `/interface/vlan` exists but its `interface=` is a physical port instead of the bridge (or vice versa).
