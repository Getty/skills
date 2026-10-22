# Firewall filter (`/ip/firewall/filter`)

## Chains and order

- `input`: packets *to* the router (its own addresses). `forward`: packets *through* the router. `output`: packets *from* the router. Custom chains via `action=jump jump-target=name` and `action=return`.
- Rules are evaluated top to bottom, first terminal match wins (`accept`, `drop`, `reject`, `tarpit`, `fasttrack-connection`). `log`, `passthrough`, `add-*-to-address-list` continue.
- No implicit drop: an empty chain accepts everything. Every chain you use ends with an explicit `action=drop`.
- Packet flow: `raw prerouting` → conntrack → `mangle prerouting` → `nat dstnat` → routing decision → `filter forward`/`input` → … → `nat srcnat`. Filter `forward` therefore sees post-dst-nat destination addresses; `input` never sees traffic that was dst-natted to a LAN host.

## Matchers you will use

| Matcher | Notes |
|---|---|
| `connection-state=established,related,new,invalid,untracked` | first rule accepts `established,related` |
| `connection-nat-state=dstnat` / `!dstnat` | "was this connection port-forwarded" |
| `in-interface=` `out-interface=` / `in-interface-list=WAN` | prefer lists (`/interface/list`) |
| `src-address=` `dst-address=` (single, CIDR, range `10.0.0.5-10.0.0.9`) | `!` negates |
| `src-address-list=` `dst-address-list=` | `/ip/firewall/address-list`, entries can carry `timeout=` |
| `protocol=tcp dst-port=22,80,443` / `port=` (either direction) | `dst-port` requires `protocol` |
| `icmp-options=8:0` (type:code) | |
| `tcp-flags=syn,!ack` | |
| `limit=10,20:packet` / `dst-limit=` | rate limiting; `limit=` is global per rule |
| `connection-mark=` `packet-mark=` `routing-mark=` | set in mangle |
| `time=8h-18h,mon,tue,wed,thu,fri` | |
| `ipsec-policy=in,ipsec` | match decrypted IPsec traffic |

Actions: `accept`, `drop`, `reject reject-with=icmp-admin-prohibited|tcp-reset`, `jump`, `return`, `log`, `passthrough`, `tarpit`, `fasttrack-connection` (IPv4, bypasses further filter/mangle/queue for that connection — must be paired with an accept rule right after it), `add-src-to-address-list address-list=x address-list-timeout=1d`, `add-dst-to-address-list`.

## Baseline rule set (interface lists `WAN`/`LAN`)

```
/interface/list
add name=WAN
add name=LAN
/interface/list/member
add list=WAN interface=ether1
add list=LAN interface=bridge

/ip/firewall/address-list
add list=mgmt address=172.16.0.0/24 comment="admin net"
add list=bogons address=0.0.0.0/8
add list=bogons address=10.0.0.0/8
add list=bogons address=100.64.0.0/10
add list=bogons address=127.0.0.0/8
add list=bogons address=169.254.0.0/16
add list=bogons address=172.16.0.0/12
add list=bogons address=192.0.0.0/24
add list=bogons address=192.0.2.0/24
add list=bogons address=192.168.0.0/16
add list=bogons address=198.18.0.0/15
add list=bogons address=198.51.100.0/24
add list=bogons address=203.0.113.0/24
add list=bogons address=224.0.0.0/3

/ip/firewall/filter
# --- input: protect the router
add chain=input action=accept connection-state=established,related,untracked comment="accept established"
add chain=input action=drop connection-state=invalid comment="drop invalid"
add chain=input action=accept protocol=icmp limit=20,50:packet comment="icmp (rate limited)"
add chain=input action=accept src-address-list=mgmt comment="management from admin net"
add chain=input action=accept in-interface-list=LAN protocol=udp dst-port=53 comment="dns from lan"
add chain=input action=accept in-interface-list=LAN protocol=tcp dst-port=53
add chain=input action=accept protocol=udp dst-port=13231 comment="wireguard"
add chain=input action=drop in-interface-list=!LAN comment="drop everything else from outside"
add chain=input action=drop comment="drop rest"
# --- forward: protect the LANs
add chain=forward action=fasttrack-connection connection-state=established,related hw-offload=yes comment="fasttrack"
add chain=forward action=accept connection-state=established,related,untracked comment="accept established"
add chain=forward action=drop connection-state=invalid comment="drop invalid"
add chain=forward action=drop in-interface-list=WAN src-address-list=bogons comment="bogons from wan"
add chain=forward action=accept in-interface-list=LAN comment="lan may go anywhere"
add chain=forward action=accept in-interface-list=WAN connection-nat-state=dstnat comment="port forwards"
add chain=forward action=drop in-interface-list=WAN connection-state=new comment="no new from wan"
add chain=forward action=drop comment="drop rest"
```
Adapt: inter-VLAN policy goes between "accept established" and "lan may go anywhere" (e.g. `add chain=forward action=drop in-interface=vlan-iot out-interface=vlan-admin`). Fasttrack breaks mangle/queues/some VPN paths; drop the fasttrack rule when using queues, policy routing marks or IPsec on those connections.

## Placing and verifying

```
/ip/firewall/filter/add chain=forward action=accept src-address=172.16.8.0/22 dst-address=172.16.10.5 protocol=tcp dst-port=6443 \
  place-before=[find comment="no new from wan"] comment="k8s api from hq"
/ip/firewall/filter/print stats where chain=forward           # hit counters
/ip/firewall/filter/reset-counters-all
/ip/firewall/connection/print where dst-address~"172.16.10.5"
/log/print where message~"drop-in"
```
Rules with `log=yes log-prefix="drop-in:"` show up in `/log`. Temporarily add a logging rule above a drop to see what is being dropped instead of guessing.

## Address lists as dynamic state

```
# SSH bruteforce staging: 3 new connections in a minute → blacklist for a day
add chain=input action=drop protocol=tcp dst-port=22 src-address-list=ssh_blacklist comment="ssh blacklist"
add chain=input action=add-src-to-address-list protocol=tcp dst-port=22 connection-state=new src-address-list=ssh_stage3 address-list=ssh_blacklist address-list-timeout=1d
add chain=input action=add-src-to-address-list protocol=tcp dst-port=22 connection-state=new src-address-list=ssh_stage2 address-list=ssh_stage3 address-list-timeout=1m
add chain=input action=add-src-to-address-list protocol=tcp dst-port=22 connection-state=new src-address-list=ssh_stage1 address-list=ssh_stage2 address-list-timeout=1m
add chain=input action=add-src-to-address-list protocol=tcp dst-port=22 connection-state=new address-list=ssh_stage1 address-list-timeout=1m
```
Address lists also accept DNS names (`address=example.org`) which RouterOS resolves periodically.

## RAW table (`/ip/firewall/raw`)

Chains `prerouting` and `output`, evaluated before connection tracking. `action=notrack` exempts traffic from conntrack (OSPF, heavy multicast, DDoS floods), `action=drop` here is the cheapest possible drop.
```
/ip/firewall/raw/add chain=prerouting action=drop in-interface-list=WAN src-address-list=bogons
```

## IPv6

Same structure under `/ipv6/firewall/filter`. Must accept `icmpv6` (input and forward), link-local (`fe80::/10`) for ND/DHCPv6, and `udp dst-port=546` for DHCPv6 client. LAN hosts are publicly reachable without NAT, so a `forward` drop of `connection-state=new in-interface-list=WAN` is mandatory.
