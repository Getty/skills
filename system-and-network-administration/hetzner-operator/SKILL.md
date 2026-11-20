---
name: hetzner-operator
description: "Use when planning, building or debugging anything on Hetzner — Cloud, Robot and dedicated servers, Floating IPs, Networks and vSwitch, VPN and NAT, Load Balancers, firewalls, Volumes, Storage Box, Object Storage, hcloud, Terraform/OpenTofu, costs, recovery."
---

# Hetzner Operator

Model the requested Hetzner system explicitly; carry the task through design,
implementation or diagnosis as requested. Explain tradeoffs in the user's language; keep
commands and configuration identifiers precise.

Operational guidance, not a frozen catalog: facts date from the **2026-10-04** snapshot.
Recheck prices, stock, limits, image behavior, permissions, supported features, API
removals and announced changes live.

## Working method

1. **Scope:** product and control plane, locations/network zones, existing resources,
   OS/network manager, desired access, acceptable downtime. Ask only for missing facts
   that change a concrete decision; keep working meanwhile. Label invented addresses
   and sizes as examples.
2. **Separate traffic:** public ingress, operator access, outbound Internet,
   server-to-server. Per flow: source, destination, protocol/port, authentication,
   encryption, forward and return path. Include public IPv6 when assessing exposure.
3. **Read selectively:** only the routed references the task needs, never every file;
   then the upstream page each cites for the action at hand. VPN: private-access-vpn,
   then wireguard-site-to-site, then the networking/firewall detail the design needs.
4. **Inspect before changing**, read-only API/CLI output and OS evidence first: tool
   versions, project/resource IDs, Network/subnet ranges, provider routes, guest
   addresses/routes, firewall rules, application bindings. Take flags from current CLI
   help or the API schema; never guess them or use obsolete datacenter fields.
5. **Design for review:** recommended arrangement first and why it fits, then concrete
   resource/traffic table, both routing layers, configuration, cost components, failure
   dependencies, rollback/recovery path. Choose the smallest design meeting the stated
   needs; a starting recommendation is not a provider guarantee.
6. **Implement within the user's authorization:** environment-specific targeted changes,
   management access kept, existing state protected. Never create resources or move
   production traffic just to answer a question. Before destructive replacement or data
   loss, resolve that authorization or the missing recovery information; add no repeated
   permission gates to ordinary authorized work.
7. **Verify** the real application path and a denied path, source addresses, return
   routes, persistence after a controlled restart when authorized. Failover: test route
   change, application recovery and reconnects together. Label results as documentation
   review, offline validation, lab test or live deployment.

## Traps

- No AWS-style VPC, managed NAT gateway, managed database or managed Kubernetes exists
  just because a design needs one. Map Console/Cloud, Robot and managed-hosting
  administration explicitly.
- A Cloud Network is a routed underlay: guests route via its provider gateway, Cloud
  routes are set separately, provider source validation is not Linux `rp_filter`.
- A Load Balancer gives no general outbound Internet and no WireGuard UDP transport.
  Choose the admin path (bastion, WireGuard gateway, outbound connector, mesh) on purpose;
  a private VM needs a real path to an external VPN endpoint.
- Connectivity is not permission: private subnets are no security boundary, private
  transport is no encryption. Check provider firewall, host firewall, container
  forwarding, application authentication.
- Server disk, Volume, S3 Object Storage, Storage Box and Storage Share differ: choose by
  access and recovery semantics; application-consistent restore covers data VM backups
  exclude.
- A second application VM does not duplicate its VPN/NAT gateway, database, storage,
  DNS/control plane, office uplink or secrets. State which failures the design tolerates.

## Answers

- Diagnosis: the observed failing layer and the next discriminating check.
  Optimization: compare total cost, measured behavior, operational work and recovery
  consequences.
- Cite the source of each provider fact. Date community observations and name their
  environment; use them for hypotheses and test selection, and never promote a forum
  workaround to a supported feature. State an unverifiable detail as a gap, never a
  deployment dependency.

## Router

- [Products, administration surfaces](references/product-map.md)
- [Cloud types, images, rescale, placement, bootstrap](references/cloud-compute.md)
- [Bare metal, Auction, Robot, installimage, RAID, Rescue/KVM](references/dedicated-robot-rescue.md)
- [Join Cloud and dedicated servers](references/hybrid-vswitch.md)
- [Web hosting, managed servers, domains, konsoleH](references/managed-web-domains.md)
- [Cloud routes, gateways, addresses, MTU](references/cloud-networking.md)
- [Primary/Floating IPs, IPv4 savings, IPv6 exposure](references/public-ips.md)
- [Private-server egress: updates, APIs, registries, backups](references/private-egress-nat.md)
- [Application ingress, health checks](references/load-balancers.md)
- [Choose VPN, bastion, mesh, headquarters link](references/private-access-vpn.md)
- [Implement WireGuard hub, office peer, admin client](references/wireguard-site-to-site.md)
- [Bundled WireGuard configs, nftables, topology validator](references/wireguard-assets.md)
- [Encrypt traffic between private Hetzner servers](references/vpn-inside-private-network.md)
- [One public gateway, separate ingress, stronger availability](references/architecture-recipes.md)
- [Provider/host firewall, private policy, roles, secrets](references/security-firewalls.md)
- [Choose storage, avoid incompatible uses](references/storage-selection.md)
- [Volumes, disks, server backups, snapshots](references/volumes-backups-snapshots.md)
- [S3, Object Lock, versioning, encryption, compatibility](references/object-storage.md)
- [Storage Box protocols and backups; Storage Share](references/storage-box-share.md)
- [Restore databases, Forgejo, registries and their data](references/database-recovery.md)
- [hcloud, REST, Terraform/OpenTofu, Ansible, cloud-init](references/automation-api-iac.md)
- [DNS Console/API, delegation, reverse DNS, TLS](references/dns-tls.md)
- [Self-managed Kubernetes, CCM/CSI, Docker, private bootstrap](references/kubernetes-containers.md)
- [CPU, disk, network, latency, load measurement](references/observability-performance.md)
- [Prices, quotas, availability, retained resources, cancellation](references/cost-capacity-lifecycle.md)
- [Diagnose outages, keep recovery access](references/troubleshooting-runbooks.md)
- [Community workarounds, tradeoffs](references/community-patterns.md)
- [Firsthand reports, dates, corroboration limits](references/community-evidence.md)
- [Refresh facts; sources disagree](references/evidence-and-refresh.md)
