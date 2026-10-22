# NAT on IOS

## Overload (PAT) for a LAN

```
ip access-list standard NAT-INSIDE
 permit 172.16.8.0 0.0.3.255
 permit 172.16.0.0 0.0.0.255
interface Vlan10
 ip nat inside
interface Vlan66
 ip nat inside
interface GigabitEthernet4
 ip nat outside
ip nat inside source list NAT-INSIDE interface GigabitEthernet4 overload
```
With a pool of public addresses: `ip nat pool PUB 203.0.113.10 203.0.113.10 netmask 255.255.255.248` + `ip nat inside source list NAT-INSIDE pool PUB overload`. Route-map variant for per-uplink NAT: `ip nat inside source route-map VIA-GI4 interface Gi4 overload` with `route-map VIA-GI4 permit 10` → `match ip address NAT-INSIDE` → `match interface Gi4`.

## Static NAT / port forwards

```
ip nat inside source static tcp 172.16.10.86 3389 interface GigabitEthernet4 33389     ! extern 33389 → intern 3389
ip nat inside source static udp 172.16.10.14 27015 203.0.113.10 27015
ip nat inside source static 172.16.10.20 203.0.113.12                                    ! 1:1 for a second public IP
```
- A static 1:1 entry answers ARP for the public IP on the outside interface automatically (proxy) as long as it is in the connected subnet; otherwise add a route for the public IP towards the router.
- An inbound ACL on the outside interface is evaluated **before** NAT (destination still public); a ZBFW OUT→IN class-map matches **after** NAT (destination already private) — write the ACLs accordingly.
- Hairpin (LAN client → public IP → LAN server) does not work with classic inside/outside NAT. Use NVI (`ip nat enable` on both interfaces + `ip nat source list … overload`, no inside/outside keywords) or split DNS.

## Verify and clear

```
show ip nat translations              show ip nat translations verbose
show ip nat statistics                # interfaces marked inside/outside, hits/misses, pool usage
clear ip nat translation *            # drops all dynamic entries (sessions reset); "clear ip nat translation inside a.b.c.d"
ip nat translation timeout 3600       ip nat translation tcp-timeout 7200 / udp-timeout 300 / icmp-timeout 60
ip nat translation max-entries 8192   # protect small routers from table exhaustion
debug ip nat                          # short bursts only
```
Empty translation table with correct rule → an interface is missing `ip nat inside|outside`, the ACL does not match the source, or traffic is not actually routed through the router (check `show ip route` and the client's gateway).

## Typical layout on an ISR 900 with public /29

Outside = Gi4 with one public IP; inside = SVIs. Publishing hosts that own their *own* public IP from the same /29 (like a VM bridged into the public VLAN) is not NAT — they need only L2 reachability to the modem; do not add them to `NAT-INSIDE`.
