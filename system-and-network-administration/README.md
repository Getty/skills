# System & network administration skills

Running machines, networks, containers, and the automation that manages
them — tool-specific reference and admin practice, independent of any
language ecosystem.

| Skill | Covers |
|---|---|
| [docker](docker/SKILL.md) | Docker and Compose as one workflow — Dockerfile layering and multi-stage builds, compose service wiring (healthcheck-gated depends_on, networks, volumes, env precedence, profiles, overrides), and the debug ladder. |
| [docker-registry](docker-registry/SKILL.md) | Running a registry — why a pull-through cache and an image store are two deployments, containerd mirror wiring and the always-tried upstream fallback, naming across the three access paths, per-client plain-HTTP rules. |
| [getty-rex](getty-rex/SKILL.md) | Rex automation framework — Rexfiles, connection types, commands, SFTP limitations, and the LibSSH backend. |
| [kubernetes-concepts](kubernetes-concepts/SKILL.md) | Kubernetes concepts, architecture, resource relationships, networking, storage, RBAC — the big picture without language-specific typing. |
| [kubernetes-cilium-concepts](kubernetes-cilium-concepts/SKILL.md) | Cilium on Kubernetes — eBPF networking, kube-proxy replacement, Gateway API, LB-IPAM/L2 on bare metal, CiliumNetworkPolicy, Hubble. Version-free concepts; site specifics stay in cluster repos. |
| [kubernetes-gpu](kubernetes-gpu/SKILL.md) | NVIDIA GPUs on Kubernetes — sysfs detection over model lists, host driver vs GPU Operator, the container toolkit and RuntimeClass under CDI, NFD labels, and proving the stack from node capacity. |
| [kubernetes-rke2](kubernetes-rke2/SKILL.md) | RKE2 and K3s — config.yaml and its merge rules, joining agents on 9345, `cni: none` and what it deliberately breaks, registries.yaml, airgap installs, and the K3s differences that bite. |
