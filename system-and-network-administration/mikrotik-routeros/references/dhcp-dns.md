# DHCP server, DHCP client, DNS

## DHCP server building blocks

```
/ip/pool/add name=hq-pool ranges=172.16.11.10-172.16.11.250
/ip/dhcp-server/add name=hq interface=vlan10-hq address-pool=hq-pool lease-time=12h disabled=no
/ip/dhcp-server/network/add address=172.16.8.0/22 gateway=172.16.8.6 dns-server=172.16.8.2 domain=example.lan ntp-server=172.16.8.2 comment="HQ"
```
- One server per interface. `authoritative=yes` (default) answers NAKs for foreign leases. `add-arp=yes` when `arp=reply-only` on the interface (locks IP↔MAC).
- `/ip/dhcp-server/setup` is an interactive wizard doing the three steps above.
- Network options: `gateway`, `dns-server`, `ntp-server`, `wins-server`, `domain`, `netmask` (override), `dhcp-option=`, `dhcp-option-set=`, `next-server`/`boot-file-name` (PXE).

## Leases

```
/ip/dhcp-server/lease/print where server=hq
/ip/dhcp-server/lease/print detail where host-name~"node1"
/ip/dhcp-server/lease/make-static [find mac-address=AA:BB:CC:DD:EE:FF]
/ip/dhcp-server/lease/add address=172.16.10.5 mac-address=AA:BB:CC:DD:EE:FF server=hq comment=node1
/ip/dhcp-server/lease/set [find comment=node1] dhcp-option-set=lan-alt      # per-host options (e.g. other gateway)
/ip/dhcp-server/lease/remove [find dynamic && host-name=""]
```
Static leases may sit outside the pool range (fixed addresses in `172.16.10.x` while the pool is `172.16.11.x`). Status column: `waiting`, `offered`, `bound`, `busy` (conflict detected). `/ip/dhcp-server/alert` logs rogue DHCP servers.

## Options and option sets

```
/ip/dhcp-server/option/add name=gw-alt code=3 value="'172.16.8.1'"                # option 3 router; quoted string = IP list
/ip/dhcp-server/option/add name=classless code=121 value=0x180A05000A050802000A050802 # RFC3442 static routes (hex)
/ip/dhcp-server/option/sets/add name=lan-alt options=gw-alt
/ip/dhcp-server/network/set [find comment=HQ] dhcp-option-set=lan-default      # network default
```
Precedence: lease options > network options > server. Values: `'text'` string, `0x…` hex, `'10.0.0.1'` IPs (single quotes inside double quotes on CLI), `$(NETWORK_GATEWAY)` variables. Clients that ask for option 121 ignore option 3 — include the default route inside the classless option.

`/ip/dhcp-server/matcher` assigns pools/option sets by vendor class (60), client-id (61) or hostname (12) substring.

## DHCP client (WAN)

```
/ip/dhcp-client/add interface=ether1 add-default-route=yes default-route-distance=1 use-peer-dns=no use-peer-ntp=no disabled=no
/ip/dhcp-client/print detail
/ip/dhcp-client/renew [find interface=ether1] ; /ip/dhcp-client/release …
```
`script=` runs on bound/deconfig with variables `$bound`, `$"lease-address"`, `$"gateway-address"` — used to fix routes into custom routing tables.

## DNS

```
/ip/dns/set servers=9.9.9.9,1.1.1.1 allow-remote-requests=yes cache-size=4096KiB cache-max-ttl=1d
/ip/dns/print ; /ip/dns/cache/print ; /ip/dns/cache/flush
/ip/dns/static/add name=node1.example.lan address=172.16.10.5 ttl=1d
/ip/dns/static/add name=node1 address=172.16.10.5
/ip/dns/static/add regexp="^(.*\\.)?lab\\.example.lan\$" address=172.16.10.1 comment="wildcard lab.example.lan"
/ip/dns/static/add name=corp.example type=FWD forward-to=10.99.0.1 comment="conditional forward"
/ip/dns/static/add name=old.host type=CNAME cname=new.host
/ip/dns/static/print
```
- `allow-remote-requests=yes` makes it a resolver for the LAN → firewall `input` must drop port 53 from WAN (open resolver otherwise).
- Static entries are ordered; regexp entries are matched first, lowercase only, and cost CPU — keep few. Names not matching DNS syntax are treated as regexp automatically.
- A static A record makes the router authoritative for that name for *all* record types (AAAA is then queried upstream and empty answers are fine).
- DoH: `/ip/dns/set use-doh-server=https://… verify-doh-cert=yes` plus an imported CA and a static A record for the DoH hostname; DoH replaces `servers=` entirely.
- Dynamic servers from DHCP/PPP show in `/ip/dns/print` as `dynamic-servers`; static ones are preferred.
- DHCP hostnames do not become DNS records by themselves; add static entries (or a small scheduler script over `/ip/dhcp-server/lease`).
