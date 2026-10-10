# Public addressing: Primary IPs, Floating IPs, and private-only servers

Evidence snapshot: 2026-10-04. Recheck the announced 2026-10-05 Load Balancer IP transition. Provider facts are linked; workflows are reference designs.

## Contents

- [Choose the resource](#choose-the-resource)
- [Network modes](#network-modes)
- [Retaining or replacing a server address](#retaining-or-replacing-a-server-address)
- [Floating address failover](#floating-address-failover)
- [IPv6 choices](#ipv6-choices)
- [Validation and costs](#validation-and-costs)

## Choose the resource

| Resource | Documented role | Operational consequence |
|---|---|---|
| Cloud Primary IPv4 | VM's public IPv4 connectivity; one per VM | Retain independently for a planned replacement |
| Cloud Primary IPv6 | VM's public IPv6 connectivity; one per VM | IPv6-only remains publicly networked |
| Cloud Floating IP | Additional public address; one active target; matching Primary IP family required | Can move while the VM is running; guest setup remains necessary |
| Load Balancer address | Public service entry point | Application ingress lifecycle, not a private VM's outbound identity |

Primary assignments to existing VMs require the VM to be powered off and the same location. Floating IP reassignment can cross locations within one network zone and project. Sources: [Primary IP FAQ](https://docs.hetzner.com/cloud/servers/primary-ips/faq/), [Floating IP overview](https://docs.hetzner.com/cloud/floating-ips/overview/).

Distinguish Cloud Floating IPs from Robot failover/additional IP products before selecting automation or migration procedures.

**Scheduled change:** from **2026-10-05**, LB addresses will be displayed/invoiced as Primary IPs; advertised LB pricing includes a Primary IPv4. [Announcement](https://docs.hetzner.com/networking/load-balancers/overview/). This does not establish arbitrary VM-to-LB reassignment support. Recheck the API and invoice model; older Primary IP pages describe server-only targets.

## Network modes

The [Cloud server overview](https://docs.hetzner.com/cloud/servers/overview/) describes these choices:

| Configuration | Direct public reachability | Private Network |
|---|---|---|
| Primary IPv4 and IPv6 | Both address families | Optional |
| Primary IPv4 only | IPv4 | Optional |
| Primary IPv6 only | IPv6 | Optional |
| Neither Primary family | None | Required |

IPv6-only remains public. A restricted firewall and an absent public interface are different designs; evaluate operational needs alongside IP costs.

Design private servers' [administrative access](private-access-vpn.md), [NAT/proxy egress](private-egress-nat.md), and [service ingress](load-balancers.md) separately.

The [server FAQ](https://docs.hetzner.com/cloud/servers/faq/) lists no Floating IPs, Cloud Firewalls, or Rescue System for servers without Primary IPs. The browser console is separate from Rescue; prepare local console credentials before removing public access.

## Retaining or replacing a server address

Reference workflow for a maintenance replacement:

1. Record IP resource ID, family, location, PTR, project, `auto_delete`, protection, and dependent allowlists.
2. Disable automatic IP deletion when the address must outlive the old VM. Understand protection interactions before changing either setting.
3. Prepare keys/data and validate the replacement through temporary or private addressing.
4. Schedule downtime; stop writes and shut down affected VMs before reassignment.
5. Assign the retained IP to the eligible replacement and verify guest configuration. Retain the old VM for rollback.
6. Boot and test connectivity, application identity, TLS, egress source, DNS, and monitoring.
7. On failure, power down and restore the old assignment/application state. IP rollback does not reverse database migrations.

The [Primary IP FAQ](https://docs.hetzner.com/cloud/servers/primary-ips/faq/) documents independent resource management and deletion settings. The [configuration guide](https://docs.hetzner.com/cloud/servers/primary-ips/primary-ip-configuration/) says initial standard-image assignment is automatic; later Primary IPv6 changes need guest configuration, unlike its documented Primary IPv4 path. Verify custom images independently.

For IPv6 changes, preserve interface matches/MACs and edit the active manager's configuration while the old management path works.

## Floating address failover

Use a Floating IP when an additional stable endpoint must move between already networked VMs. It does not supply failure detection, fencing, application replication, or connection-state synchronization by itself.

The [Floating IP FAQ](https://docs.hetzner.com/cloud/floating-ips/faq/) requires operating-system configuration. For illustration, after assigning documentation address `203.0.113.40` to the correct VM, the temporary Linux operation would be:

```sh
sudo ip address add 203.0.113.40/32 dev eth0
ip address show dev eth0
```

Substitute the actual allocated IP and observed public interface. Make the configuration persistent only after successful testing. The inverse of this temporary addition is:

```sh
sudo ip address del 203.0.113.40/32 dev eth0
```

Specify failure detection, ownership, fencing, provider API action, and application readiness. A local Keepalived/VRRP election does not update Hetzner address ownership; prepare guest configuration/listeners too.

For stable NAT egress, explicitly select and verify the Floating source IP; adding it does not guarantee masquerade selects it. Existing translated sessions need shared state or reconnection after gateway changes.

## IPv6 choices

Test IPv6 support across administrators, repositories, registries, APIs, monitoring, and callbacks. An IPv4-only laptop needs another reachable access path. Connect using an address within the assigned IPv6 `/64`, not the prefix itself; see [private/public SSH examples](https://docs.hetzner.com/cloud/servers/getting-started/connecting-via-private-ip/).

Private IPv4 behind a public dual-stack Load Balancer is compatible with this choice; the [server FAQ](https://docs.hetzner.com/cloud/servers/faq/) explicitly describes private IPv4 targets for servers with only public IPv6.

An IPv6-only VM does not obtain generic IPv4 egress merely by resolving an IPv4 destination. NAT64/DNS64, an application proxy, or a separate private IPv4 NAT route would be an additional operated service. Do not promise a provider-managed translation service without current evidence.

## Validation and costs

| Check | Why it matters |
|---|---|
| Test IPv4 and IPv6 separately | A successful family can hide the other family's failure |
| Inspect guest addresses and routes | Provider assignment and guest setup are separate |
| Validate known SSH host identity | Rebuilt machines legitimately change keys; unexpected changes still need verification |
| Inspect PTR and forward DNS independently | Moving an IP does not establish application naming |
| Check unattached IP resources | Billable IPv4 retention continues while an address is unused |
| Verify deletion protection and `auto_delete` | Prevent accidental loss of a reusable endpoint |

Current Primary IPv6 is free; Primary IPv4 is priced separately. Consult the [Primary IP overview](https://docs.hetzner.com/cloud/servers/primary-ips/overview/) and [Floating IP overview](https://docs.hetzner.com/cloud/floating-ips/overview/) for current prices instead of embedding an undated cost model. Budget gateway compute, maintenance, and redundancy together with IP charges.
