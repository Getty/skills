# Hooks, effects, subscriptions, and resource ownership

**Read when:** effects loop, subscriptions leak, stale closures appear, or asynchronous work races.

## Decision sequence

First ask whether the operation derives a value: compute it during rendering. Then ask whether it responds to a user action: perform it in that event's workflow. Use an effect for synchronizing an external resource with committed React state. Model each effect as acquiring exactly one coherent resource and returning its release operation.

Include actual reactive dependencies. Repair unstable identities at their owner rather than silencing exhaustive-deps. A ref can hold imperative handles or latest non-rendering metadata, but changing it does not request a render. `useEffectEvent` is a version-gated way to separate non-reactive effect logic; it is not a general dependency escape hatch or an event-handler factory passed throughout the tree.

## Async safety

For a request owned by an effect, create an `AbortController`, pass its signal, and abort during cleanup. Also prevent obsolete completions from committing when an underlying operation cannot cancel. Distinguish cancellation from a user-visible failure. Never make the effect callback itself `async`: return cleanup synchronously and start the asynchronous operation inside it.

For external stores, prefer a subscription contract designed for React, with stable snapshots and unsubscribe behavior; use `useSyncExternalStore` where appropriate. For DOM observers, sockets, timers, and editor instances, assign a single owner and clean up listeners, observers, object URLs, and pending tasks. Keep render-time side effects out of constructors invoked during rendering.

## Failure tests

Mount, unmount, and remount; switch resource identity during an in-flight request; simulate a delayed response from the previous identity; reject a request; disconnect and reconnect. The invariant is one live resource per active owner and no stale state overwrite. Measure retained listeners and detached DOM after repeated cycles. See the included subscription hook example for an explicit cleanup contract.

## Evidence and navigation

Primary sources (reviewed 2026-10-15 unless marked as discovery pointers):

- [R04: Effects decision guide](https://react.dev/learn/you-might-not-need-an-effect)
- [R05: useEffectEvent](https://react.dev/reference/react/useEffectEvent)
- [R13: StrictMode](https://react.dev/reference/react/StrictMode)

Procedures are original engineering recommendations. Verify API-specific changes against installed-version documentation.

[Topic index](00-index.md) · [Evidence policy](01-version-and-evidence.md) · [Source register](../SOURCES.md)
