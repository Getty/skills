# Testing Electron, Playwright, headless CI, and artifact stages

**Read when:** creating tests or evaluating what a passing suite actually proves.

## Layer the evidence

Pure tests cover schemas, URL/path policy, domain commands, migrations, and serialization. Main-process tests can exercise adapters with controlled fakes. Renderer component tests cover React behavior without privileges. Electron integration tests cover real preload/IPC/window behavior. Packaged tests cover resource layout and production policy; signed installed/update tests cover distribution. Keep these labels separate.

Playwright's Electron support is an experimental API surface; verify its current limitations and the Electron version being launched. The launcher can require runtime behaviors that production fuses disable. Maintain a clearly separate test build where necessary, and inspect production fuses independently rather than weakening the release to suit a test harness.

## CI setup

Run as an appropriate non-root user with supported display/sandbox configuration. Do not add `--no-sandbox` as a permanent shortcut. Headless tests do not validate tray, native permission prompts, signing reputation, keychain dialogs, or all display-server behavior. Use per-platform runners and manual/device tests for those claims.

Isolate user-data/session directories per run. Control network responses and time where possible. Clean up application processes and temporary files even after failure. Record executable path, Electron/runtime version, OS/architecture, artifact hash, and test stage.

## Acceptance

Test denied sender/frame calls, malformed payloads, navigation/window-open denial, permission denial, missing assets, cleanup on window close, and the critical document workflow. Run the built app without the dev server. Test release update separately from a launch test. The bundle includes pure executable tests and an unexecuted integration specification; its validation report must not be interpreted as full Electron security or cross-platform certification.

## Evidence and navigation

Primary sources (reviewed 2026-10-15 unless marked as discovery pointers):

- [E26: Playwright Electron support](https://playwright.dev/docs/api/class-electron)
- [E27: Headless CI](https://www.electronjs.org/docs/latest/tutorial/testing-on-headless-ci)
- [E12: Fuses](https://www.electronjs.org/docs/latest/tutorial/fuses)
- [E01: Electron security checklist](https://www.electronjs.org/docs/latest/tutorial/security)

Procedures are original engineering recommendations. Verify API-specific changes against installed-version documentation.

[Topic index](00-index.md) · [Evidence policy](01-version-and-evidence.md) · [Source register](../SOURCES.md)
