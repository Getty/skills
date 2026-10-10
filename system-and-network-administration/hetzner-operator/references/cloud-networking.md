# Cloud Networks: addressing, routing, and diagnosis

Evidence snapshot: 2026-10-04. Provider behavior is documented; examples and workflows are reference designs. Load before NAT, VPN, container, or hybrid networking work.

## Contents

- [Provider contract](#provider-contract)
- [Address plan and routing model](#address-plan-and-routing-model)
- [Configuration ownership](#configuration-ownership)
- [MTU and overlays](#mtu-and-overlays)
- [Change and validation workflow](#change-and-validation-workflow)
- [Failure interpretation](#failure-interpretation)

## Provider contract

Cloud guests communicate through a provider gateway; a coupled Robot vSwitch's dedicated-server side has Layer 2 behavior. Cloud Networks are not Ethernet VLANs. See the [architecture specification](https://docs.hetzner.com/networking/networks/technical-concepts/architecture/).

Networks use IPv4 and RFC 1918 space. Subnets are not isolated; the gateway is the first usable address of the **Network**, not each Cloud subnet. [Networks FAQ](https://docs.hetzner.com/networking/networks/faq/). Networks/subnets share one network zone; vSwitch coupling requires `eu-central`. [Location restrictions](https://docs.hetzner.com/cloud/general/locations/).

Networks are currently [free](https://docs.hetzner.com/networking/networks/overview/). Transport is isolated, not automatically encrypted; use TLS or tunnels where needed. [Networks FAQ](https://docs.hetzner.com/networking/networks/faq/).

Cloud Firewalls do not filter private Networks or attach to Load Balancers. Apply policy in guests, workload networking, or VPN gateways. [Firewall FAQ](https://docs.hetzner.com/cloud/firewalls/faq/).

## Address plan and routing model

This deliberately places the Cloud subnet away from the Network's gateway address:

| Item | Example |
|---|---|
| Network | `10.70.0.0/16` |
| Cloud subnet | `10.70.1.0/24` |
| Provider gateway | `10.70.0.1` |
| VPN gateway VM | `10.70.1.2` |
| NAT gateway VM | `10.70.1.3` |
| Load Balancer | `10.70.1.5` |
| Application VMs | `10.70.1.10`, `10.70.1.11` |
| VPN client prefix | `10.77.0.0/24` |
| Headquarters LAN | `192.168.50.0/24` |

Avoid overlapping headquarters, home LAN, VPN, Docker, and Kubernetes prefixes. Reserving all of `10.0.0.0/8` complicates later integration.

An application VM's conceptual routes are:

| Destination | Next hop | Purpose |
|---|---|---|
| `10.70.0.1/32` | private interface, directly reachable | Reach the provider gateway |
| `10.70.0.0/16` | `10.70.0.1` | Reach Network resources |
| `192.168.50.0/24` | `10.70.0.1` | Optional headquarters route |
| `10.77.0.0/24` | `10.70.0.1` | Optional VPN-client return route |
| `0.0.0.0/0` | `10.70.0.1` | Optional NAT egress for private-only VM |

The Cloud route table directs headquarters/VPN prefixes to `10.70.1.2`, and optionally the default prefix to NAT VM `10.70.1.3`. Guest and Cloud routes are separate; Console routes do not replace guest defaults. [Multi-network routing](https://docs.hetzner.com/networking/networks/technical-concepts/architecture/).

Do not use another Cloud VM as an Ethernet-adjacent gateway or improvise private failover with gratuitous ARP. Register address and routing ownership first.

## Configuration ownership

The current [server configuration guide](https://docs.hetzner.com/networking/networks/server-configuration/) describes two auto-configuration paths: recent `cloud-init` or `hc-utils`. Their behavior depends on image and distribution. Aliases require guest configuration, and manual addresses must match provider assignments.

Before changing networking, inspect:

```sh
ip -br address
ip -4 route show table all
ip rule show
ip -d link show
systemctl list-units 'hc-net-ifup@*'
cloud-init --version
```

Identify Netplan/networkd, NetworkManager, ifupdown, cloud-init, or `hc-utils` ownership. Keep one DHCP owner per interface. The [guide](https://docs.hetzner.com/networking/networks/server-configuration/) supports disabling `hc-net-ifup@` per interface; new images may have no `hc-utils` package.

Preserve this VM's MAC, interface matches, public routes, and DNS. Back up changed files and use the active manager's validation/rollback mechanism.

## MTU and overlays

The documented maximum is **1450 bytes on the private interface**, versus **1500 on the public interface**. Container bridges and overlays can introduce additional constraints. See [technical details](https://docs.hetzner.com/cloud/technical-details/faq/) and the [MTU troubleshooting guide](https://docs.hetzner.com/networking/networks/troubleshooting/mtu/).

For plain ICMPv4 across this private Network, these probes bracket 1450 bytes:

```sh
ping -c 2 -M do -s 1422 10.70.1.11
ping -c 2 -M do -s 1423 10.70.1.11
```

The first should fit where echo is permitted. The second should produce a useful size error; silence alone is inconclusive because filtering can also hide replies. Probe both directions. Successful small pings do not establish that HTTPS uploads or database replication work.

Derive container/CNI/tunnel MTUs from the path and encapsulation overhead. Permit ICMP errors for PMTUD. TCP MSS clamping is a targeted workaround, not a UDP fix. See [MTU/MSS concepts](https://docs.hetzner.com/networking/networks/technical-concepts/terminology/).

## Change and validation workflow

1. Record project, Network ID, subnet type, assigned private addresses, route objects, and current guest routes.
2. Verify console access and an independent administrative connection before touching the active management path.
3. Change one guest or one route at a time. Keep the old gateway and configuration available during migration.
4. Check the selected path with `ip route get 10.70.1.11` and `ip route get 192.168.50.10`; compare it with the intended Cloud route.
5. Test the actual application port and both directions where bidirectional access is required. Observe source addresses at the destination.
6. Reboot the changed test VM once persistence is configured; repeat route and application checks.
7. Remove only the obsolete objects whose replacement has been verified. Store the final route inventory with the infrastructure code.

## Failure interpretation

| Observation | Next useful check |
|---|---|
| VM has a private address but cannot reach a peer | Assigned address, provider gateway host route, guest firewall, correct Network attachment |
| Peer works but external LAN fails | Both guest route and Cloud route; then VPN peer route and remote LAN return path |
| Tunnel handshake works but routed payload disappears | Source validation and return prefixes; see [VPN access](private-access-vpn.md) |
| Downloads stall while small requests work | MTU/PMTUD in both directions, container bridge and tunnel MTU |
| Routes vanish after reboot | Conflicting configuration owner or a temporary `ip route` change |
| Two subnets unexpectedly communicate | A subnet is address allocation, not an isolation policy |
| Dedicated server cannot be selected as Cloud route gateway | Provider route gateway restriction; use a Cloud router or an explicit overlay design |

The dedicated-gateway restriction is documented in the [Networks FAQ](https://docs.hetzner.com/networking/networks/faq/). Collect bounded captures and route inventories for incidents; see [network report instructions](https://docs.hetzner.com/cloud/servers/network-diagnosis-and-report-to-hetzner/).
