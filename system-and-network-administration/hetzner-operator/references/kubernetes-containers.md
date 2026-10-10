# Kubernetes, containers, Cloud controllers, and private nodes

Verified on **2026-10-04**. Pin compatible Kubernetes/distribution, CNI, CCM, CSI, chart, and provider releases. Treat Kubernetes on rented Hetzner servers as operator-managed infrastructure; assigning a controller does not outsource cluster upgrades, security, quorum, or recovery.

## Contents

- Ownership and version checks
- Private-node bootstrap and routing
- Service exposure and Load Balancers
- Persistent storage and recovery
- Docker networking and diagnosis

## Ownership and version checks

| Component | Responsibility |
|---|---|
| Distribution / installer | Control plane, kubelet, runtime, upgrade workflow |
| CNI | Pod connectivity and supported NetworkPolicy enforcement |
| Hetzner CCM | Cloud node metadata, supported route reconciliation, Load Balancer integration |
| Hetzner CSI | Provisioning and attachment of Cloud Volumes |
| Ingress/Gateway controller | Application routing and, when chosen, backend TLS termination |

Use the [official CCM](https://github.com/hetznercloud/hcloud-cloud-controller-manager) and [official CSI](https://github.com/hetznercloud/csi-driver) as the primary integration references. Community installers can be useful, but inspect what they create, their update/restore contract, and their pinned dependencies before adopting them.

The CCM upstream explicitly warns that versions **1.30.0 and older** fail after removal of `server.datacenter` on **2026-07-01**; upgrade to at least 1.30.1 and then choose a currently supported release. The obsolete `latest` image tag was removed on July 7. Do not copy a historic `kubectl apply` URL pointing at an unpinned branch. [CCM migration warning](https://github.com/hetznercloud/hcloud-cloud-controller-manager)

Use `--cloud-provider=external` for kubelet as required by the distribution's CCM setup. Provide a project read/write token through a protected Kubernetes Secret or supported secret-file injection, not a literal token in a committed manifest. Understand controller RBAC and project-wide token scope. [CCM quick start](https://github.com/hetznercloud/hcloud-cloud-controller-manager/blob/main/docs/guides/quickstart.md) [Chart settings](https://github.com/hetznercloud/hcloud-cloud-controller-manager/blob/main/chart/values.yaml)

## Private-node bootstrap and routing

Design the following paths independently before creating nodes:

1. Administrator to Kubernetes API and SSH/OS-management endpoints through a VPN, bastion, or intentionally exposed endpoint.
2. Nodes and bootstrap processes to image registries, repositories, DNS, time services, and Hetzner APIs, through working egress or internal mirrors.
3. Node-to-node and pod-to-pod traffic with nonoverlapping Cloud, pod, service, office, and VPN CIDRs.
4. Public application traffic through a Load Balancer or reverse proxy to private targets.

A public Load Balancer handles inbound service traffic; private nodes still require an egress design. Build and validate that path before installation downloads or controller reconciliation depend on it. Ensure bootstrap automation can run before CoreDNS, the CNI, and the normal workload network are available.

Use the [CCM private-network guide](https://github.com/hetznercloud/hcloud-cloud-controller-manager/blob/main/docs/guides/private-network-setup.md) for the selected CNI mode. Configure `HCLOUD_NETWORK` / chart networking settings and the actual pod CIDR consistently. Decide whether CCM installs pod routes or the CNI implements encapsulation/native routing. Do not enable two competing route owners. Networking support and route reconciliation are separate concerns; recheck the release's `HCLOUD_NETWORK_ROUTES_ENABLED` behavior when the CNI owns routes.

Verify node `InternalIP`, provider ID, topology labels, routes, and removal of the cloud-provider initialization taint. Use the actual private interface and account for tunnel overhead; see [performance and MTU diagnosis](observability-performance.md). On mixed Cloud/Robot clusters, verify dedicated-server support, vSwitch paths, credentials, and scheduling constraints separately.

## Service exposure and Load Balancers

Use a `Service` of type `LoadBalancer` for CCM-managed service exposure. For many HTTP applications, consider one LB-backed ingress/Gateway service rather than one purchased Load Balancer per application; route applications in the selected controller.

These annotations have different meanings; prefix all with `load-balancer.hetzner.cloud/`:

| Suffix | Meaning |
|---|---|
| `use-private-ip: "true"` | Reach target servers using private IPs |
| `disable-public-network: "true"` | Disable public ingress; this is an internal LB decision |
| `disable-private-ingress: "true"` | Disable private ingress behavior, independent of private targets |
| `location` or `network-zone` | Placement choice; use one, not both |

Changing LB location annotations does not move an existing LB; recreation changes public IPs. Review DNS and client implications before replacement. [Annotation reference](https://github.com/hetznercloud/hcloud-cloud-controller-manager/blob/main/docs/reference/load_balancer_annotations.md)

The upstream private-network guide identifies an IPVS-specific case where `disable-private-ingress: "true"` prevents health-probe loops. Apply it based on the actual data path, not as a universal security switch. [Private Load Balancer guide](https://github.com/hetznercloud/hcloud-cloud-controller-manager/blob/main/docs/guides/load-balancer/private-networks.md)

Check service protocol, node target/NodePort health, readiness probes, source IP, and trusted proxy headers together. Hetzner supports TCP, HTTP, and HTTPS services, not UDP forwarding; HTTPS termination forwards HTTP to targets. Enable PROXY protocol only when the backend explicitly understands it. [LB FAQ](https://docs.hetzner.com/networking/load-balancers/faq/)

For a pending or unhealthy service, read `kubectl describe service`, CCM logs, target health, endpoint slices, node addresses, and host/CNI firewall rules. Check whether external-dns is advertising public, private, IPv4, or IPv6 addresses as intended. Keep Terraform and CCM ownership distinct so one reconciler does not undo the other.

## Persistent storage and recovery

The official CSI provides Cloud Volume integration, including ReadWriteOnce usage. It does not turn a Volume into shared RWX storage. A Cloud Volume attaches to one server at a time, and server Backups/Snapshots do not include attached Volumes. Use separate application-consistent data backups. [CSI scope](https://github.com/hetznercloud/csi-driver) [Volume limits](https://docs.hetzner.com/cloud/volumes/overview/)

Retain a topology-aware StorageClass and inspect `volumeBindingMode: WaitForFirstConsumer`, reclaim policy, expansion, and node affinity. The upstream manifest uses delayed binding; verify the chart you deploy rather than assuming all existing classes do. [CSI manifest](https://github.com/hetznercloud/csi-driver/blob/main/deploy/kubernetes/hcloud-csi.yml)

Treat a Volume as location-bound storage, not automatic cross-location disaster recovery. Match workloads to compatible nodes. For a failed-node attachment, investigate fencing and old mounts before forcing detach/recovery. Storage replication, database replication, backups, and multi-node application availability address different failure modes.

For HA, document control-plane quorum, placement, application replicas, network dependencies, external access, stateful recovery, and tested restore time. Three VMs alone do not prove an application survives a location failure.

## Docker networking and diagnosis

Cloud Firewalls do not filter private Cloud Network traffic and cannot currently attach to Load Balancers. Protect hosts, databases, and east-west paths with guest firewall rules and the chosen CNI's policy support. [Firewall FAQ](https://docs.hetzner.com/cloud/firewalls/faq/)

Docker published ports use forwarding/NAT chains; a host INPUT policy alone is insufficient. With Docker's iptables backend, use the supported `DOCKER-USER` hook for appropriate filtering and account for DNAT. Docker may change FORWARD policy, affecting a host that also serves as a VPN/NAT gateway. With another firewall backend, follow that backend's documented hooks instead of transplanting iptables recipes. [Docker firewall documentation](https://docs.docker.com/engine/network/firewall-iptables/)

After changes, test public ingress, private access, pod DNS, cross-node traffic, image pulls, and egress from an actual workload. During incidents, correlate application failures with CCM/CSI events and guest networking; avoid deleting Services, PVCs, or nodes merely to restart reconciliation.
