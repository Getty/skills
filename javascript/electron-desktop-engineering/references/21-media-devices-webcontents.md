# Media, screen capture, devices, printing, and WebContents features

**Read when:** adding screen sharing, camera/microphone, device access, printing, or PDF export.

## Permission and user-intent flow

Identify the exact resource, requesting window/frame/origin, purpose, and user action. Apply Electron permission policy and the platform's OS-level requirements independently. Deny by default and handle denial/revocation as normal states. Avoid exposing all sources/devices simply because a renderer requests them.

For screen capture, inspect the current desktopCapturer/session flow and platform constraints. Distinguish choosing a source, granting capture, capturing audio, and the OS privacy permission. Do not reuse a stale source ID indefinitely or log sensitive window titles/screenshots by default. Provide a visible stop indicator and release streams/tracks on completion.

## Printing and document generation

Use explicit options for paper size, margins, orientation, background graphics, and page ranges. Treat HTML/template input as untrusted content with its own CSP/isolation needs. Keep generated output paths main-owned or selected through a validated dialog. Preview/render completion and successful file writing are separate outcomes.

For devices, restrict selection and remember grants only within a deliberate identity/lifetime model. A device identifier is not permission to perform arbitrary operations forever. Long-running media work needs resource and cancellation budgets.

## Acceptance

Test first grant, denial, OS-level revocation, device unplug, source disappearance, minimized/closed windows, multiple displays, and app suspension/resume. Test printing offline/unavailable printer and PDF output with long/RTL content. Run on each supported platform with the installed artifact; a browser API existing in Chromium does not establish identical permissions or capabilities across all Electron/OS combinations.

## Evidence and navigation

Primary sources (reviewed 2026-10-15 unless marked as discovery pointers):

- [E33: Desktop capture](https://www.electronjs.org/docs/latest/api/desktop-capturer)
- [E10: Session API](https://www.electronjs.org/docs/latest/api/session)
- [E30: WebContents](https://www.electronjs.org/docs/latest/api/web-contents)

Procedures are original engineering recommendations. Verify API-specific changes against installed-version documentation.

[Topic index](00-index.md) · [Evidence policy](01-version-and-evidence.md) · [Source register](../SOURCES.md)
