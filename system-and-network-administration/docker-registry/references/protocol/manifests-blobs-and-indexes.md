# Manifests, blobs, indexes, and digest correctness

> Read when: implementing direct registry reads or validating image content.

Blobs hold content such as compressed layers and image configuration. A platform-specific manifest references blobs. An index/manifest list references platform manifests. Tags identify mutable manifest/index targets. The same hexadecimal-looking digest must be interpreted with its object type and media type, not assumed to be an image configuration ID.

Use `HEAD` or `GET /v2/REPOSITORY/manifests/REFERENCE` with an appropriate `Accept` set for supported OCI/Docker manifest and index media types. A client that accepts only OCI indexes can fail on a single-platform Docker schema-2 image even though the registry is functioning.

For integrity-sensitive reads, compute the digest of the actual response bytes and compare with the requested/expected digest. Do not parse and reserialize JSON before checking a content digest; whitespace or serialization changes alter bytes. Check schema/media-type consistency and required descriptors without assuming unknown annotations are invalid.

## Pull plan

Resolve the desired tag to an approved digest when tag resolution is necessary. Fetch the index if present, select the platform according to the runtime's requirements, then fetch the child manifest/config/layers. Validate digest and length for each content object and record the chosen platform. A retrieved manifest alone does not prove its blobs are accessible.

## Operational checks

Test an ordinary single-platform image, an amd64/arm64 index, a digest-pinned pull, and an image with attached attestations. Verify the registry/proxy returns the correct media type and the expected `Docker-Content-Digest` where supported. An empty or denied catalog is not evidence that a known repository cannot be pulled.

Deleting a manifest and reclaiming unreachable content are separate operations; read retention/GC before issuing delete requests. Never delete a raw layer because it appears old without traversing its references.

## Primary sources

- [Distribution HTTP API V2](https://distribution.github.io/distribution/spec/api/)
- [OCI Distribution specification 1.1.1](https://raw.githubusercontent.com/opencontainers/distribution-spec/v1.1.1/spec.md)
- [Multi-platform build and image structure](https://docs.docker.com/build/building/multi-platform/)
