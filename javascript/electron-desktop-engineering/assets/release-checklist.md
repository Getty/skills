# Release gate record

## Candidate identity

Source revision, lockfile, build-host toolchain, Electron/Chromium/Node, OS/architecture, package format, updater/channel, schema compatibility, artifact hash, signing identity, owner.

## Gates (record actual outputs)

Clean build; pure and integration tests; dependency/native provenance; native ABI/architecture; asset/preload paths; CSP/navigation/permission/IPC denial; production fuses read-back; ASAR/integrity scope; native/outer signatures; notarization/store checks where applicable; installed launch; previous-release update; interrupted/tampered update; database migration/recovery; rollback; accessibility/platform smoke; private-data scan; release approval.

## Promotion and recovery

Promote the tested artifact through the approved channel. Record rollout cohort, failure thresholds, pause authority, support evidence, key/certificate continuity, rollback/data compatibility, and incident owner. No gate is passed by merely having its configuration file present.
