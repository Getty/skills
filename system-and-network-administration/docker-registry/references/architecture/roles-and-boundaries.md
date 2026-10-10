# Writable registry, cache, and artifact-platform roles

> Read when: choosing topology or combining caching with internal image storage.

A Distribution instance can serve a writable registry or run in pull-through proxy mode. In proxy mode it fronts one configured upstream and is not the destination for your own pushes. For an internal artifact store plus a Docker Hub cache, deploy **two instances** with distinct endpoints/configurations/storage ownership.

Keep a stable human/configuration name such as `registry.example.com` for owned artifacts and a separate mirror endpoint such as `hub-cache.example.com`. This avoids accidentally directing a release push to a read-through service. Do not share one filesystem namespace between independently configured cache and writable instances merely to save disk.

## Define the required product surface

Distribution supplies a registry data plane. If the organization needs a UI, repository-level policy, vulnerability workflows, retention administration, replication orchestration, quotas, or identity integration, select and validate the required additional components or a registry platform providing them. Do not assume running the `registry` image alone supplies every product feature associated with “a registry.”

## Trust and availability

A writable registry is a source of release artifacts and may be critical for recovery. A cache is normally replaceable performance infrastructure, unless you deliberately depend on its contents for disconnected operation—which requires a different retention/bootstrap design. Neither is a substitute for signed release identity or tested backups.

A node pulling an image, a BuildKit worker pushing an image, and a pod reaching a service use different DNS, network, and trust configurations. Diagram those actors before choosing in-cluster placement. Avoid bootstrap dependencies where the cluster cannot pull the registry's own image until that same registry starts.

## Decision output

Record write owner, upstreams, endpoints, auth policy, digest policy, storage backend, backup tier, availability target, expected image sizes/concurrency, and client types. Route image builds to `docker`; route Engine-specific pull/push headers to `docker-engine-api`; keep direct OCI/Distribution traffic in this skill.

## Primary sources

- [Distribution pull-through cache](https://distribution.github.io/distribution/recipes/mirror/)
- [Deploy a registry](https://distribution.github.io/distribution/about/deploying/)
- [Distribution configuration](https://distribution.github.io/distribution/about/configuration/)
- [Docker Hub mirror configuration](https://docs.docker.com/docker-hub/image-library/mirror/)
