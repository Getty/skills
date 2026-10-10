---
name: hetzner-operator
description: Plan, provision, connect, secure, optimize, and troubleshoot Hetzner infrastructure. Use for Hetzner Cloud, Console, Robot, dedicated and auction servers, public IPv4/IPv6, Primary and Floating IPs, private Networks, VPN gateways and headquarters connectivity, WireGuard, Tailscale, NAT, Load Balancers, vSwitch hybrid networking, firewalls, DNS, storage, backups, managed hosting, hcloud, API, Terraform/OpenTofu, Ansible, Kubernetes, costs, and recovery. Distinguish documented capabilities from community workarounds and verify changing product, pricing, and API facts.
---

# Hetzner Operator

Build an explicit model of the requested Hetzner system, select the relevant references, and carry the task through design, implementation, or diagnosis as requested. Explain tradeoffs in the user's language. Keep commands and configuration identifiers precise.

Treat this package as operational guidance, not a frozen product catalog. Research snapshot: **2026-10-04**. Recheck live sources for prices, stock, limits, image behavior, permissions, supported features, API removals, and announced changes. Start with [evidence and refresh](references/evidence-and-refresh.md) when sources disagree.

## Working method

1. **Establish scope from the request and available state.** Identify the product and control plane, locations/network zones, existing resources, OS/network manager, desired access, and acceptable downtime. Ask only for missing information that changes a concrete decision; continue useful independent work. Label invented addresses and sizes as examples.
2. **Separate traffic purposes.** Describe public application ingress, operator access, outbound Internet access, and server-to-server traffic separately. For each needed flow, name source, destination, protocol/port, authentication, encryption, forward path, and return path. Include public IPv6 when assessing exposure.
3. **Read selectively.** Use the routing table below. For a VPN task read the VPN architecture and WireGuard implementation references first, then the networking/firewall details needed by the design. Do not load every file for a small task.
4. **Inspect before changing.** Gather current CLI/provider versions, project and resource IDs, Network/subnet ranges, provider routes, guest addresses/routes, relevant firewall rules, and application bindings. Prefer read-only API/CLI output and OS evidence. Use the current CLI help/API schema; do not guess flags or rely on obsolete datacenter fields.
5. **Make a reviewable design.** Provide a resource/traffic table, both routing layers, relevant configuration, cost components, failure dependencies, and a rollback/recovery path. Choose the smallest design meeting the stated needs. Distinguish a starting recommendation from a provider guarantee.
6. **Implement within the user's authorization.** Make targeted changes, preserve working management access, and protect existing state. Do not create resources or move production traffic merely to answer an informational question. Before destructive replacement or data loss, resolve the particular authorization or missing recovery information; do not add repetitive permission gates to ordinary authorized work.
7. **Verify the intended behavior.** Test the real application path and a denied path, inspect source addresses and return routes, and check persistence after a controlled restart when authorized. For failover, test route changes, application recovery, and reconnects together. State whether results are documentation review, offline validation, a lab test, or a live deployment.

## Product and architecture decisions

- Map Console/Cloud, Robot, and managed-hosting administration explicitly; read [product map](references/product-map.md) before choosing unfamiliar products. Do not assume an AWS-style VPC, managed NAT gateway, managed database, or managed Kubernetes service exists merely because a design needs one.
- Treat a private Cloud Network as a routed underlay. Use its provider gateway as the guest next hop and configure Cloud routes separately. Keep provider source validation distinct from Linux reverse-path filtering. Follow [Cloud networking](references/cloud-networking.md).
- Choose an administration path deliberately: an SSH bastion, WireGuard gateway, outbound site connector, or controlled mesh/subnet router. A private VM needs a real path to an external VPN endpoint. A managed Load Balancer does not supply general outbound Internet access or WireGuard UDP transport. Follow [VPN access](references/private-access-vpn.md) and [Load Balancers](references/load-balancers.md).
- Treat connectivity and permission as separate controls. Private subnets do not imply a security boundary, and private transport does not imply encryption. Check the provider firewall, host firewall, container forwarding, and application authentication. Follow [security](references/security-firewalls.md).
- Select storage by access and recovery semantics. Do not equate a server disk, Volume, S3 Object Storage, Storage Box, or Storage Share. Include data excluded from VM backups in application-consistent restoration. Follow [storage selection](references/storage-selection.md) and [database recovery](references/database-recovery.md).
- Model availability end to end. A second application VM does not duplicate its VPN/NAT gateway, database, storage, DNS/control plane, office uplink, or secrets. State which failures the design tolerates. Use [architecture recipes](references/architecture-recipes.md).

## Reference routing

Each reference contains its own relevant sources. Read upstream documentation for the particular action instead of expanding the entire package.

