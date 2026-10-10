# Registry versions, compatibility, and upgrade planning

> Read when: deploying a registry or migrating from registry:2.

The registry **product version**, configuration schema version, Distribution HTTP `/v2/` API, and OCI specification version are different things. Distribution 3 still serves `/v2/`; `version: 0.1` in its configuration is not an instruction to run an old registry binary.

At the documentation review date, **2026-10-09**, upstream lists Distribution **3.1.2**, and the official-image metadata includes the `3.1.2`, `3.1`, and `3` tags. Examples select `registry:3.1.2` as a review snapshot, not a permanent latest-version promise. For production, recheck security advisories, choose a supported release, and pin the tested image digest. Do not mechanically preserve `registry:2` from older notes.

## Migration checklist

Inventory existing binary/image digest, config path, storage driver/options, data size, auth backend, proxy mode, middleware/plugins, TLS chain, HTTP secret, telemetry, and clients. Read release notes across the full version jump. Distribution 3 has configuration/dependency changes; do not assume a v2 config copy is sufficient because the HTTP path is unchanged.

Back up storage and configuration consistently, then restore into an isolated target using the proposed binary. Test push, pull, resume, delete policy, multi-platform images, referrers/attestations, cache behavior, and garbage collection. Test a representative large image and every runtime client. Keep production untouched until the recovery and rollback plan is proven.

## Upgrade boundaries

A rolling binary upgrade requires verified shared-storage/config compatibility across versions; otherwise plan a maintenance window. Preserve the HTTP secret and storage namespace when required by the deployment. A registry image rollback is not necessarily a storage-format rollback.

The docs may contain legacy `registry:2` examples or old driver options. Treat those as release-scoped guidance. When implementing a new feature, verify both the exact registry build and the copying/scanning/runtime clients that will use it.

## Primary sources

- [Distribution releases](https://github.com/distribution/distribution/releases)
- [Official registry image tag metadata](https://raw.githubusercontent.com/docker-library/official-images/master/library/registry)
- [Distribution configuration](https://distribution.github.io/distribution/about/configuration/)
- [OCI Distribution specification 1.1.1](https://raw.githubusercontent.com/opencontainers/distribution-spec/v1.1.1/spec.md)
