# PHP extension clients and long-running workers

Evidence: [H1–H4, G1](sources.md). Verify `extension_loaded('gearman')`, extension version, linked libgearman, CLI runtime and TLS methods separately. PHP-FPM and CLI can load different INI files/extensions.

## Request path

`GearmanClient` exposes server configuration, foreground methods, background methods and task/callback APIs. A foreground return must be interpreted with its return code, especially when receiving progress or intermediate data. A background handle is only acceptance evidence. Do not keep an HTTP request open indefinitely because the Gearman library itself allows a long wait.

The example uses a bounded foreground loop that handles intermediate return codes without constructing another logical request. The application's own deadline is separate from the I/O timeout. After a transport timeout, preserve the request ID and reconcile its outcome rather than blindly invoking the same side effect again.

For background work, commit application state and an outbox record transactionally, publish from a dispatcher, and write final outcomes in a separate store. PHP session locks, database transactions or request-scoped credentials should not remain held while waiting for a long-running worker.

## Worker path

Run workers under a process supervisor using the CLI runtime, not as an indefinitely running web request. Register functions once, process jobs in a bounded loop, classify return codes and exit on unexpected persistent transport errors so the supervisor can restart with backoff. A timeout while idle is not necessarily a failed business operation.

The sample callback returns JSON for valid work. It deliberately converts rejected input into a **domain-error result envelope** (`ok: false`) rather than mixing explicit `sendFail` with automatic callback completion. Consequently this sample distinguishes transport completion from application success. Other adapters in this package demonstrate native `WORK_FAIL`; do not infer identical failure behavior from their shared happy-path contract.

The official job API also has `sendFail`, data/status/warning/exception methods. Before using manual terminal messages, test how the installed callback wrapper handles its return value afterward. Ensure exactly one terminal path; source review or a wire trace is preferable to relying on an old user-contributed snippet.

## Resource lifecycle and security

Close per-job cursors, streams, temporary files and tracing spans. Reconnect stale database connections deliberately. Recycle workers after a measured job count or RSS limit when libraries retain memory; recycling should happen between assignments, not by killing healthy in-flight effects. Put time limits on external calls rather than depending solely on a PHP runtime setting.

Use strict JSON types and ranges. The sample requires 64-bit PHP for exact integer sums/deadlines. PHP's standard JSON decoder does not reject duplicate object keys, so add a strict ingress parser for hostile data; the offline suite does not claim duplicate-key parity with Python.

For native TLS, inspect extension and libgearman support and perform wrong-CA/wrong-host negative tests. Do not assume the TLS configuration of your HTTP client applies to Gearman sockets. Run credentials and workload data through a redaction policy before logging.
