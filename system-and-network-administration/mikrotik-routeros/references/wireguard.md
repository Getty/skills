# WireGuard (`/interface/wireguard`)

Keys are generated on interface creation; the private key is shown in `print` to users with the `sensitive` policy and is exported only with `show-sensitive`.

## Site-to-site

```
# both sides
/interface/wireguard/add name=wg-siteb listen-port=13231 comment="site-to-site"
/interface/wireguard/print                     # copy public-key to the other side
# side A (172.16.0.0/16 local, remote 10.30.30.0/24)
/interface/wireguard/peers/add interface=wg-siteb public-key="<B pub>" endpoint-address=198.51.100.97 endpoint-port=51820 \
  allowed-address=10.30.30.0/24,192.168.0.0/24,10.99.0.22/32 persistent-keepalive=25s name=siteb
/ip/address/add address=10.99.0.21/32 interface=wg-siteb     # or a /30 on both ends
/ip/route/add dst-address=10.30.30.0/24 gateway=wg-siteb
/ip/route/add dst-address=192.168.0.0/24 gateway=wg-siteb
# firewall
/ip/firewall/filter/add chain=input action=accept protocol=udp dst-port=13231 comment="wireguard" place-before=[find comment="drop everything else from outside"]
/ip/firewall/filter/add chain=forward action=accept in-interface=wg-siteb dst-address=172.16.0.0/16 comment="from vpn"
/interface/list/member/add list=LAN interface=wg-siteb       # simplest: treat tunnel as LAN
```
- `allowed-address` is both the ingress ACL (packets from the peer with other source IPs are dropped) and the egress selector (packets to those prefixes go to that peer). Prefixes must not overlap between peers of one interface; a road-warrior peer therefore gets `x.x.x.x/32`.
- Routes still need to exist (`gateway=wg-siteb`); `allowed-address` does not install routes.
- `persistent-keepalive=25s` on the side behind NAT/dynamic IP. `responder=yes` on the "server" side stops it from hammering a stale endpoint.
- MTU 1420 default; lower (`1380`) over PPPoE/DS-Lite if large packets stall. Optionally clamp MSS: `/ip/firewall/mangle/add chain=forward protocol=tcp tcp-flags=syn out-interface=wg-siteb action=change-mss new-mss=clamp-to-pmtu`.

## Road warrior (phones/laptops)

```
/interface/wireguard/add name=wg-rw listen-port=13232
/ip/address/add address=10.99.1.1/24 interface=wg-rw
/interface/wireguard/peers/add interface=wg-rw public-key="<client pub>" allowed-address=10.99.1.2/32 name=phone \
  client-address=10.99.1.2/32 client-dns=172.16.8.2 client-endpoint=vpn.example.org:13232 client-keepalive=25s
/interface/wireguard/peers/show-client-config [find name=phone]   # prints config + QR (needs show-sensitive on ≥7.21)
/ip/firewall/filter/add chain=input action=accept src-address=10.99.1.0/24 comment="rw clients may use dns"
/ip/firewall/nat/add chain=srcnat action=masquerade src-address=10.99.1.0/24 out-interface-list=WAN comment="rw to internet"
```
`wg-import file=peer.conf` / `config-string=` imports a standard `[Interface]/[Peer]` file (no leading `#` comment lines).

## Diagnostics

```
/interface/wireguard/peers/print detail        # last-handshake, rx/tx, current-endpoint-address
/interface/wireguard/print
/log/print where topics~"wireguard"
/tool/torch interface=wg-siteb
```
No handshake at all → firewall input on the listener, wrong endpoint/port, or key mismatch. Handshake but no traffic → `allowed-address` does not cover the source, route missing, or forward-chain drop. Reply traffic leaves via the wrong WAN on multi-WAN routers → mangle/mark the UDP flow by incoming interface (docs "Multi-WAN setup") or set `responder=yes`.
