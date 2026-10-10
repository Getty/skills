# WireGuard gateway, headquarters connection, and administrator access

Read this file to implement the reference VPN after choosing the topology in [private access and VPN](private-access-vpn.md). For encryption solely between private Hetzner machines, use [internal WireGuard](vpn-inside-private-network.md). This is an original reference design checked against provider and upstream documentation on **2026-10-04**, not a claim of a deployed or benchmarked installation.

## Contents

- [Choose the boundary](#choose-the-boundary)
- [Address and traffic plan](#address-and-traffic-plan)
- [Prepare access and keys](#prepare-access-and-keys)
- [Configure the tunnel](#configure-the-tunnel)
- [Configure both routing layers](#configure-both-routing-layers)
- [Apply access policy](#apply-access-policy)
- [SNAT alternative](#snat-alternative)
- [Prove the path and persist it](#prove-the-path-and-persist-it)
- [Operate and recover](#operate-and-recover)

## Choose the boundary

Use a small dedicated-purpose Cloud VM with a public endpoint and an attached private Network as the initial VPN gateway when operators and an office need access to several private servers. Start with ordinary Linux plus WireGuard for a small known peer set. Choose a controlled mesh when user enrollment, device revocation, identity policy, roaming, and several networks dominate the work. Select an appliance such as OPNsense/pfSense when its routing/UI/IPsec features are needed, then honor Hetzner's routed underlay instead of assuming a physical LAN.

The public endpoint can use IPv4, IPv6, or both if every required peer can reach it. A Primary IPv6 address is public connectivity; it does not make a server private-only. A private-only connector can initiate to an office or external hub only through an existing egress path. See [public IPs](public-ips.md) and [egress](private-egress-nat.md).

A managed Hetzner Load Balancer supports TCP/HTTP/HTTPS services, not WireGuard's UDP transport, and supplies no general Internet gateway for private servers. Run the VPN endpoint on a server or another suitable reachable router. [LB FAQ](https://docs.hetzner.com/networking/load-balancers/faq/), [WireGuard](https://www.wireguard.com/).

Keep application data encrypted beyond the VPN termination where needed: the hub decrypts packets before forwarding them into the private Network. Use TLS to the service, or terminate an overlay directly on the destination. Hetzner does not automatically encrypt private Network traffic. [Networks FAQ](https://docs.hetzner.com/networking/networks/faq/).

## Address and traffic plan

Replace every example range after checking the office LAN, VPN pools, Docker bridges, Kubernetes pod/service ranges, and other sites. These addresses are a coherent example, not prescribed addresses for every deployment.

| Item | Example | Meaning |
|---|---|---|
| Cloud Network | `10.70.0.0/16` | Provider routing domain |
| Cloud subnet | `10.70.1.0/24` | VM allocation range |
| Hetzner gateway | `10.70.0.1` | Derived from the **Network**, not the subnet |
| WireGuard VM | `10.70.1.2` | Attached private address; illustrative public endpoint `203.0.113.10` |
| Private application / database | `10.70.1.10` / `10.70.1.11` | Need no WireGuard installation for this routed pattern |
| VPN addresses | `10.77.0.0/24` | Hub `.1`, office peer `.2`, administrator `.10` |
| Office LAN | `192.168.50.0/24` | Office main router `.1`, WireGuard connector `.2` |
| Office administrator | `192.168.50.10` | One permitted management workstation |
| Temporary public administrator | `198.51.100.10` | Documentation address; replace with the real source before a firewall rollout |

On the Cloud VM, verify interface names with `ip -br address`; the assets use `eth0` and `enp7s0` only as examples. Obtain private allocation and routes from the actual platform configuration. Cloud VM private interfaces are routed through the provider gateway, commonly with a `/32` address and gateway host route. Do not reconfigure them as an Ethernet `/24` merely because the allocation subnet is `/24`. [Network architecture](https://docs.hetzner.com/networking/networks/technical-concepts/architecture/).

The example authorizes the two named administrators to initiate SSH and HTTPS to private servers. Add database access, backup traffic, DNS, monitoring, or office-bound sessions as separate required flows. Establishing a site-to-site route does not authorize every host on either side.

## Prepare access and keys

1. Inventory the current resource IDs, addresses, routes, firewall owners, SSH configuration, network manager, and working administrator path. Keep a second session and an independently usable console open while changing access.
2. Prepare the public gateway and its private attachment first. Bootstrap packages through its public connectivity. Private application nodes do not need WireGuard in this pattern; their own updates still need the separate egress design.
3. Verify actual console credentials before depending on recovery. Cloud console access does not depend on a working guest network, but it still needs a working boot/login path. A private-only server has no Rescue System while it lacks a Primary IP. [Console](https://docs.hetzner.com/cloud/servers/getting-started/vnc-console/), [server FAQ](https://docs.hetzner.com/cloud/servers/faq/).
4. Install the distribution's maintained WireGuard tools on the hub, office connector, and administrator device. Use current platform instructions for Windows/macOS clients. Prefer host-level WireGuard on a dedicated gateway unless there is a concrete reason for containerization.
5. Generate each private key on its own endpoint. Transfer only public keys through normal configuration channels. Store private keys and configurations with root-only access; keep them out of repositories, shell tracing, Terraform outputs, cloud-init user data, tickets, and this package.

Example key creation in a **root shell**, for a new endpoint only:

```bash
install -d -m 700 /etc/wireguard
(
  umask 077
  set -C
  wg genkey > /etc/wireguard/private.key
)
wg pubkey < /etc/wireguard/private.key > /etc/wireguard/public.key
```

Stop on any failure; `set -C` prevents replacing an existing private key. Reuse an existing approved key rather than silently rotating it. The upstream [quick start](https://www.wireguard.com/quickstart/) documents key generation and endpoint setup.

## Configure the tunnel

Adapt these assets into `/etc/wireguard/wg0.conf` on the appropriate endpoints, with mode `0600`:

- [Hub](../assets/wireguard/hub.conf.example): `10.77.0.1/24`, listener UDP `51820`, one office peer and one administrator peer.
- [Office](../assets/wireguard/office.conf.example): `10.77.0.2/32`; initiate to the hub's public address; route `10.70.0.0/16` and the hub's tunnel address through the peer.
- [Administrator](../assets/wireguard/admin.conf.example): `10.77.0.10/32`; route only the Cloud prefix and hub's tunnel address, preserving ordinary Internet routing.

Set unique keys and an individual `/32` for every administrator device. On the hub, the office peer's `AllowedIPs` must include both its tunnel address and the LAN prefix it can originate. A roaming administrator peer gets only its own tunnel address. Avoid overlapping ownership of the same prefix by different peers on an interface. `AllowedIPs` selects peers for outgoing packets and constrains incoming source addresses; it is not a replacement for service authorization. [wg(8)](https://git.zx2c4.com/wireguard-tools/about/src/man/wg.8).

The examples use `PersistentKeepalive = 25` on NATed initiators to retain mappings during idle periods. Do not use keepalives as a failover mechanism. The hub can learn the initiator's endpoint without a fixed office public address. Configure an explicit endpoint on the side that must initiate. [WireGuard quick start](https://www.wireguard.com/quickstart/).

Use `MTU = 1380` as a conservative **starting assumption for this example**, then measure the complete path. It is not a universally optimal or guaranteed value. Preserve ICMP/ICMPv6 path-MTU signaling and account for nested tunnels and the office uplink. Do not subtract WireGuard overhead twice from a segment that carries only decrypted payload. [Hetzner MTU troubleshooting](https://docs.hetzner.com/networking/networks/troubleshooting/mtu/).

Do not set `AllowedIPs = 0.0.0.0/0` for management access by default. That changes the client into a full-tunnel design, including its egress, DNS, IPv6, and public endpoint route handling. Do not enable `SaveConfig` when files are managed declaratively; it may overwrite edits on shutdown. `wg-quick` normally installs routes derived from `AllowedIPs`. [wg-quick(8)](https://git.zx2c4.com/wireguard-tools/about/src/man/wg-quick.8).

If using Hetzner's WireGuard App image, first choose whether its UI or your automation owns configuration. The UI's Apply operation rewrites `wg0.conf`, and its watcher restarts the service; do not have both systems manage the same file. Read the image-specific update instructions. [WireGuard App](https://docs.hetzner.com/cloud/apps/list/wireguard/).

## Configure both routing layers

For routed access preserving source addresses, configure **all** of the following. The included [topology validator](../scripts/validate_topology.py) checks this narrow plan offline; it cannot observe live routing or firewall state.

### A. Cloud control-plane routes

Create these routes in the **Hetzner Network**, not merely inside Linux:

| Destination | Cloud route gateway |
|---|---|
| `10.77.0.0/24` | `10.70.1.2` |
| `192.168.50.0/24` | `10.70.1.2` |

Example current CLI shape; confirm installed `hcloud network add-route --help` before use:

```bash
hcloud network add-route private-net --destination 10.77.0.0/24 --gateway 10.70.1.2
hcloud network add-route private-net --destination 192.168.50.0/24 --gateway 10.70.1.2
```

These routes provide the return path and allow the gateway VM to forward packets with those remote source prefixes through Hetzner's source validation. Linux forwarding alone is insufficient. Use the least broad correct prefixes rather than a blanket `/0` to make source validation pass. [Provider uRPF and routes](https://docs.hetzner.com/networking/networks/faq/).

### B. Guest routes on participating private application servers

For destinations outside the Cloud Network range, send packets to the **provider gateway**:

```bash
ip route replace 10.77.0.0/24 via 10.70.0.1 dev enp7s0
ip route replace 192.168.50.0/24 via 10.70.0.1 dev enp7s0
```

Run these only after verifying the interface and existing provider-gateway reachability. The next hop is **not** the VPN VM `10.70.1.2`, and it is not `10.70.1.1`. A pre-existing default route through the provider gateway may already cover these destinations, but inspect more-specific routes and policy rules before omitting explicit routes. [Network architecture](https://docs.hetzner.com/networking/networks/technical-concepts/architecture/).

**Do not install these guest return routes on the VPN hub.** Its office route and tunnel addresses must resolve to `wg0`, while the Cloud prefix continues through its private interface. Keep the hub's own Internet default on its public uplink. Copying the application-server route back onto the VPN hub can create a loop.

### C. Office LAN routing

If the WireGuard connector is the office LAN's default router, its tunnel route may suffice. If it is a separate host at `192.168.50.2`, add a route on the main office router:

| Destination | Office next hop |
|---|---|
| `10.70.0.0/16` | `192.168.50.2` |

Add `10.77.0.1/32` via the connector only if office hosts need the hub's tunnel address. Confirm that the office gateway routes the source LAN normally, has IPv4 forwarding enabled, and permits the selected LAN-to-tunnel flows and their established responses. A route on the office connector alone does not make ordinary office machines send it their traffic.

### D. Forwarding and source validation

Enable IPv4 forwarding on the **hub and office connector**, not on every ordinary client:

```ini
# /etc/sysctl.d/60-site-vpn.conf
net.ipv4.ip_forward = 1
```

Apply the reviewed setting and inspect the effective values. Linux notes that changing `ip_forward` can reset associated configuration defaults; apply other deliberately chosen routing settings afterward. Check `rp_filter` on relevant interfaces if the topology is asymmetric. Strict mode can reject a valid asymmetric return path; loose mode may fit a verified routed design. Do not disable source validation globally as a troubleshooting reflex, and do not confuse kernel `rp_filter` with Hetzner's independent uRPF. [Linux IP sysctls](https://docs.kernel.org/networking/ip-sysctl.html).

## Apply access policy

Configure three policy locations:

1. **Hub public ingress:** allow WireGuard UDP `51820` on the selected public address families. Restrict source IPs for a fixed site when practical; roaming peers may need wider UDP reachability, with WireGuard keys providing authentication. Retain a temporary narrow SSH recovery rule during rollout. Keep required ICMP/ICMPv6 functional.
2. **Hub and office forwarding:** allow only named remote source addresses/prefixes to required private destinations and services. Allow established responses. Decide explicitly whether the Cloud side may initiate into the office; the bundled hub policy denies those new sessions by default.
3. **Application host and application authorization:** permit the retained remote source addresses only on required services; keep credentials, TLS, and role checks in the application. Do not expose PostgreSQL to every tunnel peer simply because it is on the VPN.

Cloud Firewalls do not filter private Network traffic, so private host policy cannot be delegated to that product. Docker, UFW, firewalld, and container network plugins can own forwarding hooks; inspect the actual rule path before adding another firewall. [Cloud Firewall FAQ](https://docs.hetzner.com/cloud/firewalls/faq/), [Docker firewall behavior](https://docs.docker.com/engine/network/packet-filtering-firewalls/).

The [hub nftables asset](../assets/wireguard/hub.nft.example) implements this restricted example on a dedicated gateway. It does not configure an office firewall, application firewall, or Internet NAT. Replace its addresses/interfaces and integrate it with existing rule ownership. Adding an accept in one base chain does not neutralize a drop in another. Check syntax on the target system with `nft --check --file`, then apply only the reviewed policy. [nftables server policy](https://wiki.nftables.org/wiki-nftables/index.php/Simple_ruleset_for_a_server).

For the **first addition of the previously absent `inet hetzner_vpn` table**, one rollback option is a short systemd timer that deletes just this new table. Verify the actual `nft` executable path, absence of that table, independent console access, and that removing the new table returns to the preceding policy. Do not use this rollback for edits to a pre-existing table.

```bash
systemd-run --unit=hetzner-vpn-rollback --on-active=5m /usr/sbin/nft delete table inet hetzner_vpn
nft --check --file /root/hub.nft.reviewed
nft --file /root/hub.nft.reviewed
```

After testing a **new** administrator connection and a denied flow, cancel the timer with `systemctl stop hetzner-vpn-rollback.timer`. Recover Cloud Firewall edits separately; a host rollback cannot undo control-plane rules. Use the firewall owner's persistent configuration mechanism, not an unreviewed global ruleset flush.

## SNAT alternative

For simple operator-initiated access when preserving the user's address is unnecessary, SNAT remote traffic entering the Cloud fabric to the hub's allocated private address. This can avoid distributing remote-prefix guest routes and creating remote-prefix Cloud routes for that translated flow; replies return to the hub and conntrack reverses the translation.

Illustrative nftables NAT chain to integrate separately after review:

```nft
table ip vpn_source_nat {
    chain postrouting {
        type nat hook postrouting priority srcnat; policy accept;
        oifname "enp7s0" ip saddr { 10.77.0.0/24, 192.168.50.0/24 } ip daddr 10.70.0.0/16 snat to 10.70.1.2
    }
}
```

Retain restrictive forwarding on the hub. The application sees `10.70.1.2`; central logs and gateway controls must carry more of the attribution burden. SNAT does not make unsolicited Cloud-to-office sessions work automatically, remove the office's route to the Cloud prefix, or replace application authentication. Do not mix routed and translated flows accidentally while diagnosing source addresses. Provider documentation lists NAT as an alternative to assigning return prefixes to the forwarding server. [Networks FAQ](https://docs.hetzner.com/networking/networks/faq/).

## Prove the path and persist it

Start the reviewed WireGuard configuration with the OS service manager. On systemd hosts, `systemctl start wg-quick@wg0` brings it up; enable the unit for boot only after the path is correct. Inspect success at each boundary:

| Observation | Check | Interpretation |
|---|---|---|
| UDP reaches hub | Bounded packet capture on the public interface | Underlay, source policy, and port path work |
| Tunnel authenticated | `wg show wg0 latest-handshakes` and transfer counters after generated traffic | Keys and peer reachability work; this alone proves no application route |
| Correct hub routes | `ip route get 192.168.50.10` and `ip route get 10.70.1.10` | Office resolves through `wg0`; Cloud through private gateway |
| Correct application return | `ip route get 10.77.0.10` and `ip route get 192.168.50.10` | Remote prefixes resolve through `10.70.0.1` |
| Intended service works | New SSH/HTTPS connection from each authorized source | Both routing layers, forwarding, host policy, and application work |
| Source identity is correct | Bounded private-interface capture or application access log | Retained remote source in routed mode; hub source in SNAT mode |
| Unwanted access fails | Attempt an intentionally ungranted service/peer direction | Policy denies new traffic as designed |
| Large transfers work | Representative upload/download and MTU probes | Avoid a handshake-only or small-packet false success |

WireGuard is deliberately quiet while idle; lack of a recent handshake without generated traffic is not alone an outage. Avoid `wg show ... dump` in shared diagnostics because it can expose private or preshared keys. Request only needed public state.

Persist guest routes using the actual network owner. Current Hetzner images may use cloud-init 25.3+ or `hc-utils`; neither a blanket instruction to remove `hc-utils` nor a second competing DHCP client is safe. Verify generated files, supported override mechanism, DHCP behavior, and gateway host route before changing ownership. [Current Network configuration](https://docs.hetzner.com/networking/networks/server-configuration/).

Where a controlled maintenance window is available, restart one gateway/client at a time and repeat application and denied-path checks. Record interface names, chosen route persistence, peer ownership, and recovery credentials. A successful temporary `ip route` command is not persistence evidence.

## Operate and recover

- Maintain a peer inventory: owner, public key, tunnel address, approved prefixes, device purpose, and revocation procedure. Remove one peer and its grants when access ends; do not redistribute a shared administrator private key.
- Track generated test traffic, route state, handshake age in context, transfer errors, gateway CPU/packet processing, conntrack pressure where NAT is present, disk space, and certificate/application failures separately.
- Back up encrypted gateway configuration and document how to rebuild the hub without relying on the VPN itself. Keep a credentialed console recovery route independent of office DNS and the tunnel.
- For loss of the tunnel, distinguish no UDP, failed authentication, decrypted packets dropped locally, fabric source rejection, wrong application return route, host denial, and MTU failure. Use [troubleshooting](troubleshooting-runbooks.md).
- For redundancy, design both the externally reachable endpoint and private return-route ownership. A Floating IP alone does not move Cloud routes, keys, host configuration, or connection state. Evaluate two explicit tunnels and site routing before adding automated endpoint/route failover; include fencing and control-plane availability in its design. Use [VPN architecture](private-access-vpn.md).
- Undo only changes belonging to this rollout: stop the new tunnel, restore prior route/policy ownership, remove newly added routes if no other consumers need them, and restore service reachability through the preserved recovery path. Retain established resources and keys unless their removal is explicitly part of the task.
