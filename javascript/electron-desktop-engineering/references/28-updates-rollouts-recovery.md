# Updates, channels, rollout, and recovery

**Read when:** implementing auto-update or preparing release/rollback strategy.

## Match updater to distribution

Electron's core autoUpdater has platform-specific support and installer requirements; it is not a universal Linux solution. The electron-updater/electron-builder ecosystem uses its own configuration and metadata. Store-managed or distribution-managed packages may have a different update owner. Choose one supported path per target and read the exact current documentation before writing feed configuration.

## Update state machine

Model idle, checking, available, downloading, ready, installing, failed, and deferred states as appropriate. Bound retries, keep errors visible, and avoid multiple simultaneous checks. Explain when restart is needed, preserve drafts, and support deferral consistent with product policy. Do not expose arbitrary feed URLs or updater commands through generic renderer IPC.

Treat release metadata and artifacts as security-sensitive inputs. Use authenticated/protected publishing, secure transport, the updater's verification mechanisms, and compatible signing identity. Never install arbitrary renderer-provided executables as an “update.” Separate prerelease/stable channels and deliberate downgrade policy.

## Data compatibility and recovery

An application rollback can fail after a forward-only database migration. Design compatible schema windows, backups, or tested restore paths. Staged rollout needs observable failure thresholds and a pause mechanism; merely uploading one binary is not staged rollout. Define offline behavior, interrupted downloads, low disk, locked files, and incomplete installation recovery.

## Acceptance

Exercise the actual installed previous release upgrading to the new signed release on each supported target/format. Test tampered metadata/artifacts, wrong channel, unavailable feed, interrupted download, user deferral, and data migration failure. Record feed/installer versions and hashes. Do not infer end-to-end update safety from an unsigned development app receiving an “update available” event.

## Evidence and navigation

Primary sources (reviewed 2026-10-15 unless marked as discovery pointers):

- [E20: Application updates](https://www.electronjs.org/docs/latest/tutorial/updates)
- [E21: autoUpdater API](https://www.electronjs.org/docs/latest/api/auto-updater)
- [E24: electron-builder](https://www.electron.build/)
- [E19: Code signing](https://www.electronjs.org/docs/latest/tutorial/code-signing)

Procedures are original engineering recommendations. Verify API-specific changes against installed-version documentation.

[Topic index](00-index.md) · [Evidence policy](01-version-and-evidence.md) · [Source register](../SOURCES.md)
