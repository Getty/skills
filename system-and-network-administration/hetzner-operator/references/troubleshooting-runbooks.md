# Troubleshooting runbooks

Verified against primary documentation on **2026-10-04**. Start read-only. Change one demonstrated cause at a time, preserve a recovery path, and compare the same probe before and after the change.

## Contents

- [Collect a bounded incident record](#collect-a-bounded-incident-record)
- [Private server cannot be reached](#private-server-cannot-be-reached)
- [NAT or VPN connectivity fails](#nat-or-vpn-connectivity-fails)
- [Small requests work but larger transfers stall](#small-requests-work-but-larger-transfers-stall)
- [Load Balancer reports unhealthy targets](#load-balancer-reports-unhealthy-targets)
- [Public address reassignment breaks access](#public-address-reassignment-breaks-access)
- [Provisioning and capacity errors](#provisioning-and-capacity-errors)
- [Storage and host-resource failures](#storage-and-host-resource-failures)
- [Escalate with evidence](#escalate-with-evidence)

## Collect a bounded incident record

Record UTC timestamps, account/project and resource IDs, location and network zone, OS/image version, recent changes, precise endpoints, protocol/port, expected route, and observed error. Check [Hetzner Status](https://status.hetzner.com/) for a matching service and location; an unrelated incident is not evidence of causation.

Run applicable commands on the correct host. Linux examples are read-only; tools may be absent. Outputs can contain addresses, usernames, and topology; redact before sharing outside the team.

```sh
date -u
uname -r
ip -br address
ip -details link show
ip route show table all
ip -6 route show table all
ip rule show
ss -lntup
resolvectl status
```

Use `getent ahosts app.example.com` to compare DNS results with intended endpoints. Replace example names and addresses before probing. A successful ICMP echo does not prove the application port works.

## Private server cannot be reached

1. Verify that the client is entering through the intended VPN or public bastion and that both Cloud resources are attached to the intended Network.
2. Compare provider private-IP assignment with `ip -br address`, routes, and the actual interface name.
3. Confirm the service binds to an accessible address and that guest policy allows the expected source.
4. Identify the active network manager and provisioning mechanism. Current Hetzner images configure private interfaces through cloud-init 25.3+ or `hc-utils`; two competing DHCP clients can break configuration.
5. Inspect logs for that manager and interface. Persist a fix in the owner of the configuration, then verify it survives the next planned reboot.

Sources: [Private SSH access](https://docs.hetzner.com/cloud/servers/getting-started/connecting-via-private-ip/), [Network configuration](https://docs.hetzner.com/networking/networks/server-configuration/).

Cloud Firewalls do not filter private Network traffic. A private-only server also lacks the provider Rescue system while it has no Primary IP. Use its [console](https://docs.hetzner.com/cloud/servers/getting-started/vnc-console/) for guest recovery; a rescue plan requiring a temporary public IP also requires a controlled power-state and networking change. [Server FAQ](https://docs.hetzner.com/cloud/servers/faq/), [Firewall FAQ](https://docs.hetzner.com/cloud/firewalls/faq/)

## NAT or VPN connectivity fails

Separate four facts: client route, Hetzner Network route, gateway forwarding/NAT, and return path. In the documented Cloud routing model, a client routes through the Hetzner Network gateway; the configured Network route directs traffic to the customer's gateway VM. Do not assume another server is an ordinary directly attached LAN router. [Network architecture](https://docs.hetzner.com/networking/networks/technical-concepts/architecture/)

On the relevant Linux gateway, inspect:

```sh
sysctl net.ipv4.ip_forward
sysctl net.ipv4.conf.all.rp_filter
sysctl net.ipv4.conf.default.rp_filter
sudo nft list ruleset
sudo iptables -S FORWARD
sudo iptables -t nat -S
ip route get 198.51.100.10
```

The route-get target is an example; substitute the failing destination. Also inspect `rp_filter` on the actual interfaces. Linux uses the maximum of `all` and interface settings. Strict reverse-path checks can reject valid asymmetric traffic; establish the route first and prefer a targeted, justified adjustment over globally disabling validation. [Linux IP sysctls](https://www.kernel.org/doc/html/latest/networking/ip-sysctl.html)

For forwarded VPN traffic that preserves external source prefixes, also check the Cloud Network return route to the gateway VM, or deliberately use SNAT. Changing Linux `rp_filter` cannot alter Hetzner's independent provider-side uRPF. See [VPN routing](private-access-vpn.md#routed-vpn-versus-source-nat).

Check whether Docker changed forwarding behavior. A working host connection does not prove forwarding works for clients or containers. Inspect counters on the actual backend and use a short packet capture on both gateway interfaces to locate where the observed flow stops. Diagnose DNS separately from raw IP connectivity. [Docker firewall behavior](https://docs.docker.com/engine/network/packet-filtering-firewalls/)

## Small requests work but larger transfers stall

Suspect path MTU when handshakes succeed but TLS responses, downloads, or registry pushes stall. Hetzner Cloud private interfaces have a maximum MTU of 1450; tunnel overhead can reduce the usable path further. Test both directions, including the container namespace when that is the sender.

```sh
ping -c 3 -M do -s 1422 10.20.0.10
ping -c 3 -M do -s 1423 10.20.0.10
```

These IPv4 payload sizes bracket MTU 1450 without extra tunnel overhead. A timeout alone cannot distinguish MTU failure from filtering. Inspect ICMP errors and actual interface MTUs. TCP MSS clamping may help routed TCP paths; it does not repair UDP and must match the real path. [Hetzner MTU runbook](https://docs.hetzner.com/networking/networks/troubleshooting/mtu/)

Also check connection exhaustion: `ss -s`, gateway CPU, and, where available, `conntrack -S` plus conntrack count/max sysctls. Distinguish guest conntrack exhaustion from provider connection limits and the application accept queue before increasing limits.

## Load Balancer reports unhealthy targets

Compare the configured target IP, private-network attachment, destination port, health-check protocol/path/Host header, expected status, and application binding. Probe the exact health endpoint from a host with the relevant backend reachability. Test with the expected virtual-host name; a default-site 200 response can conceal a broken application.

Check TLS mode and PROXY protocol on both sides. Hetzner HTTPS services terminate TLS at the Load Balancer and use HTTP to targets; TCP services support TLS passthrough. Enabling PROXY protocol against an unaware listener breaks service. Detailed request logs must come from targets because the Load Balancer does not provide them. [Load Balancer FAQ](https://docs.hetzner.com/networking/load-balancers/faq/)

## Public address reassignment breaks access

Compare control-plane assignment with guest addresses and routes. Primary IPv6 changes require guest reconfiguration; DHCP-based standard-image IPv4 behavior differs. Custom/static images must be inspected individually. Floating IPs also require guest configuration and a same-family Primary IP. [Primary IP configuration](https://docs.hetzner.com/cloud/servers/primary-ips/primary-ip-configuration/), [Floating IP overview](https://docs.hetzner.com/cloud/floating-ips/overview/), [Persistent configuration](https://docs.hetzner.com/cloud/floating-ips/persistent-configuration/)

Check firewall source restrictions, IPv6 client connectivity, DNS TTLs, and outbound source-address selection. Verify host-key changes against the authorized rebuild or Rescue action; never disable host-key verification globally.

## Provisioning and capacity errors

Capture HTTP status, structured error, resource ID, and asynchronous Action result. Classify authentication, insufficient permission, invalid parameters, quota, current capacity, rate limiting, and temporary provider failure separately. Use bounded backoff for transient failures; fix invalid requests instead of retrying them indefinitely.

Creation can return a visible resource before allocation fails; examine the final Action. Advertised availability is not a reservation. Check account limits and temporary location restrictions before proposing another plan or location. [Server FAQ](https://docs.hetzner.com/cloud/servers/faq/), [Cloud general FAQ](https://docs.hetzner.com/cloud/general/faq/), [API reference](https://docs.hetzner.cloud/)

## Storage and host-resource failures

Inspect `lsblk -f`, `findmnt`, `df -h`, `df -i`, and relevant kernel/application logs. Distinguish full capacity, inode exhaustion, missing mount, filesystem read-only state, I/O errors, and application permissions. Match Volume identity before touching filesystems. Provider expansion alone does not grow the filesystem. [Volume FAQ](https://docs.hetzner.com/cloud/volumes/faq/)

## Escalate with evidence

For suspected network loss, Hetzner requests at least 200-packet MTR traces in both directions. Loss at an intermediate hop that disappears by the destination can reflect ICMP handling rather than forwarded-packet loss. Include exact times, affected resource, both traces, and the smallest reproducible failure. [Hetzner network-report guidance](https://docs.hetzner.com/cloud/servers/network-diagnosis-and-report-to-hetzner/)
