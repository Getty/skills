# Local storage, databases, migrations, and multi-window consistency

**Read when:** persisting settings, storing documents, or integrating SQLite/native databases.

## Pick the owner

Keep privileged database access in main or an intentionally managed service/utility process, not directly in React. Define a typed repository boundary and one write-coordination strategy. Multiple windows should observe a shared authority rather than each mutating a separate unsynchronized copy. For renderer-only disposable cache, document eviction and rebuild behavior.

Choose storage by data shape, transaction needs, scale, recovery, portability, and threat model. A JSON preferences file, SQLite database, IndexedDB cache, and encrypted credential store solve different problems. `electron-store`, SQLite bindings, and other catalog options require current version/license/native-ABI review before adoption.

## Migration protocol

Version the schema explicitly. Check compatibility before opening a writable database. Apply migrations transactionally where possible and preserve a tested backup/recovery path. An application binary rollback may be incompatible with a migrated database; define forward/backward compatibility or a restore procedure before rollout.

Keep settings paths under an appropriate application data location, not the installation directory. Decide multi-instance behavior, file locking, import/export, retention, and secure deletion expectations. Encryption at rest requires key management; storing the key next to encrypted data does not meaningfully address local file theft.

## Acceptance

Open from every supported prior schema, interrupt migration, run out of disk space, start two windows/instances, and restore from backup. Test malformed settings and unknown future versions. Verify read/write latency does not block main's event loop and that closing a renderer does not corrupt an in-flight transaction. Test the actual packaged native database module on each OS/architecture; host Node tests alone do not establish Electron ABI compatibility.

## Evidence and navigation

Primary sources (reviewed 2026-10-15 unless marked as discovery pointers):

- [E28: App API](https://www.electronjs.org/docs/latest/api/app)
- [E16: Native Node modules](https://www.electronjs.org/docs/latest/tutorial/using-native-node-modules)
- [E14: utilityProcess](https://www.electronjs.org/docs/latest/api/utility-process)
- [E13: safeStorage](https://www.electronjs.org/docs/latest/api/safe-storage)

Procedures are original engineering recommendations. Verify API-specific changes against installed-version documentation.

[Topic index](00-index.md) · [Evidence policy](01-version-and-evidence.md) · [Source register](../SOURCES.md)
