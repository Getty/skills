# Client configuration fragments

These are intentionally **fragments**, not complete machine configurations. Replace example domains/CA paths and merge through your existing configuration management. Do not overwrite Docker/containerd defaults, auth configuration, runtime settings, or existing registry mappings.

`docker-daemon.fragment.json` configures a Docker Hub mirror on the Engine. It does not configure a separate BuildKit worker. `containerd-2.fragment.toml` selects the hosts directory for a containerd 2.x CRI plugin. `hosts.toml` allows upstream fallback; `hosts-mirror-only.toml` deliberately selects the mirror as the namespace server. These are alternatives, not files to concatenate.

The mirror is granted `resolve` only because the example assumes an internally trusted endpoint. Remove that trust for an untrusted mirror and design tag resolution accordingly. Client capabilities are not a server authorization policy. CA files must exist; credentials are not included. The secure-pair example requires additional tested client authentication configuration.

`registries.yaml` is for the appropriate K3s or RKE2 source path. `disable-default-registry-endpoint` is a node/distribution option, **not** a field to insert under `configs` here. Check release support and remember that unconfigured registries may still fall back. Standalone containerd hosts-directory reload behavior differs from distribution-generated configuration.

After applying, use the actual CRI/Engine/BuildKit actor to pull a known uncached digest. Correlate mirror logs and egress. A successful `ctr` pull without the intended hosts directory does not prove kubelet's CRI path works.
