# Export, import, backup, reset, REST API, upgrades

## Text export / import (`.rsc`)

```
/export file=full-2026-09-08                     # compact by default, secrets hidden
/export show-sensitive terse file=full-secrets   # includes keys/passwords, one command per line
/ip/firewall/export file=fw                      # per-menu
/export path=/ip/firewall,!/ip/firewall/nat      # include/exclude menus (v7.11+)
/ip/firewall/address-list/export where list=mgmt # partial (v7.13+)
/file/print ; then fetch with scp: scp user@router:full-2026-09-08.rsc .
/import file-name=fw.rsc verbose=yes dry-run=yes # syntax check without applying (v7.16+)
/import file-name=fw.rsc
```
Not in exports: user passwords, user SSH keys, certificates (export via `/certificate/export-certificate`), Dude/User-Manager DBs. Imports on a fresh device usually need interface renames (`set [find default-name=ether1] name=…`) checked first. Files named `*.auto.rsc` uploaded via FTP/SFTP execute automatically.

## Binary backup / restore

```
/system/backup/save name=edge-rtr-2026-09-08 password=… encryption=aes-sha256   # full clone incl. users/keys
/system/backup/load name=edge-rtr-2026-09-08 password=…                          # reboots
```
Backups are for the *same device model/version*; use exports to move config between models.

## Reset

```
/system/reset-configuration keep-users=yes no-defaults=yes skip-backup=no run-after-reset=my.rsc
```
Physical: hold reset 5 s at power-on (LED blink) for defaults, ~15 s for CAPs mode, ~20 s+ for Netinstall/etherboot. Netinstall reinstalls RouterOS over ether1 from a PC on the same L2.

## REST API (RouterOS ≥ 7.1)

Enable `www-ssl` with a certificate (or `www` for tests only) and use HTTP basic auth of a user with `rest-api` policy.
```
/certificate/add name=ca common-name=ca key-usage=key-cert-sign,crl-sign ; /certificate/sign ca
/certificate/add name=web common-name=edge-rtr.example.lan ; /certificate/sign web ca=ca
/ip/service/set www-ssl certificate=web disabled=no address=172.16.0.0/24
```
```
curl -k -u ops:PW https://172.16.0.8/rest/system/resource
curl -k -u ops:PW "https://172.16.0.8/rest/ip/address?interface=lan"           # GET = print, query params filter
curl -k -u ops:PW "https://172.16.0.8/rest/ip/route?.proplist=dst-address,gateway,distance,active"
curl -k -u ops:PW -X PUT   https://172.16.0.8/rest/ip/dns/static -H content-type:application/json -d '{"name":"node1.example.lan","address":"172.16.10.5"}'
curl -k -u ops:PW -X PATCH https://172.16.0.8/rest/ip/dns/static/*1A -H content-type:application/json -d '{"comment":"k8s cp"}'
curl -k -u ops:PW -X DELETE https://172.16.0.8/rest/ip/dns/static/*1A
curl -k -u ops:PW -X POST  https://172.16.0.8/rest/ip/firewall/filter/print -H content-type:application/json \
     -d '{".proplist":["chain","action","comment"],".query":["chain=input"]}'
curl -k -u ops:PW -X POST  https://172.16.0.8/rest/ping -H content-type:application/json -d '{"address":"1.1.1.1","count":"3"}'
curl -k -u ops:PW -X POST  https://172.16.0.8/rest/execute -H content-type:application/json -d '{"script":"/log/info \"hello\""}'
```
- Verbs: GET=print, PUT=add, PATCH=set, DELETE=remove, POST=any command (`…/print`, `…/move`, `/rest/export`). Ids are `*hex` from `.id`.
- All values come back as strings. 60 s hard timeout per call: give `count=`/`duration=` to long-running tools; no `monitor` streaming (use `once`).
- Errors are JSON `{"error":…, "message":…, "detail":…}` with HTTP ≥ 400.
- Legacy binary API on 8728/8729 (`api`, `api-ssl` services) is what `librouteros`/`routeros-api` libraries use.

## Upgrades

```
/system/package/update/check-for-updates ; /system/package/update/print
/system/package/update/set channel=long-term|stable ; /system/package/update/install   # reboots
/system/routerboard/print ; /system/routerboard/upgrade ; /system/reboot               # firmware (RouterBOOT) after RouterOS
/system/history/print ; /system/package/print                                            # verify afterwards
```
Take an export + backup before; long-term channel for production routers. A failed upgrade boots the previous package on RouterBOARDs; CHR needs a VM snapshot.
