# Custom protocols, CSP, asset routing, and origin design

**Read when:** serving packaged assets, avoiding file:// pitfalls, or enforcing CSP.

## Protocol lifecycle

Register scheme privileges before application readiness as required by Electron. Register handlers on the actual session used by the window; a custom partition does not automatically share every default-session handler. Grant only needed privileges and never use a bypass-CSP privilege to repair an asset-loading problem.

Design one application origin and an explicit resource map. Prefer an immutable packaged asset allowlist over mapping arbitrary URL paths to the filesystem. For dynamic mapping, validate URL structure, decoding, containment, symlinks, method, MIME, and resource size; simple string-prefix path checks are unsafe. Do not serve user-writable files as trusted application scripts.

## CSP policy

Start restrictive: no arbitrary script origins, no eval, no object embeds, explicit connection destinations, and no unintended framing/forms. Put scripts in bundled files rather than inline HTML. Allow only the style mechanisms actually required; React Flow and similar components use dynamic inline geometry, so their production policy needs a documented style-specific allowance without weakening script restrictions.

Set content types and relevant security headers on responses. Decide how unknown routes behave: a SPA fallback must not return index.html as every missing script/worker file. Restrict methods and reject unexpected hosts, ports, credentials, and query behavior. An origin label alone is not enough when authorizing privileged IPC; bind the expected page/frame too.

## Acceptance

Test direct page load, missing assets, encoded path traversal, double encoding, credentials/ports, unsupported methods, and a custom session partition. Verify CSP violations for injected scripts while normal application assets function. Test worker, font, image, and WASM loading as shipped. The example uses a fixed asset map specifically to avoid exposing a general filesystem server.

## Evidence and navigation

Primary sources (reviewed 2026-10-15 unless marked as discovery pointers):

- [E09: Protocol API](https://www.electronjs.org/docs/latest/api/protocol)
- [E01: Electron security checklist](https://www.electronjs.org/docs/latest/tutorial/security)
- [E10: Session API](https://www.electronjs.org/docs/latest/api/session)

Procedures are original engineering recommendations. Verify API-specific changes against installed-version documentation.

[Topic index](00-index.md) · [Evidence policy](01-version-and-evidence.md) · [Source register](../SOURCES.md)
