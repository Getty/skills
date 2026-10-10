# docker-registry: reference index

Read [the skill entrypoint](../SKILL.md) first. Follow only the links needed for the task. These are on-demand reference files, not instructions to load the whole directory.

## Architecture

| Reference | Read when |
|---|---|
| [Image identity, registry names, DNS, and client location](architecture/image-identity-and-naming.md) | designing image references or debugging name resolution. |
| [Writable registry, cache, and artifact-platform roles](architecture/roles-and-boundaries.md) | choosing topology or combining caching with internal image storage. |

## Artifacts

| Reference | Read when |
|---|---|
| [OCI artifacts, referrers, SBOMs, and complete promotion](artifacts/oci-referrers-and-promotion.md) | storing more than runtime images or moving signed multi-platform releases. |

## Clients

| Reference | Read when |
|---|---|
| [containerd hosts.toml, trust capabilities, and reload behavior](clients/containerd-hosts.md) | configuring standalone containerd or comparing ctr with CRI pulls. |
| [Docker Engine and BuildKit registry clients](clients/docker-and-buildkit.md) | Docker or a build worker ignores mirror/auth/TLS settings. |
| [K3s/RKE2 registry configuration and Kubernetes bootstrap](clients/k3s-rke2-and-kubernetes.md) | nodes cannot pull, a cluster bypasses a mirror, or deploying a registry in-cluster. |

## Deployment

| Reference | Read when |
|---|---|
| [Reverse proxies, load balancers, and upload correctness](deployment/reverse-proxy-and-load-balancer.md) | placing a registry behind ingress/TLS termination or scaling frontends. |
| [Filesystem/object storage, redirects, and capacity planning](deployment/storage-and-capacity.md) | choosing a storage backend or sizing a registry. |
| [TLS, private CA trust, and secure access](deployment/tls-and-private-access.md) | deploying a private registry or diagnosing certificate failures. |

## Maintenance

| Reference | Read when |
|---|---|
| [Registry backup, restore, and disaster-recovery evidence](maintenance/backup-restore-and-migration.md) | protecting owned artifacts or moving registry storage/hosts. |
| [Garbage collection without corrupting live content](maintenance/garbage-collection.md) | disk reclamation is required or scheduling registry maintenance. |
| [High availability, monitoring, and operational objectives](maintenance/ha-and-observability.md) | running multiple replicas or designing ongoing registry operations. |
| [Retention policy, manifest deletion, and protected artifacts](maintenance/retention-and-deletion.md) | automating cleanup or removing a release. |

## Mirrors

| Reference | Read when |
|---|---|
| [Mirror fallback, egress proof, and air-gapped operation](mirrors/fallback-and-airgap.md) | a pull bypasses the mirror or internet access must be prohibited. |
| [Pull-through cache design, eviction, and credential scope](mirrors/pull-through-design.md) | reducing upstream pulls or operating a Docker Hub cache. |

## Operations

| Reference | Read when |
|---|---|
| [Configuration files: readers, timing, restart, and verification](operations/config-files-and-reload.md) | changing registry/client configuration or designing automation around it. |

## Protocol

| Reference | Read when |
|---|---|
| [Registry authentication, authorization, and token challenges](protocol/authentication-and-authorization.md) | handling 401 responses or protecting private repositories. |
| [Discovery, tags, pagination, and catalog limitations](protocol/discovery-pagination-and-catalog.md) | listing registry content or building inventory/retention tooling. |
| [Manifests, blobs, indexes, and digest correctness](protocol/manifests-blobs-and-indexes.md) | implementing direct registry reads or validating image content. |
| [Blob upload sessions, resumption, and redirects](protocol/uploads-resume-and-redirects.md) | pushes fail on large layers or implementing a registry client. |

## Start Here

| Reference | Read when |
|---|---|
| [Registry troubleshooting by failing actor and protocol phase](troubleshooting.md) | a push/pull fails, cache seems bypassed, or the registry returns confusing responses. |
| [Registry versions, compatibility, and upgrade planning](versions-and-migration.md) | deploying a registry or migrating from registry:2. |

## Maintenance

Read the [source register](SOURCES.md) for upstream verification.
