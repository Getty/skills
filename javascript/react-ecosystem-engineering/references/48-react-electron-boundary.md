# React inside Electron: the renderer is not the main process

**Read when:** using React in a desktop app or sharing browser and Electron UI.

## Capability boundary

Keep React components in an unprivileged renderer with Node integration disabled, context isolation enabled, and sandboxing retained. Expose a small typed domain API through preload/contextBridge. A method such as `preferences.setTheme(theme)` is safer to review than generic `ipc.send(channel, payload)` or `fs.readFile(path)`. Main validates sender/frame/URL and payload independently of TypeScript.

A context bridge transports a deliberately constrained interface; it is not a reason to expose class instances, database handles, tokens, shell execution, or arbitrary channels. Strip Electron event objects from subscriptions and return an unsubscribe closure. Treat renderer code as compromiseable even when it loads packaged local assets.

## React integration

Declare the bridge type in a renderer-only ambient declaration and access it through a small adapter. Use effect cleanup for subscriptions. Handle missing bridge behavior explicitly for browser previews/tests; do not silently install a privileged polyfill. For shared web/desktop UI, inject the adapter through a clear composition boundary.

Keep file dialogs, path authorization, database work, secrets, updater state, and process execution outside components. Return sanitized outcomes and operation IDs rather than raw exceptions or private filesystem paths. Centralize cross-window domain state in a suitable owner; a renderer-local store is not automatic multi-window synchronization.

## Packaged acceptance

Test the real custom protocol/base path, CSP, preload output path, sandbox preload bundling, and production asset resolution. Development HTTP success does not prove packaged loading. Verify reload/deep links and worker assets used by editors/PDF/maps. React Flow uses inline geometry styles, so a desktop CSP must deliberately permit the necessary style mechanism without weakening `script-src` or granting Node access.

## Evidence and navigation

Primary sources (reviewed 2026-10-15 unless marked as discovery pointers):

- [E01: Electron security checklist](https://www.electronjs.org/docs/latest/tutorial/security)
- [E05: Context isolation](https://www.electronjs.org/docs/latest/tutorial/context-isolation)
- [E06: Process sandboxing](https://www.electronjs.org/docs/latest/tutorial/sandbox)
- [E07: IPC tutorial](https://www.electronjs.org/docs/latest/tutorial/ipc)
- [E09: Protocol API](https://www.electronjs.org/docs/latest/api/protocol)
- [R04: Effects decision guide](https://react.dev/learn/you-might-not-need-an-effect)

Procedures are original engineering recommendations. Verify API-specific changes against installed-version documentation.

[Topic index](00-index.md) · [Evidence policy](01-version-and-evidence.md) · [Source register](../SOURCES.md)
