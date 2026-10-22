# Zone-Based Policy Firewall (ZBFW) — requires `securityk9` active

Check `show license | begin securityk9` first; if it is not "Active, In Use", enable the RTU license and reload as described in references/isr900-platform.md (Licensing) before any command below.

Model: interfaces belong to **zones**; traffic between two zones is dropped unless a **zone-pair** with a **service-policy** allows it. Traffic within a zone is allowed. The router itself is the implicit **self** zone: traffic to/from `self` is allowed by default until a zone-pair involving `self` exists. An interface without a zone cannot talk to any interface that is in a zone.

## Minimal INSIDE → OUTSIDE with return traffic

```
zone security INSIDE
zone security OUTSIDE

class-map type inspect match-any CM-INSIDE-TO-OUT
 match protocol dns
 match protocol http
 match protocol https
 match protocol ftp          ! application-aware ALGs first, generic last
 match protocol icmp
 match protocol tcp
 match protocol udp
policy-map type inspect PM-INSIDE-TO-OUT
 class type inspect CM-INSIDE-TO-OUT
  inspect                    ! stateful: return traffic is allowed automatically
 class class-default
  drop log

zone-pair security IN-OUT source INSIDE destination OUTSIDE
 service-policy type inspect PM-INSIDE-TO-OUT

interface Vlan10
 zone-member security INSIDE
interface Vlan66
 zone-member security INSIDE
interface GigabitEthernet4
 zone-member security OUTSIDE
```
Actions: `inspect` (stateful), `pass` (stateless, one direction, needs a mirror zone-pair), `drop [log]`. Order inside a `match-any` class-map matters: put `match protocol http` before `match protocol tcp` so HTTP gets HTTP inspection, not plain TCP.

## Published service OUTSIDE → INSIDE (after NAT)

```
ip access-list extended ACL-OUT-TO-RDP
 permit tcp any host 172.16.10.86 eq 3389          ! post-NAT (inside) address
class-map type inspect match-all CM-OUT-TO-IN
 match access-group name ACL-OUT-TO-RDP
policy-map type inspect PM-OUT-TO-IN
 class type inspect CM-OUT-TO-IN
  inspect
 class class-default
  drop log
zone-pair security OUT-IN source OUTSIDE destination INSIDE
 service-policy type inspect PM-OUT-TO-IN
```

## Protecting the router (self zone)

Once you add a zone-pair with `self`, everything else to/from the router on that direction is dropped — include SSH, ICMP, DNS/NTP replies, routing protocols, VPN (isakmp udp 500/4500, esp).
```
ip access-list extended ACL-TO-SELF
 permit tcp 172.16.0.0 0.0.0.255 any eq 22
 permit icmp any any
 permit udp any eq domain any
 permit udp any eq ntp any
class-map type inspect match-any CM-TO-SELF
 match access-group name ACL-TO-SELF
policy-map type inspect PM-TO-SELF
 class type inspect CM-TO-SELF
  inspect                     ! "pass" for protocols inspection cannot handle (esp, gre, ospf)
 class class-default
  drop log
zone-pair security OUT-SELF source OUTSIDE destination self
 service-policy type inspect PM-TO-SELF
zone-pair security SELF-OUT source self destination OUTSIDE
 service-policy type inspect PM-SELF-OUT      ! inspect tcp/udp/icmp so replies to router-originated traffic return
```
Simpler alternative for small routers: leave `self` untouched and protect the router with an inbound ACL on the WAN interface.

## Verify and tune

```
show zone security                          show zone-pair security
show policy-map type inspect zone-pair sessions      # live sessions
show policy-map type inspect zone-pair IN-OUT        # counters per class
show class-map type inspect
parameter-map type inspect global
 log dropped-packets enable
 max-incomplete high 1000 / low 800
 tcp idle-time 3600
 alert on
```
Interfaces inside the same zone bypass inspection (intra-zone allowed); to filter between VLANs put them in separate zones with their own zone-pairs. Removing `zone-member` from an interface while a zone-pair exists cuts its traffic to every zoned interface — do it on console or with `reload in`.
