# Navigation, new windows, external links, and downloads

**Read when:** opening links, embedding remote pages, or handling downloads.

## Default deny

Define permitted navigations per window role. Reject unexpected navigation and new-window requests before they turn a trusted surface into a different page. Consider main-frame navigation, redirects, frames, and child-window creation; do not rely on checking only the original `loadURL` argument. Never pass renderer-supplied BrowserWindow configuration through unchanged.

For external links, parse the URL and permit only required schemes/destinations. Compare exact hostnames and relevant port/path constraints; prefix matching accepts deceptive suffixes and user-info tricks. Reject credentials and ambiguous inputs. A fixed documentation URL may need no arbitrary URL argument at all. Avoid opening custom OS protocols unless the product explicitly supports them with user intent and validation.

## Downloads and content

A download is a file/security workflow, not merely a navigation result. Define source allowlist, destination selection, overwrite policy, filename sanitization, maximum size, cancellation, and post-download handling. Do not automatically execute downloaded content. Treat MIME/extension as hints rather than proof of safety.

Separate external browsing from the application session when it reduces credential/cookie exposure. Remote pages should not inherit the local privileged preload bridge. Explain user-visible transitions when leaving the app or opening a browser.

## Acceptance

Try `https://allowed.example.evil.test`, `https://allowed.example@evil.test`, unexpected ports, mixed case, encoded characters, `file:`, `javascript:`, and custom schemes. Attempt `window.open`, redirects, subframe navigation, and repeated prompts. Test denied downloads and cancellation without leaving partial sensitive files. Confirm production policy excludes localhost development origins and reports a clear, non-secret reason for a denied operation.

## Evidence and navigation

Primary sources (reviewed 2026-10-15 unless marked as discovery pointers):

- [E01: Electron security checklist](https://www.electronjs.org/docs/latest/tutorial/security)
- [E30: WebContents](https://www.electronjs.org/docs/latest/api/web-contents)
- [E29: BrowserWindow](https://www.electronjs.org/docs/latest/api/browser-window)

Procedures are original engineering recommendations. Verify API-specific changes against installed-version documentation.

[Topic index](00-index.md) · [Evidence policy](01-version-and-evidence.md) · [Source register](../SOURCES.md)
