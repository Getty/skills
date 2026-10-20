# Server state: TanStack Query, SWR, and cache design

**Read when:** fetching remote data, handling mutations, or diagnosing repeated requests/stale results.

## Choose one owner

A remote cache manages snapshots, request lifetimes, invalidation, and mutation reconciliation. It is not a replacement for domain validation or an authorization layer. Prefer the application's established cache unless a different system serves a clearly separate boundary. Avoid mirroring its entire result into a local store through an effect.

TanStack Query and SWR both need deliberate key design and freshness policy. Do not equate `staleTime` with cache retention or assume stale data is immediately deleted. Review defaults for the installed generation, including retries, focus/reconnect behavior, and inactive-query cleanup. Name every response-shaping input in the key, including tenant and relevant locale; clear or partition caches on identity change.

## Request contract

Check HTTP status before accepting a response, parse the payload at the trust boundary, pass the supplied abort signal, and return stable domain data. Treat expected 404/empty state differently from transport failure. Use bounded retry with error classification; never retry authorization failures indefinitely. Ensure concurrent consumers share the intended request rather than constructing unique keys per render.

For mutations, specify invalidation scope, cache update strategy, temporary IDs, and conflict handling. A partial optimistic patch is safer than replacing a large stale snapshot. Infinite-query pagination needs stable cursors and a defined response to removed/duplicated rows. Persistence needs schema versions, data expiry, and a sensitive-data policy.

## Verification

Test cold, fresh, stale, offline, failed, and cancelled states. Change identities during a request and complete responses out of order. Inspect actual network calls when remounting and refocusing. Verify that cache restoration never exposes the previous user's data. The included query example is a source-reviewed integration sketch, not an installed-library compatibility test.

## Evidence and navigation

Primary sources (reviewed 2026-10-15 unless marked as discovery pointers):

- [R18: TanStack Query defaults](https://tanstack.com/query/latest/docs/framework/react/guides/important-defaults)
- [R19: SWR getting started](https://swr.vercel.app/docs/getting-started)

Procedures are original engineering recommendations. Verify API-specific changes against installed-version documentation.

[Topic index](00-index.md) · [Evidence policy](01-version-and-evidence.md) · [Source register](../SOURCES.md)
