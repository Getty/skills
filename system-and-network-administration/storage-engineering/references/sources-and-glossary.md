# Evidence discipline and storage terminology

Baseline research date: 2026-10-21. Source URLs within each reference are the authoritative lookup map for that topic; this file explains how to use them without turning a baseline into an evergreen promise.

## Contents

- Verify changing capabilities
- Handle conflicting documentation
- Keep evidence and inference separate
- Use precise terminology
- Search by the actual mechanism

## Verify changing capabilities

Use primary documentation, standards, vendor/project source code and release notes. A blog by the implementing project can explain a design; verify product support and release status in its current product documentation.

For a concrete recommendation, record:

| Field | Why it matters |
| --- | --- |
| Product/API and service class | Similar names can have different guarantees |
| Version and release channel | Development documentation is not stable-release support |
| Region/location and account | Availability, quotas, attachment and price vary |
| Client/driver/OS versions | A backend feature may not be exposed through this client |
| Source URL and checked date | Make re-verification possible |
| Claim type | Documented contract, observed result, engineering inference, or unknown |
| Test scope | One simple operation does not prove concurrency/durability correctness |

Recheck immediately before provisioning or changing a deployment: provider catalog, size/IOPS limits, attach modes, region restrictions, snapshot support, encryption defaults, S3 action compatibility, retention behavior, pricing, licensing, support and project maintenance status.

For broad explanations, use stable method-level reasoning and keep dated examples labeled. Avoid unnecessary price and quota tables that become stale without helping select a method.

## Handle conflicting documentation

1. Confirm that sources concern the same product, edition, location, API and version.
2. Prefer explicit API contracts and versioned technical docs for operation semantics.
3. Compare update dates and release notes; a newly crawled page can still contain old text.
4. Mark contradictory guidance and reduce the conclusion to what both sources establish.
5. Verify through a controlled experiment when it can answer the question safely.
6. Ask the provider for contractual clarification if the required guarantee remains unknown.

The Hetzner reference includes a concrete case where a general comparison cautions about network-storage database use while a block-storage product page lists databases. Resolve the actual durability and performance requirements; do not silently choose whichever sentence supports a preferred design.

Do not replace missing documentation with an assumption of AWS parity. Do not infer unsupported from absence in one search result either: use “not established” until the current product capability list resolves it.

## Keep evidence and inference separate

Use phrasing such as:

- “The documentation states …” for the supported contract.
- “In this measured workload …” for an observed result.
- “Given the stated topology, this design would …” for a conditional deduction.
- “This remains unverified …” for a capability requiring implementation-time work.

Do not present a replication factor as an SLA calculation or multiply advertised durability figures as though failures were independent. Firmware bugs, credentials, administrators, power, network, software upgrades, regions and accounts can create correlated failure.

Use runtime measurements for application latency and recovery. A published bandwidth limit does not establish achievable end-to-end throughput. A successful restore test demonstrates the tested scenario, not every possible disaster.

## Use precise terminology

| Term | Meaning to preserve |
| --- | --- |
| Availability | Ability to serve the required operation now, under a stated failure model |
| Durability | Persistence of acknowledged data across specified failures |
| Integrity | Data/metadata correctness and detectable corruption boundaries |
| Consistency | Visibility and ordering rules observed by clients |
| Recoverability | Ability to restore useful application state with available data, tools, keys and people |
| RPO | Maximum acceptable lost data measured by a defined recovery point; a target needs a mechanism |
| RTO | Maximum acceptable service recovery time; includes more than byte copying |
| Replica | Another copy with defined placement, lag and acknowledgement semantics |
| Shard | A partition of data; not automatically a redundant copy |
| Stripe | Data spread across devices/targets for layout or throughput |
| Erasure coding | Encoding k data fragments with m redundancy fragments; placement and availability rules still apply |
| Quorum | Required participating set for a particular operation/protocol, not a synonym for number of copies |
| Witness | Arbitration/voting participant; often does not contain user payload |
| Fencing | Enforced exclusion of a previous owner from further conflicting writes |
| Lease | Time-bounded authority whose safety depends on implementation and expiry assumptions |
| Snapshot | A point-in-time view/generation with a defined capture and failure boundary |
| Clone | A derived writable copy that may share underlying blocks |
| Backup | A retained, recoverable copy with a tested restore path and relevant independence |
| WORM/immutability | Restricted modification/deletion under a particular policy and threat model |
| Cache | A copy intended to accelerate access; dirty write-back can temporarily become authoritative |
| Tier | A placement class; it may hold the only current copy |
| Namespace | The mapping from names/paths/keys to data and metadata |
| Metadata plane | Names, placement, ownership, versions, catalog and other information needed to interpret payload |
| Data plane | The path serving actual data reads and writes |
| Control plane | Provisioning, membership, ownership and other management/coordination operations |
| Crash consistency | State recoverable as after an abrupt crash according to the application/storage contract |
| Application consistency | Capture coordinated with the application's own logical state requirements |
| Shared disk | More than one host can access block storage; filesystem/app coordination is separate |
| Shared filesystem | File namespace and supported coordination shared through a filesystem service |
| ReadWriteMany | A Kubernetes access capability, not proof the application is safe with many writers |
| Persistent volume | Persistence beyond a defined workload lifecycle, not indefinite retention or backup |
| S3 compatible | Supports a stated subset of an API family; verify operations and semantics |
| Active-active | Multiple active service instances; specify whether they write the same logical data |
| Split brain | Conflicting ownership/writes after loss of coordination |
| Failback | Returning authority/service after recovery, including reconciliation and exclusion of stale writers |

## Search by the actual mechanism

Use targeted terms rather than generic “best storage” searches:

- “stable write”, “flush”, “FUA”, “fsync”, “power loss protection”.
- “RWO RWOP access modes”, “CSI topology”, “WaitForFirstConsumer”, “non-graceful node shutdown”.
- “quorum min_size”, “lease fencing”, “reservation preemption”, “witness diskless”.
- “conditional PutObject”, “versioned bucket If-Match”, “multipart checksum”, “Object Lock supported actions”.
- “close-to-open consistency”, “SMB durable handle”, “NFS grace period”, “attribute cache”.
- “snapshot consistency group”, “WAL archive”, “restore catalog”, “metadata engine backup”.
- “degraded rebuild capacity”, “backfill network”, “recovery bandwidth”, “minimum retention billing”.

Resolve each result to the official version/location before treating it as evidence. Keep original commands out of production until target identity, permissions, destructive effects, rollback and current support are understood.
