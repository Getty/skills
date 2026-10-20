# Redux Toolkit and RTK Query

**Read when:** working in a Redux application or evaluating predictable cross-feature state.

## Keep responsibilities explicit

Use Redux Toolkit conventions for application-owned shared state and RTK Query where its endpoint/cache integration fits. Keep transient hover/input state local unless other features genuinely coordinate it. Do not copy RTK Query's remote entity snapshots into arbitrary slices merely to make them easier to access.

Design domain events and normalized identifiers before reducers. Reducer logic should express valid state transitions and remain free of I/O. Middleware, thunks, or listener-based orchestration can own effects depending on the installed Toolkit surface. Selectors should return focused data and preserve identity where useful; subscribing a large screen to the whole root defeats isolation.

## Implementation review

Record store construction, middleware order, serializability expectations, persistence boundaries, and SSR request isolation. A singleton server store can cross user boundaries. Keep sockets, DOM nodes, AbortControllers, and platform objects outside serializable domain state unless a documented exception has a lifecycle owner. Avoid placing credentials in development-visible action payloads or persisted state.

For RTK Query, define endpoints around resource identity, tag invalidation around actual relationships, and mutation behavior around canonical server responses. Separate request parameters from local visual state. Review subscription lifetime, polling, and focus/reconnect behavior rather than enabling background work indiscriminately.

## Test and migrate

Test reducer transitions as pure units, selectors against representative normalized data, and endpoint behavior using a controlled network boundary. Verify optimistic rollback under overlapping mutations. When migrating legacy Redux, first preserve externally visible behavior, then replace boilerplate incrementally; do not combine state-model changes with transport/cache changes unless the acceptance tests cover both. Measure bundle and debugging needs before replacing an already coherent store solely to follow a newer trend.

## Evidence and navigation

Primary sources (reviewed 2026-10-15 unless marked as discovery pointers):

- [R20: Redux Toolkit](https://redux.js.org/toolkit/introduction/getting-started)

Procedures are original engineering recommendations. Verify API-specific changes against installed-version documentation.

[Topic index](00-index.md) · [Evidence policy](01-version-and-evidence.md) · [Source register](../SOURCES.md)
