# Realtime, offline, local-first, and synchronization

**Read when:** adding sockets, background synchronization, offline editing, or local persistence.

## Define delivery semantics

Choose whether events are notifications to refetch, canonical deltas, or commands acknowledged by the server. Specify ordering, event IDs, deduplication, resume cursor, heartbeat, reconnection backoff, and bounded buffering. WebSocket/SSE connectivity is not a durable queue or a guarantee of exactly-once processing.

For offline mutation queues, define idempotency, ordering, expiration, conflict handling, authorization expiry, and user-visible pending/failed states. Separate durable domain edits from disposable presence and typing indicators. Replaying an operation after sign-out must not silently run under a different account.

## Storage model

Use schema versions, transactional writes where available, and a quota/eviction strategy. IndexedDB-based libraries such as Dexie, local databases such as RxDB, and CRDT choices such as Yjs/Automerge are distinct catalog options. Verify adapters, licensing, replication assumptions, and encryption claims in current documentation before adopting one. A client-side cache is not automatically a backup.

Define how a local snapshot reconciles with a newer server schema. Keep migrations pure and recoverable; preserve unsent user changes before destructive reset. Sensitive data persistence requires a threat model, expiry, and secure deletion expectations appropriate to the platform.

## Acceptance

Disconnect during a write, duplicate and reorder events, overflow the buffer, expire authentication offline, clear storage, and reconnect after the server compacted history. Open multiple tabs/windows editing the same record. Verify that the UI exposes unresolved conflicts rather than silently choosing an arbitrary winner. Measure storage growth and background CPU. In Electron, centralize privileged/local database ownership outside React and use bounded domain IPC rather than sharing a raw database handle.

## Evidence and navigation

Primary sources (reviewed 2026-10-15 unless marked as discovery pointers):

- [R64: Yjs](https://docs.yjs.dev/)
- [R18: TanStack Query defaults](https://tanstack.com/query/latest/docs/framework/react/guides/important-defaults)
- [R19: SWR getting started](https://swr.vercel.app/docs/getting-started)

Procedures are original engineering recommendations. Verify API-specific changes against installed-version documentation.

[Topic index](00-index.md) · [Evidence policy](01-version-and-evidence.md) · [Source register](../SOURCES.md)
