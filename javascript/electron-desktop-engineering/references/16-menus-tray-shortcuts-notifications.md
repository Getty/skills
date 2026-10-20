# Menus, tray, shortcuts, notifications, clipboard, and desktop UX

**Read when:** adding OS integration or making the app behave like a desktop application.

## API discovery map

Electron provides APIs for native menus, tray, global shortcuts, notifications, clipboard, dialogs, and related desktop integration. The API atlas links the specific modules; inspect their current platform notes before implementation. Do not infer identical behavior or permissions across Windows, macOS, and Linux from one successful development test.

## Ownership and intent

Derive menu enabled/checked state from authoritative application state. Keep command IDs stable and route menu, keyboard, and renderer buttons through the same validated domain operation. Distinguish application-local shortcuts from global OS shortcuts; request only necessary global combinations and handle registration failure without hijacking alternatives silently.

Tray/background behavior must be explicit: closing a window, minimizing, and quitting are different user intents. Offer a discoverable quit command and do not retain hidden resource-heavy work unexpectedly. Notifications need privacy-aware content, actionable navigation, and correct behavior when the app is not ready.

For clipboard operations, validate supported formats and user intent. Clipboard contents are untrusted and may contain sensitive information. Avoid automatic monitoring or copying secrets. Native menu roles can preserve platform conventions where they fit; custom replacements should justify accessibility/behavior differences.

## Acceptance

Test keyboard layouts, shortcut conflicts, multiple displays, unavailable notification services, tray absence, app reactivation from a notification, and quit from every entry point. Verify menu state after window/document changes. Release global shortcuts/listeners on shutdown and restore state after restart. Record target-specific limitations rather than claiming a uniform desktop experience based on API availability alone.

## Evidence and navigation

Primary sources (reviewed 2026-10-15 unless marked as discovery pointers):

- [E28: App API](https://www.electronjs.org/docs/latest/api/app)
- [E29: BrowserWindow](https://www.electronjs.org/docs/latest/api/browser-window)
- [E30: WebContents](https://www.electronjs.org/docs/latest/api/web-contents)

Procedures are original engineering recommendations. Verify API-specific changes against installed-version documentation.

[Topic index](00-index.md) · [Evidence policy](01-version-and-evidence.md) · [Source register](../SOURCES.md)