| Task | Read |
|---|---|
| Select products and administration surface | [Product map](references/product-map.md) |
| Cloud types, images, rescale, placement, bootstrap | [Cloud compute](references/cloud-compute.md) |
| Bare metal, Auction, Robot, installimage, RAID, Rescue/KVM | [Dedicated operations](references/dedicated-robot-rescue.md) |
| Join Cloud and dedicated infrastructure | [Hybrid vSwitch](references/hybrid-vswitch.md) |
| Web hosting, managed servers, domains, konsoleH | [Managed hosting](references/managed-web-domains.md) |
| Cloud routes, gateways, addresses, MTU | [Cloud networking](references/cloud-networking.md) |
| Primary/Floating IPs, IPv4 savings, IPv6 exposure | [Public IPs](references/public-ips.md) |
| Private-server updates, APIs, registry and backup access | [Private egress and NAT](references/private-egress-nat.md) |
| Public/private application ingress and health checks | [Load Balancers](references/load-balancers.md) |
| Choose a VPN, bastion, mesh, or headquarters connection | [Private access and VPN architecture](references/private-access-vpn.md) |
| Implement a WireGuard hub, office peer, and admin client | [WireGuard site-to-site runbook](references/wireguard-site-to-site.md) |
| Encrypt traffic entirely between private Hetzner servers | [Internal WireGuard](references/vpn-inside-private-network.md) |
| One public gateway, separate ingress, stronger availability | [Architecture recipes](references/architecture-recipes.md) |
| Provider/host firewall, private policy, roles, secrets | [Security and firewalls](references/security-firewalls.md) |
| Choose storage and avoid incompatible uses | [Storage selection](references/storage-selection.md) |
| Volumes, disks, server backups and snapshots | [Volumes and VM recovery](references/volumes-backups-snapshots.md) |
| S3, Object Lock, versioning, encryption, compatibility | [Object Storage](references/object-storage.md) |
| Storage Box protocols and backups; Storage Share | [Storage Box and Share](references/storage-box-share.md) |
| Restore databases, Forgejo, registries and associated data | [Database and application recovery](references/database-recovery.md) |
| hcloud, REST, Terraform/OpenTofu, Ansible, cloud-init | [Automation and IaC](references/automation-api-iac.md) |
| DNS Console/API, delegation, reverse DNS, TLS | [DNS and TLS](references/dns-tls.md) |
| Self-managed Kubernetes, CCM/CSI, Docker, private bootstrap | [Kubernetes and containers](references/kubernetes-containers.md) |
| CPU, disk, network, latency and load measurement | [Observability and performance](references/observability-performance.md) |
| Prices, quotas, availability, retained resources, cancellation | [Cost and lifecycle](references/cost-capacity-lifecycle.md) |
| Diagnose outages and preserve recovery access | [Troubleshooting runbooks](references/troubleshooting-runbooks.md) |
| Evaluate popular workarounds and their tradeoffs | [Community patterns](references/community-patterns.md) |
| Firsthand reports, their dates and corroboration limits | [Community evidence](references/community-evidence.md) |
| Refresh changing facts and reconcile conflicting sources | [Evidence and refresh](references/evidence-and-refresh.md) |

## VPN implementation resources

Use [WireGuard site-to-site](references/wireguard-site-to-site.md) as the implementation entry point. It supplies prerequisites, Cloud and guest routes, firewall integration, tests, SNAT alternative, rollout, and rollback. The example permits selected administrators to initiate management connections; widen policy only for actual required flows.

- [Topology example](assets/wireguard-topology.json): a routed Cloud/office/VPN address and route plan without credentials.
- [Hub configuration](assets/wireguard/hub.conf.example), [office configuration](assets/wireguard/office.conf.example), and [administrator configuration](assets/wireguard/admin.conf.example): replace documentation addresses, interface names, and key placeholders locally before use.
- [Hub firewall](assets/wireguard/hub.nft.example): an illustrative nftables policy for a dedicated gateway; integrate it with the existing firewall instead of flushing other rule owners.
- [Topology validator](scripts/validate_topology.py): validate this example schema offline using Python's standard library. It checks CIDR overlaps, reserved/duplicate addresses, missing Cloud return routes, and wrong guest next hops. It neither provisions infrastructure nor proves that a live firewall, tunnel, or network manager is correct.

Run from the skill directory:

```bash
python3 scripts/validate_topology.py assets/wireguard-topology.json
```

When adapting the input, provide all participating private application servers and relevant existing address ranges. The schema intentionally represents one routed IPv4 Cloud Network and one VPN gateway; use the references for NAT, overlapping address translation, multiple gateways, or IPv6 transport.

## Deliver useful answers

For a design, lead with the recommended arrangement, explain why it fits, and make resources and traffic paths concrete. For implementation, supply environment-specific steps and verification. For diagnosis, identify the observed failing layer and next discriminating check. For optimization, compare total cost, measured behavior, operational work, and recovery consequences.

Cite provider facts with the source supporting that particular claim. Label community observations with their date and environment; use them to form hypotheses or select tests. Do not promote a forum workaround to a supported feature. When a detail cannot be verified, state the gap and avoid making it a deployment dependency.
