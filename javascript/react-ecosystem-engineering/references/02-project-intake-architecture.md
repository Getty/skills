# Project intake and architecture selection

**Read when:** joining a repository, creating an application, choosing a framework, or planning a refactor.

## Intake deliverable

Produce a compact table with application purpose, users, data sensitivity, rendering environment, route topology, offline requirements, browser/device support, accessibility target, localization, deployment ownership, dependency constraints, and existing tests. Run the read-only inventory script before suggesting commands. Inspect its output rather than treating heuristics as authoritative.

Choose architecture from constraints: a browser-only internal tool may fit Vite plus a router; a content/product application may need framework-managed rendering and server boundaries; an embedded widget needs isolation and a narrow host contract; an Electron renderer does not automatically need a server framework. Reuse an existing coherent architecture unless its measured limitations justify replacement.

## Place responsibilities deliberately

Keep domain types, validation, transformations, and state transitions independent of JSX. Put external I/O behind adapters. Components express visual state and interactions; hooks connect lifecycle-sensitive resources; route modules coordinate navigation and loading. Define a feature boundary before creating a generic shared abstraction. A useful initial shape is `app/`, `features/`, `domain/`, `adapters/`, `ui/`, and `test/`, not a universal directory mandate.

Create an ownership map: URL owns shareable navigation/filter state; the server cache owns remote snapshots; form machinery owns drafts and field errors; a local store owns only cross-component client state; the backend owns authorization. Explicitly name the single writer or reconciliation rule when two layers touch the same datum.

## Acceptance

Deliver one vertical slice with loading, empty, failure, retry, success, keyboard use, and a deployment smoke test. Document why each dependency is necessary, its removal cost, and the alternatives rejected. Avoid installing a query cache, Redux, an atom store, and a state machine simultaneously without independent responsibilities. For React/Electron projects, review the Electron skill before adding platform access.

## Evidence and navigation

Primary sources (reviewed 2026-10-15 unless marked as discovery pointers):

- [R01: React reference](https://react.dev/reference/react)
- [R15: React Router modes](https://reactrouter.com/start/modes)
- [R16: TanStack Router overview](https://tanstack.com/router/latest/docs/overview)
- [R17: Next.js App Router](https://nextjs.org/docs/app)
- [R74: Vite](https://vite.dev/guide/)

Procedures are original engineering recommendations. Verify API-specific changes against installed-version documentation.

[Topic index](00-index.md) · [Evidence policy](01-version-and-evidence.md) · [Source register](../SOURCES.md)
