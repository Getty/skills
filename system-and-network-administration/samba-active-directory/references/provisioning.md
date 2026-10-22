# DC provisioning, DNS, FSMO, replication

## Provision — full parameters

```bash
mv /etc/samba/smb.conf /etc/samba/smb.conf.initial

# interactive:
samba-tool domain provision --use-rfc2307 --interactive

# non-interactive (reproducible):
samba-tool domain provision \
    --server-role=dc \
    --use-rfc2307 \
    --dns-backend=SAMBA_INTERNAL \
    --realm=AD.EXAMPLE.COM \
    --domain=EXAMPLE \
    --adminpass='…' \
    --option="interfaces=lo eth0" --option="bind interfaces only=yes"
```

| Parameter | Meaning |
|---|---|
| `--realm` | Kerberos realm = AD DNS zone in UPPERCASE. **Cannot be renamed.** No `.local`, never the public TLD, dedicated subdomain. |
| `--domain` | NetBIOS/workgroup, ≤ 15 characters, one word, no dot. |
| `--server-role=dc` | DC role. |
| `--dns-backend` | `SAMBA_INTERNAL` or `BIND9_DLZ`. `NONE`/`BIND9_FLATFILE` unsupported, being removed. |
| `--use-rfc2307` | NIS/POSIX attributes (uidNumber/gidNumber) in the schema. **Always.** Prerequisite for the Unix tab (ADUC) + idmap `ad`. |
| `--function-level` | Initial FL (default 2008 R2). Raising it: see below. |
| `--adminpass` | Domain admin password (must satisfy the policy). |

Post-steps: **copy** `krb5.conf` from Samba (no symlink, `private/` root-only since 4.7), `/etc/resolv.conf` → DC IP + `search`, `systemd-resolved`/`resolvconf` override off, `/etc/hosts` FQDN+short → LAN IP (not 127.0.0.1).

Checks:
```bash
samba-tool domain info 127.0.0.1
samba-tool domain level show
host -t SRV _ldap._tcp.ad.example.com.
host -t SRV _kerberos._udp.ad.example.com.
smbclient -L localhost -N          # sysvol + netlogon
kinit administrator
smbclient //localhost/netlogon -UAdministrator -c 'ls'
```

## DNS backend — `SAMBA_INTERNAL` vs. `BIND9_DLZ`

The DC must serve `ad.example.com`, `_msdcs.ad.example.com`, `DomainDnsZones`, `ForestDnsZones` authoritatively (AD-integrated in LDAP).

| | `SAMBA_INTERNAL` | `BIND9_DLZ` |
|---|---|---|
| What | Own lightweight DNS server. | BIND9 + DLZ module reads the AD LDAP live. |
| Effort | Minimal, works out of the box. `dns forwarder =` for non-AD names. | BIND separately (`named.conf`, `tkey-gssapi-keytab`, keytab permissions, `samba_upgradedns`). |
| Can | A/AAAA/PTR/SRV/CNAME, dynamic updates, GSS-TSIG. | Additionally AXFR, views, split-horizon, DNSSEC, slave/forward zones. |
| Limits | No AXFR/views/DNSSEC/flatfile alongside. | More moving parts, BIND pitfalls. |

Switchable at any time: `samba_upgradedns --dns-backend=…`. **Recommendation:** `SAMBA_INTERNAL` + forwarder, BIND9_DLZ only if there is a real need for zone transfer/DNSSEC/views.

## Kerberos, FSMO, SYSVOL, time

- **KDC:** built-in **Heimdal** (default). MIT KDC only experimental since 4.7. Do nothing.
- **FSMO:** five roles (schema, domain naming, RID, PDC emulator, infrastructure master), initially all on DC1. `samba-tool fsmo show` · `transfer|seize --role=<role>`.
- **SYSVOL:** `\\dc\sysvol` with GPO files/logon scripts. Check/fix NT ACLs with `samba-tool ntacl sysvolcheck` / `sysvolreset`.
- **Time** is Kerberos-critical (tolerance 5 min). PDC emulator = time source. `chrony`/`ntpd` with `ntpsigndsocket /var/lib/samba/ntp_signd/` (signed NTP for Windows). If the network has an internal NTP server, use it as upstream.

