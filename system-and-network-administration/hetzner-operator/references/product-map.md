# Product and control-plane map

Evidence snapshot: **2026-10-04**. Product names describe capabilities; live orderability, pricing, hardware generations, quotas and locations must be checked again when selecting or buying a service.

## Contents

- [Choose the responsibility boundary](#choose-the-responsibility-boundary)
- [Find the correct administration surface](#find-the-correct-administration-surface)
- [Understand the product families](#understand-the-product-families)
- [Discover current offers](#discover-current-offers)
- [Build a coherent design](#build-a-coherent-design)

## Choose the responsibility boundary

Start with the workload and the operator's responsibilities, not a server SKU. Determine whether the user needs root access, a supported web-hosting environment, file collaboration, backup storage, object access, or physical hardware. Hetzner's documentation deliberately separates Cloud, Robot, Managed, Network & Security, and Storage; these products have different lifecycle and networking contracts. [Official documentation map](https://docs.hetzner.com/).

For a self-operated application, record who owns operating-system updates, application deployment, database recovery, certificate renewal and on-call response. A virtual machine with dedicated CPU resources is still a virtual machine; it does not imply managed application operations. Conversely, a managed hosting product trades root-level control for an administered server stack. [Cloud server overview](https://docs.hetzner.com/cloud/servers/overview/), [managed server responsibilities](https://www.hetzner.com/managed-server/).

## Find the correct administration surface

| Surface | Primary responsibilities | Mistake to avoid |
|---|---|---|
| Hetzner Console | Cloud projects, servers, networking resources; current DNS, Object Storage and Storage Box administration | Treating every product as the same Cloud API resource |
| Robot | Dedicated root servers, Server Auction machines, vSwitch, dedicated-server recovery, hardware support, Domain Registration Robot, colocation administration | Applying a Cloud Firewall or Cloud Floating IP recipe directly to a dedicated server |
| konsoleH | Web Hosting, Managed Servers, Storage Share and associated hosting/domain administration | Calling it obsolete because DNS management moved |
| accounts.hetzner.com | Central customer and login details | Confusing account identity with a project's access rights |
| Product data interfaces | SSH/RDP to a server; S3-compatible requests to Object Storage; file protocols to Storage Box; Nextcloud interface to Storage Share | Assuming an administrative API credential also authenticates to stored data |

Sources: [documentation map](https://docs.hetzner.com/), [Object Storage overview](https://docs.hetzner.com/storage/object-storage/overview/), [current Storage Box overview](https://docs.hetzner.com/storage/storage-box/general/), [konsoleH product/account overview](https://docs.hetzner.com/managed/administration-on-konsoleh/account-overview/), [current DNS administration](https://docs.hetzner.com/managed/domain-and-dns/dnsadministration/).

The Storage Box overview was updated on 2026-09-18 and explicitly uses Console. Older comparison articles may still refer to Robot. Prefer the current product-specific procedure, and inspect where an existing resource actually appears before automating a legacy account.

## Understand the product families

| Family | Candidate use | Selection questions |
|---|---|---|
| Cloud shared resources | Small services, development, bursty applications, elastic workers | Does tail latency remain acceptable under sustained load? Is the software available for the selected architecture? |
| Cloud dedicated resources | Sustained CPU use with VM lifecycle and Cloud networking | Does the application need exclusive CPU allocation or actually an entire physical host? |
| Dedicated root servers | Sustained compute/storage, virtualization hosts, predictable hardware layout | Local disk recovery, replacement time, remote access and spare capacity? |
| Server Auction | Dedicated machines from changing inventory | Exact CPU, disks, RAM, NIC, location and extras in this individual offer? |
| Dedicated GPU/GEX | GPU workloads on a rented physical server | VRAM, supported numerical formats, driver/runtime compatibility, concurrency and model memory budget? |
| Web Hosting | Websites, supported runtimes, mail and hosting databases | Required processes, memory limits, runtime versions, SSH availability and domain setup? |
| Managed Server | Hosting stack with more resources and provider administration | Does the supported stack cover every required daemon, extension and privilege? |
| Object Storage | Application objects, artifacts and suitable backup repositories | S3 feature compatibility, consistency requirements, credentials and restore workflow? |
| Storage Box | File-based backup/archive and supported remote file access | Backup-tool compatibility, retention, restricted account access and tested recovery? |
| Storage Share | Managed Nextcloud-based file collaboration | Users, sharing policy, supported apps and export/recovery requirements? |
| Colocation/custom solutions | Customer-owned or specially arranged infrastructure | Present availability, power, remote hands, uplink and physical maintenance? |

The catalog includes these distinct families; their use-case matching above is engineering guidance, not a claim that every plan includes every feature. Consult the [product catalog](https://www.hetzner.com/), [Server Auction FAQ](https://docs.hetzner.com/robot/general/server-auction-faqs/), and dedicated modules for implementation.

Cloud building blocks also include Volumes, Backups/Snapshots, Primary/Floating IPs, Networks, Firewalls, Load Balancers and Placement Groups. Select their persistence, ingress, routing or failure-isolation role explicitly. [Cloud resource map](https://docs.hetzner.com/cloud/servers/overview/). DNS hosting and certificate products are separate catalog services; buying compute does not establish domain registration or certificate renewal.

Two snapshot-specific availability traps matter: the **RX ARM dedicated** page currently says no RX servers can be offered; this does not remove Cloud ARM as a separate option. The **colocation FAQ** currently says no new data-center space is available until further notice, even though the sales page describes the service. Never turn a catalog category into an availability guarantee. [RX status](https://www.hetzner.com/dedicated-rootserver/matrix-rx/), [colocation availability](https://docs.hetzner.com/robot/colocation/faq/).

## Discover current offers

1. Capture the user's architecture, geography, storage, traffic and availability requirements.
2. Read the current catalog and applicable product FAQ. For Cloud, query server types, locations, images, pricing and project limits through the current API/CLI. Record timestamp and account/project context. [Cloud API](https://docs.hetzner.cloud/reference/cloud).
3. Distinguish catalog existence, regional support, current capacity, account quota and actual reservation. A listed type does not reserve capacity.
4. Compare total cost: compute, public IPs, load balancing, disks, snapshots/backups, object/file storage, external traffic, setup fees, taxes and operational work.
5. For dedicated offers, preserve the actual offer configuration. Replacing one Auction machine with another may change hardware and recovery assumptions.

## Build a coherent design

For a typical application, map each requirement separately: frontend ingress, administrative access, inter-service communication, outbound downloads, persistence and recovery. Then choose products that implement those paths. A Load Balancer, a VPN gateway and a backup target solve different requirements.

Do not infer an AWS-style managed PostgreSQL, managed Kubernetes, container registry or serverless platform from Cloud VMs, Apps, or networking integrations. With a self-deployed stack, assign those duties explicitly to the operator or a separately selected managed service. Hosting databases inside Web Hosting/Managed Server have that hosting product's contract; they are not evidence of a generic Cloud database service. Start at [cloud-compute.md](cloud-compute.md), [dedicated-robot-rescue.md](dedicated-robot-rescue.md), [hybrid-vswitch.md](hybrid-vswitch.md), or [managed-web-domains.md](managed-web-domains.md).
