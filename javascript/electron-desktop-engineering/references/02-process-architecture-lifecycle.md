# Processes, ownership, and application lifecycle

**Read when:** designing the application, assigning work, or diagnosing shutdown and crash behavior.

## Ownership map

The main process owns application/OS coordination and privileged operations. BrowserWindow/WebContents host renderer content; preload exposes a deliberately constrained bridge. Use a worker or utility process for suitable CPU-intensive or fault-sensitive tasks instead of blocking main. Process separation improves responsiveness and fault containment, but ordinary Node-capable processes are not a hostile-code sandbox.

Write an ownership table for windows, sessions, database connections, background jobs, file watchers, timers, credentials, and updater state. Every resource needs a creation condition, authority, shutdown path, crash/restart policy, and observability. A hidden window is still a process/resource owner, not automatically suspended work.

## Lifecycle procedure

Register early application/protocol hooks at the required stage. Create Electron-dependent UI after readiness. Handle platform-specific application activation and window closure deliberately. Acquire a single-instance lock when required and route second-instance/deep-link requests to a validated dispatcher. Do not assume all quit/shutdown paths allow asynchronous cleanup; persist important state as part of normal operations.

Avoid synchronous disk, network, or large computation in main's event loop. Return structured progress and cancellation handles to the renderer. Keep job ownership independent from a view when the operation should survive closing that view; otherwise cancel it explicitly.

## Acceptance

Start cold, launch a second instance, close all windows, reactivate the app, quit with a job in progress, and simulate a renderer crash. Verify no orphan child processes, duplicate listeners, locked databases, or hidden unbounded work. Document which operations survive renderer restart and how their status is recovered. Keep authoritative state outside a renderer-local React store when multiple windows must agree.

## Evidence and navigation

Primary sources (reviewed 2026-10-15 unless marked as discovery pointers):

- [E04: Electron process model](https://www.electronjs.org/docs/latest/tutorial/process-model)
- [E28: App API](https://www.electronjs.org/docs/latest/api/app)
- [E29: BrowserWindow](https://www.electronjs.org/docs/latest/api/browser-window)
- [E14: utilityProcess](https://www.electronjs.org/docs/latest/api/utility-process)

Procedures are original engineering recommendations. Verify API-specific changes against installed-version documentation.

[Topic index](00-index.md) · [Evidence policy](01-version-and-evidence.md) · [Source register](../SOURCES.md)
