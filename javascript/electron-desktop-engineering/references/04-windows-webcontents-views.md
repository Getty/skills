# BrowserWindow, WebContents, WebContentsView, and embedded content

**Read when:** adding multiple windows, tabs, embedded pages, or window controls.

## Choose the surface deliberately

BrowserWindow manages a native window; WebContents represents its web content. Current Electron documentation deprecates BrowserView in favor of WebContentsView. The `webview` tag is not the default recommended embedding strategy. Evaluate trust, lifecycle, session separation, focus, accessibility, and ownership before choosing an embedded-content mechanism.

Keep untrusted remote content separate from the privileged local application surface and never grant it the application's bridge. A trusted wrapper does not make everything it embeds trusted. Set explicit policies for navigation, window creation, downloads, permissions, and session data for each content surface.

## Window architecture

Keep a registry of application-owned windows with role, allowed origin/page, session partition, bridge capabilities, and shutdown behavior. Grant the minimum interface required by each role. Use one validated dispatcher rather than accepting arbitrary BrowserWindow option objects from a renderer.

Persist window bounds as untrusted preferences: validate finite numbers, minimum/maximum size, and visibility on the current display arrangement. Recover gracefully after a monitor is removed or scaling changes. Frameless/titlebar customization must preserve drag regions, interactive controls, keyboard access, and platform conventions.

## Acceptance

Open/close windows repeatedly, move them between displays, change scale, remove a display, and restart with old bounds. Test focus restoration between views and native dialogs. Deny unexpected `window.open` and navigation attempts, including subframes. Ensure WebContents and listeners are disposed when their owner is destroyed. Do not assume destroying a wrapper view automatically terminates every related background job or child process.

## Evidence and navigation

Primary sources (reviewed 2026-10-15 unless marked as discovery pointers):

- [E29: BrowserWindow](https://www.electronjs.org/docs/latest/api/browser-window)
- [E30: WebContents](https://www.electronjs.org/docs/latest/api/web-contents)
- [E11: WebContentsView](https://www.electronjs.org/docs/latest/api/web-contents-view)
- [E38: webview tag](https://www.electronjs.org/docs/latest/api/webview-tag)
- [E39: BrowserView deprecation](https://www.electronjs.org/docs/latest/api/browser-view)

Procedures are original engineering recommendations. Verify API-specific changes against installed-version documentation.

[Topic index](00-index.md) · [Evidence policy](01-version-and-evidence.md) · [Source register](../SOURCES.md)
