# Storage architecture brief

## Decision

State the recommended architecture and the workload constraint that drives it.

## Assumptions and unresolved facts

| Item | Known value or assumption | How to verify | Decision affected |
| --- | --- | --- | --- |
| Workload/data classes | | | |
| Required operations | | | |
| Scale/change rate | | | |
| RPO/RTO and failure target | | | |
| Hosts/sites/network | | | |
| Provider/service/version | | | |
| Budget/operator capacity | | | |

## Dataset contract

| Dataset | Authoritative owner | Interface | Writer/transaction model | Success acknowledgement | Restore source |
| --- | --- | --- | --- | --- | --- |
| | | | | | |

## Candidate comparison

| Candidate | Semantic fit | Failure coverage | Performance/capacity | Operational cost | Reason selected/rejected |
| --- | --- | --- | --- | --- | --- |
| | | | | | |

## Placement and dependencies

Describe data replicas/fragments, metadata, voters/witnesses, client endpoints, identity, keys, network and replacement compute. Use a diagram only when it makes the dependency or failure boundary clearer.

## Failure behavior

Complete the companion failure matrix for the failures the user actually needs to survive. Include asymmetric partition, stale writer and a second failure during rebuild where relevant.

## Capacity and performance budget

State physical and logical units, protection overhead, headroom, snapshots/versions, growth, metadata, degraded capacity, latency percentiles and the bottleneck. Distinguish calculated estimates from measured results.

## Recovery and failback

Specify backup consistency, retention, independent credentials, keys/catalog, restore order, promotion authority, writer fencing, validation, and return to redundancy.

## Implementation or migration stages

| Stage | Preconditions | Action | Acceptance evidence | Rollback boundary |
| --- | --- | --- | --- | --- |
| | | | | |

## Cost model

Include storage allocation/use, replicas, IOPS/throughput, API calls, retrieval, inter-site/egress traffic, cache, idle recovery capacity and operator effort. Date actual price assumptions.

## Validation and sources

List the representative application test, failure test and clean restore test; record results and what remains untested. Cite primary documentation for concrete product guarantees.
