![sysadmin](../assets/sysadmin.png)

# System & network administration skills

Running machines, networks, containers and the automation that manages them —
tool reference and admin practice, independent of any language ecosystem. No skill
here carries site specifics: those belong in the repo that owns the cluster. Several
are routers over a reference tree and name the date or release their research was
checked against — release-dependent facts are to be rechecked against what is
actually installed.

Rough reading order for a bare-metal Kubernetes stack:
[kubernetes-concepts](kubernetes-concepts/SKILL.md) → [kubernetes-rke2](kubernetes-rke2/SKILL.md)
→ [kubernetes-cilium-concepts](kubernetes-cilium-concepts/SKILL.md) → [kubernetes-gpu](kubernetes-gpu/SKILL.md),
with [docker](docker/SKILL.md), [docker-registry](docker-registry/SKILL.md) and
[docker-engine-api](docker-engine-api/SKILL.md) covering what feeds it images.

## Containers

### [docker](docker/SKILL.md)

A decision and operations skill for Docker images, local and remote Engines, and
Compose applications. `SKILL.md` is a small entrypoint: a task-and-symptom table
routes to references on building (Dockerfile design, contexts, cache and CI, secrets
and SSH, multi-platform, Bake, supply chain), on Compose (project model,
interpolation, merge and include, health and lifecycle, networks, volumes, Watch,
resources, deploy and rollback) and on operations (diagnostic ladder, daemon and
storage, backup, rootless and Desktop, security and agent access).

The rules it keeps in front: start from the target context rather than from a
command, and render the Compose model before applying it. Interpolation sources are
not container environment, readiness is not creation order, a restart does not apply
changed configuration, and a read-only socket mount is not a read-only API. No prune
or `down -v` without scope and a recovery path. Ships a modular Compose lab,
environment and lifecycle fixtures, and a read-only evidence script.

**Load when** designing, building, debugging or operating Docker images or Compose
stacks.

### [docker-registry](docker-registry/SKILL.md)

Registry protocol and operations, with writable image storage, pull-through caching,
runtime configuration and artifact retention kept apart — a cache is not
interchangeable with a private push destination. Routes by task to references on
roles and naming, TLS and auth, reverse proxies and uploads, storage, the per-client
mirror wiring (Docker and BuildKit, containerd hosts, K3s/RKE2), manifests and
indexes, retention and garbage collection, backup and migration, and OCI referrers.

A successful pull does not prove the mirror was used: test the cold-cache, the
warm-cache and the upstream-denied path from the client that actually pulls. A login
in one client authenticates no other runtime, and retention is a content-graph
policy, not a list of old tags. Ships a loopback lab, a secure-pair template (a TLS
writable registry beside a Hub cache), client config fragments and a read-only
registry probe.

**Load when** running a registry or cache, wiring a client to one, or diagnosing
pulls that bypass the mirror.

### [docker-engine-api](docker-engine-api/SKILL.md)

For software that speaks the Engine API directly instead of delegating to the CLI —
a protocol and client-engineering guide, not an endpoint dump. It starts with the
contract: record the server's API range and the client's, select a supported
intersection, and never adopt the daemon maximum because it is advertised.
Wire-format examples are pinned to Moby 28.5.2 / API 1.51.

Routes to references on transport and discovery, request shapes and filters,
container lifecycle, multiplexed output and hijacked attach/exec, progress streams
that report false success, registry auth, events and stats, archives, prune, and
Podman compatibility. The client invariants: keep transport errors, endpoint status,
streamed operation errors and exit status apart; parse non-TTY frame headers across
arbitrary network boundaries; a malformed filter is not a safe deletion guard. Ships
a Python helper package — version negotiation, padded registry auth, bounded
multiplex and NDJSON parsers, tests, a read-only socket probe.

**Load when** writing or debugging an Engine API client, or chasing garbled log
output, a pull that falsely succeeds, or filters that match nothing.

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

Authoring, reviewing, debugging and safely operating Perl Rex automation. The
researched baseline is Rex 1.16.1, with source observations pinned in
`SOURCE_LOCK.json`.

