# Zustand, Jotai, and other client-state choices

**Read when:** choosing a lightweight store or diagnosing subscription fan-out.

## Match the model

Zustand offers a store-and-selector style; Jotai organizes state around atoms and their dependencies. Choose based on the shape of coordination, not a universal speed ranking. Existing MobX or Valtio projects need their own installed-version semantics reviewed; this chapter treats them as comparison/discovery options, not verified interchangeable APIs.

Create a state ownership diagram. Identify local values, shared values, derived values, persisted values, and external remote snapshots. Keep one authoritative representation of each domain fact. A component's subscription should be narrower than the whole store whenever high-frequency updates would otherwise invalidate unrelated UI.

## Store engineering

Define updates as meaningful actions with invariants. Preserve immutable structural sharing where the chosen library expects it. Review selector equality and stable outputs against the installed major; an allocating selector can undermine intended isolation. For atom graphs, avoid uncontrolled atom creation during rendering and make async lifetime/error behavior visible.

For SSR, scope stores to the request or deliberate provider instance. For multiple documents/workspaces, decide whether stores are independent and how they are disposed. Persistence needs schema versioning, migration, unknown-field handling, hydration status, and a reset path. Never assume local storage is encrypted, unlimited, or available synchronously in every rendering environment.

## Verification

Open two workspaces, change one rapidly, and verify the other does not accidentally share data. Restore an old persisted schema; reject corrupt data; sign out; reconnect a remote source. Profile subscription frequency and retained memory after disposal. For React Flow, keep transient selection and drag changes from causing every inspector or node to subscribe to the entire nodes array. Test the chosen adapter with actual library versions before migrating stores.

## Evidence and navigation

Primary sources (reviewed 2026-10-15 unless marked as discovery pointers):

- [R21: Zustand official repository](https://github.com/pmndrs/zustand)
- [R22: Jotai documentation](https://jotai.org/docs)

Procedures are original engineering recommendations. Verify API-specific changes against installed-version documentation.

[Topic index](00-index.md) · [Evidence policy](01-version-and-evidence.md) · [Source register](../SOURCES.md)
