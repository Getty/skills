# React Flow persistence, history, collaboration, and migrations

**Read when:** saving diagrams, implementing undo/redo, or supporting multiple users.

## Persist a document, not a runtime

Define a versioned schema containing domain node/edge data and deliberate layout/viewport preferences. Exclude React elements, functions, subscriptions, measured internals, transient dragging/selection state, and credentials. Parse imports into a fresh validated structure; do not merge unknown JSON into live objects. Bound file size before parsing and graph size after parsing.

Maintain migrations as pure transformations with fixtures from every supported schema. Back up the original before writing an irreversible migration. Reject an unknown future version rather than silently dropping fields. Use revisions or ETags for saves so stale writers cannot overwrite newer work without an explicit conflict decision.

## History model

Group a drag gesture, multi-delete, paste, or automatic layout as one semantic transaction. Limit history by count and memory. Exclude remote presence, selection, and continuously arriving execution telemetry unless product requirements say otherwise. Clear redo after a new local branch. Preserve immutable snapshots or commands; a mutated snapshot corrupts the past.

The included history helper demonstrates bounded immutable snapshot history only. It does not implement collaborative undo or merge semantics. For collaborative editing, use an intentional operation/CRDT model such as a reviewed Yjs integration, stable IDs, authorization, persistence, and reconnection rules. Presence is ephemeral and should not inflate document history.

## Collaboration acceptance

Undo should reverse the user's intended local change without restoring an old whole-document snapshot over another user's work. Test simultaneous rename/delete/connect, offline edits, reconnect after compaction, permission revocation, and duplicate operation delivery. Define tombstone/orphan behavior and port compatibility under concurrent schema changes. Encrypt/authenticate transport as appropriate and enforce document permissions server-side; a shared room name is not access control.

## Evidence and navigation

Primary sources (reviewed 2026-10-15 unless marked as discovery pointers):

- [R60: React Flow external state](https://reactflow.dev/learn/advanced-use/state-management)
- [R64: Yjs](https://docs.yjs.dev/)
- [R50: React Flow learning index](https://reactflow.dev/learn)

Procedures are original engineering recommendations. Verify API-specific changes against installed-version documentation.

[Topic index](00-index.md) · [Evidence policy](01-version-and-evidence.md) · [Source register](../SOURCES.md)
