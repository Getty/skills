# Project layout, TypeScript, bundling, and ESM/CJS

**Read when:** creating a project, fixing preload imports, or configuring build output.

## Separate compilation targets

Use distinct main, preload, renderer, and shared-contract boundaries. Main targets Electron's embedded Node environment; renderer targets Chromium without Node imports; preload has a constrained execution environment. Shared contracts contain serializable types/schemas and no implicit privileged module side effects. A browser bundle should fail when it imports `fs`, `child_process`, or a main-only credential module.

## Module-format gate

Electron's ESM behavior differs across main, preload, and renderer. Inspect the current documentation and package `type`, output extensions, bundler transformations, and sandbox options. Do not assume that because main is ESM the sandboxed preload can load arbitrary ESM or relative CommonJS modules the same way.

A sandboxed preload has a restricted `require` surface. Bundle it into a self-contained supported output, commonly one `.cjs` file, or deliberately keep it self-contained. Splitting it into relative CommonJS files without validating loader behavior can make the bridge disappear in production. The supplied secure-shell preload intentionally has no relative imports.

## Build layout

Resolve preload and asset paths from the built application location, not the developer's working directory. Map development and packaged paths explicitly. Keep `electron` external where the selected main/preload bundler requires it; do not accidentally bundle a browser shim for a privileged module. Configure source maps with a privacy/publication policy.

## Acceptance

Inspect emitted files and import graphs. Run typechecks for each target, then launch the built app without the development server. Verify the preload loaded, the bridge is present, no Node globals exist in the renderer, and renderer assets/workers resolve under the packaged protocol. Test a path containing spaces/non-ASCII characters and a production installation location. A successful Vite hot reload is not a packaged preload test.

## Evidence and navigation

Primary sources (reviewed 2026-10-15 unless marked as discovery pointers):

- [E08: ES modules](https://www.electronjs.org/docs/latest/tutorial/esm)
- [E05: Context isolation](https://www.electronjs.org/docs/latest/tutorial/context-isolation)
- [E06: Process sandboxing](https://www.electronjs.org/docs/latest/tutorial/sandbox)
- [E23: Forge Vite plugin](https://www.electronforge.io/config/plugins/vite)
- [E25: electron-vite](https://electron-vite.org/guide/)

Procedures are original engineering recommendations. Verify API-specific changes against installed-version documentation.

[Topic index](00-index.md) · [Evidence policy](01-version-and-evidence.md) · [Source register](../SOURCES.md)
