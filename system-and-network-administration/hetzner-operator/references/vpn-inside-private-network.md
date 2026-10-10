# VPN inside a private Hetzner Network

Reviewed: 2026-10-04. Read for encryption between Hetzner servers, private-only WireGuard endpoints, or the distinction between an access VPN and encryption all the way to a workload. The configurations below are examples for already provisioned Linux hosts; no live deployment or tunnel test is implied.

## Encrypt traffic between private-only nodes

Hetzner Cloud Networks provide private layer-3 connectivity but do not automatically encrypt server-to-server traffic. [Network FAQ](https://docs.hetzner.com/networking/networks/faq/)

Two reachable private nodes can use WireGuard **over their private IPs**. For the tunnel below, neither node needs a public IPv4, public IPv6, Internet NAT gateway or external coordination service. This follows from ordinary private IP reachability and WireGuard's IP-over-UDP design; Internet transit is not a WireGuard requirement. Package installation, initial configuration and updates still need a separate delivery path: a prepared image, internal repository, management connection or controlled egress. [WireGuard design](https://www.wireguard.com/#conceptual-overview), [quick start](https://www.wireguard.com/quickstart/)

| Role | Hetzner-assigned underlay address | WireGuard overlay address |
|---|---|---|
| Node A | `10.70.1.10` | `10.78.0.10/32` |
| Node B | `10.70.1.11` | `10.78.0.11/32` |

Assume both underlay addresses are actually allocated to these servers in the same reachable Cloud Network. Reserve the overlay range to avoid collisions with Cloud Networks, LANs, container networks and other VPNs. The overlay addresses belong to the WireGuard interfaces; do not assign them as extra addresses on the Hetzner private interface.

## Minimal two-peer configuration

Generate unique keys on each node, exchange only public keys and protect the configuration files. Replace every angle-bracket key placeholder. Use `/etc/wireguard/wg-internal.conf` on each host.

Node A:

```ini
[Interface]
Address = 10.78.0.10/32
ListenPort = 51820
PrivateKey = <NODE_A_PRIVATE_KEY>

[Peer]
PublicKey = <NODE_B_PUBLIC_KEY>
Endpoint = 10.70.1.11:51820
AllowedIPs = 10.78.0.11/32
```

Node B:

```ini
[Interface]
Address = 10.78.0.11/32
ListenPort = 51820
PrivateKey = <NODE_B_PRIVATE_KEY>

[Peer]
PublicKey = <NODE_A_PUBLIC_KEY>
Endpoint = 10.70.1.10:51820
AllowedIPs = 10.78.0.10/32
```

`Endpoint` identifies the reachable outer UDP destination. `AllowedIPs` selects encrypted destinations and constrains accepted inner source addresses. `wg-quick` installs routes from `AllowedIPs`; `Address` is its interface-address extension. [wg manual](https://git.zx2c4.com/wireguard-tools/about/src/man/wg.8), [wg-quick manual](https://git.zx2c4.com/wireguard-tools/about/src/man/wg-quick.8)

Preserve the existing private-interface address and DHCP routes. Only the peer's overlay `/32` should enter this tunnel. Adding the underlay prefix can capture the endpoint path. A default-route VPN changes the design and needs separate review; Linux `wg-quick` has special policy-routing handling for defaults, so it is not accurate to claim every default necessarily recurses. Do not replace Hetzner's gateway with the peer's address: the underlying Network remains routed through the provider gateway. [Network architecture](https://docs.hetzner.com/networking/networks/technical-concepts/architecture/), [wg-quick routing](https://git.zx2c4.com/wireguard-tools/about/src/man/wg-quick.8)

Permit inbound UDP destination port `51820` on each host's actual private interface only from the other node's allocated underlay `/32`; permit the corresponding outbound traffic. Separately allow required application ports on `wg-internal` from the peer overlay `/32`. Hetzner Cloud Firewalls do not filter private Network traffic, so enforce these restrictions in the guest firewall. [Firewall FAQ](https://docs.hetzner.com/cloud/firewalls/faq/)

For applications terminating on these two hosts, IP forwarding, SNAT and Cloud routes for `10.78.0.0/24` are unnecessary. Start the reviewed configuration with `wg-quick up wg-internal`, then validate before enabling its persistent service. Keepalive is optional and normally unnecessary for these reachable peers; add it only for an observed stateful-path requirement. [WireGuard quick start](https://www.wireguard.com/quickstart/)

## Bind the application to the protected path

Connect to the overlay address, or use internal DNS names resolving to it. Bind the service to its overlay address where practical and prevent an unintended cleartext alternative on the underlay. Verify certificate names and application authentication: a tunnel authenticates peers, not individual application users. Continue using TLS/mTLS when service identity or protection beyond the host-to-host tunnel is required.

Make a strict encryption requirement fail closed: deny the protected application's new connections arriving outside `wg-internal`, and retain an output rule denying the peer's overlay address if it would leave through another interface. Keep those rules when the tunnel stops. For example, on A an output-policy fragment is `oifname != "wg-internal" ip daddr 10.78.0.11 drop`; integrate it with the actual firewall owner and mirror it on B. This prevents a broader fallback/default route from sending protected packets in cleartext if the tunnel route disappears. Check forwarding/container policy separately for containerized services.

## Distinguish a VPN hub from workload encryption

A remote-access tunnel terminating on a hub at `10.70.1.2` decrypts traffic there. If the hub then routes it normally to an application at `10.70.1.11`, that Cloud leg is private but receives no encryption from the terminated VPN. Use application TLS or a tunnel terminating on the workload node to protect that leg. This is an architectural consequence of where decryption occurs. [WireGuard packet processing](https://www.wireguard.com/#simple-network-interface)

An optional internal hub/spoke overlay can use a **separate** transit range: hub `10.79.0.1/32`, A `10.79.0.10/32`, B `10.79.0.11/32`. Give the hub one peer entry per spoke with that spoke's `/32`. A routes the required B/hub overlay addresses through its hub peer, and B reciprocates. Enable controlled forwarding at the hub. Traffic is decrypted and re-encrypted there, so the hub remains trusted; this is not encryption excluding the hub.

Provider source validation becomes relevant when a hub forwards **decrypted packets into the Hetzner fabric** while preserving an unassigned client/overlay source. Provide a provider route for that source prefix pointing to the hub, plus appropriate guest return routing, or deliberately SNAT and accept the loss of original source identity. Pure node-to-node overlay traffic needs no such fabric route: its outer source/destination are already allocated `10.70.1.x` addresses. [uRPF requirements](https://docs.hetzner.com/networking/networks/faq/)

## Reach a private hub from outside

An outside client needs a pre-existing path to a private-only hub: an access VPN through another gateway, or a tunnel initiated outward through an egress/NAT path. Assigning public IPv6 creates a public endpoint, so the hub is no longer private-only. A managed Hetzner Load Balancer supplies TCP/HTTP/HTTPS services, not a native WireGuard UDP entry point. [Load Balancer protocols](https://docs.hetzner.com/networking/load-balancers/faq/)

Managed mesh products add dependencies. Tailscale's hosted coordination and relay services require their documented outbound connectivity; plan bootstrap and ongoing control access. These requirements belong to that mesh service, not to raw WireGuard between statically configured private endpoints. [Tailscale connectivity](https://tailscale.com/docs/reference/faq/firewall-ports)

## Verify without exposing keys

On A, check the following, then repeat reciprocally on B:

```bash
ip route get 10.70.1.11
ip route get 10.78.0.11
wg show wg-internal endpoints
wg show wg-internal latest-handshakes
wg show wg-internal transfer
```

Expect the first route through the existing private interface and the second through WireGuard. Generate permitted application traffic before judging handshake inactivity. Verify the protected service succeeds and its disallowed underlay path fails. Test realistic transfer sizes: tunnel overhead reduces usable MTU; retain `wg-quick` discovery initially and investigate PMTU if small requests work but large transfers stall. Record routes, handshake age and counters without dumping private keys. [MTU architecture](https://docs.hetzner.com/networking/networks/technical-concepts/architecture/), [wg-quick MTU handling](https://git.zx2c4.com/wireguard-tools/about/src/man/wg-quick.8)
