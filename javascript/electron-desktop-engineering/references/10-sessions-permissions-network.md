# Sessions, permissions, cookies, proxies, and networking

**Read when:** separating accounts, granting device access, using proxies, or troubleshooting requests.

## Session ownership

Choose persistent versus ephemeral session partitions deliberately. Record which windows share cookies/cache/storage and which must be isolated by tenant, account, or trust level. Switching a visible account label is not sufficient isolation if old session state remains. Define logout cleanup and recovery without deleting unrelated user data.

Set both permission-check and permission-request policies as applicable to the installed API. Deny by default and allow only a named permission, expected origin/frame, application context, and user-approved operation. Avoid a global callback returning true. Device selection, display capture, and OS privacy prompts may have separate API and platform requirements.

## Network contract

Distinguish Chromium session networking, Electron `net`, renderer fetch, and Node HTTP libraries. They may not automatically share cookie/proxy/certificate behavior. Choose the boundary based on required session integration and credential ownership. Do not move a request into main merely to bypass CORS; authenticate and constrain it as a privileged operation.

Respect enterprise proxy and certificate requirements without introducing blanket TLS bypasses. Keep debugging overrides out of production. Sanitize network diagnostics and redact headers, cookies, tokens, and sensitive URLs. Bound retries, timeouts, response sizes, and concurrent requests.

## Acceptance

Test two isolated sessions, sign-out/sign-in, permission denial/revocation, corporate proxy behavior, offline mode, captive-portal-like errors, expired certificates, and cache cleanup. Verify both permission query and request paths. Inspect the actual packaged app because development servers and host Node requests may not exercise Chromium's session policy. Document exactly which credentials/cookies are attached to each request path.

## Evidence and navigation

Primary sources (reviewed 2026-10-15 unless marked as discovery pointers):

- [E10: Session API](https://www.electronjs.org/docs/latest/api/session)
- [E32: Networking](https://www.electronjs.org/docs/latest/api/net)
- [E01: Electron security checklist](https://www.electronjs.org/docs/latest/tutorial/security)

Procedures are original engineering recommendations. Verify API-specific changes against installed-version documentation.

[Topic index](00-index.md) · [Evidence policy](01-version-and-evidence.md) · [Source register](../SOURCES.md)
