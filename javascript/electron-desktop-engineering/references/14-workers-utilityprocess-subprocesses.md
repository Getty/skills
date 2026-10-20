# Workers, utility processes, subprocesses, and resource limits

**Read when:** offloading CPU work, running native services, or managing background jobs.

## Match isolation to the workload

Use renderer workers for suitable browser-side computation, Node workers for trusted parallel Node work, and utility/child processes for an intentional process boundary. Electron's utilityProcess API supports a Node-capable service process; that is not an operating-system sandbox for hostile arbitrary code. Untrusted execution needs additional isolation, filesystem/network restrictions, and resource enforcement outside this abstraction.

## Job contract

Define a bounded input schema, job ID, owner, progress protocol, cancellation, deadline, output limit, and exit/error mapping. Limit concurrent jobs and queue depth. Avoid passing unbounded buffers repeatedly across IPC. Use message ports or transfer-friendly designs where appropriate and implement backpressure, not just faster transport.

For subprocesses, use fixed executables and argument arrays rather than shell-interpolated strings. Validate working directory, environment allowlist, inherited handles, and output encoding/size. Killing a parent does not necessarily terminate a whole process tree on every platform; document the target-specific strategy. Never expose a general command runner to the renderer.

## Lifecycle

Supervise startup, readiness, health, crash/restart, and graceful shutdown. Use bounded restart backoff and prevent crash loops. Decide whether a job survives a window closing and how progress resumes after renderer restart. Do not let orphan jobs retain files, ports, or credentials indefinitely.

## Acceptance

Run CPU/memory-heavy representative jobs, flood the queue, cancel during startup/execution, kill the child, close the window, and quit the app. Verify UI responsiveness, output limits, cleanup, and accurate final status. Record OS-level limits separately from application-level cooperative quotas; a JavaScript timeout does not prove a hung native operation was terminated.

## Evidence and navigation

Primary sources (reviewed 2026-10-15 unless marked as discovery pointers):

- [E14: utilityProcess](https://www.electronjs.org/docs/latest/api/utility-process)
- [E15: Message ports](https://www.electronjs.org/docs/latest/tutorial/message-ports)
- [E18: Electron performance](https://www.electronjs.org/docs/latest/tutorial/performance)
- [E04: Electron process model](https://www.electronjs.org/docs/latest/tutorial/process-model)

Procedures are original engineering recommendations. Verify API-specific changes against installed-version documentation.

[Topic index](00-index.md) · [Evidence policy](01-version-and-evidence.md) · [Source register](../SOURCES.md)
