# Constraint-driven stack recipes

**Read when:** proposing a coherent stack without assembling unnecessary dependencies.

## Internal CRUD application

Start from the existing router/framework. Use one remote-data cache, a form library only when validation/field complexity warrants it, and one UI system. Add a table/grid based on actual editing/scale needs. Put shareable filters in URL state, authorization in the backend, and record drafts in a form boundary. Acceptance: reload a filtered route, edit with validation failure, recover from expired login, and resolve a stale save.

## Workflow or topology editor

Use React Flow for the canvas, a pure domain graph model, a focused local store when coordination requires it, and a durable API for saved documents/execution. Add layout and collaboration as separate adapters. Keep inspectors/forms outside high-frequency canvas subscriptions. Acceptance: invalid connection rejection, import validation, undo transaction, stale-layout rejection, persistence round-trip, and recovery after a failed save.

## Public/content application

Evaluate a framework with the needed rendering/deployment model. Keep interactive client boundaries narrow and server data access explicit. Choose animation, rich media, and personalization only with budgets and fallback behavior. Acceptance: initial content, hydration, direct deep links, cache isolation, accessible navigation, and old-client/new-deployment behavior.

## Desktop application

Use React as the renderer, static assets where possible, and the Electron skill for process/security/distribution design. Keep platform data behind typed domain IPC, not Node imports in components. Acceptance: packaged production launch, denied untrusted bridge calls, multiple-window consistency, offline operation, and signed update recovery.

These are original starting recipes, not vendor-approved stacks or measured popularity rankings. Produce a dependency decision record with alternatives and removal cost. Adding Redux, Zustand, Jotai, XState, and multiple query caches simultaneously requires distinct documented ownership; a long dependency list is not architectural completeness.

## Evidence and navigation

Primary sources (reviewed 2026-10-15 unless marked as discovery pointers):

- [R15: React Router modes](https://reactrouter.com/start/modes)
- [R16: TanStack Router overview](https://tanstack.com/router/latest/docs/overview)
- [R17: Next.js App Router](https://nextjs.org/docs/app)
- [R18: TanStack Query defaults](https://tanstack.com/query/latest/docs/framework/react/guides/important-defaults)
- [R20: Redux Toolkit](https://redux.js.org/toolkit/introduction/getting-started)
- [R24: React Hook Form repository](https://github.com/react-hook-form/react-hook-form)
- [R31: Radix Primitives overview](https://www.radix-ui.com/primitives/docs/overview/introduction)
- [R32: shadcn/ui documentation](https://ui.shadcn.com/docs)
- [R40: TanStack Table](https://tanstack.com/table/latest)
- [R50: React Flow learning index](https://reactflow.dev/learn)

Procedures are original engineering recommendations. Verify API-specific changes against installed-version documentation.

[Topic index](00-index.md) · [Evidence policy](01-version-and-evidence.md) · [Source register](../SOURCES.md)
