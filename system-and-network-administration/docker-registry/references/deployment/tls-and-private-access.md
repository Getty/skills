# TLS, private CA trust, and secure access

> Read when: deploying a private registry or diagnosing certificate failures.

Use TLS with a certificate whose subject alternative names match the advertised registry hostname. A self-signed or private-CA deployment should distribute the CA to the actual clients; bypassing verification is a temporary test, not a security design.

For Linux Docker Engine, registry trust commonly lives under `/etc/docker/certs.d/HOST[:PORT]/` with CA files using `.crt`. Client certificate/key conventions differ from CA files. The authority must match the image reference; Desktop trust integration has platform-specific handling. BuildKit and containerd can need their own configuration.

## Three unrelated decisions

Plain HTTP selects an unencrypted transport. `skip_verify` disables HTTPS certificate/hostname verification. Authentication determines who may access repositories. None automatically enables the others. In containerd `hosts.toml` the field is `skip_verify`; in K3s/RKE2 `registries.yaml` TLS uses `insecure_skip_verify`. Do not copy names between schemas.

Prefer private CA trust over insecure-registry entries. Docker's daemon, the builder, the node runtime, and an application container have separate trust stores. Test the hostname used by each actor, including token service and redirected object-storage endpoints.

## Certificate rotation

Stage a renewed chain/key securely, verify hostname, validity window, permissions, and chain completeness. Restart/reload according to the selected registry/proxy version. Test a new connection from each client class. Keep overlap for CA rotation and verify that removing old trust does not break background workers.

The included secure deployment is a **configuration template** requiring user-provided certificates, auth data, and a generated HTTP secret. It is not a certificate authority or a production security certification. The separate loopback-only lab intentionally uses HTTP and must not be exposed to other machines.

## Primary sources

- [Docker registry certificate trust](https://docs.docker.com/engine/security/certificates/)
- [Distribution configuration](https://distribution.github.io/distribution/about/configuration/)
- [containerd registry hosts configuration](https://raw.githubusercontent.com/containerd/containerd/main/docs/hosts.md)
- [RKE2 private registry configuration](https://docs.rke2.io/install/private_registry)
- [Deploy a registry](https://distribution.github.io/distribution/about/deploying/)
