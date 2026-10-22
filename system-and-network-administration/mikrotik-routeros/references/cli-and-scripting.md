# CLI details, scripting, users, services, diagnostics

## print options

```
print detail                      # all properties, multi-line
print terse                       # one item per line: "0 X chain=input action=drop …"
print brief / print without-paging
print where chain=input && action=drop
print where address~"^10\\.5\\."   # ~ is regex
print proplist=name,running       # only listed properties (v7: `proplist=`)
print count-only
print stats                       # firewall: bytes/packets per rule
print interval=1                  # refresh every second (Ctrl+C to stop)
print file=routes                 # writes routes.txt into /file
print as-value                    # scripts: returns array instead of text
```

Find/where operators: `=` `!=` `<` `>` `~` (regex) `in` (`address in 10.0.0.0/8`), combine with `&&`, `||`, `!`.
Flags column legend appears on top of every `print` (`X` disabled, `D` dynamic, `I` invalid, `A` active, `R` running…).

## Scripting essentials

```
:local gw [/ip/route/get [find dst-address=0.0.0.0/0 && active] gateway]
:put $gw
:foreach i in=[/ip/dhcp-server/lease/find dynamic=yes] do={
  :put ([/ip/dhcp-server/lease/get $i address] . " " . [/ip/dhcp-server/lease/get $i host-name])
}
:if ([/ping 1.1.1.1 count=3] = 0) do={ :log warning "uplink down" } else={ :log info "uplink ok" }
```

- Variables: `:local`, `:global`; strings concatenate with `.`; `[ … ]` evaluates a command; `$var` expands.
- Conversions: `:tostr` `:tonum` `:toip` `:toarray`; `:len`, `:pick $s 0 3`, `:find`, `:typeof`.
- `:delay 5s`, `:log info "…"`, `:error "abort"`, `:execute` (run in background).
- Store: `/system/script/add name=chk source={ … }`; run with `/system/script/run chk`; schedule with `/system/scheduler/add name=chk interval=5m on-event=chk start-time=startup`.
- Scripts run with the policies of their owner; `policy=read,write,test` on the script limits them. Scripts started by scheduler cannot ask for interactive input.
- Netwatch for simple reachability actions: `/tool/netwatch/add host=1.1.1.1 interval=30s down-script="…" up-script="…"`.

## History, undo, safe mode

```
/system/history/print detail      # every change with the exact undo/redo command
/undo   /redo
```
Safe mode: `Ctrl+X` on (prompt `<SAFE>`), `Ctrl+X` again commits, `Ctrl+D` aborts and reverts. Up to 100 actions are tracked; beyond that safe mode silently drops out — make small steps. Another admin entering safe mode gets a hijack prompt (u = undo yours, r = keep, d = leave).

## Users, groups, SSH keys

```
/user/group/print                             # built-in: read, write, full
/user/add name=ops group=full password=…
# built-in "read" = local,telnet,ssh,reboot,read,test,winbox,password,web,sniff,sensitive,api,romon,rest-api
# → it includes "sensitive": a read user prints WireGuard private keys, PPP/hotspot secrets, SNMP communities.
# For audits and monitoring create a group without it:
/user/group/add name=audit policy=read,ssh,rest-api,test,!sensitive,!write,!policy,!local,!ftp,!winbox,!web,!reboot,!sniff,!password,!romon
/user/add name=ops group=audit password=…
/user/group/add name=ops-api policy=read,write,api,rest-api,!local,!ftp,!ssh,!winbox,!web,!sensitive
/user/set ops group=ops-api
/user/ssh-keys/import public-key-file=id_ed25519.pub user=ops   # upload the .pub first (scp/sftp/WinBox Files)
/user/ssh-keys/print
/user/active/print                            # who is logged in from where
```
Policies that matter: `sensitive` (show keys/passwords in print/export), `policy` (manage users), `write`, `test` (ping/traceroute/torch), `ssh`/`winbox`/`web`/`api`/`rest-api`/`ftp` (which services the user may use), `local` (console), `reboot`, `romon`, `sniff`.

## Services and hardening

```
/ip/service/print
/ip/service/set ssh address=172.16.0.0/24,10.99.0.0/24
/ip/service/disable telnet,ftp,www,api          # keep ssh, winbox, www-ssl/api-ssl as needed
/ip/ssh/set strong-crypto=yes forwarding-enabled=no
/tool/mac-server/set allowed-interface-list=LAN
/tool/mac-server/mac-winbox/set allowed-interface-list=LAN
/ip/neighbor/discovery-settings/set discover-interface-list=LAN
/tool/bandwidth-server/set enabled=no
/ip/dns/set allow-remote-requests=yes            # then firewall port 53 from WAN (see firewall reference)
```
Interface lists (`/interface/list`, `/interface/list/member`) are the way to say "LAN"/"WAN" in firewall, services and discovery; default configs ship `LAN` and `WAN`.

## Logging

```
/log/print where topics~"firewall"
/log/print follow-only
/system/logging/print
/system/logging/add topics=firewall action=memory
/system/logging/action/add name=syslog target=remote remote=172.16.10.1 remote-port=514
/system/logging/add topics=info,!debug action=syslog
```
Firewall rules log with `log=yes log-prefix="drop-in:"`.

## Diagnostics

```
/ping 172.16.0.1 count=4 src-address=172.16.8.2 interface=ether1
/tool/traceroute 1.1.1.1 count=1
/tool/torch interface=ether1 src-address=0.0.0.0/0 dst-address=0.0.0.0/0 port=any   # live top talkers
/tool/sniffer/quick interface=ether1 ip-address=172.16.0.5 duration=10
/tool/sniffer/set file-name=cap.pcap filter-interface=ether1 ; /tool/sniffer/start ; /tool/sniffer/stop   # then /file
/interface/monitor-traffic ether1 once
/interface/ethernet/monitor ether1 once            # link speed, negotiation
/ip/arp/print ; /ip/neighbor/print                 # ARP table, LLDP/CDP/MNDP neighbours
/interface/bridge/host/print                        # bridge MAC table
/ip/firewall/connection/print where dst-address~":443"
/tool/profile                                       # CPU by process
/system/resource/print ; /system/health/print ; /system/clock/print
/system/ntp/client/print ; /system/ntp/client/set enabled=yes servers=time.cloudflare.com
```
