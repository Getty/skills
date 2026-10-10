# Image identity, registry names, DNS, and client location

> Read when: designing image references or debugging name resolution.

An image reference has a registry authority, repository path, and tag or digest. A registry hostname changes the **reference and credential/trust scope**, not the bytes of a manifest by itself. Moving identical content between hosts can preserve the manifest digest. Rewriting manifests or losing/recreating index metadata can change identity.

Use an unambiguous hostname containing a dot, an explicit host:port, or a recognized special case such as `localhost`. A dotless first path segment is commonly interpreted as a Docker Hub namespace. `registry.local` already contains a dot; it is not a valid example of a dotless name. Prefer a name under a domain you control; do not rely on incidental mDNS behavior.

## Resolve from the actual actor

| Actor | Required resolution/reachability |
|---|---|
| Developer CLI with local Engine | The Engine host must reach registry/token/blob endpoints |
| Remote Engine or BuildKit | The remote host/worker needs its own DNS, CA, credentials |
| Kubernetes image pull | The node runtime, before the pod starts |
| In-pod build tool | That pod's network namespace and mounted credentials |

A Service DNS name can work inside pods but fail for the node runtime. Editing node `/etc/hosts` does not generally configure pod DNS. A `localhost:NodePort` image reference is not a portable Kubernetes pattern; behavior depends on node/proxy mode and every node's routing. Use one stable node-reachable name unless a special topology is intentionally tested.

## Migration contract

Changing registry authority requires updating image references, login/helper configuration, CA placement, token service audience/scope handling, mirrors, CI variables, and admission/signature policies. Keep artifact digests and platform/referrer completeness as separate acceptance criteria. Do not rename a registry merely as a cosmetic change without reviewing these consumers.

## Primary sources

- [Distribution HTTP API V2](https://distribution.github.io/distribution/spec/api/)
- [OCI Distribution specification 1.1.1](https://raw.githubusercontent.com/opencontainers/distribution-spec/v1.1.1/spec.md)
- [K3s private registry configuration](https://docs.k3s.io/installation/private-registry)
- [containerd registry hosts configuration](https://raw.githubusercontent.com/containerd/containerd/main/docs/hosts.md)
- [Docker registry certificate trust](https://docs.docker.com/engine/security/certificates/)
