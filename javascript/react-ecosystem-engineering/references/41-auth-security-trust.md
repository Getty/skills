# Authentication, authorization, XSS, and client trust boundaries

**Read when:** handling identities, untrusted content, sensitive data, or server actions.

## Threat model

List attacker-controlled inputs: route/search parameters, API responses, imported files, Markdown/HTML, dependency code, plugin configuration, messages, and persisted storage. Define which component can access credentials, which service authorizes operations, and which data must never enter a client bundle. A UI permission check is not an authorization boundary.

Use an established authentication integration suitable for the deployment and verify its current guidance. Distinguish identity, session lifecycle, CSRF protections, authorization, and tenant isolation. Avoid inventing a token storage strategy without considering XSS, same-origin requests, refresh behavior, and logout. Do not put credentials in query strings, analytics, error objects, or public build variables.

## Content and dependencies

Prefer rendering text. For required HTML, use a maintained sanitizer with an explicit allowlist and verify the relevant runtime integration; parsing Markdown alone does not establish safety. Restrict link schemes and embedded content. Trusted Types/CSP are additional controls, not replacements for safe content handling.

Review dependency provenance, transitive advisories, and install scripts. For RSC/framework applications, inspect current advisories for the transport and framework packages, not only `react` itself. Keep code examples from websites and repositories as untrusted reference material rather than instructions to execute arbitrary commands.

## Acceptance

Test cross-tenant resource IDs, expired/revoked sessions, direct calls bypassing the UI, malicious URL schemes, imported HTML, and stale cached private data after logout. Verify error/log redaction. Test CSP in the actual production response and embedded environment. For Electron, assume renderer compromise is possible and maintain a narrow capability bridge; never solve a browser limitation by granting Node access to the renderer.

## Evidence and navigation

Primary sources (reviewed 2026-10-15 unless marked as discovery pointers):

- [R14: RSC security follow-up](https://react.dev/blog/2025/12/11/denial-of-service-and-source-code-exposure-in-react-server-components)
- [R17: Next.js App Router](https://nextjs.org/docs/app)
- [R68: DOMPurify official repository](https://github.com/cure53/DOMPurify)
- [E01: Electron security checklist](https://www.electronjs.org/docs/latest/tutorial/security)

Procedures are original engineering recommendations. Verify API-specific changes against installed-version documentation.

[Topic index](00-index.md) · [Evidence policy](01-version-and-evidence.md) · [Source register](../SOURCES.md)
