# React 19.3 adoption and older-version compatibility

**Read when:** using newer React APIs or updating an older skill/example.

## Snapshot-specific facts

The official September 9, 2026 release announces stable `ViewTransition` and Fragment refs, `addTransitionType`, `browser()` from `react-dom`, Trusted Types interoperability, and direct rendering in Server Components of Context imported from a client module. These features must not be labeled canary merely because an older article says so. Conversely, do not backport their syntax into a project on an older React runtime or type package.

## Adoption procedure

Update React and its renderer as a compatible pair through the repository's normal dependency process. Inspect framework support, type declarations, lint rules, and testing utilities. Adopt one feature at a time with an explicit fallback and rollback commit. Do not combine a framework-major upgrade, compiler rollout, state-library rewrite, and animation redesign into one unreviewable change.

For view transitions, define which changes are non-urgent, preserve reduced-motion behavior, and test interrupted navigation and focus. Do not animate a loading placeholder so slowly that it delays useful feedback. For Fragment refs, validate the public instance methods and null/cleanup lifecycle; it is not a promise of a single wrapper DOM element.

For browser-only rendering, test both the server fallback and client reveal. `use(browser())` requires the corresponding release and an intentional Suspense boundary; it is not a general solution for avoidable hydration nondeterminism. Trusted Types support is interoperability, not automatic sanitization: policy creation must still be restrictive and reviewed.

## Compatibility output

Add a small table to the change record: feature, minimum installed runtime/type support, framework gate, fallback, tests executed, and rollback. Keep legacy compatibility wrappers at one boundary with an expiry condition. Do not spread version checks throughout application components. Record exactly which APIs were actually exercised rather than asserting complete React 19.3 compatibility.

## Evidence and navigation

Primary sources (reviewed 2026-10-15 unless marked as discovery pointers):

- [R02: React 19.3 release](https://react.dev/blog/2026/09/09/react-19-3)
- [R01: React reference](https://react.dev/reference/react)

Procedures are original engineering recommendations. Verify API-specific changes against installed-version documentation.

[Topic index](00-index.md) · [Evidence policy](01-version-and-evidence.md) · [Source register](../SOURCES.md)
