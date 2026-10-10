# Application-consistent backup and recovery

Reviewed: 2026-10-04. Read for self-managed databases, Forgejo, registries and stateful applications on Hetzner. This is engineering guidance using application/vendor requirements; it does not describe a managed database service. Load [Volumes and images](volumes-backups-snapshots.md) when mapping protection to Cloud disks.

## Define a recoverable unit

Write down the allowed data loss (RPO), allowed outage (RTO), retention, recovery location and operator. Inventory all required state: database, repository/object files, queues, configuration, encryption keys, identity-provider dependencies and infrastructure definition. For each item, name its backup method and recovery timestamp. A timestamped archive with missing secrets or an incompatible application binary is not a usable recovery plan.

Plan the network path in both directions. A private database can be backed up by a host on its private network, while that host sends an encrypted repository to storage through egress. Recovery needs the reverse path, enough disk space, working DNS, credentials and application packages even if production is unavailable.

## Choose a PostgreSQL method

| Need | Method | Requirement |
|---|---|---|
| Portable backup of a database or selected objects | Logical dump with `pg_dump` | Include cluster-global roles/tablespaces separately; rehearse restore time. |
| Whole-cluster physical recovery | Consistent physical/base backup | Keep compatible PostgreSQL binaries/extensions and every tablespace. |
| Restore near a selected transaction time | Physical base backup plus continuous WAL archive | Preserve the uninterrupted WAL sequence and recovery metadata. |

PostgreSQL distinguishes logical dumps, filesystem backups and continuous archiving. [Backup methods](https://www.postgresql.org/docs/current/backup.html)

`pg_dump` creates a consistent database dump while the database is in use. It does not establish a shared transaction boundary with external application files. Global objects require `pg_dumpall --globals-only` or equivalent controlled provisioning. Use a sufficiently privileged backup role, check failures and use compatible client versions. For regular production protection, assess physical backups with WAL; logical dumps alone mainly suit simple cases and appropriate recovery objectives. [pg_dump](https://www.postgresql.org/docs/current/app-pgdump.html), [pg_dumpall](https://www.postgresql.org/docs/current/app-pg-dumpall.html)

Illustrative logical-backup workflow, with an existing protected directory and preconfigured libpq services; names are placeholders:

```bash
umask 077
pg_dump --dbname='service=app-backup' --format=custom \
  --file=/backup/staging/app.dump
```

Publish the artifact to the retained repository only after the dump succeeds. In automation, use unique staging paths or enforce a single running backup job; propagate nonzero exits and avoid treating a partially written file as the newest valid backup. Preserve required roles, ownership and grants separately; globals may contain sensitive authentication material.

Restore into a prepared, empty, isolated test database and exercise application queries. A readable archive listing is only preliminary inspection. For a lab with precreated ownership, `pg_restore --exit-on-error --no-owner --no-privileges` can simplify validation, but production recovery must restore the intended ownership and access controls. [pg_restore](https://www.postgresql.org/docs/current/app-pgrestore.html)

For physical backup, use PostgreSQL's supported procedures, not an unsynchronized copy of live `PGDATA`. A filesystem copy generally requires shutdown; an atomic filesystem snapshot must include all required files/WAL and respect multi-filesystem consistency. [Filesystem backups](https://www.postgresql.org/docs/current/backup-file.html)

`pg_basebackup` can back up a running cluster and include WAL needed for that backup. It does not by itself provide continuing recovery points after completion; continuous archiving must be established and monitored. Do not combine a logical dump with WAL and call it PITR. Failed archiving can fill `pg_wal`, and a missing segment can break recovery. [pg_basebackup](https://www.postgresql.org/docs/current/app-pgbasebackup.html), [PITR](https://www.postgresql.org/docs/current/continuous-archiving.html)

Use `pg_verifybackup` for a supported physical backup manifest, then still restore/start the database and verify contents; the utility does not prove every runtime check will pass. [Verification limits](https://www.postgresql.org/docs/current/app-pgverifybackup.html)

## Coordinate Forgejo state

Inventory the database, Git repositories, LFS, attachments, packages, configuration, secrets and any separate object/queue storage. Stop writes and background workers when stores cannot be captured together. Forgejo's upgrade guide explicitly calls for stopping the application when its state is split across stores, and warns about SQL-dump problems in `forgejo dump`; create the database engine's native dump in addition to any archive. Do not generalize an atomic single-disk example into a guarantee for Hetzner live images. [Forgejo backup requirements](https://forgejo.org/docs/latest/admin/upgrade/#backup)

Restore the matching application version and coordinated data set in isolation. Validate login, clone, an authorized test push, LFS, issue attachment retrieval and package downloads. Run diagnostics without repair first; inspect results before any repair command. Prevent restored jobs, webhooks and mail from contacting production recipients during the test.

## Coordinate a container registry

Preserve registry configuration, authentication material and the complete storage backend, including manifest references and blobs. A filesystem registry stores data under its configured root directory. For S3, verify the driver's operations against Hetzner compatibility; backup copies must retain the application's key layout. [Filesystem driver](https://distribution.github.io/distribution/storage-drivers/filesystem/), [S3 driver](https://distribution.github.io/distribution/storage-drivers/s3/)

Quiesce writes for a coordinated copy when no application-supported online backup method exists. Garbage collection is a separate destructive maintenance operation: Distribution requires read-only/stopped operation to avoid deleting blobs involved in concurrent uploads. Do not run garbage collection to “clean up” an unverified recovery copy. [Garbage collection](https://distribution.github.io/distribution/about/garbage-collection/)

## Prove recovery and retain evidence

Restore periodically into an isolated environment using only documented recovery credentials. Verify representative old and recent data, file hashes, role permissions and an application transaction. For PITR, select a time before a known test change and prove the boundary. Record elapsed time, recovered timestamp, errors and the exact backup identity.

Keep retention/admin credentials separate from application writers. A replica can reproduce a dropped table; a synchronized mirror can reproduce a deleted repository. Keep historical copies that survive the failure you intend to cover. Do not expire older recoverable backups solely because a new upload completed; first establish that the new set is complete and periodically prove restoration.
