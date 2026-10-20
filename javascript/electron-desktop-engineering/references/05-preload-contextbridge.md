# Preload and contextBridge capability design

**Read when:** exposing desktop functionality to React or another renderer.

## Design capabilities, not transport

Expose specific application operations such as `preferences.get()`, `preferences.setTheme(theme)`, or `documents.chooseAndOpen()`. Do not expose `ipcRenderer`, generic `send`/`invoke`, arbitrary channel names, filesystem modules, shell execution, environment variables, or a function that accepts unrestricted commands. A generic bridge makes every future channel an implicit renderer capability.

Keep `contextIsolation: true`, `sandbox: true`, and `nodeIntegration: false`. Use contextBridge for a small serializable interface. Validate arguments in main regardless of TypeScript types or validation in preload; a compromised renderer can call the bridge directly. Keep secrets and authorization decisions out of preload and renderer.

## Events and cleanup

Wrap subscriptions so callbacks receive only sanitized domain payloads, never the Electron event object. Return an unsubscribe closure that removes the exact wrapped listener. Bound event frequency and payload size. Do not let every React render install another listener. For high-volume data, review a bounded stream/message-port design rather than broadcasting huge arrays.

Document bridge version, method input/output schema, error envelope, cancellation behavior, and availability. Avoid exposing mutable privileged objects through clever proxy abstractions. Keep sandbox preload bundling constraints explicit; the example's preload is one self-contained CommonJS file.

## Acceptance

Call every method with missing, extra, malformed, oversized, and prototype-related input. Attempt arbitrary channel selection and verify it is impossible through the exposed API. Mount/unmount a React consumer repeatedly and assert listener cleanup. Navigate or replace the renderer and verify main still validates the caller. Treat bridge typing as developer assistance, not as evidence of a security boundary.

## Evidence and navigation

Primary sources (reviewed 2026-10-15 unless marked as discovery pointers):

- [E05: Context isolation](https://www.electronjs.org/docs/latest/tutorial/context-isolation)
- [E06: Process sandboxing](https://www.electronjs.org/docs/latest/tutorial/sandbox)
- [E07: IPC tutorial](https://www.electronjs.org/docs/latest/tutorial/ipc)

Procedures are original engineering recommendations. Verify API-specific changes against installed-version documentation.

[Topic index](00-index.md) · [Evidence policy](01-version-and-evidence.md) · [Source register](../SOURCES.md)
