# Management plane: logging, time, SNMP, discovery, service hygiene

```
service timestamps log datetime msec localtime show-timezone
service timestamps debug datetime msec localtime
logging buffered 65536 informational
logging console warnings              ! or "no logging console" on busy routers
logging monitor informational         ! + "terminal monitor" in a session to see logs
logging host 172.16.10.1                ! syslog UDP 514; "transport udp port 5514" optional
logging trap informational
logging source-interface Vlan66
login block-for 120 attempts 3 within 60
login on-failure log
login on-success log
banner motd ^ Authorized access only ^
no ip http server
no ip http secure-server              ! or restrict: ip http access-class NAME, ip http secure-server only from inside
no ip source-route
no ip bootp server
no service pad
no service finger
service tcp-keepalives-in
service tcp-keepalives-out
no cdp run                            ! or keep globally and "no cdp enable" on WAN interfaces
lldp run                              ! optional, then "no lldp transmit/receive" on WAN
no ip domain-lookup                   ! stops typo → DNS lookups on the CLI (keep name-server for the router's own needs)
```

## NTP as a server for the LAN, not for the world

```
ip access-list standard NTP-PEERS
 permit host 162.159.200.1
 permit host 216.239.35.0
ip access-list standard LAN-INTERN
 permit 172.16.0.0 0.0.0.255
 permit 172.16.8.0 0.0.3.255
ntp server 162.159.200.1
ntp server 216.239.35.0
ntp access-group peer NTP-PEERS          ! who may be our time source
ntp access-group serve-only LAN-INTERN  ! who may ask us for time
ntp source Vlan66
show ntp status                          ! "Clock is synchronized, stratum 4"
show ntp associations                    ! * = selected peer
```
Without access-groups an IOS router answers NTP to anyone reaching its WAN IP (amplification abuse).

## SNMP (read-only, ACL-bound)

```
ip access-list standard SNMP-RO
 permit host 172.16.10.1
snmp-server community <community> RO SNMP-RO
snmp-server location HQ rack
snmp-server contact ops@example
snmp-server ifindex persist
! SNMPv3 instead:
snmp-server group RO-V3 v3 priv read ISO-VIEW access SNMP-RO
snmp-server user monitor RO-V3 v3 auth sha <pw> priv aes 128 <pw>
snmp-server view ISO-VIEW iso included
show snmp ; show snmp user ; show snmp community
```

## Discovery and neighbours

`show cdp neighbors detail`, `show lldp neighbors detail`, `show mac address-table` (switch ports), `show ip arp`, `show ip dhcp binding`. Devices that send neither CDP nor LLDP (Linux hosts, VMs) are located via MAC table → port.

## Users, AAA, privilege

- Local users with `privilege 15 secret`; avoid shared `enable` for daily work but keep `enable secret` set.
- `aaa new-model` + `aaa authentication login default local` + `aaa authorization exec default local` gives consistent behaviour on console and VTY; `aaa authentication login CONSOLE none` bound to `line con 0` is a common escape hatch on lab gear (not for production).
- `show users`, `show line`, `clear line vty 0` to kick a stuck session.
- `archive` → `log config` → `logging enable` + `hidekeys` gives a change audit log (`show archive log config all`).
