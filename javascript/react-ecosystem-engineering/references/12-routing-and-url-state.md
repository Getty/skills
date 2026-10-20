# Routing, loaders, navigation, and URL state

**Read when:** adding routes, filters, navigation guards, or typed search parameters.

## Version and mode gate

React Router exposes Declarative, Data, and Framework modes with different integration surfaces; the inspected current selector was 8.4.0. TanStack Router provides a separate typed routing approach. Read the installed declarations and chosen mode before importing an API. Do not combine a Framework-mode example with a plain declarative router and assume all loading behavior is available.

## State contract

Put bookmarkable location, sort, pagination, and shareable filters in validated URL state. Define canonical serialization: omitted defaults, repeated values, empty strings, invalid enums, and bounded numeric ranges. Keep credentials, oversized drafts, and sensitive records out of URLs. Distinguish a navigation that should push history from a transient filter edit that should replace it.

Align data fetching with route identity. Forward cancellation where supported and avoid fetching the same resource independently in both a loader and a query hook without an explicit cache bridge. Preloading must respect authorization and data sensitivity. A route guard improves UX but does not authorize backend requests.

## Navigation UX

Define focus movement after navigation, document titles, nested error boundaries, pending indicators, scroll restoration, and unsaved-draft behavior. A modal route needs a direct-link fallback and predictable browser-back behavior. Preserve drafts intentionally during route changes rather than depending on accidental component identity.

## Tests

Load a nested URL directly; change search parameters rapidly; navigate backward and forward; paste an invalid enum; switch tenant/user; encounter an expired session; cancel a slow navigation. Confirm that restored URL state and displayed data agree. Exercise base-path deployments and, in Electron, the packaged custom-protocol URL rather than only a development HTTP server.

## Evidence and navigation

Primary sources (reviewed 2026-10-15 unless marked as discovery pointers):

- [R15: React Router modes](https://reactrouter.com/start/modes)
- [R16: TanStack Router overview](https://tanstack.com/router/latest/docs/overview)

Procedures are original engineering recommendations. Verify API-specific changes against installed-version documentation.

[Topic index](00-index.md) · [Evidence policy](01-version-and-evidence.md) · [Source register](../SOURCES.md)
