# Static routing, failover, PBR

```
ip route 0.0.0.0 0.0.0.0 203.0.113.1                  ! AD 1
ip route 0.0.0.0 0.0.0.0 172.16.8.6 254                   ! floating backup (higher AD loses while primary exists)
ip route 172.16.2.0 255.255.255.0 172.16.0.2 name via-hv1
ip route 192.0.2.0 255.255.255.0 Null0                  ! blackhole
show ip route | begin Gateway      show ip route 172.16.2.5      show ip cef 172.16.2.5 detail
```
Prefer next-hop IPs over exit interfaces on Ethernet (an interface-only static route relies on proxy-ARP for every destination).

## IP SLA tracked failover

```
ip sla 1
 icmp-echo 1.1.1.1 source-interface GigabitEthernet4
 frequency 10
 timeout 2000
ip sla schedule 1 life forever start-time now
track 1 ip sla 1 reachability
 delay down 30 up 10
ip route 1.1.1.1 255.255.255.255 203.0.113.1          ! pin the probe to the primary path
ip route 0.0.0.0 0.0.0.0 203.0.113.1 track 1
ip route 0.0.0.0 0.0.0.0 172.16.8.6 254
show track ; show ip sla statistics ; show ip route 0.0.0.0
```
A tracked route is withdrawn while the track is down; the floating route takes over. With NAT per uplink add a second overload rule with a route-map matching the backup interface, and clear translations on failover (`event manager applet` on `track 1 state down` → `clear ip nat translation *`).

## Policy-based routing

```
ip access-list extended PBR-VIA-ISP2
 permit ip host 172.16.10.1 any
route-map VIA-ISP2 permit 10
 match ip address PBR-VIA-ISP2
 set ip next-hop 172.16.8.6
route-map VIA-ISP2 permit 20          ! empty clause = normal routing for the rest
interface Vlan10
 ip policy route-map VIA-ISP2
ip local policy route-map …           ! for router-originated traffic
show route-map VIA-ISP2              ! match counters
```
`set ip next-hop verify-availability 172.16.8.6 1 track 1` skips the next hop when the track is down. PBR is CEF-switched; `debug ip policy` for short tests.

## Dynamic routing pointers

`router ospf 1` → `network 172.16.0.0 0.0.0.255 area 0`, `passive-interface default`, `no passive-interface Vlan66`; `show ip ospf neighbor`, `show ip protocols`. `router bgp <asn>` needs no license on ISR 900 but memory is the limit (no full tables). Redistribution and route-maps follow the same `match`/`set` grammar as PBR.

## Troubleshooting order

1. `show ip interface brief` — is the interface up/up with an address?
2. `show ip route <dst>` — which route wins, which next hop?
3. `show ip arp <next-hop>` — is the next hop resolvable?
4. `ping <dst> source <inside-ip>` / `traceroute <dst> source …` — path from the LAN's point of view.
5. `show ip cef <dst>` — CEF adjacency (CEF drop vs. process switching); `show ip cef exact-route src dst`.
6. ACL/NAT/ZBFW counters (`show access-lists`, `show ip nat statistics`, `show policy-map type inspect zone-pair sessions`).
