# Configuration files: readers, timing, restart, and verification

> Read when: changing registry/client configuration or designing automation around it.

Keep configuration ownership and consumption time explicit. Editing a file is not proof that the active process uses it.

| File/input | Reader and timing | Apply and verify |
|---|---|---|
| Distribution config YAML | Registry process at startup | Restart/recreate the intended instance; verify selected config path and behavior |
| `REGISTRY_*` environment | Registry startup configuration override | Change container/service config, recreate; inspect only non-secret effective evidence |
| TLS/htpasswd material | Registry/auth implementation; rotation behavior varies | Use a controlled restart unless hot reload is documented/tested for that version |
| Docker `daemon.json` | Docker daemon | Some options reload, others need restart; follow option-specific docs and validate first |
| containerd main `config.toml` | containerd daemon/plugin startup | Updating `config_path` typically needs daemon restart; inspect plugin configuration |
| containerd `certs.d/*/hosts.toml` | Registry resolver | Hosts-directory updates are designed not to require daemon restart; test a new pull |
| K3s/RKE2 `registries.yaml` | Distribution startup/config generation | Restart affected node service in a controlled rollout; inspect generated runtime config |
| Client login/credential helper | The invoking client/tool | Verify with that exact client identity and endpoint |
| BuildKit registry settings | The selected builder | Apply to that builder, not just Docker Engine; verify worker-side pull |

This table is a routing guide. Long-running transfers can retain old connections/tokens even after files change. Validate new sessions and authentication rotation explicitly.

## Change procedure

Identify the live reader and exact path. Back up current configuration without exposing secrets. Render/validate the new structure, explain required restart and workload impact, apply only to the intended service, and test the behavior that motivated the change. Keep a rollback path and record old/new config hashes rather than copying secrets into change logs.

Do not edit generated containerd config inside K3s/RKE2 as the durable source of truth. Do not overwrite an existing `daemon.json` merely to add a mirror; merge intentionally, preserve unrelated settings, and detect conflicts with daemon command-line flags.

## Primary sources

- [Distribution configuration](https://distribution.github.io/distribution/about/configuration/)
- [Docker daemon configuration](https://docs.docker.com/engine/daemon/)
- [containerd registry hosts configuration](https://raw.githubusercontent.com/containerd/containerd/main/docs/hosts.md)
- [K3s private registry configuration](https://docs.k3s.io/installation/private-registry)
- [RKE2 private registry configuration](https://docs.rke2.io/install/private_registry)
