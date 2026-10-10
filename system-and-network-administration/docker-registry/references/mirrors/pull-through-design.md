# Pull-through cache design, eviction, and credential scope

> Read when: reducing upstream pulls or operating a Docker Hub cache.

In Distribution proxy mode, `proxy.remoteurl` identifies one upstream. The instance is not a normal writable destination for internal builds. Keep that role split in endpoint names, storage, credentials, and operational policy. Multiple upstreams usually mean separate instances or a product intentionally supporting that topology.

A tag lookup can require upstream freshness checks; cached blobs alone do not guarantee that a mutable-tag pull works offline. Configure TTL/eviction deliberately and enable deletion as required by the cache scheduler. Cache TTL is not the same as “keep every image needed for disaster recovery.”

## Credential design

Anonymous upstream pulls avoid accidental expansion of private access. If an upstream account is required, minimize its scope and secure downstream access. Do not hand a broad private-account view to every node with network access to the cache. Test anonymous and authenticated downstream requests to a private repository before deployment.

## Performance evidence

Distinguish cold pull, warm pull, tag-resolution traffic, manifest requests, blob requests, and node-local content hits. A repeat pull on the same node may exercise only the node cache. Use a disposable fresh client or a known uncached digest and observe registry access/storage/backend metrics.

Multiple cache replicas sharing storage do not guarantee elimination of duplicate in-flight upstream fetches. Measure upstream request count and bandwidth during concurrent misses. Keep a separate capacity policy for writable release storage and expendable cached content.

## Failure contract

Decide explicitly whether clients may fall back to upstream and whether the cache must remain useful during upstream failure. Test unreachable cache, unreachable upstream, expired upstream credentials, tag mutation, cache eviction, and rate limiting. Do not claim cache use because a pull succeeded; correlate the actual mirror path and network egress.

## Primary sources

- [Distribution pull-through cache](https://distribution.github.io/distribution/recipes/mirror/)
- [Docker Hub mirror configuration](https://docs.docker.com/docker-hub/image-library/mirror/)
- [Distribution configuration](https://distribution.github.io/distribution/about/configuration/)
- [containerd registry hosts configuration](https://raw.githubusercontent.com/containerd/containerd/main/docs/hosts.md)
