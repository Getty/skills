# Monitoring, discovery, mirroring, logging, time, SNMP

## Interface state

```
show interfaces status                  # Up/Down, speed, duplex, type per port
show interfaces status gi22
show interfaces description
show interfaces configuration           # admin state, negotiation, flowcontrol
show interfaces counters                # all ports; "clear counters" resets
show interfaces counters gi1            # errors, CRC, collisions, oversize
show interfaces switchport gi22         # mode, PVID, tagged/untagged membership
show interfaces utilization             # 2.x
show ip interface ; show arp
```

## Neighbours (who is on which port)

```
show lldp neighbors                     # Linux/ESXi/Proxmox with lldpd, phones, other switches
show lldp neighbors gi1                 # detail incl. management address, capabilities
show lldp local gi1 ; lldp run ; lldp med …
show cdp neighbors ; show cdp neighbors detail
cdp device-id format hostname           # advertise hostname instead of MAC
show mac address-table                  # 1.4+/2.x; privilege 15 (level 1 → "% Unrecognized command")
show mac address-table interface gi22
show mac address-table vlan 65
show mac address-table address 00:00:5e:00:53:01
show bridge address-table               # firmware ≤1.3 wording, also privilege 15 only
mac address-table aging-time 600
show bridge multicast address-table / show ip igmp snooping
```
Hosts without LLDP/CDP (hypervisors, VMs, IoT) are located via MAC table → port, or by trunk signature (`show interfaces switchport`) when the MAC table is not available at the current privilege level.

Trunk-signature example (level 1 is enough): `show interfaces switchport gi22` reports `Port Mode: Trunk`, native (untagged) 66 and tagged 10, 65. A Proxmox host whose bridge is VLAN-aware with management untagged in 66 and VMs tagged into 10 and 65 is the only candidate with exactly that set; a port with native 66 + tagged 65, 67 matches the host that owns interfaces `eno2.65` and `eno2.67`. Compare against `ip -d link` / `bridge vlan show` on the hosts.

## Port mirroring (SPAN)

```
configure
interface gi24                          # destination/analyzer port
 port monitor gi22                      # both directions; "port monitor gi22 rx|tx"
 port monitor gi23
show ports monitor                      # 1.x; 2.x: "show monitor session"
no port monitor gi22                    # remove
```
Analyzer port stops forwarding normal traffic while mirroring.

## Logging

```
show logging                            # RAM buffer; "show logging file" = flash
logging buffered informational
logging file warnings
logging host 172.16.10.1                  # syslog; "logging host 172.16.10.1 port 514 severity informational"
logging origin-id hostname
logging on / no logging console
clear logging ; clear logging file
```

## Time

```
clock source sntp
sntp unicast client enable
sntp unicast client poll
sntp server 172.16.8.2 poll
sntp source-interface vlan 66
clock timezone CET +1
clock summer-time CEST recurring eu     # check "clock summer-time ?" on 1.x
show clock ; show sntp status ; show sntp configuration
```

## SNMP

```
snmp-server server
snmp-server community <ro-community> ro view Default
snmp-server location "HQ rack" ; snmp-server contact ops@example
snmp-server host 172.16.10.1 traps version 2c <community>
snmp-server user monitor RO-GROUP v3 auth sha <pw> priv aes128 <pw>   # v3 (2.x syntax)
show snmp ; show snmp views ; show snmp users
```
Bind community access with `snmp-server community X ro <ip>` where supported, and restrict the SNMP service via management access-list.

## System

```
show system                             # description, uptime, MAC, temperature/fans (PoE models)
show version                            # firmware, boot version, hardware
show bootvar                            # image-1 / image-2, active + next boot
show cpu utilization ; show cpu input rate
show memory statistics                  # 2.x
show system power ; show env all        # models with sensors
show users ; show sessions
ping 172.16.0.8 ; traceroute 172.16.0.8
```
