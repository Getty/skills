# Cloud compute: selection, bootstrap and lifecycle

Evidence snapshot: **2026-10-04**. Refresh available types, images, architecture support, quotas and prices before implementation. Example commands below inspect a Linux guest; they do not provision resources.

## Contents

- [Select resources and architecture](#select-resources-and-architecture)
- [Provision a reproducible guest](#provision-a-reproducible-guest)
- [Rescale without losing the return path](#rescale-without-losing-the-return-path)
- [Placement and application availability](#placement-and-application-availability)
- [Console, Rescue and custom systems](#console-rescue-and-custom-systems)
- [Acceptance evidence](#acceptance-evidence)

## Select resources and architecture

Cloud offers shared and dedicated CPU-resource classes. Select shared resources for workloads that tolerate contention; evaluate dedicated resources for sustained CPU pressure. Neither classification by itself promises application latency. The current overview distinguishes cost-optimized and regular shared offerings and dedicated general-purpose offerings. Compare the actual workload over time, including p95/p99 latency, CPU pressure, memory, disk latency and network throughput. [Server overview](https://docs.hetzner.com/cloud/servers/overview/).

The documented architecture choices constrain images and migration: x86 and Arm64 backups/ISOs are not interchangeable, and rescale stays within the existing architecture. CX hardware may be Intel or AMD according to allocation; a rescale can change the vendor. A dedicated vCPU represents an exclusively allocated physical CPU thread, not necessarily an entire physical core. [Server FAQ](https://docs.hetzner.com/cloud/servers/faq/).

Before choosing Arm64, check every container image, native dependency, build tool, monitoring agent and restore utility. Benchmark a representative request and full restore. An architecture switch is a new deployment plus data migration, with compatible application artifacts, not an in-place resize.

The FAQ also excludes nested virtualization, Secure Boot and vTPM/TPM. Check these requirements before selecting Cloud for a hypervisor or appliance. [Platform limitations](https://docs.hetzner.com/cloud/servers/faq/).

Cloud uses KVM with virtio devices and local NVMe storage. The provider's technical FAQ does not promise per-instance network bandwidth. A host uplink specification must not become a VM throughput guarantee. [Technical details](https://docs.hetzner.com/cloud/technical-details/faq/).

## Provision a reproducible guest

Record project, location, type, architecture, image, SSH-key fingerprints, labels, network attachment, storage and backup policy. Use a standard image when its lifecycle fits. The creation workflow supports cloud-init and labels; Console's cloud-config input is limited to 32 KiB. Treat user data as bootstrap configuration rather than a place for durable secrets. [Creation guide](https://docs.hetzner.com/cloud/servers/getting-started/creating-a-server/).

A practical bootstrap sequence:

1. Establish the management route and required outbound access first. A private-only guest cannot fetch packages merely because it has a private IP.
2. Configure users, SSH keys, time synchronization and baseline host firewall rules.
3. Mount persistence by stable identifiers, then start services only after the mount is available.
4. Wait for initialization to finish before testing the application; API creation success is not application readiness.
5. Capture the image and provisioning revision so a second server can be rebuilt without manual discovery.

Useful guest inspection:

```bash
uname -m
cloud-init status --long
ip -br address
ip route show
ip -6 route show
lsblk -f
findmnt
systemctl --failed
```

If cloud-init fails, inspect its local logs and fix the first failing dependency. Avoid rerunning an entire bootstrap script blindly: package installation, account creation and filesystem initialization have different retry safety.

## Rescale without losing the return path

Disk growth is the key irreversible choice: the platform cannot rescale to a disk smaller than the server's already allocated disk, even when little data is used. Keeping the disk size unchanged while increasing CPU/RAM preserves more downgrade options. A filesystem/partition may require a separate growth operation after the virtual disk grows. [Rescale and disk FAQ](https://docs.hetzner.com/cloud/servers/faq/).

Recommended workflow:

1. Measure the bottleneck and confirm the target type actually addresses it.
2. Check same-architecture compatibility, current target capacity and allocated disk size.
3. Make an application-consistent recovery point, and identify separately attached data disks.
4. Drain traffic and stop writers cleanly. Plan a shutdown window for the resize; follow the current `change_type` action's state requirements. [Cloud API](https://docs.hetzner.cloud/reference/cloud).
5. Choose disk growth explicitly. Never bundle it into a CPU/RAM-only performance experiment by accident.
6. After boot, inspect block-device size, partitions, LVM and filesystem independently. Use the actual filesystem's supported growth procedure.
7. Re-run a representative workload. Keep the original data recovery point until the new configuration is accepted.

A smaller replacement server plus logical/file-based data migration is a distinct option when reducing disk allocation. A snapshot of a large virtual disk is not automatically a shortcut to a smaller disk. Confirm restore constraints before deleting the source.

## Placement and application availability

A spread Placement Group puts members on different physical hosts. The documented limit is ten servers in one spread group, with one group per server. This reduces host co-failure; it does not provide a separate datacenter, network zone, database quorum or application failover. [Placement overview](https://docs.hetzner.com/cloud/placement-groups/overview/), [failure-scope FAQ](https://docs.hetzner.com/cloud/placement-groups/faq/).

For replicas, separate host failures first, then assess location failures and replication latency. A provider live migration can include a brief interruption and performance disturbance; it is not a substitute for retry logic and redundancy. [Live-migration architecture](https://docs.hetzner.com/cloud/servers/technical-concepts/architecture/).

## Console, Rescue and custom systems

The browser VNC console is a guest screen/keyboard path, useful when SSH or guest routing is broken. It requires a usable guest login. Standard images include QEMU guest agent for the documented password-reset feature; removing it removes that recovery mechanism. Check this before relying on a newly requested password. [Console procedure](https://docs.hetzner.com/cloud/servers/getting-started/vnc-console/), [guest-agent behavior](https://docs.hetzner.com/cloud/technical-details/faq/).

**Private-only Cloud servers have no Rescue system under the documented contract.** They also cannot use Cloud Floating IPs or Cloud Firewalls. Plan console credentials and a tested management route before removing the last Primary IP. [Private-only restrictions](https://docs.hetzner.com/cloud/servers/faq/).

For a server eligible for Rescue, enable it and boot into the temporary recovery environment; distinguish examining disks from reinstalling them. [Cloud Rescue](https://docs.hetzner.com/cloud/servers/getting-started/rescue-system/). Custom operating systems need compatible virtio support, networking and recovery tooling. Windows Server is a manual, unsupported guest scenario subject to the applicable licensing terms; use its specific guide. [Windows on Cloud](https://docs.hetzner.com/cloud/servers/windows-on-cloud/).

## Acceptance evidence

Record successful initialization, service readiness, management access after a reboot, a backup restore, resource utilization under representative load, and the remaining bottleneck. Confirm billing separately: shutting down a Cloud server does not stop its resource charges. [Cloud billing FAQ](https://docs.hetzner.com/cloud/billing/faq/).
