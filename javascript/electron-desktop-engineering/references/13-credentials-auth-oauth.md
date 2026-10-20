# Credentials, safeStorage, OAuth, and session boundaries

**Read when:** storing secrets, authenticating a desktop app, or handling sign-in redirects.

## Credential authority

Keep long-lived secrets in a privileged owner and expose only the operations the renderer needs. A desktop application distributed to users cannot reliably hide an embedded OAuth client secret. Choose a public-client authentication flow supported by the identity provider, including its current PKCE, redirect, state, and nonce requirements as applicable; verify provider documentation before implementing.

Use an external system browser or a deliberately justified authentication surface. Bind the returned callback to the initiated request, expire it, and reject replay or unsolicited callbacks. A custom protocol URL is an untrusted external message, not proof that authentication succeeded. Do not put bearer credentials into application deep links, logs, analytics, or window titles.

## safeStorage limitations

Electron safeStorage integrates with platform-dependent protection. Check availability and selected backend; on Linux, a `basic_text` fallback may provide no meaningful confidentiality. Decide whether to refuse persistence, request a secure environment, or store only non-sensitive data in that state. Do not describe encryption as uniformly equivalent across all supported desktops.

Separate encrypted-at-rest storage from a compromised running process: main may still be able to decrypt values. Minimize retention, scope credentials, rotate/revoke where supported, and clear relevant sessions/caches on logout. Never send raw tokens through progress events for convenience.

## Acceptance

Test unavailable secure storage, locked keychain/keyring, first launch, logout, account switching, expired refresh credentials, replayed callbacks, and multiple simultaneous sign-in attempts. Inspect logs/crash payloads for secrets. Verify the release's actual OS/backend behavior rather than relying on a successful development machine. Document what remains accessible after renderer compromise and why each retained credential is necessary.

## Evidence and navigation

Primary sources (reviewed 2026-10-15 unless marked as discovery pointers):

- [E13: safeStorage](https://www.electronjs.org/docs/latest/api/safe-storage)
- [E10: Session API](https://www.electronjs.org/docs/latest/api/session)
- [E34: Deep linking](https://www.electronjs.org/docs/latest/tutorial/launch-app-from-url-in-another-app)
- [E01: Electron security checklist](https://www.electronjs.org/docs/latest/tutorial/security)

Procedures are original engineering recommendations. Verify API-specific changes against installed-version documentation.

[Topic index](00-index.md) · [Evidence policy](01-version-and-evidence.md) · [Source register](../SOURCES.md)
