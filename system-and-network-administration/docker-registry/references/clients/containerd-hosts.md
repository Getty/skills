# containerd hosts.toml, trust capabilities, and reload behavior

> Read when: configuring standalone containerd or comparing ctr with CRI pulls.

Containerd resolves registry configuration by namespace under a configured hosts directory. The main CRI plugin configuration differs between containerd 1.x and 2.x; inspect the installed version before choosing the plugin table.

```toml
# containerd 2.x main configuration fragment
version = 3
[plugins."io.containerd.cri.v1.images".registry]
  config_path = "/etc/containerd/certs.d"
```

For containerd 1.x, the relevant table is `plugins."io.containerd.grpc.v1.cri".registry` in a v2 configuration. Do not replace the entire main config with a fragment.

A Docker Hub namespace example lives at `/etc/containerd/certs.d/docker.io/hosts.toml`:

```toml
server = "https://registry-1.docker.io"
[host."https://hub-cache.example.com"]
  capabilities = ["pull", "resolve"]
  ca = "/etc/containerd/certs.d/docker.io/cache-ca.crt"
```

Grant `resolve` only to a mirror trusted to map mutable names to content digests. Public/untrusted mirrors should not automatically receive it. `pull` permits content retrieval; `push` is not appropriate for a read-through mirror. Capabilities guide the client and express trust; they are **not server-side authorization** preventing every client from pushing.

## File timing and client choice

Hosts-directory updates are designed not to require a containerd restart. Changing the main plugin `config_path` is different and typically needs a restart. Test a fresh resolution/pull after changes; an in-flight request may keep old state.

`ctr` has its own `--hosts-dir` flag and is not proof that CRI uses identical resolver inputs. `crictl` exercises the configured CRI endpoint; kubelet adds its own image-pull credentials. Compare the exact socket, namespace, auth, and hosts directory. Use `skip_verify` only for an approved temporary TLS diagnostic; prefer CA trust. A plain-HTTP endpoint needs `http://`, which is not equivalent to disabling HTTPS verification.

## Primary sources

- [containerd registry hosts configuration](https://raw.githubusercontent.com/containerd/containerd/main/docs/hosts.md)
- [K3s private registry configuration](https://docs.k3s.io/installation/private-registry)
- [RKE2 private registry configuration](https://docs.rke2.io/install/private_registry)
