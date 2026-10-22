# File server (domain member), ACLs, VFS, idmap, clients

**Do not use the DC as a file server.** On the DC: SMB signing is enforced, `acl_xattr` is forced (no POSIX ACLs), the member `idmap config` lines have no effect, different upgrade cycles. If unavoidable, run a second Samba instance/VM as a member on the DC host.

## `smb.conf` — member file server, complete

```ini
[global]
    security = ADS
    workgroup = EXAMPLE
    realm = AD.EXAMPLE.COM

    idmap config * : backend = tdb
    idmap config * : range = 3000-7999
    idmap config EXAMPLE : backend = rid
    idmap config EXAMPLE : range = 10000-999999
    template shell = /bin/bash
    template homedir = /home/%U

    winbind use default domain = yes
    winbind refresh tickets = yes
    vfs objects = acl_xattr
    map acl inherit = yes
    store dos attributes = yes

[data]
    path = /srv/samba/data
    read only = no
    vfs objects = acl_xattr shadow_copy2 recycle
```

## ACLs — POSIX vs. Windows NT

- **POSIX ACLs** (`acltype=posixacl`): classic Unix ACLs, need a filesystem with `acl`+`user_xattr` (e.g. an ext4 RAID volume: mount with `acl,user_xattr`).
- **`vfs_acl_xattr`**: stores the **full Windows NT ACL** in xattr `security.NTACL` → permissions 1:1 from Explorer (inheritance, owner, complex ACEs). Standard for "real" Windows behaviour, needs `user_xattr`.
- Combinable; for Windows-centric administration `acl_xattr` is the standard.

## VFS modules (order matters)

| Module | Purpose |
|---|---|
| `shadow_copy2` | "Previous Versions" tab — maps snapshots (ZFS/LVM/btrfs/rsync) to VSS, self-service restore. |
| `fruit` | macOS (Time Machine, AAPL, resource forks, `.DS_Store`). Note: `fruit:posix_rename` removed in 4.22. |
| `recycle` | Server-side recycle bin (`.recycle` directory). |
| `full_audit` | Access auditing → syslog (who opens/deletes/renames) for SIEM. |
| `acl_xattr` | Windows ACLs in xattr. |
| `catia`, `streams_xattr` | Character mapping / NTFS alternate data streams. |

**Pitfall:** `vfs objects = recycle` alone switches off the defaults `dfs_samba4 acl_xattr` → explicitly `vfs objects = dfs_samba4 acl_xattr recycle`.

## Protocol & performance

- **SMB3** standard; **SMB1 off since 4.11** (minimum SMB2). Re-enableable only with `client/server min protocol = NT1` — don't (ransomware vector).
- **SMB3 multichannel** (multiple streams/NICs, "experimental" but widespread), **directory leases** (4.22, fewer SMB requests), **CTDB** (cluster HA, overkill for a small setup).
- `shadow_copy2` needs real snapshots — ext4/LVM without native snapshots → LVM-thin or rsync snapshot directories.

## idmap backends (on members, never on the DC)

| Backend | How | When |
|---|---|---|
| `rid` | UID/GID algorithmically from RID + range offset, deterministic, identical on every member, no AD write access. | **Default for a small setup.** |
| `autorid` | like `rid`, ranges assigned automatically per domain. | Multi-domain/trusts. |
| `ad` | UID/GID **read** from RFC2307 (`uidNumber`/`gidNumber`) in AD, maintained manually, needs `--use-rfc2307`. | IDs exactly identical everywhere + control shells/home in AD (NFS interop). |

Range convention: `*` e.g. `3000-7999` (always `tdb`, well-known SIDs), `EXAMPLE` `10000-999999`, trusts from `1000000`. **Never overlap ranges.** The 3000000-range IDs on a DC are **not** RFC2307 values and not transferable to members.

## Home shares, roaming, redirected folders, FSLogix

- **Home shares:** `[homes]` or `[home] path = /srv/samba/home/%U`; on the user `homeDirectory`/`homeDrive` (ADUC/`samba-tool`). Simplest step with the greatest everyday value.
- **Roaming profiles:** `[profiles]` (`profile path = \\fileserver\profiles\%U`), user attribute `profilePath`. Versioning `.V6` per Windows build. Fragile (version conflicts).
- **Redirected folders:** via GPO (User Config → Folder Redirection) Desktop/Documents/AppData to UNC — more robust than full roaming profiles.
- **FSLogix profile container:** whole profile as VHDX on an SMB share (any share, **Samba too**), mounted at login, solves the roaming problems. Agent is free; shines with RDS/VDI.

## Joining clients

**Windows** (Pro/Enterprise — Home cannot join): client DNS to the DC (via DHCP), join the domain. GPOs (incl. software deployment) are processed by the **client**.

**Linux:**
```bash
net ads join -U administrator          # winbind stack
realm join ad.example.com -U administrator    # SSSD (realmd default)
```

- **winbind** (`winbindd`): resolves SIDs ↔ UIDs/GIDs, provides domain users via NSS (`passwd: files winbind`) + PAM (`pam_winbind`). **Mandatory if the host is also a Samba file server** (SMB needs the mappings).
- **SSSD:** strong for pure login/identity (caching, offline login, HBAC). More convenient for pure login hosts (SSH).
- **Rule of thumb:** file server → winbind; pure login host → SSSD.

## GPO administration (headless)

```bash
samba-tool gpo listall / list <user> / show <GUID>
samba-tool gpo create "Software deployment" -U Administrator
samba-tool gpo backup  <GUID> --tmpdir=/srv/gpo-backup
samba-tool gpo restore "Name" /srv/gpo-backup/… -U Administrator
samba-tool gpo admxload -U Administrator --admx-dir=…   # ADMX Central Store
```

The CLI can save/link; **editing** the policy contents (Software Installation, Folder Redirection, scripts) runs **only** via GPMC/RSAT on a Windows client. ADMX Central Store: `\\ad.example.com\SYSVOL\ad.example.com\Policies\PolicyDefinitions`. Linux clients do not apply GPOs natively (`samba-gpupdate` covers only a VGP part).
