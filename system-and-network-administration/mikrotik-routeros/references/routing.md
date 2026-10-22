# Routing (`/ip/route`, `/routing/*`)

## Reading routes

```
/ip/route/print                              # DAC connected, AS static active, I inactive, X disabled
/ip/route/print detail where dst-address=0.0.0.0/0
/ip/route/print where static
/routing/route/print detail                  # all afi, includes filtered/unreachable (F/U flags)
/ip/route/print where routing-table=wan2
```
Flags: `D` dynamic, `A` active, `I` inactive, `X` disabled, `C` connected, `S` static, `d` dhcp, `+` ECMP, `H` HW-offload candidate, `B` blackhole. Selection: lowest `distance` wins among candidates with resolvable gateways; ties → arbitrary (or ECMP if `+`). Static default distance 1, DHCP 1 (configurable `default-route-distance` on the client), OSPF 110, BGP 20/200.

## Static routes and failover

```
/ip/route/add dst-address=172.16.2.0/24 gateway=172.16.0.2 comment="via hv1"
/ip/route/add dst-address=0.0.0.0/0 gateway=203.0.113.1 distance=1 check-gateway=ping comment="primary"
/ip/route/add dst-address=0.0.0.0/0 gateway=198.51.100.1 distance=2 check-gateway=ping comment="backup"
/ip/route/add dst-address=0.0.0.0/0 type=blackhole distance=250 comment="never leak via masquerade"
```
`check-gateway=ping|arp|bfd`: probes every 10 s, two misses → route inactive, next distance takes over. Ping only tests the *next hop*, not the internet behind it.

### Recursive routes (test real reachability)

```
/ip/route
add dst-address=1.1.1.1/32 gateway=203.0.113.1 scope=10 comment="probe isp1"
add dst-address=0.0.0.0/0 gateway=1.1.1.1 distance=1 check-gateway=ping comment="default via isp1"
add dst-address=9.9.9.9/32 gateway=172.16.8.6 scope=10 comment="probe isp2"
add dst-address=0.0.0.0/0 gateway=9.9.9.9 distance=2 check-gateway=ping comment="default via isp2"
```
The default route's gateway is not on-link; RouterOS resolves it through the `/32` route (nexthop lookup uses routes with `scope <= target-scope`; static default `scope=30`, `target-scope=10`, connected `scope=10` — hence `scope=10` on the probe routes). Ping to 1.1.1.1 now travels via ISP1 only; if the ISP's upstream dies the default flips even though the modem still answers ARP. Use different probe hosts per uplink. A WireGuard interface cannot be a recursive gateway (interface gateways have no IP); use `gateway=wireguard1` directly.

### ECMP

`gateway=203.0.113.1,198.51.100.1` on one route → `+` flag, per-connection hashing (layer-3 by default). Combine with `check-gateway` to drop dead members.

## Policy routing (v7)

```
/routing/table/add name=via-isp2 fib
/ip/route/add dst-address=0.0.0.0/0 gateway=172.16.8.6 routing-table=via-isp2
/routing/rule/add src-address=172.16.10.1/32 action=lookup-only-in-table table=via-isp2 comment="srv1 via isp2"
# or by firewall mark:
/ip/firewall/mangle/add chain=prerouting src-address=172.16.11.0/24 action=mark-routing new-routing-mark=via-isp2 passthrough=no
```
Rules: `action=lookup` (fall back to main if no match), `lookup-only-in-table` (no fallback), `drop`, `unreachable`. Interface-based `in-interface=` rules exist too. Remember NAT: a per-table default route needs a matching `srcnat` rule for that uplink (`out-interface=`).

## Routing filters / dynamic protocols (pointer)

`/routing/filter/rule/add chain=ospf-in rule="if (dst in 10.0.0.0/8) { accept } else { reject }"` — v7 filter language, chains referenced from `/routing/ospf/instance` (`in-filter-chain`, `out-filter-chain`) or `/routing/bgp/connection`. `/routing/ospf/neighbor/print`, `/routing/bgp/session/print`, `/routing/stats/print`.

## Common questions

- "Route shows but is inactive (`I`)": gateway not resolvable (no connected route covering it, interface down, or `scope`/`target-scope` too strict).
- Default route from DHCP client and a static one both exist: the DHCP one has the distance from `/ip/dhcp-client default-route-distance`; disable `add-default-route` on the client if the static one should win.
- `pref-src=` chooses the router's source address for locally generated traffic on that route (multi-IP interfaces).
- Tracing the decision: `/tool/traceroute` with `src-address=`, or `/routing/route/print detail where dst-address=…` to see `immediate-gw`.
