---
name: docker-registry
description: "Use when deploying, securing, debugging, or maintaining container registries and pull-through caches: Distribution/OCI HTTP API, TLS/auth, storage, Docker/BuildKit/containerd/K3s/RKE2 clients, mirror fallback, air gaps, uploads, retention, garbage collection, backup, HA, referrers, or migration. Load the relevant operational references."
---

# Container Registries and Mirrors

A registry protocol and operations skill. Keep writable image storage, pull-through caching, runtime configuration, and artifact retention separate. Documentation review: **2026-10-09**. Begin with [versions and migration](references/versions-and-migration.md); example image versions are dated review snapshots, not permanent recommendations.

## Establish the topology

Identify whether the service is a writable registry, an upstream cache, or part of a broader artifact platform. Record its canonical authority, intended clients, upstreams, network paths, authentication/authorization, TLS trust, backing storage, data criticality, and allowed egress.

Read [roles and boundaries](references/architecture/roles-and-boundaries.md) before selecting a deployment. A cache is not interchangeable with a private push destination. Read [image identity and naming](references/architecture/image-identity-and-naming.md) before publishing names into manifests or pipelines.

## Load by task

| Task or symptom | Required reference | Related reference |
|---|---|---|
| New service or version upgrade | [Versions/migration](references/versions-and-migration.md) | [Roles](references/architecture/roles-and-boundaries.md) |
| Changed files have no effect | [Config readers and reload](references/operations/config-files-and-reload.md) | Client-specific reference below |
| Certificate, login, permissions, or exposed endpoint | [TLS/private access](references/deployment/tls-and-private-access.md) | [Authentication/authorization](references/protocol/authentication-and-authorization.md) |
| Proxy, load balancer, large upload, or redirect failure | [Proxy/load balancer](references/deployment/reverse-proxy-and-load-balancer.md) | [Upload protocol](references/protocol/uploads-resume-and-redirects.md) |
| Storage choice, capacity, or multiple instances | [Storage](references/deployment/storage-and-capacity.md) | [HA/observability](references/maintenance/ha-and-observability.md) |
| Pull-through cache design | [Cache model](references/mirrors/pull-through-design.md) | [Fallback and air gap](references/mirrors/fallback-and-airgap.md) |
| Docker or BuildKit ignores the mirror | [Docker/BuildKit clients](references/clients/docker-and-buildkit.md) | [Fallback proof](references/mirrors/fallback-and-airgap.md) |
| containerd host namespace or trust issue | [containerd hosts](references/clients/containerd-hosts.md) | [Config consumption](references/operations/config-files-and-reload.md) |
| K3s/RKE2 or kubelet pull failure | [K3s/RKE2/Kubernetes](references/clients/k3s-rke2-and-kubernetes.md) | [Identity and naming](references/architecture/image-identity-and-naming.md) |
| Missing manifest, wrong architecture, or digest mismatch | [Manifests/blobs/indexes](references/protocol/manifests-blobs-and-indexes.md) | [Discovery/catalog](references/protocol/discovery-pagination-and-catalog.md) |
| Delete old images or recover disk | [Retention/deletion](references/maintenance/retention-and-deletion.md) | [Garbage collection](references/maintenance/garbage-collection.md) |
| Disaster recovery or storage migration | [Backup/restore](references/maintenance/backup-restore-and-migration.md) | [Versions](references/versions-and-migration.md) |
| Promote signatures/SBOMs/multi-platform releases | [OCI referrers/promotion](references/artifacts/oci-referrers-and-promotion.md) | [Content graph](references/protocol/manifests-blobs-and-indexes.md) |
| Unclassified pull or push failure | [Troubleshooting](references/troubleshooting.md) | Select the exact client and protocol layer |

## Operational invariants

A successful pull does not prove that a mirror was used. Validate the cold-cache path, warm-cache path, and upstream-denied case from the actual pulling client. Do not promise air-gap enforcement solely from mirror configuration.

Prefer a stable, resolvable registry authority with verified TLS. Install a CA in the correct client's trust store rather than disabling verification. Node, Pod, daemon, builder, and human-client DNS/trust are separate concerns. A login in one client does not authenticate all other runtimes.

Keep cache and private-registry storage/configuration independent. Protect a credentialed cache: it can expose content available to its upstream account. Authentication is not repository-scoped authorization; test permissions with the intended identity and tool.

Treat retention as a content-graph policy, not a list of old tags. Do not run deletion or garbage collection without explicit scope, release-specific behavior, a write-quiescence plan, backups, and a proven restore. Include multi-platform children and referrers in preservation tests. Never recommend direct storage-file deletion as a normal cleanup operation.

## Examples and output

The [local lab](examples/local-lab/README.md) is loopback-only HTTP and unsuitable for private data. The [secure-pair template](examples/secure-pair/README.md) separates a TLS-protected writable registry from a Hub cache and requires real certificates, credentials, and secrets before use. [Client fragments](examples/clients/README.md) are merge inputs, not replacement system configuration. The [registry probe](scripts/README.md) performs bounded, non-authenticated, non-redirecting diagnostic requests without writes.

For a deployment/change, provide topology, authorities, exact config readers and paths, secret handling, apply/restart requirements, positive and negative tests, and rollback. For incidents, separate reachability, trust, authentication, authorization, manifest resolution, and blob transfer.

Use sibling `docker` for builds/Compose and `docker-engine-api` for daemon HTTP clients. K3s/RKE2 details here are usable without another skill. See the [full index](references/INDEX.md) and [source register](references/SOURCES.md).
