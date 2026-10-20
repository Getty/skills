# Build systems, monorepos, package exports, and CI

**Read when:** configuring Vite, building a component package, or managing workspaces.

## Reproducible inputs

Respect the repository's package manager and lockfile. Pin the toolchain through its existing mechanism and use frozen/immutable installs in CI. Review package lifecycle scripts before running newly introduced dependencies. Environment variables intended for the browser are public once bundled; keep secrets in a server or privileged process.

For monorepos, map application and library boundaries, dependency direction, workspace resolution, and build order. Avoid duplicate React installations caused by incorrectly packaged shared UI. A reusable React package generally needs an intentional peer-dependency policy and an export map tested by a separate consumer; do not bundle a private React copy by accident.

## Build contract

Separate typechecking, linting, tests, production build, and smoke tests; a fast transform is not a typecheck. Test emitted declarations and ESM/CJS expectations against supported consumers. Inspect CSS/assets/worker paths, side-effect declarations, tree-shaking behavior, and source-map publication. Keep environment-specific entry points from leaking Node imports into browser bundles.

Code splitting needs failure recovery and asset-cache consistency. Publish immutable hashed assets with a deliberate HTML/cache policy. A stale tab may request a removed chunk after deployment; provide a recoverable update experience rather than a permanent blank screen.

## Acceptance

Install and build from a clean checkout, consume local packages through packed artifacts, load a nested route behind the production base path, and run the critical browser workflow. Inspect licenses and bundle composition. Record build outputs and checksums where appropriate. Do not claim a reproducible or air-gapped build merely because the source compiles once; document registry/cache requirements and any native/platform-specific build inputs.

## Evidence and navigation

Primary sources (reviewed 2026-10-15 unless marked as discovery pointers):

- [R74: Vite](https://vite.dev/guide/)
- [R12: React TypeScript guide](https://react.dev/learn/typescript)
- [R70: Vitest](https://vitest.dev/guide/)
- [R71: Playwright](https://playwright.dev/docs/intro)

Procedures are original engineering recommendations. Verify API-specific changes against installed-version documentation.

[Topic index](00-index.md) · [Evidence policy](01-version-and-evidence.md) · [Source register](../SOURCES.md)
