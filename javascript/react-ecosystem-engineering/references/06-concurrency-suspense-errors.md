# Concurrency, Suspense, Activity, and error boundaries

**Read when:** implementing deferred UI, loading boundaries, hidden workspaces, or recovery.

## Separate urgency from correctness

Use urgent updates for typing and immediate control feedback. A transition can mark a heavier view update as non-urgent; it is not a background thread and does not make a CPU-bound loop cheap. Defer expensive work to a worker or server when scheduling alone cannot meet the interaction budget. Preserve a visible indication when displayed results correspond to an older query.

Place Suspense boundaries around useful reveal units, not indiscriminately around every small component. Define skeleton dimensions and accessible status text. Ordinary fetching started in an effect does not automatically integrate with Suspense. Use a framework or data resource whose lifecycle and cache behavior are explicitly compatible. Do not repeatedly create a new uncached promise during rendering and expect stable suspension.

`Activity` can preserve UI state while hidden and change effect lifecycle; validate the installed React version and test resources that should not remain active. Hidden is not disposed, nor is it a permission boundary. Set a memory policy for many retained workspaces.

## Error taxonomy

Render failures need an appropriate error boundary; event-handler and asynchronous failures need explicit handling in their own workflow. Route errors, request failures, authorization expiry, empty data, and cancellation deserve different recovery paths. Reset an error boundary when its resource identity changes, not merely by looping a retry forever.

## Acceptance

Throttle CPU and network, navigate during pending work, reject a lazy import, interrupt a transition, and recover from expired credentials. Confirm keyboard focus survives a fallback replacement and screen-reader status is not repeatedly announced. Verify server streaming behavior separately from client navigation. Do not use global error handlers as substitutes for local recovery and preserved user drafts.

## Evidence and navigation

Primary sources (reviewed 2026-10-15 unless marked as discovery pointers):

- [R01: React reference](https://react.dev/reference/react)
- [R06: Activity](https://react.dev/reference/react/Activity)
- [R09: use](https://react.dev/reference/react/use)
- [R11: hydrateRoot](https://react.dev/reference/react-dom/client/hydrateRoot)

Procedures are original engineering recommendations. Verify API-specific changes against installed-version documentation.

[Topic index](00-index.md) · [Evidence policy](01-version-and-evidence.md) · [Source register](../SOURCES.md)
