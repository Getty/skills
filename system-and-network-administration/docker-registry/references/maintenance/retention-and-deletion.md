# Retention policy, manifest deletion, and protected artifacts

> Read when: automating cleanup or removing a release.

Define retention in terms of releases and artifact reachability, not filesystem age. Protect deployed digests, rollback windows, approved releases, legal/operational holds, index children, and required signatures/SBOMs/attestations. A tagless child manifest can still belong to a retained multi-platform index.

## Two distinct operations

Deleting a registry manifest/reference makes it unavailable according to the endpoint's semantics. Garbage collection later reclaims content no longer reachable from retained objects. Removing a tag is not a universal equivalent of deleting one isolated image; several tags can point to the same digest and a digest can be referenced by an index.

For Distribution, deletion must be enabled in configuration and authorized by policy. Resolve the exact intended digest with suitable media-type negotiation before any deletion. Do not guess a manifest digest from an image config ID or a locally selected platform image.

## Reviewable deletion plan

Create an inventory with complete pagination and visibility. Build a candidate set excluding protected digests and dependencies. Record repository, digest, tags, object type, platform/index relationships, artifact attachments, last-use evidence, expected effect, and backup status. Present the explicit candidate list and command/API operation for approval.

A last-pull timestamp from a single log stream is not definitive evidence of non-use; logs can be incomplete and deployments can run already-cached images. Avoid retention based solely on missing recent traffic.

## Postconditions

Verify retained releases still resolve and pull on required platforms. Record deleted identities and GC eligibility separately from bytes reclaimed. Do not configure object-storage lifecycle expiration to delete registry blobs independently of this graph. For products with a retention engine, validate its artifact/referrer semantics rather than layering a second uncoordinated cleanup process over it.

## Primary sources

- [Distribution garbage collection](https://distribution.github.io/distribution/about/garbage-collection/)
- [Distribution HTTP API V2](https://distribution.github.io/distribution/spec/api/)
- [OCI Distribution specification 1.1.1](https://raw.githubusercontent.com/opencontainers/distribution-spec/v1.1.1/spec.md)
- [Distribution configuration](https://distribution.github.io/distribution/about/configuration/)
- [Multi-platform build and image structure](https://docs.docker.com/build/building/multi-platform/)
