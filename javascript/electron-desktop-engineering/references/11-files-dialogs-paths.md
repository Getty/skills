# Files, native dialogs, path authorization, and safe writes

**Read when:** opening/saving documents, watching files, or granting filesystem access.

## Capability model

Prefer main-owned native dialogs that yield a scoped document capability rather than a generic renderer `readFile(path)` API. Track the selected resource, allowed operations, owner window/account, and expiry. Revalidate before use where external filesystem changes matter. A path string received through IPC is untrusted even when TypeScript calls it `FilePath`.

Bound bytes before reading/parsing, validate expected document structure, and distinguish content validation from extension checks. Resolve directory traversal and symlink concerns explicitly. Lexical containment alone does not prevent symlink races; for hostile mutable directories use an OS-appropriate secure-open strategy or avoid exposing arbitrary paths. Keep trusted application assets outside user-controlled document roots.

## Write protocol

Use an application-owned serialization queue where concurrent writes target the same file. Write a temporary file in the appropriate directory, flush/durability steps according to requirements, then atomically replace where the target platform/filesystem supports the chosen method. Preserve a recovery backup for migrations. Handle disk-full, permission errors, antivirus/file locks, and interrupted writes without claiming success.

File watchers generate hints, not a perfect ordered transaction log. Debounce/reconcile by reading the authoritative state and handle rename/delete/recreate. Never treat a watcher event's path as authorization for a new arbitrary file.

## Acceptance

Cancel dialogs, select oversized/corrupt files, change the file during reading, save to read-only/full storage, collide with another writer, and reopen after a crash. Test paths with spaces, Unicode, network shares, and platform-specific path forms when supported. Avoid exposing full private paths in renderer errors or telemetry. Document whether an import copies content or retains authority to the original file.

## Evidence and navigation

Primary sources (reviewed 2026-10-15 unless marked as discovery pointers):

- [E31: Native dialogs](https://www.electronjs.org/docs/latest/api/dialog)
- [E28: App API](https://www.electronjs.org/docs/latest/api/app)
- [E07: IPC tutorial](https://www.electronjs.org/docs/latest/tutorial/ipc)

Procedures are original engineering recommendations. Verify API-specific changes against installed-version documentation.

[Topic index](00-index.md) · [Evidence policy](01-version-and-evidence.md) · [Source register](../SOURCES.md)
