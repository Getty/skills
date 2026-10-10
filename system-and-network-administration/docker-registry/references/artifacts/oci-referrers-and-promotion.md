# OCI artifacts, referrers, SBOMs, and complete promotion

> Read when: storing more than runtime images or moving signed multi-platform releases.

OCI registries can carry artifacts and relationships in addition to traditional images. The actual feature set depends on registry version, client tooling, media types, and referrers support. Do not infer OCI 1.1 behavior merely from `/v2/` being reachable.

A signature/SBOM/attestation may refer to a subject digest. Image indexes have their own graph of platform children. Promotion and retention need both graphs. Copying only the manifest selected for the local architecture can produce a seemingly valid image while losing other platforms and evidence.

## Capability test

Use a disposable repository to publish an image/index and a small artifact that references it. Discover the relationship using the registry/tooling's supported referrers mechanism or documented fallback. Copy to the destination, then verify subject digest, artifact digest, all required platforms, and discoverability. Repeat after tag changes and a retention/GC dry run.

The existence of an OCI specification feature does not guarantee it is supported by every Distribution release or managed registry. Record the exact server/client versions and fallback behavior. Do not invent a `/referrers` endpoint for an older implementation without checking the contract.

## Trust policy

A stored signature is not a verified signature. Establish trusted issuer/key, subject identity, verification policy, expiration/revocation handling, and offline verification requirements. Provenance and SBOMs have different purposes and may reveal sensitive build information; authorize access and retention accordingly.

A complete release manifest should list source/destination digest, platform set, required attachments, tool versions, and verification outcome. Only promote after all required objects pass. Keep artifact compatibility regressions in the registry upgrade test plan, not just in the build pipeline.

## Primary sources

- [OCI Distribution specification 1.1.1](https://raw.githubusercontent.com/opencontainers/distribution-spec/v1.1.1/spec.md)
- [Build attestations](https://docs.docker.com/build/metadata/attestations/)
- [Multi-platform build and image structure](https://docs.docker.com/build/building/multi-platform/)
- [Distribution releases](https://github.com/distribution/distribution/releases)
