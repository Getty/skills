# IPC contracts, sender authorization, cancellation, and quotas

**Read when:** implementing privileged operations or reviewing a bridge.

## Validate three independent things

Authorize the caller: expected WebContents identity, expected top-level frame, and an exact permitted application URL/origin policy. Checking only a hostname or string prefix is insufficient; same-window subframes and navigated content can change the threat model. Parse URLs and compare the required scheme/host/port/path fields. Define whether query/hash values are permitted.

Validate the operation: a fixed channel/method with a domain schema, exact allowed keys, bounded strings/arrays, and meaningful authorization. Validate state: current account/document permission, resource revision, and capability lifetime. A correctly typed request from the right window can still be unauthorized for a particular document.

## Protocol design

Use discriminated result envelopes with stable error codes and sanitized user-facing messages. Keep raw stacks, paths, tokens, and database errors in protected logs. For long work, return an operation ID with progress/cancel methods scoped to the initiating authority. Reject stale/duplicate completion and define cancellation semantics: requested cancellation is not necessarily confirmed termination.

Set quotas for in-flight requests, payload bytes, event rate, and job resources. Reject overload predictably and release reservations in `finally`. For binary/high-volume streams, use an appropriate message-port or transfer mechanism with backpressure and lifecycle handling. Do not treat IPC as an unlimited queue.

## Test matrix

Exercise a valid top-frame caller, same-window subframe, different window, destroyed frame, wrong scheme/host/path, credentials in URL, and unexpected port. Test unknown methods, malformed payloads, extra keys, large strings, duplicate requests, cancellation races, and window closure mid-operation. Pure helper tests validate policy logic only; verify sender/frame behavior inside the actual packaged Electron runtime separately.

## Evidence and navigation

Primary sources (reviewed 2026-10-15 unless marked as discovery pointers):

- [E07: IPC tutorial](https://www.electronjs.org/docs/latest/tutorial/ipc)
- [E30: WebContents](https://www.electronjs.org/docs/latest/api/web-contents)
- [E15: Message ports](https://www.electronjs.org/docs/latest/tutorial/message-ports)

Procedures are original engineering recommendations. Verify API-specific changes against installed-version documentation.

[Topic index](00-index.md) · [Evidence policy](01-version-and-evidence.md) · [Source register](../SOURCES.md)
