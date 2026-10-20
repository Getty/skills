# SSR, streaming, hydration, and Server Components

**Read when:** server-rendering a React app, diagnosing hydration, or adding Server Components.

## Separate the mechanisms

SSR produces initial HTML. Hydration attaches client behavior to compatible initial output. Server Components define a server/client module and serialization architecture supplied by an RSC-aware framework/toolchain. They are related but not interchangeable. A `'use client'` boundary is not a declaration that its component can never participate in initial server rendering.

Keep database credentials and privileged modules behind server-only boundaries. Send the minimum serializable information required by the UI. Treat server-callable actions as externally invocable operations requiring validation and authorization. Do not assume hiding a button or importing a server function through a framework provides access control.

## Hydration investigation

Compare server output and the first client render using identical inputs. Check time, random values, locale/time zone, generated IDs, invalid HTML nesting, browser-only branching, user-specific caches, and third-party DOM mutation. Fix the cause rather than suppressing hydration warnings globally. Use stable request-scoped data and isolate client-only features intentionally.

Define streaming boundaries and error behavior before headers are committed. Per-request stores and caches must not leak one user's state to another. Inspect cache keys, revalidation, tag invalidation, and mutation visibility in the specific framework version; do not transfer caching assumptions between Next.js releases or router modes.

## Security and verification

Inventory the framework and all transitive RSC transport packages. Check current advisories and patched versions, including follow-up issues; an old initial fix is not a perpetual guarantee. Test a direct deep-link request, hydration after a slow response, expired sessions, navigation between tenants, and a deployment with stale client chunks. Keep request IDs across server logs and client errors while excluding secrets and private payloads.

## Evidence and navigation

Primary sources (reviewed 2026-10-15 unless marked as discovery pointers):

- [R10: Server Components](https://react.dev/reference/rsc/server-components)
- [R11: hydrateRoot](https://react.dev/reference/react-dom/client/hydrateRoot)
- [R14: RSC security follow-up](https://react.dev/blog/2025/12/11/denial-of-service-and-source-code-exposure-in-react-server-components)
- [R17: Next.js App Router](https://nextjs.org/docs/app)

Procedures are original engineering recommendations. Verify API-specific changes against installed-version documentation.

[Topic index](00-index.md) · [Evidence policy](01-version-and-evidence.md) · [Source register](../SOURCES.md)
