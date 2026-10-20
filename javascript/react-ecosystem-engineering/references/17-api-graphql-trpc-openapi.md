# API clients: REST, GraphQL, tRPC, and generated contracts

**Read when:** integrating a backend, choosing an API client, or generating typed contracts.

## Select by backend contract

REST/OpenAPI clients fit independently deployed services and language boundaries; GraphQL clients add operation-centric data access and potentially normalized entity caching; tRPC fits an end-to-end TypeScript contract under compatible deployment ownership. These are architecture choices, not evidence that runtime validation or authorization is optional.

Apollo Client and Relay have different operation, cache, and build workflows. Inspect the existing project before introducing a second normalized cache. Relay's compiler/fragment conventions should not be approximated by ad-hoc queries. For tRPC, verify the current client integration and its query adapter in the installed major; older React Query setup snippets may not match the selected adapter. urql and code-generation tools are catalog discovery options requiring a separate version check.

## Boundary design

Parse external values even when types were generated. Decide how missing versus null fields, enums extended by the server, partial errors, date/time strings, and pagination tokens are represented. Bound response sizes and avoid including sensitive input in URLs or logs. Propagate cancellation, request IDs, authentication renewal, and retry policy through one client boundary.

For GraphQL normalized caches, define entity identity and field policies before optimistic updates. Prevent cross-tenant entity collisions. Treat schema introspection/code generation as a build input with controlled provenance, not arbitrary instructions downloaded from a service.

## Acceptance

Test a server enum unknown to the client, partial GraphQL data with errors, expired credentials, duplicate mutation retries, stale pagination cursors, and a backend/client version skew. Verify the generated client is reproducible in CI. Keep domain objects separate from transport structures when server changes should not spread through every component. Document which validations belong at the client for UX and which must be repeated at the backend for trust.

## Evidence and navigation

Primary sources (reviewed 2026-10-15 unless marked as discovery pointers):

- [R27: Apollo Client React](https://www.apollographql.com/docs/react)
- [R28: Relay](https://relay.dev/docs/)
- [R29: tRPC documentation overview](https://trpc.io/docs/)
- [R25: Zod](https://zod.dev/)

Procedures are original engineering recommendations. Verify API-specific changes against installed-version documentation.

[Topic index](00-index.md) · [Evidence policy](01-version-and-evidence.md) · [Source register](../SOURCES.md)
