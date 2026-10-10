# Registry backup, restore, and disaster-recovery evidence

> Read when: protecting owned artifacts or moving registry storage/hosts.

Back up the coherent content/metadata namespace and the configuration needed to read it. Also protect auth configuration, TLS/private keys through an approved secret process, the HTTP secret, backend credentials, and any external identity/metadata dependencies. Keep sensitive key material separated and recoverable according to policy.

A writable registry's artifacts can be irreplaceable if source/build infrastructure or dependencies disappear. A cache may be rebuildable from upstream, but that assumption fails for deleted private tags, rate-limited/disconnected recovery, or intentionally offline inventory. Assign backup tiers deliberately.

## Consistency plan

Coordinate snapshots with writes using the backend's supported consistency mechanism and registry operation model. Document object-store versioning and replication lag. Copying a changing filesystem recursively is not automatically a coherent backup. Retain a digest-based inventory and checksums outside the same failure domain.

## Restore drill

Restore to a new storage namespace and isolated registry endpoint. Start a compatible image with restored configuration and controlled auth. Pull known releases by digest, traverse all platform children, verify blob hashes where required, and rediscover attached metadata. Test a controlled write only after proving old content is intact.

Do not test restore by overwriting production storage. Keep clients from pushing into the test copy accidentally. Record actual recovery time and the external dependencies needed, including DNS, token service, object storage, CA trust, and bootstrap image availability.

## Cutover

For hostname/backend migration, freeze or reconcile writes, transfer the final delta, verify content identity/completeness, then switch clients or DNS with a rollback plan. Plain pull/tag/push on one architecture may not migrate the full artifact graph. Use a copy tool whose all-platform and referrer behavior has been tested against both endpoints.

## Primary sources

- [Distribution configuration](https://distribution.github.io/distribution/about/configuration/)
- [Deploy a registry](https://distribution.github.io/distribution/about/deploying/)
- [Distribution S3 storage driver](https://distribution.github.io/distribution/storage-drivers/s3/)
- [OCI Distribution specification 1.1.1](https://raw.githubusercontent.com/opencontainers/distribution-spec/v1.1.1/spec.md)
- [Multi-platform build and image structure](https://docs.docker.com/build/building/multi-platform/)
