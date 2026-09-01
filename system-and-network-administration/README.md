![sysadmin](../assets/sysadmin.png)

# System & network administration skills

Running machines, networks, containers and the automation that manages them —
tool reference and admin practice, independent of any language ecosystem. Every
skill here is deliberately version-free: pinned versions and site specifics belong
in the repo that owns the cluster, not in a shared skill.

Rough reading order for a bare-metal Kubernetes stack:
[kubernetes-concepts](kubernetes-concepts/SKILL.md) → [kubernetes-rke2](kubernetes-rke2/SKILL.md)
→ [kubernetes-cilium-concepts](kubernetes-cilium-concepts/SKILL.md) → [kubernetes-gpu](kubernetes-gpu/SKILL.md),
with [docker](docker/SKILL.md), [docker-registry](docker-registry/SKILL.md) and
[docker-engine-api](docker-engine-api/SKILL.md) covering what feeds it images.

## Containers

### [docker](docker/SKILL.md)

Docker and Compose as one workflow, covering the decisions and traps rather than
the basics. The Dockerfile rules that pay rent: order layers by change frequency so
a source edit does not rebuild the dependency layer, multi-stage for anything
compiled, cleanup in the same `RUN` that made the mess, `USER` non-root,
`.dockerignore` as non-optional, and `CMD` in exec form — shell form wraps PID 1 in
`/bin/sh`, which swallows SIGTERM and turns every stop into the ten-second kill
timeout.

Then compose service wiring (healthcheck-gated `depends_on`, networks, volumes, env
precedence, profiles, overrides) and a debug ladder for a service that will not come
up or cannot be reached. Also notes the CLI split: `docker compose` v2 is current,
the `version:` key is obsolete, and the project name defaults to the directory name.

**Load when** writing or debugging Dockerfiles or compose files.

### [docker-registry](docker-registry/SKILL.md)

The `registry:2` image is two products behind one binary, and the expensive mistake
is assuming it is one: `proxy.remoteurl` turns it into a read-only pull-through
cache mirroring exactly **one** upstream. A cache for Docker Hub plus somewhere to
push your own builds is two deployments, not one with two configs.

Covers wiring containerd to it (per-host resolution, not Docker's
`--registry-mirror`), the trap that the upstream default endpoint is **always tried
last** — so an unreachable mirror does not fail a pull, it quietly goes out to the
internet — naming across the three access paths that are not interchangeable, why a
dotless registry name is read as a Docker Hub namespace, and the per-client rules
for plain HTTP.

**Load when** running a registry, wiring containerd to one, or diagnosing pulls that
bypass the mirror.

### [docker-engine-api](docker-engine-api/SKILL.md)

For code that speaks the Engine API over the socket instead of shelling out to
`docker` — the CLI hides everything a client has to handle. Covers version
negotiation and what a too-new version does, the response shapes that are not
errors (204 with no body, 304 for "already in that state"), and the fact that a
failed build, pull or push is still **HTTP 200** with the failure buried as
`errorDetail` inside the NDJSON event stream.

The centrepiece is the multiplexed stream: `logs`, `attach` and `exec/start`
return 8-byte-framed data for every container created **without** a TTY, and raw
text with one — so hand-testing interactively shows clean output while the shipped
client emits header bytes into real callers' logs. Also filters (a JSON map of
string to array of *string*; a wrong shape returns an unfiltered list, never a
400), `X-Registry-Auth` needing its base64 padding, `X-Registry-Config` for
builds, and where Podman's compat socket stops being Docker.

**Load when** writing or debugging an Engine API client, probing the socket with
`curl`, or chasing garbled log output, a 400 on push, or filters that match
nothing.

## Kubernetes

### [kubernetes-concepts](kubernetes-concepts/SKILL.md)

The big picture, independent of any client library: control plane and node
components, the resource hierarchy and how ownership and selectors tie it together,
the networking model with its four rules and service discovery, the PV/PVC storage
model, scheduling, and RBAC.

**Load when** reasoning about Kubernetes itself rather than about a specific tool.

### [kubernetes-rke2](kubernetes-rke2/SKILL.md)

RKE2 and K3s share an agent codebase, so this is one skill for both, with the
differences named where they exist.

The config file is the interface, and it is read exactly once at start — a changed
`config.yaml` means a service restart. Drop-ins merge alphabetically and the last
value for a key **replaces** a list rather than extending it, unless the `+` suffix
says otherwise. Agents join on **9345**, not 6443. `cni: none` leaves the cluster
deliberately broken until a CNI is installed — that is the expected middle state,
not a failed install. Also covers `registries.yaml` and its two differently-keyed
sections, airgap installs, the K3s differences that bite (RKE2's systemd unit sets
no `PATH`), and why a partial containerd template silently drops the mirrors, the
sandbox image and the CNI settings.

**Load when** installing or configuring RKE2 or K3s, or when a node is stuck
NotReady.

### [kubernetes-cilium-concepts](kubernetes-cilium-concepts/SKILL.md)

Cilium replaces a whole stack of separate components — CNI, kube-proxy,
NetworkPolicy including L7, encryption, ingress, and observability. If a cluster
runs Cilium *and* nginx-ingress or Istio, that is a decision to question rather than
a given.

Covers what changes once `kubeProxyReplacement` is on (no iptables service rules to
inspect; debugging moves to `cilium-dbg` and Hubble), Gateway API with the CRDs that
must be installed *before* Cilium, LB-IPAM and L2 announcements as the bare-metal
substitute for a cloud LoadBalancer, operator CRD timing, network policy, and
version coupling.

**Load when** working on a Cilium cluster — eBPF routing, Gateway API, LB-IPAM, or
service routing that misbehaves.

### [kubernetes-gpu](kubernetes-gpu/SKILL.md)

Four things must line up before a pod can use a GPU: a kernel driver on the host, a
container runtime that can inject devices, a device plugin advertising
`nvidia.com/gpu`, and a scheduling request for it. Every failure is one of the four
missing — or two of them installed twice.

Detect the card from sysfs vendor and class IDs, never from a model list: `lspci`
renders names from a `pci.ids` file that is always older than the newest card, so a
current GPU matches no marketing name while vendor `0x10de` keeps working. Then host
driver versus GPU Operator (never both), the container toolkit and RuntimeClass under
CDI, telling the operator where containerd lives, NFD discovery labels, and verifying
from node capacity inward.

**Load when** getting NVIDIA GPUs onto Kubernetes, or when `nvidia.com/gpu` is
missing from node capacity.

## Automation

### [rex](rex/SKILL.md)

Rex is a Perl automation framework driven by a `Rexfile`. The skill exists mostly
for one trap: `set connection => 'OpenSSH'` makes every file operation call
`Rex::get_sftp()`, so on a host without an SFTP subsystem it crashes with a
misleading `Can't call method "stat" on an undefined value`. The fix is the LibSSH
backend, which does file operations over exec channels instead.

Includes a table of which `Rex::Commands` actually need SFTP, the `Rex::Interface`
architecture that explains why, the gather and run command surfaces, and Getty's own
Rex distributions on CPAN (`Rex-LibSSH`, `Rex-GPU`, `Rex-Rancher`). Closes with ten
gotchas — among them that `<> line N` in an error message is Perl's `$.` tracker and
not a source line, and that a Rex task name silently overwrites an imported function
of the same name.

**Load when** writing or debugging a Rexfile or Rex task.
