# Discovery, tags, pagination, and catalog limitations

> Read when: listing registry content or building inventory/retention tooling.

`/v2/_catalog` is not a universal inventory interface across all hosted registries or permission configurations. It can be restricted, unsupported, paginated, or affected by proxy/cache behavior. A cache's empty initial catalog is plausible; an empty result after expected pulls is a condition to investigate, not a permanent healthy-state requirement.

Use a known repository/tag/digest as the first connectivity test. `/v2/` returning 200 proves an unauthenticated API response; 401 with a valid challenge can prove an authenticated endpoint is present. Neither proves that a particular manifest and all its blobs are readable.

## Pagination discipline

Follow documented pagination links/markers for repository and tag listing. Preserve query state, bound iteration, and deduplicate names across pages. Do not assume the first page contains all content. Tags can change during traversal; an inventory of a live registry is not an atomic snapshot.

Empty arrays, null fields, unsupported endpoints, authorization filtering, and true absence are different outcomes. Surface them separately. Keep pagination regression tests, especially where one repository/tag name is a prefix of another; release notes have addressed real listing issues.

## Retention inventory

Combine repository discovery, tag-to-digest resolution, index traversal, and artifact/referrer discovery. Obtain an authoritative repository list from the owning platform when catalog access is unavailable. An inventory account should have enough visibility for safe decisions; a restricted account returning “nothing” must not become a reason to delete underlying storage.

For backup/recovery or compliance, list operations alone do not verify content integrity. Sample or fully verify manifests and blob digest reachability according to the assurance requirement. Keep the inventory timestamp, auth scope, pagination completion state, and endpoint version in the report.

## Primary sources

- [Distribution HTTP API V2](https://distribution.github.io/distribution/spec/api/)
- [OCI Distribution specification 1.1.1](https://raw.githubusercontent.com/opencontainers/distribution-spec/v1.1.1/spec.md)
- [Distribution releases](https://github.com/distribution/distribution/releases)
- [Distribution pull-through cache](https://distribution.github.io/distribution/recipes/mirror/)
