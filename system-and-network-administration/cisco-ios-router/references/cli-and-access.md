# CLI access, SSH, users, config management, upgrades

## SSH v2 server (minimum)

```
hostname rtr-b
ip domain-name example.lan
crypto key generate rsa modulus 2048 label SSH-KEY     # 4096 if the box is fast enough
ip ssh rsa keypair-name SSH-KEY
ip ssh version 2
ip ssh time-out 60
ip ssh authentication-retries 3
ip ssh logging events
! 15.5(2)+ : restrict algorithms (check with "ip ssh server algorithm ?")
ip ssh server algorithm encryption aes256-ctr aes192-ctr aes128-ctr
ip ssh server algorithm mac hmac-sha2-256 hmac-sha1
ip ssh server algorithm kex diffie-hellman-group14-sha1      # newer: ecdh-sha2-nistp256, group-exchange-sha256
username admin privilege 15 secret <pw>                       # "secret" = hashed; never "password"
username admin algorithm-type scrypt secret <pw>              # 15.3+ stronger hash
enable secret <pw>
service password-encryption                                    # obfuscates type-7 leftovers only
ip access-list standard LAN-INTERN
 permit 172.16.0.0 0.0.0.255
 permit 172.16.8.0 0.0.3.255
line vty 0 4
 access-class LAN-INTERN in
 login local
 transport input ssh
 exec-timeout 10 0
line con 0
 login local
 exec-timeout 15 0
 logging synchronous
```
Verify: `show ip ssh` (version, algorithms), `show ssh` (sessions), `show users`, `show crypto key mypubkey rsa`. Public-key login: `ip ssh pubkey-chain` → `username admin` → `key-string` (paste base64 in ≤254-char chunks) → `exit`; or `key-hash ssh-rsa <md5>`.

`aaa new-model` switches all lines to AAA method lists (`aaa authentication login default local`, `aaa authorization exec default local`); without it `login local` on the lines is enough.

## Connecting from a modern client

Old IOS (≤15.x) offers `ssh-rsa` host keys, `diffie-hellman-group-exchange-sha1`/`group14-sha1` KEX and CBC ciphers. OpenSSH ≥ 8.8 refuses `ssh-rsa` signatures by default, so:
```
ssh -o KexAlgorithms=+diffie-hellman-group-exchange-sha1,diffie-hellman-group14-sha1 \
    -o HostKeyAlgorithms=+ssh-rsa -o PubkeyAcceptedAlgorithms=+ssh-rsa \
    -o Ciphers=+aes128-cbc,aes256-cbc,3des-cbc -o MACs=+hmac-sha1 admin@172.16.0.5
```
Put it in `~/.ssh/config` as a `Host` stanza. Classic IOS ignores a command given on the ssh line (`ssh host "show version"` just opens a shell) — drive it interactively; see skill `network-device-ssh-cli` for a pexpect driver and the full legacy-algorithm table.

## Config files, archive, rollback

```
show running-config | section …      show startup-config       show archive config differences
write memory                          copy running-config startup-config
copy running-config tftp://172.16.10.1/rtr-b.cfg     copy running-config scp://user@172.16.10.1/rtr-b.cfg
copy tftp://172.16.10.1/rtr-b.cfg running-config     # merges! (does not replace)
configure replace tftp://172.16.10.1/rtr-b.cfg force # replaces atomically (diff-based)
archive
 path flash:archive/rtr-b
 maximum 14
 write-memory                       # snapshot on every write mem
 time-period 1440                   # daily
show archive
configure replace flash:archive/rtr-b-3 force  # rollback to snapshot 3
show archive config differences flash:archive/rtr-b-3 system:running-config
reload in 10 / reload at 03:00 / reload cancel     # safety net for remote work; "reload" alone reboots now
```
`show archive log config all` (needs `log config` + `logging enable` under `archive`) records who changed what.

## Files and images

```
dir flash:            show flash:          delete flash:old.bin       verify /md5 flash:c900-universalk9-mz.SPA.159-3.M9.bin
copy tftp: flash:     copy scp://user@host/img.bin flash:     copy usbflash0:img.bin flash:
boot system flash:c900-universalk9-mz.SPA.159-3.M9.bin      # first matching line wins; "no boot system" clears
show version | include register                             # 0x2102 normal, 0x2142 ignore startup-config (password recovery), 0x0 ROMMON
config-register 0x2102
```
Upgrade sequence: backup config + image → copy new image to flash → `verify /md5` → `boot system flash:<new>` (and keep old as second line) → `write memory` → `reload` → `show version`. ROMMON (`rommon 1 >`): `dir flash:`, `boot flash:<img>`, `confreg 0x2102`, `tftpdnld` with `IP_ADDRESS=… TFTP_SERVER=… TFTP_FILE=…` set first, `reset`. Password recovery: break into ROMMON, `confreg 0x2142`, `reset`, then `copy startup-config running-config`, set new secrets, `config-register 0x2102`, `write memory`.

## Useful show commands

```
show version                     show inventory                  show environment all / show env
show ip interface brief          show interfaces Gi4             show interfaces status (switch ports)
show run interface Vlan10        show ip route                   show ip arp
show mac address-table           show cdp neighbors detail       show lldp neighbors detail
show logging                     show clock                      show ntp status / associations
show processes cpu sorted | exclude 0.00   show memory statistics   show tech-support (huge)
show controllers Gi4             show interfaces counters errors  show ip traffic
debug ip packet detail <acl>     ! only with an ACL and "undebug all" ready; console floods kill small routers
```
