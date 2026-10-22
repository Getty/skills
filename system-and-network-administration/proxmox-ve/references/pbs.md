# Proxmox Backup Server (PBS)

A separate appliance (PBS 4 = Debian 13 trixie). Managed via `proxmox-backup-manager` (server) and `proxmox-backup-client` (client side/restore). Configs under `/etc/proxmox-backup/`. Backup is based on deduplicated **chunks**: `prune` only deletes snapshot metadata, only **garbage collection** frees the space of unreferenced chunks.

## Creating a datastore

A datastore is a directory (ideally its own ZFS dataset) holding a chunk store.
```
proxmox-backup-manager datastore create store1 /mnt/datastore/store1
proxmox-backup-manager datastore list
proxmox-backup-manager datastore show store1
```
Set the GC/prune schedule directly on the datastore (calendar-event format as in systemd, e.g. `daily`, `sat 03:00`):
```
proxmox-backup-manager datastore update store1 --gc-schedule 'sat 03:00'
proxmox-backup-manager datastore update store1 --delete gc-schedule   # disable
```
Config: `/etc/proxmox-backup/datastore.cfg`. **Maintenance mode** for work on the storage: `--maintenance-mode read-only` or `offline` (running operations may finish).

## Creating backups

**From PVE** (PBS attached as storage, see SKILL): via GUI backup jobs or `vzdump`:
```
vzdump 100 --storage pbs-store --mode snapshot --notes-template '{{guestname}}'
```
`--mode snapshot` (uninterrupted, default) vs. `suspend` vs. `stop`. A recurring job lives in `/etc/pve/jobs.cfg` (GUI: Datacenter → Backup).

**Any Linux host** (file level) with `proxmox-backup-client`:
```
export PBS_REPOSITORY='backup@pbs@pbs.host:store1'
export PBS_PASSWORD='…'          # or --repository / prompt
proxmox-backup-client backup root.pxar:/ --ns prod
proxmox-backup-client snapshot list
```

## Remote + sync job (off-site — core of the 3-2-1 rule)

A **remote** is a second PBS. Get the fingerprint there: `proxmox-backup-manager cert info | grep Fingerprint`.
```
proxmox-backup-manager remote create pbs2 \
  --host pbs2.example --auth-id sync@pam --password 'SECRET' \
  --fingerprint 64:d3:ff:3a:...:ab:fe
proxmox-backup-manager remote list        # -> /etc/proxmox-backup/remote.cfg
```
A **sync job** pulls a remote datastore into a local one (`/etc/proxmox-backup/sync.cfg`):
```
proxmox-backup-manager sync-job create pbs2-local \
  --remote pbs2 --remote-store store1 --store store1 --schedule 'Wed 02:30'
proxmox-backup-manager sync-job update pbs2-local --remove-vanished true --group-filter type:vm
proxmox-backup-manager sync-job run  pbs2-local     # test immediately
proxmox-backup-manager sync-job list
```
- **Pull** (default) fetches from the remote; **push** (`--sync-direction push`) pushes to a less trusted target (separate remote user per push job, otherwise jobs overwrite each other). `--verified-only`/`--encrypted-only` restrict to verified/encrypted snapshots.
- Permissions for a pull job: `Remote.Read` on `/remote/{remote}/{store}` **and** ≥ `Datastore.Backup` on the local target; `--remove-vanished` additionally needs `Datastore.Prune`.
- Cap bandwidth: `--rate-in 20MiB` (pull) / `--rate-out` (push).

## Prune / GC / Verify

**Prune** (retention) — order of the options: `keep-last` → `keep-hourly` → `keep-daily` → `keep-weekly` → `keep-monthly` → `keep-yearly`. As a job (`/etc/proxmox-backup/prune.cfg`):
```
proxmox-backup-manager prune-job create pj-store1 --store store1 \
  --schedule 'daily' --keep-daily 14 --keep-weekly 8 --keep-monthly 12
```
**Garbage collection** frees the space (unreferenced chunks, after a grace period of ~24h because of `relatime`). Schedule on the datastore (see above); manually:
```
proxmox-backup-manager garbage-collection start  store1
proxmox-backup-manager garbage-collection status store1
```
**Verify** checks chunk integrity against bit rot. Manually or as a verify job:
```
proxmox-backup-manager verify store1 --ignore-verified true --outdated-after 30
```
Recommended cadence: prune daily, GC weekly, verify new backups frequently + a monthly full re-verify.

## Restore

- **VM/CT from PVE:** `qmrestore <backup-volume> <vmid>` or `pct restore <vmid> <volume>`; volume ID via `pvesm list pbs-store` or the GUI. Single files in the GUI via "File Restore".
- **File level via client:**
  ```
  proxmox-backup-client snapshot list
  proxmox-backup-client restore <snapshot> root.pxar /target/path
  proxmox-backup-client mount   <snapshot> root.pxar /mnt   # FUSE
  ```
- **Disaster (without a running PBS server):** a statically linked `proxmox-backup-client` can read directly from the chunk store — keep it ready for bare-metal recovery.

## Token & ACL

Create user/token, assign permissions by path + role:
```
proxmox-backup-manager user create backup@pbs
proxmox-backup-manager user generate-token backup@pbs bkp   # prints the secret ONCE
proxmox-backup-manager acl update /datastore/store1 DatastoreBackup --auth-id 'backup@pbs!bkp'
proxmox-backup-manager acl update /datastore/store1 DatastoreAudit  --auth-id 'backup@pbs!bkp'
```
Important roles: `DatastoreAudit` (see/list), `DatastoreBackup` (write + read own), `DatastoreReader`, `DatastorePowerUser`, `DatastoreAdmin`, `RemoteSyncOperator`.

**Typical trap:** a token has `DatastoreBackup` but **not** `DatastoreAudit` → backups run, but the datastore list in the API/UI comes back **empty** (no audit permission = nothing visible). Set both roles. Path permissions are hierarchical: `/datastore` applies to all, `/datastore/store1/ns1` only to one namespace.
