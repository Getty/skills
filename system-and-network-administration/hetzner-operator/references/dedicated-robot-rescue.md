# Dedicated servers, Robot and recovery

Evidence snapshot: **2026-10-04**. Recheck the individual hardware offer, network options, support workflow and maintenance terms. Instructions here are a planning and diagnostic workflow, not permission to reinstall an existing machine.

## Contents

- [Choose the physical platform](#choose-the-physical-platform)
- [Provision with an explicit disk plan](#provision-with-an-explicit-disk-plan)
- [Keep recovery paths distinct](#keep-recovery-paths-distinct)
- [Respect dedicated-server networking](#respect-dedicated-server-networking)
- [Handle hardware incidents](#handle-hardware-incidents)
- [Accept the deployment](#accept-the-deployment)

## Choose the physical platform

Dedicated root servers give the customer an entire physical machine and root-level software responsibility. Robot handles server administration, vSwitch, recovery and authenticated hardware support. Some models permit hardware upgrades, but this is a model-specific service rather than a Cloud rescale operation. [Bare-metal overview](https://docs.hetzner.com/robot/dedicated-server/getting-started/root-server-guide/).

Compare current EX, AX, SX, DX, GPU and Auction offers by workload requirements rather than memorized suffixes. Record CPU generation, usable memory, ECC where specified, disk model/count, RAID options, hardware-controller presence, NIC bandwidth, hot-swap capability, location and setup charges. The hardware overview links current models and upgrade options. [Hardware overview](https://docs.hetzner.com/robot/dedicated-server/dedicated-server-hardware/dedicated-server-hardware-overview/).

Auction machines come from changing inventory and can retain custom hardware. Their actual configuration matters more than the headline model name. Hetzner tests these machines and replaces defective hardware; the customer still owns configuration, monitoring and backups. A low purchase decision cost does not remove the cost of rebuilding a failed host. [Auction FAQ](https://docs.hetzner.com/robot/general/server-auction-faqs/).

GPU servers are a separate dedicated product. As of this snapshot, the GEX catalog includes the Blackwell-based GEX45 and the GEX131 family; always reopen the actual offer for GPU model, VRAM, numerical-format support and availability. Size an inference deployment from model weights plus KV cache and concurrency; marketing AI-TOPS is not an application throughput result. [GPU catalog](https://www.hetzner.com/dedicated-rootserver/matrix-gpu/). For detailed serving design, use a relevant model/runtime skill if available.

## Provision with an explicit disk plan

For a fresh authorized installation, choose between a standard installation, `installimage` in Rescue, or custom ISO installation through KVM. `installimage` supports partitioning, LVM and software RAID. Its selected `DRIVE` devices are wiped, and an existing `/autosetup` file can supply the configuration automatically. [Installimage](https://docs.hetzner.com/robot/dedicated-server/operating-systems/installimage/), [maintained source](https://github.com/hetzneronline/installimage).

Before installation:

1. Match Robot server identity and delivery information to the machine in front of you.
2. Inventory disks by model, serial, capacity and existing filesystems. Use stable identity when translating the plan into device paths.
3. Decide which drives hold the OS, application data and disposable scratch space. Record precisely which may be erased.
4. Select software RAID only after considering usable capacity, rebuild duration and application behavior during degradation. RAID is not a versioned backup.
5. If a hardware RAID controller is present, configure its logical disks before an OS installer expects them. Do not accidentally layer two RAID designs.
6. Inspect generated boot, partition and network configuration before committing the installation. Preserve the reviewed configuration outside the host.

Read-only inventory for a Linux environment:

```bash
lsblk -o NAME,PATH,SIZE,MODEL,SERIAL,FSTYPE,MOUNTPOINTS
findmnt
cat /proc/mdstat
ip -br link
ip -br address
ip route show
```

Avoid generic wildcard disk-wiping commands in reusable automation. A storage layout designed for two NVMe devices should fail closed when a third data device or a different inventory appears.

## Keep recovery paths distinct

| Path | What it provides | Operational implication |
|---|---|---|
| SSH/RDP | Access through the installed OS and configured network | Depends on the guest service and network configuration |
| Robot reset | Power/reset control | Can interrupt writes; it does not diagnose the problem |
| Rescue | Network-booted Linux environment running in RAM | Requires reboot; existing disks can be inspected or repaired |
| KVM console | Keyboard/video/mouse and boot/virtual-media access | Physical console equipment is attached by technicians; arrange availability |

Rescue activation schedules the next boot; it does not switch a running system immediately. The documented activation is one-use and expires if not used within an hour. Preserve evidence before rebooting a failing system where possible. [Rescue system](https://docs.hetzner.com/robot/dedicated-server/troubleshooting/hetzner-rescue-system/).

KVM can repair boot or network problems and mount installation media. It is not the same always-present browser console offered for a Cloud VM. Request it through Robot; equipment is finite and extended use may be charged. Check the assigned KVM model's media procedure. [KVM console](https://docs.hetzner.com/robot/dedicated-server/maintenance/kvm-console/).

When recovering data, first identify RAID/LVM/encryption layers. Mount the correct logical volume; never assume the example `/dev/md2` is the application's root filesystem. For filesystem repair, use the filesystem-specific offline procedure and a recovery copy where needed. [Filesystem checks](https://docs.hetzner.com/robot/dedicated-server/troubleshooting/filesystem-check/).

## Respect dedicated-server networking

Dedicated public networking uses provider routing constraints. Hetzner documents an IPv4 `/32` point-to-point configuration with a route to the gateway; blindly applying the apparent public subnet mask can break communication to neighboring servers. The documented IPv6 default gateway is `fe80::1`. For virtualization, routed and bridged designs differ; publicly bridged additional single IPv4 addresses require the corresponding Robot-issued virtual MAC. [Debian/Ubuntu network configuration](https://docs.hetzner.com/robot/dedicated-server/network/net-config-debian-ubuntu/).

For private host-to-host connections or Cloud coupling, use [hybrid-vswitch.md](hybrid-vswitch.md). Plan public ingress and outbound access separately. A private VLAN does not automatically disable the physical server's public networking or convert it to a Cloud private-only resource.

## Handle hardware incidents

Collect the server ID, UTC timestamps, symptoms, kernel errors, drive serials, SMART/NVMe or controller diagnostics, RAID status and the acceptable maintenance window. Ask for the affected component by serial; a device name may change after reboot or replacement. Hot-swap support is model-specific and can be checked in Robot's faulty-drive support workflow. [Hot swapping](https://docs.hetzner.com/robot/dedicated-server/maintenance/hot-swapping/).

A replacement drive is normally the start of recovery: partitioning, array rebuild, bootloader restoration and application verification remain operator work. Monitor the rebuild and verify which disks can boot. For a complete host replacement, recheck firmware/boot mode, NIC identity and network configuration before declaring recovery complete.

## Accept the deployment

Require successful boot, remote management, correct disk/RAID layout, monitored hardware, alert delivery, a representative workload, and a restoration exercise to another machine or isolated target. Record rebuild steps and external backup credentials independently from the server being protected.
