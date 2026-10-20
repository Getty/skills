# Debugging, structured logs, crashes, and diagnostics

**Read when:** diagnosing production failures or designing support telemetry.

## Correlate without leaking

Assign operation IDs across renderer requests, main handlers, jobs, and persistence. Log bounded structured metadata: operation type, phase, duration, result code, and sanitized resource identity. Do not dump IPC payloads, environment variables, tokens, raw documents, full paths, or browsing/capture contents by default. Define retention, access, redaction, and user-consent requirements.

Separate renderer exceptions, preload failures, main uncaught failures, utility/native crashes, GPU problems, and updater failures. Each has different recovery and evidence. A global exception handler should not conceal corrupted state and continue blindly. Preserve a safe support bundle with an explicit list of included data.

## Tools and reproduction

Use DevTools for renderer behavior, Node/main debugging for privileged logic, content tracing for cross-process timing, and crashReporter according to the application's privacy/backend policy. Keep debug ports and insecure remote access out of production defaults. Source maps and symbols need a controlled publication/access strategy.

For a blank production window, check packaged asset paths, protocol handler/session, CSP, preload output/format, renderer console, and missing native/worker resources before enabling insecure flags. For hangs, capture process/event-loop evidence before attributing everything to React.

## Acceptance

Trigger a controlled renderer failure, rejected IPC request, failed preload, job crash, and simulated updater error. Verify useful correlation without secret exposure and a coherent recovery path. Test log rotation and disk-full handling. Confirm telemetry is actually sent/disabled as configured; configuring a crash endpoint is not proof that symbols, upload consent, retention, and support workflows are operational.

## Evidence and navigation

Primary sources (reviewed 2026-10-15 unless marked as discovery pointers):

- [E36: Crash reporter](https://www.electronjs.org/docs/latest/api/crash-reporter)
- [E37: Content tracing](https://www.electronjs.org/docs/latest/api/content-tracing)
- [E30: WebContents](https://www.electronjs.org/docs/latest/api/web-contents)
- [E28: App API](https://www.electronjs.org/docs/latest/api/app)

Procedures are original engineering recommendations. Verify API-specific changes against installed-version documentation.

[Topic index](00-index.md) · [Evidence policy](01-version-and-evidence.md) · [Source register](../SOURCES.md)
