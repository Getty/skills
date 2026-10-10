# Storage Box and Storage Share

Reviewed: 2026-10-04. Read for file backups, Borg/restic, remote file access or managed Nextcloud. Use [Object Storage](object-storage.md) for S3 and [database recovery](database-recovery.md) for application consistency.

## Choose the correct service and control plane

Storage Box provides remote file storage for tools and protocols. Storage Share provides a Nextcloud collaboration service, including browser/client access, users, groups and sharing. Choose based on the consuming workflow rather than capacity alone. [Product comparison](https://docs.hetzner.com/storage/storage-box/faq/storage-box-vs-storage-share/)

Manage stand-alone Storage Boxes through Hetzner Console and the Hetzner API. Robot Web Service stopped supporting them in July 2025. The free BX10 still bound to certain dedicated servers is the documented exception. Do not apply legacy Robot automation to a migrated box. Password authentication cannot be disabled merely by provisioning an SSH key. [Storage Box FAQ](https://docs.hetzner.com/storage/storage-box/faq/faq/)

## Storage Box access and isolation

The main user sees all directories; subaccounts see their assigned subdirectory and share the box's capacity. A read-only subaccount cannot upload/delete. Use each subaccount's own username, hostname and key file. Port 22 provides SFTP/SCP without interactive access; optional SSH support enables port 23. Other interfaces include FTP/FTPS, SMB and WebDAV. Public IPs can change, so use the service hostname. [Overview](https://docs.hetzner.com/storage/storage-box/general/)

Port 23 provides a restricted command environment, not a general Linux server: no remote pipelines, redirects or uploaded scripts. Run schedules and orchestration on your own machine. Use `help` to inspect available commands. Enabling “External Reachability” permits access from outside Hetzner's network; it does not attach the box to a customer-private Cloud Network. A private-only VM still needs a viable route to its endpoint. [SSH access](https://docs.hetzner.com/storage/storage-box/access/access-ssh-rsync-borg/)

Port 22 and port 23 require different public-key formats: RFC4716 and OpenSSH respectively. Preserve existing keys when adding another; blindly uploading `authorized_keys` with SCP can replace them. Verify the service host key using Hetzner's published fingerprint list. [SSH keys](https://docs.hetzner.com/storage/storage-box/ssh-keys/add-ssh-keys/), [fingerprints](https://docs.hetzner.com/storage/storage-box/general/)

Give each backup source a distinct subaccount/repository where practical. Keep the main password and management API token off the backed-up workload. Confirm what the source can overwrite or delete, not only whether authentication succeeds.

## Use backup tools through supported interfaces

Borg supports version selection through `--remote-path`; choose a compatible advertised server version instead of assuming the default matches a newly installed client. Restic supports the SFTP backend; Rclone's SFTP backend is also supported. Direct rsync cannot preserve arbitrary ownership IDs and is a poor substitute for a whole-system backup format. Check current concurrent-connection limits before raising parallelism. [SSH, Borg, rsync, Rclone and restic](https://docs.hetzner.com/storage/storage-box/access/access-ssh-rsync-borg/)

For restic, use a relative repository path inside the account and keep its encryption password separately from SSH credentials. This read-only example assumes the repository already exists and keys/password handling are configured:

```bash
restic -r 'sftp://uXXXXX-sub1@uXXXXX-sub1.your-storagebox.de:23/backups' snapshots
```

In restic's URL syntax one slash introduces a home-relative path; an absolute path needs another slash. Do not assume SFTP expands `~`. [Restic SFTP documentation](https://restic.readthedocs.io/en/stable/030_preparing_a_new_repo.html#sftp)

Borg append-only mode can preserve previous repository segments against a restricted Borg client, but it does not constrain unrestricted SFTP or shell deletion. Enforce the restricted `borg serve` entry point, isolate other credentials, and inspect integrity before trusted maintenance/compaction. Never describe append-only as provider-enforced immutability. [Borg append-only notes](https://borgbackup.readthedocs.io/en/stable/usage/notes.html#append-only-mode-forbid-compaction)

## Understand Storage Box snapshots

Snapshots live on the same Storage Box and consume its capacity as data changes. They are recovery points for that box, not independent full backups or a source for cloning another box. Restoring an older snapshot removes subsequent data **and newer snapshots**. Prefer downloading selected files from the read-only snapshot directory when a full rollback is unnecessary; port 23 exposes it under `/home/.zfs/snapshot`. Snapshot visibility and management privileges are separate from ordinary file writes. [Snapshot behavior](https://docs.hetzner.com/storage/storage-box/snapshots/)

The underlying RAID resides on a single host. Retain another independently recoverable copy when host loss or account compromise must be covered. Keep enough free capacity for the backup tool's temporary files and retained snapshots; deleting current files may not reclaim space while snapshots reference them. [Storage Box architecture](https://docs.hetzner.com/storage/storage-box/general/)

## Operate Storage Share as managed Nextcloud

Hetzner performs Nextcloud platform updates; the customer cannot run its own platform upgrade. Supported OCC operations are exposed through konsoleH, with unavailable operations handled through support. Treat its application database and filesystem as a managed service boundary. [Updates](https://docs.hetzner.com/storage/storage-share/faq/upgrade/), [OCC commands](https://docs.hetzner.com/storage/storage-share/configuration/occ-commands/)

Additional Nextcloud apps are possible but are not covered by Hetzner technical support. Built-in OnlyOffice/Collabora processing is not supported; an external document server is required for those integrations. [Additional apps](https://docs.hetzner.com/storage/storage-share/faq/additional-apps/)

Automatic backups run several times daily: a database dump and ZFS snapshot are transferred to another host, with seven days retained. Recovery restores the full instance, causes downtime and resets subsequent backup history; it is not provider-level single-file restore. Hetzner documents that a full restore may take one to two days depending on backup size; measure the actual recovery against the required RTO. Export an independent copy for longer retention and test the intended user-facing recovery workflow. [Storage Share backup/restore](https://docs.hetzner.com/storage/storage-share/faq/backup-snapshot/)

For failures, first identify the layer: DNS/reachability, enabled protocol, authentication/key format, subaccount path, capacity, concurrency or application state. For Storage Share, inspect service status and OCC `status` before changing maintenance mode during a provider update. Preserve error timestamps and sanitized reproduction steps for support.
