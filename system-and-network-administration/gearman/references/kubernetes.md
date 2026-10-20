# Kubernetes design: state, identity and execution pools

The manifests are **unapplied templates**. Kubernetes fields must be validated against the target cluster API and policy before use. Gearman topology semantics are grounded in [G2, S1](sources.md); the orchestration choices here are explicit design recommendations.

## One pod is one queue owner

The supplied StatefulSet has one replica, one stable network identity and one queue volume. Increasing replicas produces independent queues; it does not add replication. A headless service exposes identities, while an ordinary service can distribute TCP connections without coordinating which queue contains a particular job.

When scaling to multiple independent servers, make routing explicit and connect the intended worker pools to every required endpoint. When implementing active/passive recovery, provide fencing and storage ownership guarantees. ReadWriteOnce storage access alone is not proof that an old process cannot still execute work. Do not run independent owners over the same persistence table.

## Worker design

Use separate deployments for function classes with materially different CPU, memory, GPU, dependency or trust requirements. Define execution slots per pod; the native worker count is not a precise autoscaling signal for free slots. Scale using age, sustained backlog and measured execution time together with downstream capacity ceilings.

On termination, stop acquisition and finish bounded in-flight work within the grace window. Coordinate application shutdown and the entrypoint so signals reach the worker, not only a shell wrapper. A lifecycle hook that sleeps without stopping acquisition is not a reliable drain. Protect effects against forced pod loss and rescheduling.

## Probes and resources

Use a small ECHO probe for server liveness and an appropriate readiness policy. Neither guarantees workers or persistence are healthy. Avoid probes that enqueue jobs, and avoid restarting a live server merely because a downstream service is briefly unavailable. Startup probes should allow realistic queue replay before liveness begins.

Give the server memory headroom for queued payloads and replay. Set worker resources according to measured jobs, not a guessed identical limit for every function. A server OOM with persistent storage can still produce duplicate/unknown effects. Persist outcomes outside ephemeral pod filesystems when callers require them.

## Network and configuration

The example NetworkPolicy allows selected producer/worker/observer pods to reach the server's native port. This is a coarse network boundary, not per-command authorization; those clients can potentially reach native administration. NetworkPolicy enforcement depends on the cluster networking implementation. TLS/VPN or other authenticated transport is a separate decision.

Replace the deliberately invalid example image reference with your tested image digest, select a storage class and resource budget, and choose certificate/secret distribution before deployment. Do not expose the native listener using an Internet-facing LoadBalancer by default. Validate manifests with the cluster's schema and dry-run tools only under authorized credentials.

## Rollout acceptance

Test server replay, worker-version coexistence, readiness during draining, loss of a node, stale owner fencing, delayed-job behavior, duplicate effects and origin-specific diagnostics. A successful rolling deployment does not establish these properties automatically.

Deployment API background: [O1–O3 and verification caveats](sources.md).
