# NAT (`/ip/firewall/nat`)

Chains: `srcnat` (after routing, packets leaving), `dstnat` (before routing, packets arriving); v7 also has `input`/`output` NAT chains for router-local traffic. NAT matches only the first packet of a connection; conntrack applies the result to the rest. **Changing NAT rules does not affect existing connections** — remove them: `/ip/firewall/connection/remove [find dst-address~"^10\\.5\\.10\\.12"]`.

## Source NAT

```
# dynamic public IP (DHCP/PPPoE): masquerade
/ip/firewall/nat/add chain=srcnat action=masquerade out-interface-list=WAN comment="masq"
# static public IP: src-nat (survives link flaps, keeps conntrack)
/ip/firewall/nat/add chain=srcnat action=src-nat to-addresses=203.0.113.11 out-interface=wan11 src-address=10.0.0.0/8
# per-segment / per-uplink
/ip/firewall/nat/add chain=srcnat action=src-nat to-addresses=198.51.100.254 out-interface=wan12 src-address=172.16.8.0/22
```
Masquerade picks the outgoing interface address and purges related connections on interface down/IP change; with unstable multi-WAN this leaks private IPs over the backup path. Mitigation: `action=src-nat` with explicit `to-addresses`, plus a blackhole default route with higher distance than every real one.

## Destination NAT (port forward)

```
/ip/firewall/nat/add chain=dstnat action=dst-nat dst-address=203.0.113.11 protocol=tcp dst-port=33389 \
  to-addresses=172.16.10.86 to-ports=3389 comment="RDP"
/ip/firewall/nat/add chain=dstnat action=dst-nat in-interface=wan11 protocol=udp dst-port=27015 to-addresses=172.16.10.14 comment="game"
```
- Match on `dst-address=<public ip>` (or `in-interface`), never on `dst-address-type=local` alone if the router has several public IPs.
- The filter `forward` chain must allow it: `connection-nat-state=dstnat` accept rule (see firewall reference).
- Restrict sources with `src-address=` or `src-address-list=` on the dst-nat rule.
- `action=redirect to-ports=53` sends traffic to the router itself (transparent DNS/proxy).

## Hairpin NAT (LAN clients using the public IP)

```
/ip/firewall/nat/add chain=srcnat action=masquerade src-address=172.16.8.0/22 dst-address=172.16.10.14 \
  out-interface=lan protocol=udp dst-port=27015 comment="hairpin game"
```
Without it the server replies directly to the LAN client with its private IP and the client discards the packet. Keep the dst-nat rule matching on `dst-address=<public ip>` (not `in-interface=wan`) so LAN-originated packets hit it too.

## Other actions

| Action | Use |
|---|---|
| `netmap to-addresses=192.168.10.0/24` | 1:1 mapping of whole prefixes |
| `same` | keep same public IP per client across connections |
| `endpoint-independent-nat` (UDP only, srcnat + dstnat pair) | NAT traversal friendliness for games/VoIP |
| `redirect` | to router itself |
| `socksify` | route via SOCKS proxy |

NAT helpers (ALGs) live in `/ip/firewall/service-port` (ftp, sip, pptp, h323, tftp…). Disable `sip` if VoIP behaves strangely behind NAT.

## Checking

```
/ip/firewall/nat/print stats
/ip/firewall/connection/print where protocol=tcp && dst-address~":3389"
/ip/firewall/connection/print detail where reply-dst-address~"172.16.10.86"
```
