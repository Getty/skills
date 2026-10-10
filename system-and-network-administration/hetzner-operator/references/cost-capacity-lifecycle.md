# Cost, capacity, and resource lifecycle

Verified against primary documentation on **2026-10-04**. Obtain current prices for the account currency, VAT treatment, location, plan, and billing period before quoting a total. This module intentionally avoids a fixed price list.

## Contents

- [Build a complete cost model](#build-a-complete-cost-model)
- [Resource lifetime and billing](#resource-lifetime-and-billing)
- [Traffic and Object Storage](#traffic-and-object-storage)
- [Resize and migration decisions](#resize-and-migration-decisions)
- [Capacity and performance planning](#capacity-and-performance-planning)
- [Availability has a cost](#availability-has-a-cost)
- [Retirement and verification](#retirement-and-verification)

## Build a complete cost model

Start with workload measurements and a resource inventory. Include compute, public addresses, load balancing, block storage, server images, independent backups, object storage, outbound traffic, and operational effort. Show steady-state cost separately from migration overlap and recovery capacity.

For each price, record its source, retrieval date, currency, tax basis, unit, included allowance, and minimum charge. A calculator result using the wrong location or older plan can be internally consistent and still be wrong for the proposed deployment. Use the [Cloud product calculator](https://www.hetzner.com/cloud/) and each relevant product's pricing page.

Compare options at the same service level. A single gateway carrying VPN, NAT, and ingress can be economical, but its failure affects several functions simultaneously. Calculate the savings after gateway compute, retained addresses, monitoring, patching, and recovery work. Compare alternatives by expected workload and recovery requirements, not by VM count alone.

## Resource lifetime and billing

| Resource | Lifecycle fact to include in estimates |
|---|---|
| Cloud server | Hourly billing with a monthly cap; shutdown does not stop billing; deletion does |
| Primary IPv4 | Separate resource, billed even when unassigned; delete it to end that charge |
| Primary IPv6 | Currently free; when assigned and configured on a running server, provides public IPv6 connectivity subject to firewall policy |
| Floating IP | Independent priced resource; distinguish it from Primary IPs |
| Load Balancer | Hourly billing with a monthly cap |
| Volume | Independent block-storage resource, billed hourly with a monthly cap |
| Snapshot | Retained separately from the server; charged for compressed stored size |
| Server Backup | Tied to its server and deleted with it |

Sources: [Cloud billing](https://docs.hetzner.com/cloud/billing/faq/), [Floating IP overview](https://docs.hetzner.com/cloud/floating-ips/overview/), [Load Balancer FAQ](https://docs.hetzner.com/networking/load-balancers/faq/), [Volume overview](https://docs.hetzner.com/cloud/volumes/overview/), [Backup/Snapshot FAQ](https://docs.hetzner.com/cloud/servers/backups-snapshots/faq/).

For long inactivity, compare keeping the server with creating a restorable Snapshot and deleting compute. First record IP retention, external data, architecture, configuration, and restart dependencies. Server Backups and Snapshots omit attached Volumes; a Snapshot alone is not a complete recovery plan. [Backup/Snapshot FAQ](https://docs.hetzner.com/cloud/servers/backups-snapshots/faq/)

Cost-alert emails do not cap spending. Current billing rules also reprice legacy servers after rescaling, restoring deleted servers, or transferring to a project with a different currency. A same-currency project transfer or rebuild does not itself trigger this repricing. Verify the current rule before a lifecycle operation. [Cloud billing](https://docs.hetzner.com/cloud/billing/faq/)

## Traffic and Object Storage

Cloud billing distinguishes outgoing, incoming, and internal traffic. Public communication between Cloud servers in different network zones is outgoing traffic; same-zone Cloud traffic and private Network communication are treated differently. Do not infer that every address owned by Hetzner has the same traffic treatment. Record source product, destination, zone, and direction; use the relevant product's rule. [Cloud billing](https://docs.hetzner.com/cloud/billing/faq/)

Object Storage has an account-wide base charge for hours with at least one active Bucket, including empty Buckets. Storage and egress allowances accrue hourly and are aggregated across projects and locations; unused allowance does not roll over. Excess consumption is charged separately. Requests, ingress, and qualifying internal `eu-central` traffic are free, but resulting external egress can cost money. Small objects have a **64 kB minimum billable size**. [Object Storage overview](https://docs.hetzner.com/storage/object-storage/overview/)

Consequences for planning:

- Model TB-hours rather than assuming every temporary Bucket receives a full month's allowance.
- Include retained versions, incomplete multipart uploads, and backup retention when measuring stored data.
- Test restore traffic and time, not only upload cost.
- When consolidating clients behind NAT, check Object Storage limits per source IP as well as per Bucket; connection concentration can matter independently of total bytes.

The current overview publishes source-IP, Bucket, connection, request, and size limits. Read these live when designing high-concurrency clients. Treat published maxima as limits rather than guaranteed performance. [Object Storage overview](https://docs.hetzner.com/storage/object-storage/overview/)

## Resize and migration decisions

Cloud rescaling cannot shrink the current virtual disk, regardless of actual filesystem usage. Preserve disk size during a CPU/RAM upgrade when a future downgrade is important. Rescaling also stays within the same CPU architecture. Changing a server's location requires creating another server, for example from an image, rather than moving the existing instance. [Server FAQ](https://docs.hetzner.com/cloud/servers/faq/)

Volumes grow but do not shrink through the service. Guest filesystem growth is a separate step. To reduce allocated capacity, plan a new smaller destination, a consistent data copy, verification, cutover, and rollback. Never derive a resize command merely from a guessed `/dev/sdX` name. [Volume FAQ](https://docs.hetzner.com/cloud/volumes/faq/)

Primary IPs are location-bound; changing locations therefore also changes the public-address plan. Check `auto_delete` and protection settings before retiring compute. A retained Primary IP can be reassigned only within its supported scope. [Primary IP FAQ](https://docs.hetzner.com/cloud/servers/primary-ips/faq/)

## Capacity and performance planning

Request quota increases ahead of demand. Quota approval and physical capacity are different constraints. The current general FAQ lists unavailable resources, account limits, and temporary location restrictions as possible provisioning blockers; requests for larger limits are reviewed manually. [Cloud general FAQ](https://docs.hetzner.com/cloud/general/faq/)

Measure representative CPU, memory, I/O latency, throughput, connections, and tail latency. Shared plans suit variable load; dedicated-vCPU plans target sustained compute requirements. Verify architecture compatibility before choosing Arm for savings. [Cloud product guidance](https://www.hetzner.com/cloud/)

For a capacity fallback, specify acceptable alternate plans and locations before an incident. Include application images, storage placement, address changes, replication lag, and performance consequences. A spare resource held in reserve has a cost; a plan visible in the order form is not a reservation.

## Availability has a cost

Spread Placement Groups place Cloud servers on different physical hosts. This reduces a particular shared-host failure risk; it does not establish independent sites, credentials, gateways, or storage systems. [Placement Group overview](https://docs.hetzner.com/cloud/placement-groups/overview/)

Define recovery objectives and enumerate common dependencies: NAT, VPN, ingress, DNS, deployment state, database quorum, backup credentials, and provider account. Budget and test the response to losing each dependency. Two database machines require a deliberate quorum/failover design; their count alone does not establish safe automatic failover.

## Retirement and verification

Create a keep/delete manifest before destructive cleanup. Include IP resources, Volumes, Snapshots, Buckets and retained objects, Load Balancers, DNS, integrations, and backups. Validate a restore before deleting the source. After authorized deletion, reconcile provider inventory and current usage against the manifest, then check the invoice when available. Record any deliberately retained resource and its ongoing purpose.
