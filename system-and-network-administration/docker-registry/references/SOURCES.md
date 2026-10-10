# Primary-source register

Documentation review: **2026-10-09**. The references in this skill link to the sources relevant to each topic. This register is for maintenance; agents should not fetch every source on every task.

Dynamic documentation and release branches can change. Revalidate exact release-dependent options before implementation. Pinned implementation sources describe that release, not all compatible products. No upstream manual or complete source repository is bundled. Operational checklists, examples, and decision guidance are authored additions.

| Source | Evidence scope |
|---|---|
| [Distribution configuration](https://distribution.github.io/distribution/about/configuration/) | Maintained primary documentation/source |
| [Deploy a registry](https://distribution.github.io/distribution/about/deploying/) | Maintained primary documentation/source |
| [Distribution pull-through cache](https://distribution.github.io/distribution/recipes/mirror/) | Maintained primary documentation/source |
| [Docker Hub mirror configuration](https://docs.docker.com/docker-hub/image-library/mirror/) | Maintained primary documentation/source |
| [Distribution garbage collection](https://distribution.github.io/distribution/about/garbage-collection/) | Maintained primary documentation/source |
| [Distribution HTTP API V2](https://distribution.github.io/distribution/spec/api/) | Maintained primary documentation/source |
| [Registry token authentication](https://distribution.github.io/distribution/spec/auth/token/) | Maintained primary documentation/source |
| [Distribution S3 storage driver](https://distribution.github.io/distribution/storage-drivers/s3/) | Maintained primary documentation/source |
| [Distribution notifications](https://distribution.github.io/distribution/about/notifications/) | Maintained primary documentation/source |
| [Distribution reverse-proxy recipe](https://distribution.github.io/distribution/recipes/nginx/) | Maintained primary documentation/source |
| [Distribution releases](https://github.com/distribution/distribution/releases) | Maintained primary documentation/source |
| [Official registry image tag metadata](https://raw.githubusercontent.com/docker-library/official-images/master/library/registry) | Maintained primary documentation/source |
| [OCI Distribution specification 1.1.1](https://raw.githubusercontent.com/opencontainers/distribution-spec/v1.1.1/spec.md) | Pinned implementation/specification |
| [containerd registry hosts configuration](https://raw.githubusercontent.com/containerd/containerd/main/docs/hosts.md) | Maintained primary documentation/source |
| [K3s private registry configuration](https://docs.k3s.io/installation/private-registry) | Maintained primary documentation/source |
| [RKE2 private registry configuration](https://docs.rke2.io/install/private_registry) | Maintained primary documentation/source |
| [Docker registry certificate trust](https://docs.docker.com/engine/security/certificates/) | Maintained primary documentation/source |
| [Docker daemon configuration](https://docs.docker.com/engine/daemon/) | Maintained primary documentation/source |
| [Multi-platform build and image structure](https://docs.docker.com/build/building/multi-platform/) | Maintained primary documentation/source |
| [Build attestations](https://docs.docker.com/build/metadata/attestations/) | Maintained primary documentation/source |
| [BuildKit cache backends](https://docs.docker.com/build/cache/backends/) | Maintained primary documentation/source |
| [Compose secrets](https://docs.docker.com/compose/how-tos/use-secrets/) | Maintained primary documentation/source |
| [Engine-specific registry auth header](https://raw.githubusercontent.com/moby/moby/v28.5.2/api/types/registry/authconfig.go) | Pinned implementation/specification |

## Maintenance procedure

When updating a claim, check the target product release and primary reference, update its feature gate and examples together, and add a regression test where practical. Record an integration result separately from a documentation review. If documentation and measured behavior disagree, preserve the discrepancy and scope the claim; do not silently choose the more convenient interpretation.
