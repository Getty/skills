# React and React DOM API atlas

**Read when:** choosing a hook/API or checking whether a remembered pattern still fits the installed version.

## Hooks by responsibility

| Responsibility | APIs to inspect | Use boundary |
|---|---|---|
| Local state and transitions | `useState`, `useReducer` | Pure state transitions; functional updates; one owner |
| Shared context | `createContext`, `useContext` | Scoped dependencies; avoid broad frequently changing values |
| Imperative handles | `useRef`, `useImperativeHandle` | Non-rendering resource handles; expose minimal imperative surface |
| External synchronization | `useEffect`, `useLayoutEffect` | Acquire/release resources; layout effect only for justified pre-paint work |
| Styling infrastructure | `useInsertionEffect` | Specialized style-library integration, not general application effects |
| Effect-local nonreactive logic | `useEffectEvent` | Version gate; not a dependency-suppression device |
| Optimization | `useMemo`, `useCallback`, `memo` | Measure; never depend on optimization for correctness |
| Deferred presentation | `useTransition`, `startTransition`, `useDeferredValue` | Prioritize UI; not worker threads or arbitrary request cancellation |
| External stores | `useSyncExternalStore` | Stable snapshot and subscribe/unsubscribe contract, including SSR |
| Accessibility IDs | `useId` | Component relationship IDs, not domain/list identity |
| Action workflows | `useActionState`, `useOptimistic` | Explicit pending/reconciliation semantics and framework/version checks |
| Resources / context reads | `use` | Supported resource lifecycle; special call rules differ from ordinary hooks |
| Hook diagnostics | `useDebugValue` | Developer-tool labels for reusable hooks, not product state |

Do not mechanically replace every older pattern with an API from this table. Verify the installed runtime/types and the task-specific reference. A hook's availability does not establish that a particular framework or renderer supports the surrounding integration.

## Components and supporting APIs

Review `Fragment`, `StrictMode`, `Suspense`, lazy component loading, Context, and error-boundary class behavior according to the application. Version-gate `Activity` and React 19.3 `ViewTransition`/Fragment refs. Treat `Children`, `cloneElement`, and imperative ref composition as specialized tools; explicit props/composition are often easier to reason about. `forwardRef` remains relevant to compatibility with older consumer generations even when new React code can use ref props.

## React DOM boundaries

Use `createRoot` for client-owned roots and `hydrateRoot` for compatible server HTML. Assign root lifecycle to the application/host integration; do not create another root on every component render. Portals change DOM placement without creating an independent application ownership model. Review `createPortal` when overlays need a different container, preserving focus and event semantics.

`flushSync` is an exceptional synchronous escape hatch for justified integration constraints, not a routine fix for stale state. Server streaming/prerender APIs depend on the selected environment and framework; inspect pipeable versus readable-stream support and error/abort handling. Resource hints such as preload/preinit/preconnect should follow measured loading needs and framework ownership rather than being scattered through components.

The React DOM `useFormStatus` hook belongs inside the relevant form context; verify version/framework behavior. React 19.3 `browser()` belongs to `react-dom`, not `react`; use it only for an intentional server fallback/client-only boundary. Test these integrations with the actual renderer and type declarations, not syntax transpilation alone.

## Acceptance

For any selected API, state why a simpler existing mechanism is insufficient, which version enables it, what owns its lifecycle, and which failure path is tested. Avoid importing experimental/canary APIs into a stable project without explicit authorization and a compatibility plan.

## Evidence and navigation

Primary sources (reviewed 2026-10-15 unless marked as discovery pointers):

- [R01: React reference](https://react.dev/reference/react)
- [R02: React 19.3 release](https://react.dev/blog/2026/09/09/react-19-3)
- [R03: React Compiler 1.0](https://react.dev/blog/2025/10/07/react-compiler-1)
- [R05: useEffectEvent](https://react.dev/reference/react/useEffectEvent)
- [R06: Activity](https://react.dev/reference/react/Activity)
- [R07: useActionState](https://react.dev/reference/react/useActionState)
- [R08: useOptimistic](https://react.dev/reference/react/useOptimistic)
- [R09: use](https://react.dev/reference/react/use)
- [R10: Server Components](https://react.dev/reference/rsc/server-components)
- [R11: hydrateRoot](https://react.dev/reference/react-dom/client/hydrateRoot)
- [R12: React TypeScript guide](https://react.dev/learn/typescript)

Procedures are original engineering recommendations. Verify API-specific changes against installed-version documentation.

[Topic index](00-index.md) · [Evidence policy](01-version-and-evidence.md) · [Source register](../SOURCES.md)