## Raising functional level & schema

- Default DFL/FFL = 2008 R2 (sufficient for Win 10/11 incl. NIST 800-171). Schema default since 4.11 = 2012_R2.
- Raising (since 4.19) up to **DFL 2016** (highest supported FL), schema up to version 88 (2019/2022/2025). Higher FLs are officially "work in progress, not production".
- Prerequisite: **Samba ≥ 4.20 on all DCs**, `ad dc functional level = 2016` in `[global]`, then:

```bash
samba-tool domain level show
samba-tool domain schemaupgrade --schema=2019
samba-tool domain functionalprep --function-level=2016
samba-tool domain level raise --domain-level=2016 --forest-level=2016
```

## Multiple DCs, DRS replication, the SYSVOL gap

```bash
samba-tool domain join ad.example.com DC -U administrator \
    --dns-backend=SAMBA_INTERNAL --option='idmap_ldb:use rfc2307 = yes'
samba-tool drs showrepl
samba-tool drs replicate <target-dc> <source-dc> <naming-context>
```

DRS replicates `sam.ldb`/schema/config automatically — **but NOT SYSVOL** (no DFS-R/FRS). Workaround:

```bash
# systemd timer on the leading DC:
rsync -aAX --delete /var/lib/samba/sysvol/ dc2:/var/lib/samba/sysvol/
ssh dc2 samba-tool ntacl sysvolreset      # fix NT ACLs after every sync
```

- `rsync` (unidirectional, `--acls`/xattr mandatory) for a single leading DC.
- `osync`/`unison` (bidirectional) for equal-rights DCs.
- Without `sysvolreset`, GPOs do not apply after the sync.
- **Irrelevant with one DC.** A second DC is the recommended failover protection.

## Backup / restore

```bash
samba-tool domain backup offline --targetdir=/srv/dcbackup
samba-tool domain backup online  --server=dc1 -U administrator --targetdir=…
samba-tool domain backup restore --backup-file=… --newservername=dc-new --targetdir=…
```

## Can / cannot (vs. Windows Server AD)

| Feature | Samba AD |
|---|---|
| LDAP/Kerberos/NTLM, DNS, GPO storage, RSAT, FSMO, multi-DC/DRS, RODC (4.7+), RFC2307, PSO (4.9+), backup/restore | ✅ |
| **SYSVOL replication (DFS-R/FRS)** | ❌ (rsync/osync) |
| **Multiple domains / child domains per forest** | ❌ (single domain only) |
| **AD-CS / PKI (auto-enrollment)** | ❌ (external PKI: step-ca/FreeIPA/MS-CA) |
| Exchange schema | ⚠️ fragile/unsupported |
| Trusts (external/forest, since 4.8) | ⚠️ without SID filtering |
| FL > 2016 | ❌ |
| Entra ID (`himmelblaud`, 4.22) | ⚠️ experimental |

## Versions & CVEs

- **Samba 4.22.0** (06.03.2025): SMB3 directory leases, Netlogon ping over LDAP/LDAPS, experimental Himmelblaud. Samba maintains the three most recent series (~18 months). Before rollout, check the current stable series on `samba.org` (09/2026 possibly already 4.24/4.25).
- **Debian 12/Bookworm = 4.17** (upstream dead, security backports only; `bookworm-backports` = 4.22.6). **Debian 13/Trixie = 4.22.x.** Run a DC only on a maintained series (Debian 13, backports or SAMBA+/SerNet). **Never a DC on 4.17.**
- CVEs: **CVE-2025-10230** (WINS hook command injection, CVSS 10.0, remote root) only with `wins support=yes`+`wins hook` → do not enable WINS; **CVE-2020-1472 Zerologon** (`server schannel=yes` default since 4.8); **CVE-2016-2118 Badlock**. General stance: maintained series, SMB1 off, WINS off, LDAPS/TLS on, RPC signing on. Advisories: `samba.org/samba/history/security.html`.
