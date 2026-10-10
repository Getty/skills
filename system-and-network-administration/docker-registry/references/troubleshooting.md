# Registry troubleshooting by failing actor and protocol phase

> Read when: a push/pull fails, cache seems bypassed, or the registry returns confusing responses.

Identify the actor first: developer Engine, remote BuildKit, Kubernetes node runtime, in-pod build tool, or direct HTTP client. Capture exact image reference/digest, timestamp, endpoint, server/client versions, auth identity scope, and the failing phase. Redact credentials and presigned URLs.

| Symptom | Distinguish first |
|---|---|
| `x509` failure | Wrong hostname/chain/CA store; token/blob host versus registry host |
| HTTP/HTTPS mismatch | Actual scheme and per-client insecure policy |
| 401 | Expected auth challenge versus failed credentials/token exchange |
| 403 / denied | Scope/repository policy versus proxy/WAF policy |
| 404 / manifest unknown | Wrong repository/tag, media type, auth masking, incomplete copy |
| Pull succeeds but no mirror logs | Node cache, upstream fallback, wrong daemon/builder |
| Small push works, large push fails | Proxy limit/timeout/buffering, upload Location, backend capacity |
| Blob unknown / digest mismatch | Incomplete publication, corrupt storage, unsafe GC, client content verification |
| One architecture fails | Missing index child, incompatible platform selection |
| Disk remains large after delete | Shared/reachable blobs, no GC, backend versioning, aborted uploads |

## Read-only ladder

Probe `/v2/` without following redirects automatically. Read an authorized known manifest with a broad supported Accept set. Verify its digest/type, then referenced content access. Compare registry logs, token service, proxy, and storage around the same request. Use a fresh isolated client for cache-path tests.

The included `scripts/registry_probe.py` checks API and optional manifest headers without modifying anything or accepting credentials. It reports expected 401 challenges separately; it does not claim that authentication, upload, or blob integrity has been proven.

## Escalation discipline

Do not solve unknown TLS failures with permanent verification bypass, unknown storage errors with manual file deletion, or mirror routing problems with a global cluster restart. State a hypothesis, choose a narrow reversible test, record the result, and only then change configuration. Preserve failing artifacts and logs before cleanup.

## Primary sources

- [Distribution HTTP API V2](https://distribution.github.io/distribution/spec/api/)
- [Registry token authentication](https://distribution.github.io/distribution/spec/auth/token/)
- [containerd registry hosts configuration](https://raw.githubusercontent.com/containerd/containerd/main/docs/hosts.md)
- [Distribution S3 storage driver](https://distribution.github.io/distribution/storage-drivers/s3/)
- [Distribution garbage collection](https://distribution.github.io/distribution/about/garbage-collection/)
- [Docker registry certificate trust](https://docs.docker.com/engine/security/certificates/)
