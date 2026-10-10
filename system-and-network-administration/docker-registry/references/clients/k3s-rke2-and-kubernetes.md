# K3s/RKE2 registry configuration and Kubernetes bootstrap

> Read when: nodes cannot pull, a cluster bypasses a mirror, or deploying a registry in-cluster.

Use the distribution-owned source file: `/etc/rancher/k3s/registries.yaml` or `/etc/rancher/rke2/registries.yaml`. It defines mirrors and per-endpoint auth/TLS. These distributions generate containerd configuration; edits to generated files are not a durable configuration workflow.

Apply the file on every node that may run workloads, including schedulable server nodes. Restart the appropriate node service in a controlled rollout and verify a fresh CRI pull. Do not restart every node simultaneously just to test a mirror change.

```yaml
mirrors:
  docker.io:
    endpoint:
      - "https://hub-cache.example.com"
configs:
  "hub-cache.example.com":
    tls:
      ca_file: /etc/rancher/registry-cache-ca.crt
```

This is a non-secret fragment. Auth fields belong under the actual endpoint configuration; file permissions and rotation matter. Kubernetes imagePullSecrets are a separate per-workload credential path, not a way to install node CA trust or rewrite registry endpoints.

## Fallback and bootstrap

Check `disable-default-registry-endpoint` support and its limited scope for configured registries. Rewrites are version-dependent and need testing against the target release. Treat normal mirror preference as fail-open unless you verify otherwise and enforce the desired egress policy.

The node runtime must reach the registry before the workload pod exists. Do not assume ClusterIP DNS or a `localhost` NodePort works for every node. Use a stable endpoint resolvable from the nodes, and plan how the registry's own image/storage/auth service starts when the cluster is degraded or empty.

## Acceptance evidence

Test each node class with the correct CRI socket and a known uncached image. Verify mirror logs and upstream egress. Then run a workload using its intended imagePullSecret and digest. Distinguish node trust/DNS errors from pod-level application connectivity; debugging from an already running pod can test the wrong namespace.

## Primary sources

- [K3s private registry configuration](https://docs.k3s.io/installation/private-registry)
- [RKE2 private registry configuration](https://docs.rke2.io/install/private_registry)
- [containerd registry hosts configuration](https://raw.githubusercontent.com/containerd/containerd/main/docs/hosts.md)
- [Docker registry certificate trust](https://docs.docker.com/engine/security/certificates/)
