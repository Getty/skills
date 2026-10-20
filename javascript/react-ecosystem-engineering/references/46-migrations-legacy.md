# Migration planning and legacy React maintenance

**Read when:** upgrading React/libraries, retiring obsolete patterns, or modernizing an older app.

## Separate migration axes

Inventory runtime/renderers, router mode, state/cache libraries, styling, test environment, build tooling, and framework/server boundaries. Create a compatibility matrix before changing versions. Treat a React upgrade, router-major migration, CSS-framework upgrade, and data-model rewrite as independent changes unless evidence demands otherwise.

Old patterns are not automatically defects. Class components and existing reducers can be maintained while new code follows current conventions. Prioritize security/support exposure and measured maintenance pain. Do not rewrite a stable feature solely to replace every class or effect with a newer API.

## Procedure

Freeze a known-good behavioral baseline with tests and representative screenshots. Read official migration notes for every crossed major. Apply mechanical codemods in isolated commits, inspect their diff, then handle semantic changes manually. Record removed APIs, altered defaults, provider/configuration changes, and behavior that requires product decisions.

React Flow's package rename and v12 geometry/parent changes require a focused migration; copying old `reactflow` imports into a new `@xyflow/react` app is not a harmless spelling issue. Similarly, current dnd kit and TanStack Table examples must match their selected generation. Keep a temporary compatibility adapter at one boundary and define when it will be removed.

## Acceptance and rollback

Run clean install, typecheck, lint, unit/component tests, browser smoke, SSR where relevant, and packaged Electron checks for shared code. Compare bundle/startup/interaction budgets. Exercise old persisted data and mixed client/server deployment versions. Prepare a rollback that includes data compatibility, not only reverting package.json. Document unresolved warnings explicitly and do not declare an upgrade complete because the development server starts.

## Evidence and navigation

Primary sources (reviewed 2026-10-15 unless marked as discovery pointers):

- [R01: React reference](https://react.dev/reference/react)
- [R02: React 19.3 release](https://react.dev/blog/2026/09/09/react-19-3)
- [R03: React Compiler 1.0](https://react.dev/blog/2025/10/07/react-compiler-1)
- [R15: React Router modes](https://reactrouter.com/start/modes)
- [R58: React Flow v12 migration](https://reactflow.dev/learn/troubleshooting/migrate-to-v12)

Procedures are original engineering recommendations. Verify API-specific changes against installed-version documentation.

[Topic index](00-index.md) · [Evidence policy](01-version-and-evidence.md) · [Source register](../SOURCES.md)
