# Maintenance, support policy, incident handling, and deprecation

**Read when:** operating a shipped desktop app or planning long-term ownership.

## Maintenance register

Track runtime support status, critical dependencies, native modules, signing identities, update channels, distribution formats, OS targets, storage schemas, and ownership. Refresh support/security information on an explicit cadence owned by the project. A documentation snapshot is not continuous monitoring or evidence that today's release remains supported indefinitely.

Keep a release inventory with version, source revision, artifact hashes, signature identity, supported schema range, and rollback/update path. Define how unsupported OS versions are communicated and whether users can export their data before support ends. Do not silently strand data behind an incompatible runtime upgrade.

## Support workflow

Collect a consented, redacted diagnostic bundle containing runtime/OS versions, bounded logs, operation IDs, configuration metadata, and crash references. Avoid private documents, tokens, browsing history, or full filesystem listings by default. Give users a way to inspect what is being shared where practical.

For incidents, distinguish renderer content compromise, privileged bridge misuse, dependency/native vulnerability, leaked credentials, and release-pipeline compromise. Pause affected rollout, preserve evidence, revoke relevant authority, and ship a validated fix through a trusted channel. An update channel compromised at its source cannot be trusted merely because the UI calls it “official.”

## Acceptance

Exercise backup/restore, support-bundle redaction, release rollback/data compatibility, credential rotation, and an unavailable update service. Verify old installed clients fail safely when servers retire an API. Keep known limitations and support commitments concrete, with owners and target dates in project records rather than unbounded promises inside generated documentation.

## Evidence and navigation

Primary sources (reviewed 2026-10-15 unless marked as discovery pointers):

- [E02: Electron support timelines](https://www.electronjs.org/docs/latest/tutorial/electron-timelines)
- [E36: Crash reporter](https://www.electronjs.org/docs/latest/api/crash-reporter)
- [E20: Application updates](https://www.electronjs.org/docs/latest/tutorial/updates)
- [E28: App API](https://www.electronjs.org/docs/latest/api/app)

Procedures are original engineering recommendations. Verify API-specific changes against installed-version documentation.

[Topic index](00-index.md) · [Evidence policy](01-version-and-evidence.md) · [Source register](../SOURCES.md)
