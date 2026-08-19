---
name: docker-registry
description: "Use when running a container registry — pull-through cache, in-cluster image store, wiring containerd to it, pulls bypassing the mirror, or a rejected push."
---

# Running a Container Registry

The CNCF `distribution` image (`registry:2`) is two products behind one binary,
and the single most expensive mistake is assuming it is one.

## A cache cannot store your images

`proxy.remoteurl` turns a registry into a **pull-through cache**: read-only,
mirroring exactly **one** upstream. Pushes are rejected, and no second
`remoteurl` can be added. If you need both a Docker Hub cache and somewhere to
put your own builds, that is **two deployments**, not one with two configs.

```yaml
# cache — config.yml
version: 0.1
storage:
  filesystem:
    rootdirectory: /var/lib/registry
  delete:
    enabled: true          # required, or the scheduler cannot expire stale blobs
proxy:
  remoteurl: https://registry-1.docker.io
  ttl: 168h
```

Use the `filesystem` driver for a cache — correctness and performance both
depend on it. Credentials in the `proxy` block are optional and dangerous: they
make every private image that account can reach available through your mirror,
so a cache with credentials **must** carry authentication of its own.

The storage registry is the same image with no `proxy` block, plus `delete`
enabled if anything is ever to be reclaimed. Untagged blobs survive deletion
until `registry garbage-collect config.yml` runs, and that wants the registry
read-only or stopped.

## Pointing containerd at it

Not Docker's `--registry-mirror`; containerd resolves per-host. On K3s/RKE2 the
file is `/etc/rancher/{k3s,rke2}/registries.yaml` and needs a service restart —
see skill `kubernetes-rke2`. Elsewhere it is `hosts.toml` under
`config_path` (commonly `/etc/containerd/certs.d/<host>/hosts.toml`):

```toml
server = "https://registry-1.docker.io"

[host."http://cache.internal:5000"]
  capabilities = ["pull", "resolve"]
```

`capabilities` is the honest way to say "cache": omit `push` and a client that
tries gets a clear error instead of a confusing upstream one.

**The upstream default is always tried last.** A mirror that is merely
unreachable does not fail the pull — it falls through to the internet, quietly.
So "the mirror works" is never proven by a successful `crictl pull`; prove it by
watching egress, or by taking the upstream route away.

## Naming decides more than it looks

A registry's name is part of every image reference, so it is baked into
manifests, caches and image IDs. Three access paths for the same registry are
normal, and they are not interchangeable:

| From | Reference | Why |
|---|---|---|
| in-cluster build | `registry.ns.svc:5000/img:tag` | ClusterIP DNS, no node involved |
| node / kubelet pull | `localhost:30500/img:tag` | NodePort, resolvable on every node |
| human and config | `registry.internal/img:tag` | stable name, needs real DNS |

A short name without a dot (`registry.local`, `myregistry`) is not automatically
a registry host to every client — Docker treats a dotless first segment as a
Docker Hub namespace. Give internal names a dot, or accept that some tools will
resolve them somewhere else entirely. Where a name has to resolve inside the
cluster too, add it to CoreDNS rather than hoping node `/etc/hosts` is consulted
by pods:

```
hosts {
    10.0.0.5 registry.internal
    fallthrough
}
```

## Plain HTTP is a per-client decision

An HTTP registry is refused by default everywhere, and each client refuses it
differently: containerd needs the `http://` endpoint spelled out (and
`insecure_skip_verify` for a self-signed HTTPS one), Docker needs
`insecure-registries` in `daemon.json`, Podman needs an entry in
`registries.conf`. There is no cluster-wide switch — a registry that "works on
the node but not in the cluster" is almost always this.

## Diagnosing a pull

```bash
curl -s http://cache.internal:5000/v2/                       # 200 = reachable, speaks v2
curl -s http://cache.internal:5000/v2/_catalog                # a cache answers empty — expected
curl -sI http://cache.internal:5000/v2/library/alpine/manifests/latest \
  -H 'Accept: application/vnd.oci.image.index.v1+json'        # a cache fetches on demand
crictl pull docker.io/library/alpine:latest                   # then check the cache's storage grew
```

`_catalog` on a pull-through cache returning nothing is **not** a fault: it
lists what has been cached, and it caches on first pull.

## Related

- `kubernetes-rke2` — `registries.yaml` and when it is read.
- `docker` — building the images that end up here.
