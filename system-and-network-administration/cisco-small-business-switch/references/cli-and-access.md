# Access, users, SSH, system mode, IP, saving config

## Ways in

| Path | Notes |
|---|---|
| Console RJ45/mini-USB, 115200 8N1 | always works; needed for password recovery and system-mode changes |
| Web UI `https://<ip>` | default `cisco`/`cisco`, forced password change on first login; every setting exists there |
| SSH (`ip ssh server`) | in-band `User Name:`/`Password:` prompt after the SSH channel opens; legacy algorithms |
| Telnet (`ip telnet server`) | disable it |
| SNMP | v1/v2c/v3, see monitoring reference |

## Users and privilege

```
configure
username admin password <pw> privilege 15         # 1.4: "username NAME password PW privilege 15"; 1.3 order may be "username NAME privilege 15 password PW"
enable password level 15 <pw>                     # for "enable" from a level-1 user
passwords aging 0                                 # stop the "password exceeded maximum lifetime" nag
passwords complexity enable / no passwords complexity enable
show users accounts
show passwords configuration
```
Level 1 = read-only (`show` for most things; `show running-config`, MAC table and some `show` verbs are level 15 → "% Unrecognized command" or "Insufficient privilege"). Level 15 = full. `show privilege` shows the current level.

## SSH server

```
configure
ip ssh server
crypto key generate rsa                           # host key (1024-bit on 1.x)
ip ssh password-auth                              # allow password login
ip ssh pubkey-auth                                # allow key login
crypto key pubkey-chain ssh
 user-key admin rsa
  key-string
   <paste openssh public key lines>
  exit
 exit
no ip telnet server
show ip ssh
show crypto key pubkey-chain ssh
```
Old firmware (1.x) cannot restrict algorithms; the server offers `ssh-rsa`/`ssh-dss` host keys, `diffie-hellman-group1-sha1`/`group-exchange-sha1` KEX, CBC ciphers and `hmac-sha1`. Client side:
```
ssh -o KexAlgorithms=+diffie-hellman-group-exchange-sha1,diffie-hellman-group1-sha1 \
    -o HostKeyAlgorithms=+ssh-rsa,ssh-dss -o PubkeyAcceptedAlgorithms=+ssh-rsa \
    -o Ciphers=+aes128-cbc,3des-cbc,aes256-cbc -o MACs=+hmac-sha1 -o PubkeyAuthentication=no \
    -o PreferredAuthentications=password,keyboard-interactive ops@172.16.0.99
```
The username given to ssh may be ignored — the switch asks again. A pexpect driver that handles the in-band prompt and `terminal datadump`: skill `network-device-ssh-cli` (`scripts/netcli.py --profile sx300`).

## Management access lists (lockout-prone)

```
management access-list ADMIN-ONLY
 permit ip-source 172.16.0.0 mask 255.255.255.0 service ssh
 permit ip-source 172.16.0.0 mask 255.255.255.0 service https
 deny
management access-class ADMIN-ONLY
show management access-list ; show management access-class
```
Apply from console; `no management access-class` removes it.

## System mode, IP, gateway

```
show system mode                      # 1.4+/2.x: "switch" = L2 (default), "router" = L3; 1.3.x: "% Wrong number of parameters" → web UI Administration → System Mode
set system mode router                # REBOOTS AND ERASES STARTUP-CONFIG — save a backup first
interface vlan 66
 ip address 172.16.0.99 255.255.255.0
 ! or: ip address dhcp
exit
ip default-gateway 172.16.0.8            # L2 mode
ip route 0.0.0.0 0.0.0.0 172.16.0.8      # L3 mode (default gateway becomes a route)
show ip interface ; show ip route ; show arp
```
Only one IP interface in L2 mode on very old firmware (1.1/1.2); 1.3+ allows several. The management VLAN must reach the uplink port (tagged or native) or you cannot log in.

## Save, backup, restore, reset

```
copy running-config startup-config      # or: write   (answer Y)
copy running-config backup-config       # local second copy
copy startup-config tftp://172.16.10.1/sw-startup.cfg
copy running-config scp://user@172.16.10.1/sw.cfg   # 1.4+/2.x
copy tftp://172.16.10.1/sw-startup.cfg startup-config   # restore, then reload
show startup-config ; show running-config ; show backup-config
delete startup-config                   # + reload = factory defaults (keeps firmware)
reload ; reload in 10 ; reload cancel   # "reload in" exists on 1.4+/2.x
```
Physical reset: hold Reset ≥10 s (LEDs blink) → factory defaults. Password recovery: console, interrupt boot (`Esc`/menu), "Password Recovery Procedure" entry which clears passwords without wiping config.

## Misc CLI

`hostname core-sw`, `clock timezone CET +1`, `clock summer-time CEST recurring eu` (syntax varies: `clock summer-time web …` on 1.x; check `clock summer-time ?`), `terminal datadump`, `terminal width 0`, `show users`, `show sessions`, `exit`/`logout`, `?` and Tab work as in IOS.
