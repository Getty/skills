# Observability, performance diagnosis, and measured optimization

Verified on **2026-10-04**. Read current product limits and status before interpreting measurements. Treat public benchmarks and forum reports as hypotheses; compare equivalent workloads and record the actual plan, architecture, location, image, time window, and path.

## Contents

- Define the symptom and baseline
- CPU, memory, and disk
- Network and MTU diagnosis
- Load Balancers and application telemetry
- Optimization and incident evidence

## Define the symptom and baseline

Start with the application's impact: throughput, p50/p95/p99 latency, error rate, queue growth, replication lag, or missed jobs. Define success numerically and select one investigation window. “CPU is high” can describe useful work; “load average is high” does not identify the limiting resource.

Combine provider-level measurements with guest and application telemetry. Install an appropriate host exporter, collect its CPU/memory/filesystem/disk/network metrics, and instrument the application. Expose metrics through private or authenticated access. The [Prometheus node exporter](https://github.com/prometheus/node_exporter) supplies machine metrics; it cannot explain an application query plan by itself.

Record configuration and deployment changes beside the graphs. Use UTC timestamps, stable resource IDs, hostnames, Cloud location, and relevant network interfaces. Observe both a quiet and busy period before buying a larger plan.

## CPU, memory, and disk

Shared-vCPU plans share processor resources with other instances; Hetzner positions them for variable workloads. Dedicated-vCPU Cloud plans are a candidate for steadier sustained demand. Compare measured tail latency under equivalent load before assuming a specific plan family is inherently faster for your application. [Cloud product guidance](https://www.hetzner.com/cloud/)

| Symptom | Inspect | Possible experiment |
|---|---|---|
| Latency under CPU demand | Per-core utilization, run queue, steal time, throttling, process profile | Move a representative workload to dedicated vCPU; compare cost per successful request |
| Memory stalls or OOM | Working set, swap, cgroup limit, OOM logs, memory pressure | Fix a leak or change cache limits before only adding RAM |
| Slow database commits | fsync latency, queue depth, device mapping, query/write workload | Compare local disk and Volume using representative persistence settings |
| Slow bulk file transfer | Read/write throughput, CPU encryption cost, network retransmits | Test storage and network separately |

Linux Pressure Stall Information reports CPU, memory, and I/O stalls at system and supported cgroup scopes. Use it with utilization and workload latency to identify contention; it measures waiting rather than a vendor cause. [Kernel PSI documentation](https://docs.kernel.org/accounting/psi.html)

Read-only starting commands, where installed:

```bash
date -u
uptime
vmstat 1 5
iostat -xz 1 5
lsblk -o NAME,TYPE,SIZE,FSTYPE,MOUNTPOINTS
df -hT
df -i
cat /proc/pressure/cpu /proc/pressure/memory /proc/pressure/io
```

Cloud Volumes are networked block storage. Published limits currently distinguish sustained from burst performance: up to 5,000/7,500 IOPS and 200/300 MB/s respectively. These are ceilings, not promised per-query latency. Record block size, queue depth, read/write mix, caching, and fsync behavior before comparing results. [Volume overview](https://docs.hetzner.com/cloud/volumes/overview/)

Never run a write benchmark against a live device or database directory. Use a disposable file on a suitable test filesystem, bound runtime/size, and avoid saturating production workloads. Verify backup and restore separately; good disk benchmark results say nothing about recoverability.

## Network and MTU diagnosis

Hetzner does not guarantee Cloud server bandwidth. The technical FAQ describes shared host connectivity and an indicative 300–500 Mbit/s expectation; neither a virtual NIC's reported speed nor one fast iperf result is an individual server guarantee. Maximum supported Cloud interface MTUs are currently **1500 public / 1450 private**. Additional VPN/CNI encapsulation consumes further headroom. [Technical FAQ](https://docs.hetzner.com/cloud/technical-details/faq/)

Follow this sequence:

1. Identify the exact path: public IP, private Network, vSwitch, VPN, NAT gateway, LB, IPv4/IPv6, and both endpoint locations.
2. Check addresses, route choice, source address, MTU, DNS, and firewall counters before testing throughput.
3. Measure host-to-host in the same location, then the real cross-location/client path. A comparison that changes both location and server size cannot isolate either effect.
4. Inspect retransmissions and CPU usage while testing. Repeat a small set of controlled trials; separate single-stream behavior from aggregate parallel throughput.
5. For a large-packet stall with successful small pings, investigate path MTU and blocked fragmentation-needed / packet-too-big feedback. Do not disable ICMP wholesale or paste an arbitrary MSS value.

Useful local inspection:

```bash
ip -br addr
ip route
ip rule
ip -s link
ss -s
```

For support-quality packet-loss evidence, Hetzner requests traces in both directions with at least 200 packets, for example `mtr -s 1000 -r -c 200 TARGET`. Save the reports rather than quoting one hop. Intermediate-hop ICMP loss that disappears by the destination may just be control-plane rate limiting. Asymmetric routes make the reverse trace valuable. [Hetzner network report guide](https://docs.hetzner.com/cloud/servers/network-diagnosis-and-report-to-hetzner/)

## Load Balancers and application telemetry

Measure concurrent connections, new-connection rate, TLS-handshake cost, target health, service timeout, and backend saturation separately. Hetzner Load Balancers do not provide individual request logs; configure application/reverse-proxy logs for that purpose. Protect trusted-proxy handling so logged client addresses are meaningful. [LB FAQ](https://docs.hetzner.com/networking/load-balancers/faq/)

For long-lived streaming, WebSockets, SSE, or slow APIs, inspect idle timeout and application heartbeat behavior before interpreting disconnects as capacity exhaustion. Recheck the current configurable timeout range and service settings rather than relying on an old fixed-limit tutorial. Use separate readiness and liveness probes so a downstream dependency problem does not trigger unproductive restart loops.

## Optimization and incident evidence

Prioritize experiments by the observed bottleneck: cache/coalesce repeated work, colocate latency-sensitive application/database traffic, right-size memory, control concurrency, batch I/O where the application permits it, and use local registry/package mirrors when repeated downloads dominate. Hetzner maintains Debian/Ubuntu package mirrors used by standard images; preserve update authenticity and repository correctness. [Package mirror](https://docs.hetzner.com/robot/dedicated-server/operating-systems/hetzner-package-mirror/)

For any optimization, record baseline, one change, expected effect, measurement interval, result, and rollback. Recheck cost after rescaling. Retain changes only when they improve the chosen objective without violating recovery or reliability requirements.

Prepare an incident packet with timestamps, impacted resource IDs, topology, application impact, relevant metrics/logs, both-direction traces, and recent changes. Remove credentials and unnecessary payload data. Consult current [Hetzner status](https://status.hetzner.com/); an empty status page does not disprove a localized issue. Preserve evidence before disruptive reboots, migrations, or rebuilds.
