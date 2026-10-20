# Upgrades and production-only troubleshooting

**Read when:** upgrading Electron or fixing blank windows, preload/native failures, or regressions.

## Migration sequence

Read the exact intervening Electron breaking changes and bundled Chromium/Node changes. Inventory APIs, native modules, packaging, fuses, and updater assumptions. Upgrade in reviewable steps with a known-good installed artifact and a database compatibility plan. A new Electron version may change browser behavior and native ABI independently of application source changes.

## Diagnostic routes

Blank window: inspect built HTML/script paths, custom protocol/session registration, CSP, renderer errors, and preload existence/format. Missing bridge: inspect sandbox preload bundling, output extension, absolute preload path, contextBridge execution, and renderer environment. Native load error: inspect runtime ABI, architecture, unpacked location, dependent libraries, and rebuild ownership.

Network discrepancy: compare Chromium session versus Node request path, proxy/cookies/certificates, and production allowlists. Broken embedding: inspect deprecated BrowserView assumptions and the current WebContentsView lifecycle. Update failure: inspect installed format, feed/channel metadata, signing identity, permissions, and data compatibility.

## Anti-fixes

Do not set `nodeIntegration: true`, `webSecurity: false`, `contextIsolation: false`, `--no-sandbox`, certificate bypasses, or permissive navigation as a diagnostic “fix” that remains in production. A temporary controlled experiment must be isolated and removed; prefer logs and minimal reproductions that retain the relevant security boundary.

## Acceptance

Reproduce the original defect in the failing artifact stage, add the narrowest regression test, and verify on every affected target. Re-run packaged launch, bridge denial tests, native feature tests, signing/fuse inspection, and update compatibility as appropriate. State exactly what changed and what remains untested. Do not declare migration complete based only on the development app starting.

## Evidence and navigation

Primary sources (reviewed 2026-10-15 unless marked as discovery pointers):

- [E02: Electron support timelines](https://www.electronjs.org/docs/latest/tutorial/electron-timelines)
- [E08: ES modules](https://www.electronjs.org/docs/latest/tutorial/esm)
- [E16: Native Node modules](https://www.electronjs.org/docs/latest/tutorial/using-native-node-modules)
- [E09: Protocol API](https://www.electronjs.org/docs/latest/api/protocol)
- [E39: BrowserView deprecation](https://www.electronjs.org/docs/latest/api/browser-view)

Procedures are original engineering recommendations. Verify API-specific changes against installed-version documentation.

[Topic index](00-index.md) · [Evidence policy](01-version-and-evidence.md) · [Source register](../SOURCES.md)
