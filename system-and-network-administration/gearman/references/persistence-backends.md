# Persistence backends and storage-specific review

Read after [the persistence model](persistence-model.md). Evidence: [G9–G12, G1, S3](sources.md). Availability depends on the actual build. Backend tuning below is an operational review checklist, not a universal vendor configuration.

## SQLite / libsqlite3

A useful single-owner lab choice is `--queue-type=libsqlite3` with `--libsqlite3-db=/absolute/path/queue.sqlite3`, **after confirming both options in help**. Own the directory as the daemon user. Keep this file on supported local/block storage; do not share it across replicas or assume arbitrary network filesystem locking is suitable. Bound backlog so full replay fits RAM and startup time.

The documented historical schema combines unique key and function name. Do not pre-create a table from a website without checking the installed plugin's current schema and migrations. Use the database's backup mechanism or a quiesced copy; copying a live database and ignoring associated journal/WAL files is not a recovery plan. The application's SQLite result-store demo is a different database, not this queue file.

## PostgreSQL / libpq

The documented selector is `libpq`; connection information is supplied through supported libpq settings or the server's `--libpq-conninfo` option, and the table is configurable. Provision a dedicated database role and storage namespace. Keep connection secrets out of process arguments and collected help/log artifacts whenever the packaging supports protected configuration.

Review transport verification to PostgreSQL, connection timeout, statement behavior, role permissions, schema ownership, backup/PITR policy and storage capacity. Database HA can recover the database; it does not replicate a gearmand process's in-memory state. After database failover test the plugin's reconnect path and the outcome of in-flight add/delete operations. Run each independent gearmand with a distinct owned table/namespace unless coordination is demonstrably implemented.

## MySQL/MariaDB

The native MySQL plugin is selected as `mysql` where built. Verify exact `--mysql-*` flags from help and identify which client library and database versions are used. Test payloads around the database packet limit, storage interruptions and deletion failures. Do not increase packet limits blindly without a memory budget. Schema indexes, character treatment of function/unique fields and binary payload preservation belong in the acceptance record.

## Redis

Verify the build actually contains the Redis plugin, its option names, authentication support, selected database and key layout. In 2.1.0 release notes, reconnect, replay scanning and hyphenated-function handling changed. Exercise reconnect and replay with the actual credentials and data shape. Redis durability depends on Redis persistence/replication settings and loss windows; “in Redis” is not a sufficient durability claim. Never let unrelated caches evict job records or flush the selected namespace.

## Other/legacy plugins

Historical docs list Memcached, TokyoCabinet and Drizzle integrations. Treat these as compatibility subjects, not automatic new-deployment recommendations. In particular, an evictable cache without an independently verified persistence layer does not establish disk durability merely because Gearman calls the integration a persistent-queue module.

## Backend selection record

Record queue namespace ownership, acknowledged-write loss window, replay duration at maximum backlog, steady-state add/delete latency, behavior on full disk/permission failure, backup verification, upgrade compatibility, and whether credentials rotate without losing jobs. Choose on these measured properties rather than on database popularity. Keep storage maintenance separate from live queue administration.