Opens with ten safeguards. A Rexfile is executable Perl — listing tasks or compiling
it can already load code. No host can mean local execution, so locality has to be
proven. A successful `run 'true'` does not validate filesystem access, an argument
array is shell-quoted rather than shell-free, and `rex -c` enables caching, not a
check mode. Then a task table into references on the execution model, tasks,
inventory and CMDB, transports (capability matrix, OpenSSH, LibSSH, the SFTP-less
procedure, sudo), run status and quoting, idempotency, resources, testing, module and
backend authoring, and the optional `Rex::GPU` and `Rex::Rancher` integrations.

Ships examples, a heuristic Rexfile audit script, an offline module inventory, and
change-brief and bug-report templates. The package also carries its own validation
record, and the superseded original skill under `audit/` — for audit only, not as
guidance.

**Load when** writing, reviewing or debugging a Rexfile or Rex task, or choosing a
Rex transport.

## Hosting

### [hetzner-operator](hetzner-operator/SKILL.md)

Planning, provisioning, connecting, securing and troubleshooting Hetzner
infrastructure across Console/Cloud, Robot (dedicated and auction servers) and
managed hosting. The method: model the system, then describe public ingress, operator
access, outbound access and server-to-server traffic separately — each with source,
destination, port, authentication, forward path and return path. Inspect before
changing, and verify with a real application path and a denied one.

It guards against assumptions carried over from other clouds. Nothing like an
AWS-style VPC, a managed NAT gateway, a managed database or managed Kubernetes exists
merely because a design needs one. A private Cloud Network is a routed underlay, a
Load Balancer supplies neither general egress nor WireGuard UDP transport, and a
private subnet is not a security boundary.

A task table routes into 28 references: Cloud networking, public IPs, private egress
and NAT, Load Balancers, VPN architecture, vSwitch, firewalls, storage, database
recovery, automation and IaC, DNS, Kubernetes, cost, troubleshooting, and community
patterns kept apart from documented behaviour. Ships a WireGuard site-to-site runbook
with hub, office and admin config examples, an nftables policy and an offline
topology validator. Research snapshot 2026-10-04; prices, limits and API facts are to
be rechecked live.

**Load when** designing, building or debugging anything on Hetzner — Cloud, Robot,
private networks, VPN access, storage or cost.

## TLS and PKI

### [ssl-tls-pki](ssl-tls-pki/SKILL.md)

Designing, deploying, auditing, operating and debugging TLS and the PKI behind it:
public Web PKI, private certificate authorities, ACME and Let's Encrypt, mTLS,
chains, trust stores, and TLS clients across operating systems and runtimes. "SSL"
is taken as the user's umbrella term, never as a request to enable obsolete
protocols.

Modular: `SKILL.md` holds an eight-step workflow from inventory to report and routes
through `CONTENTS.md` into the branches — foundations, public PKI, ACME, private PKI,
deployment, clients, debugging, operations. Draw every TLS hop. A trusted client
certificate is not an authorization policy. A failure is never fixed by disabling
verification or by installing a root obtained from an unauthenticated peer. Test with
the real consuming client and check the live certificate at every termination point,
not a file or a controller status.

Ships a local lab, certificate inspection tooling, config examples, a claim ledger
with its sources and a validation report. Snapshot 2026-10-10, with a policy calendar
for the claims that carry a date.

**Load when** setting up or debugging HTTPS, certificates, ACME renewal, a private CA
or mTLS, or analysing a TLS incident.

## Inference serving

### [vllm-operator](vllm-operator/SKILL.md)

Planning, installing, running, measuring and tuning vLLM on affordable hardware —
consumer GPUs, small workstations, DGX Spark, small rented GPU servers (1-4 GPUs).
Written in German. `SKILL.md` is a router and workflow: it points at the matching one
of 28 numbered references (engine fundamentals, memory capacity, prefix/KV caching and
offload, scheduling under load, benchmarking, metrics and tracing, quantization,
multi-GPU, deployment security, troubleshooting, recipes) instead of dumping them into
context. Ships measurement scripts (capacity, cost, bench sweep, stream probe, metrics
inventory), config templates (nginx, Prometheus, OTel, KV offload) and experiment
templates. Optimises correct answers within a latency budget per euro, not headline
tokens/s, and refuses to invent GPU benchmark numbers.

**Load when** serving an LLM with vLLM, sizing GPU memory or context, diagnosing TTFT/ITL
or OOM, or deciding on multi-GPU.
