# Private-server Internet egress through a NAT gateway

Evidence snapshot: 2026-10-04. Operator-managed reference design based on [Hetzner routing](https://docs.hetzner.com/networking/networks/technical-concepts/architecture/). Consult the provider-authored [NAT tutorial](https://community.hetzner.com/tutorials/how-to-set-up-nat-for-cloud-networks/) for distribution-specific background.

## Contents

- [Choose an egress design](#choose-an-egress-design)
- [Three routing responsibilities](#three-routing-responsibilities)
- [Scoped Linux NAT example](#scoped-linux-nat-example)
- [Persistence and bootstrap](#persistence-and-bootstrap)
- [Validation and rollback](#validation-and-rollback)
- [Capacity and availability](#capacity-and-availability)

## Choose an egress design

| Requirement | Reference choice | Tradeoff |
|---|---|---|
| General outbound IPv4 for private VMs | Public Cloud VM with forwarding and source NAT | Gateway maintenance, connection state, shared failure domain |
| Only HTTP(S) package/API access | Explicit authenticated proxy where applications support it | Smaller protocol scope; configuration needed in each client |
| Many repeated package/image downloads | Repository mirror or cache plus controlled upstream access | Cache integrity, refresh, and storage become operational tasks |
| No runtime Internet dependency | Prebuilt images and private mirrors | Stronger bootstrap and release discipline |
| Direct public reachability acceptable | Individual Primary IPs plus firewall policy | More public endpoints, less gateway dependency |

A [Load Balancer](load-balancers.md) provides service ingress, not clients' Internet routing or outbound translation.

## Three routing responsibilities

Example: Network `10.70.0.0/16`, Cloud subnet `10.70.1.0/24`, provider gateway `10.70.0.1`, NAT VM `10.70.1.3`, private client `10.70.1.10`. NAT's illustrative public IP is `203.0.113.20`; substitute an allocated address.

| Configuration plane | Required example state |
|---|---|
| Client operating system | Default via provider gateway `10.70.0.1` on the private interface |
| Hetzner Network route | Destination `0.0.0.0/0`, gateway `10.70.1.3` |
| NAT operating system | Public default route retained; `10.70.0.0/16` reachable through `10.70.0.1`; forwarding and scoped NAT enabled |

The client does not use `10.70.1.3` as an Ethernet-adjacent next hop. Both directions traverse the provider gateway. [Documented routing](https://docs.hetzner.com/networking/networks/technical-concepts/architecture/).

NAT's own default must not loop back through itself. Keep headquarters/VPN routes more specific than the Internet default.

## Scoped Linux NAT example

Assumptions: dedicated Linux NAT VM; observed interfaces `eth0` public, `enp7s0` private; no Docker/Kubernetes/firewalld forwarding controller. Confirm first. Host INPUT policy, SSH, DNS, and Cloud Firewall settings remain separate.

Record existing configuration without exposing secrets:

```sh
ip -4 route show table all
ip rule show
sysctl net.ipv4.ip_forward
sudo nft list ruleset
```

Enable forwarding only when the intended forwarding rules are ready. Linux documents `net.ipv4.ip_forward` and its side effects in [IP sysctl](https://docs.kernel.org/networking/ip-sysctl.html).

```sh
sudo sysctl -w net.ipv4.ip_forward=1
```

These task-owned tables allow outbound IPv4 and related replies, without changing gateway administration. Narrow destinations/ports where required.

```nft
table inet hetzner_egress_filter {
    chain forward {
        type filter hook forward priority filter; policy drop;
        ct state invalid drop
        ct state established,related accept
        iifname "enp7s0" oifname "eth0" ip saddr 10.70.0.0/16 accept
    }
}

table ip hetzner_egress_nat {
    chain postrouting {
        type nat hook postrouting priority srcnat; policy accept;
        oifname "eth0" ip saddr 10.70.0.0/16 masquerade
    }
}
```

Validate the saved fragment with `nft -c -f <file>`, then apply once with `nft -f <file>`. This initial installation is not idempotent. For managed firewalls, configure their controller instead; one base chain's accept cannot override another's drop.

The [nftables NAT documentation](https://wiki.nftables.org/wiki-nftables/index.php/Performing_Network_Address_Translation_(NAT)) explains masquerading and stateful bindings. For a specific Floating IP egress identity, replace masquerade with explicit SNAT only after that IP is correctly assigned and configured; see [public IPs](public-ips.md).

Add the Cloud route above through Console or the current API. On a **private-only client without an existing default**, the corresponding temporary guest change is:

```sh
sudo ip route add default via 10.70.0.1 dev enp7s0
```

Investigate existing defaults before changes. The provider gateway host route must already exist; see [Cloud networking](cloud-networking.md).

## Persistence and bootstrap

Persist forwarding, nftables, routes, and DNS through the active OS configuration. Current [Hetzner docs](https://docs.hetzner.com/networking/networks/server-configuration/) distinguish cloud-init from `hc-utils`; do not blindly copy older package-removal steps.

Validate gateway and Cloud route before clients need downloads. Avoid bootstrap cycles: use prepared images, locally available cloud-init configuration, or controlled temporary access.

Configure a reachable resolver; test DNS separately from IP connectivity. Enforce guest forwarding policy: translation is not authorization.

## Validation and rollback

1. From the NAT VM, validate its own Internet access and its private route back to the client.
2. From the client, inspect `ip route get 1.1.1.1`; expect the private interface and provider gateway. This command only inspects routing.
3. Test DNS and a required HTTPS endpoint; inspect destination logs or an approved address-echo endpoint to confirm NAT's actual public source.
4. Observe bounded captures on both NAT interfaces. Check nftables counters and connection-tracking pressure when packets disappear.
5. Test large transfers, not only small pings; investigate the [1450-byte private-path MTU](https://docs.hetzner.com/networking/networks/troubleshooting/mtu/).
6. Reboot the gateway and one client, then repeat the checks. Confirm a failed gateway produces the expected monitoring alert.

Rollback: remove only the client default added by this change; restore any prior route from the recorded configuration; remove the exact Cloud default route only after checking other clients. Remove these task-owned tables if they were newly created:

```sh
sudo nft delete table inet hetzner_egress_filter
sudo nft delete table ip hetzner_egress_nat
```

Remove their persistent fragments and restore the prior forwarding value only if no other routed workload depends on it. Never use `nft flush ruleset` as a generic cleanup step.

## Capacity and availability

Measure bandwidth, packet/connection rates, active flows, softirq CPU, drops, and API latency. Connection state or source ports may exhaust before bandwidth. Cache repeated downloads when measurements justify it.

Redundancy requires health decisions, route ownership, fencing, and tested switching. Failover may require both Cloud route and Floating IP changes. Lost connection state can interrupt sessions despite stable public addressing. Measure recovery with reconnecting clients.

Layer 2 VRRP does not move Cloud routes. Prefer a documented restore objective over untested failover; separate VPN, ingress, and egress failure domains where required.
