# Hybrid Cloud and dedicated networking with vSwitch

Evidence snapshot: **2026-10-04**. Revalidate limits and regional support before deployment. Address ranges below are examples and must be checked against office, VPN, container and existing Hetzner ranges.

## Contents

- [Understand the two network models](#understand-the-two-network-models)
- [Check supported topology](#check-supported-topology)
- [Build the coupling](#build-the-coupling)
- [Design routed access and egress](#design-routed-access-and-egress)
- [Diagnose failures by layer](#diagnose-failures-by-layer)
- [Evaluate alternatives and rollback](#evaluate-alternatives-and-rollback)

## Understand the two network models

A Robot vSwitch provides a tagged layer-2 network between dedicated servers and uses their existing physical uplink. A Cloud Network provides private layer-3 connectivity through a provider gateway. Coupling the two does not turn Cloud machines into ordinary Ethernet neighbors on the dedicated VLAN. [Robot vSwitch](https://docs.hetzner.com/robot/dedicated-server/network/vswitch/), [Cloud Network FAQ](https://docs.hetzner.com/networking/networks/faq/).

This is useful for cloud frontends or workers that communicate privately with a dedicated database/storage host. Evaluate the application's latency, connection behavior and failure handling before distributing a tightly coupled service across locations.

## Check supported topology

Snapshot constraints:

| Constraint | Design consequence |
|---|---|
| Cloud Network subnets share a network zone; vSwitch coupling is limited to `eu-central` | Do not assume the same private Network extends to US or Singapore locations |
| One vSwitch per Cloud Network | Plan the dedicated segment before attaching multiple existing VLANs |
| Cloud private Networks are IPv4 | A public IPv6 deployment still needs separate reasoning for private traffic |
| Cloud route gateways must be Cloud servers | A dedicated host cannot directly be the next-hop gateway in a Cloud Network route |
| vSwitch uses the physical uplink | Public and private traffic share that link's capacity |

Sources: [Network FAQ and route restrictions](https://docs.hetzner.com/networking/networks/faq/), [coupling procedure](https://docs.hetzner.com/networking/networks/connect-dedi-vswitch/), [vSwitch behavior](https://docs.hetzner.com/robot/dedicated-server/network/vswitch/).

The vSwitch documentation currently specifies VLAN IDs 4000–4091, at most 100 servers per vSwitch, five vSwitches per server and 32 MAC addresses per physical switch port. Check these before bridging many VMs or containers into a VLAN. Cloud capacity/attachment limits remain separate. [vSwitch limits](https://docs.hetzner.com/robot/dedicated-server/network/vswitch/).

## Build the coupling

Use an explicit address plan, for example:

| Role | Example |
|---|---|
| Cloud Network | `10.60.0.0/16` |
| Cloud server subnet | `10.60.10.0/24` |
| Dedicated vSwitch subnet | `10.60.20.0/24` |
| Dedicated host | `10.60.20.10/24` |
| vSwitch-subnet gateway | `10.60.20.1` |
| VLAN ID | `4000` |

1. Verify private communication between Cloud servers before adding the hybrid link.
2. Create the vSwitch in Robot, assign a permitted VLAN ID and attach the exact dedicated servers.
3. Add a **vSwitch-type subnet** to the existing Cloud Network, referencing that vSwitch ID. Use a non-overlapping range that excludes the reserved beginning of the parent Network.
4. On each dedicated host, create a VLAN interface on the actual uplink with MTU **1400**. Assign a unique address from the vSwitch subnet.
5. Route the Cloud Network prefix via the first usable address of the vSwitch subnet. Keep the existing public default route unless the design explicitly changes egress.
6. Persist the configuration using the network manager already responsible for the host. Do not run Netplan, ifupdown and NetworkManager as competing owners of the same interface.

These address/gateway roles and the required OS-side configuration follow the [official coupling guide](https://docs.hetzner.com/networking/networks/connect-dedi-vswitch/). Obtain values from the actual Console configuration instead of transcribing an example.

## Design routed access and egress

Private connectivity alone adds no Internet gateway, NAT, VPN, encryption or service authorization. Write down the full outbound and return paths for each destination: other Cloud servers, dedicated hosts, headquarters, package repositories and external APIs.

A **Cloud server can act as router for dedicated clients** when the necessary routes are configured and the Network's route-exposure option is enabled for vSwitch. The reverse provider-route setup, with a dedicated server as the Cloud Network gateway, is not supported. A dedicated host can still be an application endpoint; those are different uses. [Routing FAQ](https://docs.hetzner.com/networking/networks/faq/).

By default, the vSwitch sees Cloud-product addresses rather than every custom route. If a design needs custom Network routes available on the dedicated side, enable **Expose routes to vSwitch** and configure the corresponding guest routes. This setting has propagation time; it does not configure forwarding, filtering or NAT on the chosen router. [Route exposure](https://docs.hetzner.com/networking/networks/connect-dedi-vswitch/).

Prefer an explicit Cloud gateway for a straightforward supported hybrid egress design. A tunnel overlay is an alternative when the required routing topology falls outside provider support; document its extra MTU, encryption, CPU and availability costs.

## Diagnose failures by layer

Inspect both endpoints and the provider objects before changing rules:

```bash
ip -d link show
ip -br address
ip route show
ip route get 10.60.10.10
ping -c 3 10.60.10.10
```

Replace the target with an allocated reachable peer. Then test a real TCP service in both directions. Ping success alone does not prove usable application connectivity.

| Symptom | Next check |
|---|---|
| No dedicated VLAN communication | vSwitch membership, VLAN ID, uplink name, link state and Robot firewall |
| Dedicated VLAN works, Cloud fails | Coupling ID, subnet range, dedicated route and its gateway |
| One direction works | Return route, forwarding policy and source-address validity |
| Small packets work, transfers stall | Path MTU, blocked ICMP errors and overlay overhead |
| Reboot loses connectivity | Persistent network configuration and interface-name assumptions |
| Custom remote subnet disappears | Route-exposure setting and guest routes |

Robot's server firewall also applies to vSwitch packets, so internal addresses must be permitted when that firewall is enabled. This differs from the Cloud Firewall/private-traffic model. [vSwitch firewall behavior](https://docs.hetzner.com/robot/dedicated-server/network/vswitch/).

Cloud private interfaces support 1450-byte MTU while the vSwitch configuration uses 1400. Do not increase an interface beyond the smallest supported path segment. Inspect path-MTU behavior and test a sustained transfer after any change. [Cloud technical details](https://docs.hetzner.com/cloud/technical-details/faq/), [MTU troubleshooting](https://docs.hetzner.com/networking/networks/troubleshooting/mtu/).

## Evaluate alternatives and rollback

Co-locating dependent tiers can simplify latency and incident handling. An encrypted overlay can span unsupported topologies but introduces another routing/control plane. A second provider or location can improve failure separation only when the application and data layer are designed to survive it.

Before applying a new route, preserve console/KVM access, export provider topology and save working guest configuration. Revert a hybrid change in reverse dependency order: stop dependent traffic, restore guest routes, remove the coupling, and only then remove unused VLAN membership. Never remove a shared vSwitch as a routine rollback for one host.
