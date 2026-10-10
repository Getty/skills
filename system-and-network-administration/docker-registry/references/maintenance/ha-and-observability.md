# High availability, monitoring, and operational objectives

> Read when: running multiple replicas or designing ongoing registry operations.

Start with explicit objectives: successful digest-pull rate, push completion time, recovery time, acceptable publication loss, and maintenance windows. Multiple frontends sharing one unhealthy backend are not independent availability domains.

## Shared-state design

Registry replicas require compatible storage, auth, HTTP-secret, and URL configuration. Coordinate GC and backend maintenance across all replicas. Test upload resumption through a different replica, failover of the proxy/storage/auth service, and partial network failure. Include token service and redirected blob endpoints in dependency monitoring.

## Observe useful signals

Track request rate/status/latency by operation, auth failures, upstream errors, blob bytes, upload durations/abandonment, storage bytes/inodes, cache hit/miss behavior where exposed, backend latency, certificate expiry, and backup/restore freshness. Avoid unbounded per-digest metric labels. Logs and trace attributes must omit credentials, bearer tokens, and presigned query strings.

Distribution notifications can integrate external workflows; do not assume exactly-once delivery or use an event alone as proof all artifact metadata is complete. Receivers should be idempotent, durable where necessary, and reconciled against current registry state. Test retries and receiver downtime.

## Failure drills

Exercise unavailable upstream, expired credentials, full backend, unreachable object redirect, one failed replica, rejected write during maintenance, and restored content with a missing blob. Verify alerts distinguish client 4xx/policy failures from backend service failure.

Measure before tuning concurrency. A burst of CI pushes competes for CPU, network, storage I/O, and auth capacity; a bigger frontend count may simply amplify backend pressure. Apply rate/connection limits at the appropriate layer and keep independent capacity headroom for recovery pulls.

## Primary sources

- [Distribution configuration](https://distribution.github.io/distribution/about/configuration/)
- [Deploy a registry](https://distribution.github.io/distribution/about/deploying/)
- [Distribution notifications](https://distribution.github.io/distribution/about/notifications/)
- [Distribution S3 storage driver](https://distribution.github.io/distribution/storage-drivers/s3/)
- [Distribution pull-through cache](https://distribution.github.io/distribution/recipes/mirror/)
