# Topology, failover, and queue ownership

Read when adding a second server or promising high availability. Evidence: [G2, G13, S1](sources.md). Topologies below are engineering patterns, not built-in replication modes.

## Distinguish three forms of availability

**Admission availability** means a client can submit new work somewhere. **Execution availability** means a suitable worker can receive the already queued work. **Durable state availability** means accepted requests can be recovered with their business outcomes. A server list can improve the first without automatically solving the other two.

Each ordinary gearmand instance owns its own live queue. Connecting clients and workers to A and B does not copy A's jobs into B. When A fails, new work can move to B while A's pending work remains inaccessible until A recovers or the application reconciles and republishes it. Backend replication alone does not turn B into a coordinated successor to A.

## Patterns

| Pattern | Appropriate use | Required control |
|---|---|---|
| One server, supervised restart, durable backend | Small deployments with an acceptable restart window | Tested restore, bounded replay, application reconciliation |
| Independent servers, workers connected to each | Higher submission capacity and reduced admission dependence | Explicit routing, per-server monitoring, stranded-job procedure |
| Sharded functions/tenants | Resource isolation and scale | Stable mapping, shard migration, duplicate protection across moves |
| Active/passive owner | Recovery of one storage namespace | Fencing, single active writer, endpoint move and replay tests |

Do not implement active/passive by merely running two processes against one queue table. Define who proves the old owner is unable to run before the new owner starts.

## Load balancers and stable identity

A generic TCP load balancer selects connections, not individual jobs already queued on other servers. A worker pinned to A cannot see B's queue by magic. If client and worker connections distribute unevenly, jobs may have no useful workers even when the aggregate pool looks healthy. Long-lived connections also make naive round-robin expectations misleading.

Prefer explicit server endpoints when your binding understands multiple servers. Inspect that binding's selection, reconnection and duplicate-submission behavior rather than assuming all libraries are identical. For diagnostics store the submitting endpoint with each protocol handle. A live status request routed to another server can report “unknown” without telling you the original outcome.

## Failure drill

Submit identified work to A and B. Disable A, keep B healthy, verify new-work admission, and separately inventory uncompleted A requests. Recover A after selected requests have been safely republished to B; verify business deduplication. Repeat during producer and worker rolling upgrades. Track both assignment count and effect count.

## Capacity and migrations

Move producers and workers in a controlled sequence. During draining, stop new admission to the old shard, leave compatible workers connected, observe backlog and oldest age, and reconcile remaining IDs. Do not retire the last worker capable of processing a versioned function with queued jobs. A zero aggregate queue length is not sufficient if the old server has become unreachable rather than empty.
