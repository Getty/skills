# React renderer integration and multi-window state

**Read when:** building an Electron frontend with React, React Flow, or heavy browser components.

## Keep the renderer portable

React components should depend on a typed application adapter, not import Electron or Node. Declare the preload bridge interface and implement a browser/test adapter only with explicitly nonprivileged behavior. Main remains responsible for runtime validation and authorization. Keep secrets and raw filesystem/process/database APIs out of the bridge.

Subscriptions need cleanup and stable ownership. A React effect subscribes once per intended resource and returns the actual unsubscribe function. Use operation IDs or sequence/revision numbers to ignore obsolete async results. A development Strict Mode remount should not create duplicate long-running jobs or listeners.

## State architecture

Keep per-window view state local. Put shared document/account/job authority in a main-owned service or other explicit shared backend, then publish sanitized revisions/events to windows. Do not synchronize entire React stores blindly in both directions. Define conflict handling and what happens when a window misses events or restarts.

For React Flow, retain pure graph validation and document schemas outside the canvas. Privileged execution of graph nodes belongs behind a validated service with quotas, cancellation, and authorization. The diagram library is not a reason to let renderer node data invoke arbitrary commands.

## Packaging/CSP

Verify static asset base paths, custom-protocol routing, lazy chunks, workers, fonts, editor/PDF resources, and the bundled preload. Dynamic layout libraries may require style-specific CSP allowances; do not respond by allowing eval or remote scripts. A full SSR web framework is optional and adds local-server lifecycle/security work if shipped inside the desktop app.

## Acceptance

Run the packaged app offline, reload a nested route, mount/unmount subscribing components, open two windows editing the same document, and deny malformed IPC. Test that a missing bridge produces a clear environment error rather than silently bypassing platform protections. Use the React skill for UI/state/library details and this skill for all privileged/runtime/distribution decisions.

## Evidence and navigation

Primary sources (reviewed 2026-10-15 unless marked as discovery pointers):

- [E05: Context isolation](https://www.electronjs.org/docs/latest/tutorial/context-isolation)
- [E07: IPC tutorial](https://www.electronjs.org/docs/latest/tutorial/ipc)
- [E09: Protocol API](https://www.electronjs.org/docs/latest/api/protocol)
- [R04: Effects decision guide](https://react.dev/learn/you-might-not-need-an-effect)
- [R50: React Flow learning index](https://reactflow.dev/learn)

Procedures are original engineering recommendations. Verify API-specific changes against installed-version documentation.

[Topic index](00-index.md) · [Evidence policy](01-version-and-evidence.md) · [Source register](../SOURCES.md)
