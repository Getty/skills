# Interfaces, VLANs, SVIs, DHCP, DNS, NTP client

## Routed WAN port

```
interface GigabitEthernet4
 description WAN modem
 ip address 203.0.113.10 255.255.255.248
 no ip redirects
 no ip unreachables
 no ip proxy-arp
 no cdp enable
 ip nat outside            ! if NAT is used
 no shutdown
ip route 0.0.0.0 0.0.0.0 203.0.113.1
```
DHCP-addressed WAN: `ip address dhcp` (adds a default route automatically; `ip dhcp client default-router distance 254` on newer IOS). PPPoE: `pppoe-client dial-pool-number 1` + `interface Dialer1` with `ip mtu 1492`, `ppp authentication chap callin`, `ip tcp adjust-mss 1452` on the LAN SVI.

## Built-in switch ports (Gi0–Gi3) and VLANs

```
vlan 10
 name HQ
vlan 66
 name ADMIN
! older 800/900 images use "vlan database" → "vlan 10" → "exit" instead
interface GigabitEthernet0
 description trunk to core-sw
 switchport mode trunk
 switchport trunk allowed vlan 10,66
 switchport trunk native vlan 66
interface GigabitEthernet1
 switchport mode access
 switchport access vlan 10
 spanning-tree portfast
interface Vlan10
 ip address 172.16.8.1 255.255.252.0
 ip nat inside
interface Vlan66
 ip address 172.16.0.5 255.255.255.0
```
- Verify: `show vlan-switch` (or `show vlan`), `show interfaces trunk`, `show interfaces Gi0 switchport`, `show interfaces status`, `show mac address-table`.
- An SVI is `up` only if at least one switch port carrying that VLAN is up.
- Routed sub-interfaces exist on the WAN ports for tagged uplinks: `interface Gi4.65` → `encapsulation dot1Q 65` → `ip address …`.
- `interface Vlan1` is the default; shut it if unused.

## DHCP server

```
ip dhcp excluded-address 172.16.8.1 172.16.8.99
ip dhcp pool HQ
 network 172.16.8.0 255.255.252.0
 default-router 172.16.8.1
 dns-server 172.16.8.2 9.9.9.9
 domain-name example.lan
 lease 0 12
ip dhcp pool PRINTER
 host 172.16.10.19 255.255.252.0
 client-identifier 0100.1122.3344.55        ! 01 + MAC for Ethernet clients; or "hardware-address 0011.2233.4455"
show ip dhcp binding / pool / conflict / server statistics
clear ip dhcp binding *
```
`ip dhcp relay information trust-all` / `ip helper-address 172.16.8.2` on an SVI forwards DHCP to another server instead (also forwards other UDP broadcasts unless restricted with `no ip forward-protocol udp <port>`).

## DNS and NTP client

```
ip name-server 9.9.9.9 1.1.1.1
ip domain-lookup                      ! or "no ip domain-lookup" to stop typo lookups on the CLI
ip domain-name example.lan
ntp server 162.159.200.1
ntp server 216.239.35.0 prefer
ntp source Vlan66
clock timezone CET 1 0
clock summer-time CEST recurring last Sun Mar 2:00 last Sun Oct 3:00
show ntp status ; show ntp associations ; show clock detail
```
NTP needs UDP 123 replies allowed inbound (reflexive ACLs do not track router-originated traffic — permit `udp any eq ntp host <wan-ip>`), same for DNS (`udp any eq domain`).

## Interface hygiene

`description` on every interface; `shutdown` unused ports; `no ip proxy-arp`, `no ip redirects` on WAN; `ip mtu`/`ip tcp adjust-mss` on tunnels; `speed`/`duplex` only when auto-negotiation fails. `show interfaces | include line protocol|errors|drops` for a quick health sweep; `clear counters` before measuring.
