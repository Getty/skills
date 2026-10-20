# Electron ecosystem and core API atlas

**Read when:** locating an Electron module or selecting a companion library.

## Evidence and package policy

Core references in the source register were reviewed for their stated topic. The table's **C** entries have a related reviewed guide; **P** entries are discovery pointers, not maintenance endorsements or verified versions. Helpers are optional: do not install a generic bridge/helper package as a substitute for capability review. Tauri is an alternative technology, not an Electron plugin; an architectural comparison requires separate current research.

| Area | Tool | Package recognition | Evidence | Load |
|---|---|---|---|---|
| Build | [Electron Forge](https://www.electronforge.io/) | `@electron-forge/cli`, `@electron-forge/core` | C | [25-forge-builder-electronvite](25-forge-builder-electronvite.md) |
| Build | [Forge Vite plugin](https://www.electronforge.io/config/plugins/vite) | `@electron-forge/plugin-vite` | C | [25-forge-builder-electronvite](25-forge-builder-electronvite.md) |
| Build | [electron-builder](https://www.electron.build/) | `electron-builder` | C | [25-forge-builder-electronvite](25-forge-builder-electronvite.md) |
| Build | [electron-vite](https://electron-vite.org/guide/) | `electron-vite` | C | [25-forge-builder-electronvite](25-forge-builder-electronvite.md) |
| Hardening | [Electron fuses](https://www.electronjs.org/docs/latest/tutorial/fuses) | `@electron/fuses` | C | [30-fuses-integrity](30-fuses-integrity.md) |
| Native build | [Electron rebuild](https://www.electronjs.org/docs/latest/tutorial/using-native-node-modules) | `@electron/rebuild` | C | [15-native-addons-abi](15-native-addons-abi.md) |
| Testing | [Playwright Electron](https://playwright.dev/docs/api/class-electron) | `playwright`, `@playwright/test` | C | [24-testing-playwright-ci](24-testing-playwright-ci.md) |
| Updates | [electron-updater](https://www.electron.build/) | `electron-updater` | P | [28-updates-rollouts-recovery](28-updates-rollouts-recovery.md) |
| Storage | [electron-store](https://github.com/sindresorhus/electron-store) | `electron-store` | P | [12-storage-databases-migrations](12-storage-databases-migrations.md) |
| Logs | [electron-log](https://github.com/megahertz/electron-log) | `electron-log` | P | [23-debugging-logging-crashes](23-debugging-logging-crashes.md) |
| Helpers | [electron-toolkit](https://github.com/alex8088/electron-toolkit) | `@electron-toolkit/preload`, `@electron-toolkit/utils` | P | [05-preload-contextbridge](05-preload-contextbridge.md) |
| Native DB | [better-sqlite3](https://github.com/WiseLibs/better-sqlite3) | `better-sqlite3` | P | [15-native-addons-abi](15-native-addons-abi.md) |
| Native DB | [node-sqlite3](https://github.com/TryGhost/node-sqlite3) | `sqlite3` | P | [15-native-addons-abi](15-native-addons-abi.md) |
| Terminal backend | [node-pty](https://github.com/microsoft/node-pty) | `node-pty` | P | [14-workers-utilityprocess-subprocesses](14-workers-utilityprocess-subprocesses.md) |
| Notarization | [Electron notarize](https://github.com/electron/notarize) | `@electron/notarize` | P | [27-signing-notarization](27-signing-notarization.md) |
| macOS signing | [Electron osx-sign](https://github.com/electron/osx-sign) | `@electron/osx-sign` | P | [27-signing-notarization](27-signing-notarization.md) |
| Diagnostics | [Sentry Electron](https://docs.sentry.io/platforms/javascript/guides/electron/) | `@sentry/electron` | P | [23-debugging-logging-crashes](23-debugging-logging-crashes.md) |
| Alternative scope | [Tauri](https://tauri.app/) | `@tauri-apps/api`, `@tauri-apps/cli` | P | [02-process-architecture-lifecycle](02-process-architecture-lifecycle.md) |

## Core API atlas

The following is a discovery map to **official APIs**, not permission to expose them to a renderer. Read the installed-version API page, supported processes, lifecycle requirements, platform notes, and security implications before use. APIs not separately present in the source register have not received individual substantive review in this bundle.

| Need | APIs to inspect | Boundary and chapter |
|---|---|---|
| App lifecycle / paths / single instance | `app` | Main; process lifecycle and deep links |
| Windows and content | `BrowserWindow`, `BaseWindow`, `WebContentsView`, `webContents` | Main; window roles, navigation, ownership |
| Renderer capability bridge | `contextBridge`, `ipcRenderer`, `ipcMain` | Narrow preload methods; main validates every call |
| Structured streams | `MessageChannelMain`, `MessagePortMain` | Main/owned endpoints; quotas and backpressure |
| Background services | `utilityProcess` | Main supervision; not a hostile-code sandbox |
| App resources | `protocol`, `session` | Register privileges/handlers at the correct stage/session |
| Network / diagnostics | `net`, `netLog`, `session` | Explicit cookie/proxy/authentication ownership |
| Files / external apps | `dialog`, `shell`, `webUtils` | Main-owned selection/authorization; never generic renderer access |
| Credentials | `safeStorage` | Main; backend availability and Linux fallback policy |
| Menus / tray / shortcuts | `Menu`, `MenuItem`, `Tray`, `globalShortcut` | Main; domain command mapping and cleanup |
| Display / images / theme | `screen`, `nativeImage`, `nativeTheme`, `systemPreferences` | Platform-specific review; validate bounds/resources |
| Notifications / clipboard | `Notification`, `clipboard` | User intent, privacy, allowed formats |
| Capture / devices | `desktopCapturer`, session permission/device handlers | Origin/frame/user/OS permission checks |
| Printing / PDF | WebContents printing methods | Controlled content/options/output destination |
| Power / suspend | `powerMonitor`, `powerSaveBlocker` | Bounded ownership; avoid surprising background behavior |
| Updates | `autoUpdater` | Installer/platform-specific; not an arbitrary executable launcher |
| Crashes / tracing | `crashReporter`, `contentTracing` | Consent, redaction, symbol and storage policy |
| Platform-specialized features | `TouchBar`, `inAppPurchase`, `pushNotifications` | Verify current availability/platform/channel constraints |
| Legacy embeddings | `BrowserView`, `webview` | Migration/security review; prefer current supported architecture |

Official entry point: [Electron API documentation](https://www.electronjs.org/docs/latest/api/app). Use its navigation to the exact module rather than guessing an API from a similarly named third-party helper.

## Compatibility matrix before installation

Record package/runtime versions, embedded Node ABI, OS/architecture, bundled versus external modules, preload sandbox compatibility, native binaries, ASAR placement, license, signing implications, and updater ownership. A wrapper's convenience is not evidence that its defaults meet the application threat model. Preserve the current coherent toolchain unless a measured requirement justifies replacement.

## Evidence and navigation

Primary sources (reviewed 2026-10-15 unless marked as discovery pointers):

- [E04: Electron process model](https://www.electronjs.org/docs/latest/tutorial/process-model)
- [E07: IPC tutorial](https://www.electronjs.org/docs/latest/tutorial/ipc)
- [E22: Electron Forge](https://www.electronforge.io/)
- [E24: electron-builder](https://www.electron.build/)
- [E25: electron-vite](https://electron-vite.org/guide/)
- [E12: Fuses](https://www.electronjs.org/docs/latest/tutorial/fuses)

Procedures are original engineering recommendations. Verify API-specific changes against installed-version documentation.

[Topic index](00-index.md) · [Evidence policy](01-version-and-evidence.md) · [Source register](../SOURCES.md)
