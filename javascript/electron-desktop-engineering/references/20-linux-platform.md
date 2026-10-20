# Linux distributions, display systems, packaging, and secure storage

**Read when:** targeting Linux or diagnosing differences across desktop environments.

## Define support rather than saying “Linux”

Record distributions/versions, architectures, libc/toolchain requirements, package formats, display environments, and desktop integration expectations. Validate the chosen Electron release's supported targets. X11, Wayland, desktop portals, keyring services, tray support, and notification behavior can differ; build an explicit test matrix rather than assuming one desktop represents all installations.

## Packaging and runtime

Choose AppImage, distribution packages, sandboxed distribution channels, or another supported strategy based on deployment ownership. Their filesystem permissions, dependencies, update mechanisms, and integration differ. A core Electron updater recipe for another platform does not establish Linux update support. Prefer the distribution's update owner when appropriate and avoid two independent systems replacing the same installation.

Keep Chromium sandboxing enabled. Running as root or using a poorly configured CI container is not a reason to ship `--no-sandbox`. Investigate the supported user/container sandbox setup and separate test infrastructure failures from application requirements.

## Secrets and native features

Check safeStorage's actual backend; Linux `basic_text` fallback must not be advertised as strong protection. Define secure-storage-unavailable behavior. Test native modules, shared-library resolution, file permissions, locale/font availability, and screen capture through the intended environment. Handle unavailable tray/global shortcut/notification features gracefully.

## Acceptance

Launch packaged artifacts on clean supported distributions with a standard user. Test Wayland/X11 as claimed, proxy/certificate configuration, missing keyring, offline startup, update ownership, and uninstall. Exercise screen capture and file dialogs in the real desktop/portal context. Record unsupported combinations explicitly; a successful headless smoke test does not validate every desktop interaction or security control.

## Evidence and navigation

Primary sources (reviewed 2026-10-15 unless marked as discovery pointers):

- [E02: Electron support timelines](https://www.electronjs.org/docs/latest/tutorial/electron-timelines)
- [E13: safeStorage](https://www.electronjs.org/docs/latest/api/safe-storage)
- [E27: Headless CI](https://www.electronjs.org/docs/latest/tutorial/testing-on-headless-ci)
- [E18: Electron performance](https://www.electronjs.org/docs/latest/tutorial/performance)

Procedures are original engineering recommendations. Verify API-specific changes against installed-version documentation.

[Topic index](00-index.md) · [Evidence policy](01-version-and-evidence.md) · [Source register](../SOURCES.md)
