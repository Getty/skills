# Proxmox VE — Versions and apt repositories

Read when running `apt update` or an upgrade on a PVE or PBS host, setting up or fixing
the apt repositories (`apt update` fails with 401), or upgrading PVE 8 → 9.

| PVE | Base | PBS |
|---|---|---|
| PVE 8 | Debian 12 **bookworm** | PBS 3 |
| PVE 9 | Debian 13 **trixie** | PBS 4 |

From Debian 13/PVE 9 on, the **deb822** format (`.sources`) is the default; apt complains
about the old single-line format (`.list`) — `apt modernize-sources` migrates it. Without
a subscription: **disable the enterprise repo, add the no-subscription repo.**

**PVE 9 (trixie), setting up no-subscription:**
```
# Disable enterprise: add Enabled: no (or delete the file)
/etc/apt/sources.list.d/pve-enterprise.sources   # + line:  Enabled: no
/etc/apt/sources.list.d/ceph.sources             # same, if no Ceph subscription

# Create new: /etc/apt/sources.list.d/proxmox.sources
Types: deb
URIs: http://download.proxmox.com/debian/pve
Suites: trixie
Components: pve-no-subscription
Signed-By: /usr/share/keyrings/proxmox-archive-keyring.gpg
```
Then `apt update && apt full-upgrade`. The Debian base lives in
`/etc/apt/sources.list.d/debian.sources`. PBS is analogous with URI `…/debian/pbs`,
component `pbs-no-subscription`.

**PVE 8 (bookworm), single-line:** `/etc/apt/sources.list.d/pve-no-subscription.list` →
`deb http://download.proxmox.com/debian/pve bookworm pve-no-subscription`; comment out the
enterprise `.list`.

**Upgrade 8 → 9 (in-place, short path):** update to the last 8.4.x → `pve8to9 --full` and
work through **all** findings → change `bookworm` → `trixie` in all repos (or
`apt modernize-sources` + adjust the suite) → `apt update && apt dist-upgrade` → reboot →
run `pve8to9` again. In a cluster, one node at a time, migrate the VMs away first. Always
work via **console/IPMI**, not SSH (a network restart kills the session). The subscription
"nag" dialog in the web UI is purely cosmetic.

## Common mistakes

- **Enterprise repo active without a subscription** → `apt update` aborts with 401.
  Disable the enterprise repo (`.sources`/`.list`), add no-subscription.
- **Single-line repos on trixie** → apt warns; `apt modernize-sources`.
