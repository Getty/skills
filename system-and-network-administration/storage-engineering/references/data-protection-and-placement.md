# Data Protection and Placement

Evidence checked: 2026-10-21. Use this reference to select a protection method and prove which failures its placement can survive. Treat capacity formulas as planning models, not durability predictions.

## Contents

- [Separate protection goals](#separate-protection-goals)
- [Compare protection methods](#compare-protection-methods)
- [Place copies against real failure domains](#place-copies-against-real-failure-domains)
- [Budget capacity and recovery](#budget-capacity-and-recovery)
- [Detect and repair corruption](#detect-and-repair-corruption)
- [Work through two examples](#work-through-two-examples)
- [Verify the design](#verify-the-design)
- [Primary references](#primary-references)

## Separate protection goals

State four requirements independently:

1. **Integrity:** detect an incorrect stored value and identify a trustworthy replacement.
2. **Durability:** retain acknowledged data through the specified failure event.
3. **Availability:** continue serving the required operations during that event.
4. **Recoverability:** reconstruct a usable earlier state after deletion, compromise, or software error.

A mirror can preserve two copies of an accidental deletion. A parity group can retain its bytes while an unavailable metadata service prevents access. A readable old backup can satisfy recovery while failing a five-minute RPO. Never use one of these outcomes as proof of the others.

Separate redundancy inside a device, inside a storage node, across nodes, and across sites. Identify which layer acknowledges writes, detects failures, repairs data, and decides whether degraded writes may continue. More layers can be useful, but they multiply write traffic and can obscure the real failure boundary.

## Compare protection methods

| Method | Basic capacity model | Useful property | Boundary to investigate |
| --- | --- | --- | --- |
| Striping / RAID 0 | Sum of participating capacity | Parallelism and aggregate space | Provides no redundancy; failure of a required member loses the stripe set |
| Mirroring / RAID 1 | One copy's usable capacity for a simple equal-sized mirror | Straightforward copies; comparatively simple reconstruction | Protects only failures that leave a current, reachable copy |
| RAID 10 | About half raw capacity for two-way mirrors | Stripe performance with mirror recovery | Failure tolerance depends on which mirror members fail; do not claim any half of disks may fail |
| Single/double parity RAID | Approximately (n−1)/n or (n−2)/n of equal-sized raw capacity | Better capacity efficiency than two-way mirrors | Small writes, degraded reads, rebuild load, parity consistency, and enclosure correlation |
| Distributed replication | Raw capacity divided by replica count r | Copies can be placed in different hosts/racks/sites | Data durability and serving quorum depend on acknowledgement and placement policies |
| Erasure coding | Data fraction k/(k+m) | Recover a stripe from sufficient surviving fragments with lower capacity overhead | CPU, read/write amplification, small objects, rebuild fan-out, metadata protection, and actual fragment placement |
| Local reconstruction / hierarchical coding | Code-specific | Reduce some repair traffic or combine local and global protection | Failure patterns differ from a simple maximum-distance-separable k+m code |
| Snapshot / clone | Changed/shared blocks plus metadata | Fast rollback or economical copies | Usually shares a failure and administration domain with its origin |
| Independent versioned backup | Retention and change-rate dependent | Recover previous states | Requires independent keys, catalog, permissions, and a tested restore path |

For a conventional maximum-distance-separable k+m erasure code, any k intact fragments reconstruct the stripe and up to m missing fragments are tolerable. Do not apply that statement indiscriminately to every code or to whole cluster availability. A missing metadata quorum, an unavailable gateway, or a placement that puts several fragments in one rack can stop service before the mathematical reconstruction limit is reached.

RAID implementations also differ in their handling of interrupted parity updates. The Linux MD documentation explicitly describes the danger of starting an array that is both dirty and degraded; a forced assembly is a recovery decision, not a routine availability fix. Consult the implementation's journal, write-intent bitmap, partial-parity logging, or equivalent mechanisms before drawing conclusions about power-loss behavior. [Linux MD documentation](https://www.kernel.org/doc/html/latest/admin-guide/md.html)

## Place copies against real failure domains

Create a placement table with device, controller, chassis, host, rack/PDU, switch, room, site, provider, and administrative domain. Add dependencies such as shared UPS, hypervisor, SAN, KMS, identity tenant, and deployment pipeline. Two virtual machines are not proven independent storage failure domains merely because their names differ.

For every required failure, remove the affected components on paper and count separately:

- Current data copies or reconstructable fragments.
- Metadata and voting members needed for reads and writes.
- Reachable gateways, client paths, authentication services, and encryption keys.
- Remaining free capacity, IOPS, CPU, and network bandwidth for repair.

Specify whether placement is a hard constraint or a preference. A soft anti-affinity rule may intentionally colocate copies when capacity runs out. A hard rule may leave data under-replicated instead. Monitor the actual placement rather than treating the configured replica number as evidence of protection.

Ceph's CRUSH model is an example of topology-aware placement: its hierarchy and rules can distribute replicas or fragments across hosts, racks, and other configured domains. Its cluster view must accurately represent the physical or provider topology; software labels do not create physical independence. [Ceph CRUSH maps](https://docs.ceph.com/en/tentacle/rados/operations/crush-map/)

## Budget capacity and recovery

For an initial equal-device estimate, calculate:

- Replicated nominal usable capacity = raw capacity / r.
- EC nominal usable capacity = raw capacity × k / (k+m).
- Planned logical occupancy = nominal usable capacity × an explicitly chosen operating occupancy limit.

Deduct or model filesystem reserves, metadata, journals, snapshots, object rounding, unequal device sizes, fragmentation, and rebuild space. Treat compression and deduplication as measured workload properties; use a conservative ratio of 1 unless measurements justify another value. Thin provisioning changes allocation timing, not physical capacity.

Then calculate whether the surviving domains can restore the desired protection level. With one replica per host and exactly three hosts, three-way replication cannot be restored after losing a host until another eligible host is available. Free space on the two surviving hosts does not solve the topology constraint.

Estimate a lower bound for recovery time as bytes that must be read/transferred/written divided by the slowest effective throughput. EC recovery may read substantially more than the amount eventually written, depending on the code and repair algorithm. Reserve normal workload capacity while measuring repair, and include detection, provisioning, placement, and verification in the operational estimate.

Do not compute a reassuring annual loss probability from independent disk failure rates unless independence, repair time, latent error behavior, and common-mode faults are explicitly justified. Firmware defects, power events, operator mistakes, and shared dependencies can dominate the result.

## Detect and repair corruption

Use checksums at meaningful boundaries and periodically read cold data. Detection alone cannot reconstruct a correct value. Repair needs a verified alternate replica, parity with adequate intact fragments, or a backup. A storage checksum can also correctly validate bytes that were already wrong when the application wrote them; validate application invariants separately.

Differentiate a **scrub**, which searches stored data for errors, from a **rebuild/resilver**, which restores missing or outdated redundancy. OpenZFS documents this distinction and repairs detected damage when suitable redundant data exists. Schedule checks so they do not consume the entire recovery or latency budget. [OpenZFS scrub documentation](https://openzfs.github.io/openzfs-docs/man/master/8/zpool-scrub.8.html)

## Work through two examples

**Example A — six equal storage hosts with 4+2 EC.** One fragment per host allows a stripe to remain reconstructable after any two host losses, subject to the code and intact surviving fragments. Place three hosts in each of two sites and losing one site removes three fragments: the host-failure result does not become site protection. A majority of metadata voters somewhere else cannot reconstruct those missing bytes.

**Example B — three-way replication in a single room.** Three independent hosts can address one host failure if their implementation's serving policy permits it. A shared switch or room power failure can remove all copies from reach. Add an independent backup or another site according to the required event, and evaluate networking and identity alongside the disks.

For Ceph-specific EC proposals, verify the selected release's allowed overwrite modes, metadata requirements, recovery behavior, and placement rules. The general k+m capacity calculation does not prove that a particular pool supports the intended workload. [Ceph erasure coding](https://docs.ceph.com/en/tentacle/rados/operations/erasure-code/)

## Verify the design

Record healthy, degraded, recovering, and full states. For each, predict whether reads, writes, deletion, provisioning, and repair succeed; then compare those predictions with a bounded test. Check acknowledgement semantics with the actual cache and power-loss configuration. After repair, verify the number, location, and health of copies before declaring the system protected again.

## Primary references

- [Linux MD RAID arrays](https://www.kernel.org/doc/html/latest/admin-guide/md.html): parity consistency and recovery behavior.
- [Ceph CRUSH maps](https://docs.ceph.com/en/tentacle/rados/operations/crush-map/): topology-aware placement.
- [Ceph erasure coding](https://docs.ceph.com/en/tentacle/rados/operations/erasure-code/): code parameters and implementation constraints.
- [OpenZFS scrub manual](https://openzfs.github.io/openzfs-docs/man/master/8/zpool-scrub.8.html): integrity checking and redundancy-assisted repair. The master manual may describe features absent from an installed release.
