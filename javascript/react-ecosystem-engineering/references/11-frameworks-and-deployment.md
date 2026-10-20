# Framework selection and deployment boundaries

**Read when:** selecting a framework, adding SSR, or choosing deployment topology.

## Compare operational requirements

Evaluate initial content visibility, route data dependencies, SEO requirements, authenticated versus public pages, static export constraints, server hosting, streaming, edge/runtime restrictions, and team ownership. React itself does not dictate one router or deployment model. A framework is an operational commitment as well as a component API.

For Next.js, inspect whether the repository uses App Router or Pages Router, the exact version, rendering/cache choices, and server/client module boundaries. For React Router, identify Declarative, Data, or Framework mode before using loaders, actions, file routing, or build instructions. For TanStack Router/Start, distinguish the routing library from the full-stack framework and verify the selected adapter/version. For a Vite SPA, explicitly configure server fallback for deep links and cache invalidation for assets.

## Proposed decision experiment

Implement the same vertical slice: nested routes, authenticated loading, a mutation, validation failure, a slow dependency, and deployment. Measure total dependency/operational cost rather than only lines of UI code. Confirm that the target host actually supports the chosen server runtime, filesystem assumptions, and streaming behavior.

Do not include a Node server in a desktop product solely because a web tutorial used one. For Electron, prefer static renderer assets unless a real local service is needed; then model its listening interface, authentication, port conflicts, lifecycle, and update ownership separately.

## Delivery gate

Document route manifest, asset base path, runtime environment variables, secrets boundary, deep-link behavior, error pages, cache policy, and rollback. Test direct requests and reloads on nested routes, deployment behind a prefix, and an old browser tab loading a new release. Separate public build-time values from server secrets; a renamed environment variable is not protection once bundled into client JavaScript.

## Evidence and navigation

Primary sources (reviewed 2026-10-15 unless marked as discovery pointers):

- [R15: React Router modes](https://reactrouter.com/start/modes)
- [R16: TanStack Router overview](https://tanstack.com/router/latest/docs/overview)
- [R17: Next.js App Router](https://nextjs.org/docs/app)
- [R74: Vite](https://vite.dev/guide/)

Procedures are original engineering recommendations. Verify API-specific changes against installed-version documentation.

[Topic index](00-index.md) · [Evidence policy](01-version-and-evidence.md) · [Source register](../SOURCES.md)
