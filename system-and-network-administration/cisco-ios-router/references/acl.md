# Access control lists

## Types and syntax

| Type | Numbers | Match on |
|---|---|---|
| Standard | 1–99, 1300–1999 | source only |
| Extended | 100–199, 2000–2699 | protocol, src, dst, ports, flags |
| Named (`ip access-list standard|extended NAME`) | — | same, but editable with sequence numbers — **always use named** |

Wildcard masks are inverted netmasks: `/24` → `0.0.0.255`, `/22` → `0.0.3.255`, `/29` → `0.0.0.7`, host → `host x.x.x.x` (or `0.0.0.0`), any → `any`. Every ACL ends with an implicit `deny ip any any` (add an explicit `deny ip any any log` to count/see what hits it). A packet is compared top-down; first match wins. An ACL that does not exist yet but is referenced permits everything.

```
ip access-list extended WAN-IN
 remark --- replies to sessions started from inside (reflexive) ---
 evaluate LAN-REFLECT
 remark --- router-generated UDP replies (reflexive ACLs never track these) ---
 permit udp any eq ntp host 203.0.113.10
 permit udp any eq domain host 203.0.113.10
 remark --- diagnostics ---
 permit icmp any any echo-reply
 permit icmp any any unreachable
 permit icmp any any time-exceeded
 permit icmp any any packet-too-big
 remark --- published service example ---
 permit tcp any host 203.0.113.10 eq 22
 deny   ip any any log
ip access-list extended WAN-OUT
 permit ip any any reflect LAN-REFLECT timeout 300
interface GigabitEthernet4
 ip access-group WAN-IN in
 ip access-group WAN-OUT out
```
Reflexive ACLs (`reflect`/`evaluate`) give stateful behaviour without `securityk9`. They are created by traffic *forwarded* through the outbound ACL; the router's own DNS/NTP/SSH/SNMP-trap traffic is not seen by outbound ACLs, so its replies need explicit inbound permits. TCP-only alternative for old IOS: `permit tcp any any established` (matches ACK/RST set, no state).

## Editing named ACLs

```
ip access-list extended WAN-IN
 15 permit tcp host 203.0.113.5 host 203.0.113.10 eq 443     ! insert with sequence number
 no 40                                                        ! delete line 40
ip access-list resequence WAN-IN 10 10                        ! renumber
show access-lists WAN-IN                                      ! with hit counts
show ip access-lists | include matches
clear ip access-list counters
show ip interface Gi4 | include access list                   ! what is applied where
```
Adding a line without a sequence number appends at the end (after your `deny any`). Object groups (12.4(20)T+): `object-group network MGMT` → `host 172.16.0.1` / `172.16.8.0 255.255.252.0`; use as `permit tcp object-group MGMT any eq 22`.

## Where ACLs apply

| Use | Command |
|---|---|
| Interface filter | `ip access-group NAME in|out` (config-if) |
| VTY login restriction | `access-class NAME in` (config-line), standard ACL |
| SNMP | `snmp-server community X RO NAME` |
| NTP | `ntp access-group peer|serve|serve-only|query-only NAME` |
| NAT scope | `ip nat inside source list NAME …` |
| Route-map / PBR / ZBFW class-map | `match ip address NAME` / `match access-group name NAME` |
| Control plane policing | `class-map` + `control-plane` → `service-policy input` |
| Debug scope | `debug ip packet detail NAME` |

`log` / `log-input` on an ACE writes syslog lines (rate limited, CPU cost; `ip access-list logging interval`). `log-input` includes the ingress interface and source MAC.

## Checklist before applying an inbound WAN ACL

1. Established/reflexive or ZBFW allows replies.
2. Router-generated UDP (DNS 53, NTP 123, syslog is outbound only) has inbound permits.
3. ICMP unreachable / time-exceeded / echo-reply permitted (PMTUD, traceroute).
4. Your management path (SSH from inside) is not on that interface, or is permitted.
5. `reload in 10` armed; `show access-lists` shows hits where expected; `reload cancel`.
