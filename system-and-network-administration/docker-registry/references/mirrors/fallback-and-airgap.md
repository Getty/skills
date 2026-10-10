# Mirror fallback, egress proof, and air-gapped operation

> Read when: a pull bypasses the mirror or internet access must be prohibited.

A mirror configuration often prefers a mirror but retains an upstream fallback. Successful pulls alone do not prove the mirror is used or the environment is offline. A node may already hold content, fetch directly from upstream, or follow a redirect to an external blob host.

## Prove the path

Use an isolated test node/runtime and a known image not already present there. Correlate its request with mirror logs and egress observation. Then test with upstream access blocked at the relevant runtime network boundary. Do not destructively clear production node caches to create this test.

For plain containerd, `hosts.toml` `server` and host entries define resolver fallback/trust. Do not merely omit `server` and assume no upstream is used; the namespace can become the implicit server. Explicitly point the namespace's server at the approved mirror where that is the intended supported design, and verify it.

K3s/RKE2 provide `disable-default-registry-endpoint` on supported releases. It applies to configured mirror registries; unconfigured registries can still use default behavior. Confirm the installed version and generated runtime configuration. A network egress policy is a separate enforcement layer and also needs DNS, token service, redirects, and bootstrap dependencies considered.

## Offline inventory

Preload/replicate every required index, platform manifest, config, layer, attestation/referrer, registry bootstrap image, control-plane image, and build dependency needed for the scenario. Protect this inventory from cache expiry. Pin digests and test after disconnecting upstream, including fresh-node and disaster-recovery startup.

Air-gapped availability is an architecture property, not a side effect of a warm cache. Define who refreshes the inventory, verifies integrity and signatures, handles revocation/security updates, and proves restore without external DNS/auth/object-storage services.

## Primary sources

- [containerd registry hosts configuration](https://raw.githubusercontent.com/containerd/containerd/main/docs/hosts.md)
- [K3s private registry configuration](https://docs.k3s.io/installation/private-registry)
- [RKE2 private registry configuration](https://docs.rke2.io/install/private_registry)
- [Distribution pull-through cache](https://distribution.github.io/distribution/recipes/mirror/)
- [OCI Distribution specification 1.1.1](https://raw.githubusercontent.com/opencontainers/distribution-spec/v1.1.1/spec.md)
