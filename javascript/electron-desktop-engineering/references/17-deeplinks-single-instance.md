# Deep links, file associations, and single-instance dispatch

**Read when:** registering a URL scheme, opening documents from the OS, or handling a second launch.

## Treat every launch payload as untrusted

Define an exact command grammar with a scheme, action, allowed parameters, size limits, and parsing rules. Reject unknown actions, duplicate sensitive parameters, credentials, malformed encodings, and values that would become arbitrary paths or commands. A deep link should identify a domain operation, not serialize an unrestricted IPC request.

Register application event listeners at the required early lifecycle stage and queue validated intents until the app is ready. Platform delivery differs: inspect the official guidance for open-url, second-instance arguments, and file-opening events. Do not assume the URL is always the final command-line argument. Separate initial launch from delivery to an existing instance.

## Dispatch policy

Acquire the single-instance lock where appropriate. Route each accepted intent to an authorization-aware dispatcher, deduplicate it, and choose the target window/document. Bring the appropriate window forward without creating duplicates or bypassing user confirmation for destructive actions. For authentication callbacks, require a matching pending request and replay protection.

File associations require the same content/path validation as a native open dialog. A trusted OS launch mechanism does not make the selected file trustworthy. Preserve user drafts before switching documents and handle an unknown or incompatible schema visibly.

## Acceptance

Test cold launch, already-running delivery, multiple rapid links, malformed/oversized URLs, replayed auth callbacks, spaces/Unicode in paths, and requests received before readiness. Verify installed package registration on each target OS, not only manual invocation during development. Test uninstall/update registration behavior. Keep logs limited to normalized action metadata rather than full links that may contain private data.

## Evidence and navigation

Primary sources (reviewed 2026-10-15 unless marked as discovery pointers):

- [E34: Deep linking](https://www.electronjs.org/docs/latest/tutorial/launch-app-from-url-in-another-app)
- [E28: App API](https://www.electronjs.org/docs/latest/api/app)

Procedures are original engineering recommendations. Verify API-specific changes against installed-version documentation.

[Topic index](00-index.md) · [Evidence policy](01-version-and-evidence.md) · [Source register](../SOURCES.md)
