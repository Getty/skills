# 22 — Small, Secure Production Deployments

## Minimal architecture

```text
Client / agent
    → private access or authenticating gateway
        → bounded queue / quota / request limits
            → vLLM on loopback or a private service network
                → local, controlled model/cache storage
        ↘ internal metrics / limited tracing
```

Docker, systemd, or an existing small cluster can support this design.
A single GPU does not require Kubernetes. vLLM provides inference; tenant
management, product quotas, billing, and tool permissions are separate
responsibilities. Explicitly inventory network and API surfaces.
[S17, S27, S32](28-sources.md)

## Model/image supply chain

Pin versions and image digests; use revision-pinned weights and trusted
artifacts. Do not reflexively enable `trust_remote_code`: required third-party
code is executable code and must be reviewed. Avoid running as root where
possible; mount only what is needed; do not put cloud credentials in the
container or expose the Docker socket. Protect storage, log, and profiling
directories with access controls. [S27](28-sources.md)

Containers need appropriately exposed GPU devices and sufficient shared memory.
`--ipc=host` is a common example but shares a broader isolation boundary;
evaluate an explicitly sized `--shm-size` path where the specific stack
supports it. Do not offer `--privileged` as a general installation fix.
[S32](28-sources.md)

## Authentication and public surface

An API key does not automatically protect every administrative, health,
metrics, or internal endpoint. Do not expose worker/Ray/communication ports
publicly. Use positive API allowlists at the gateway and exclude management
functions: profiling, cache reset, dynamic adapters, sleep/wake, and other
administrative operations. Add network policies/firewalls. [S27](28-sources.md)

`configs/nginx-vllm.conf` deliberately binds **only to 127.0.0.1:8080**, without
promising public TLS or tenant authentication. It is a local SSE diagnostic/
proxy template, not a complete internet gateway. For remote use, deploy an
authenticated private tunnel or an explicitly hardened gateway. Do not simply
replace the address with `0.0.0.0` and call that production security.

## SSE, timeouts, and cancellation

Disable proxy buffering/caching for streams; configure the upstream connection
and HTTP version appropriately. A read timeout is often an inactivity limit,
not total request duration; also enforce an end-to-end deadline in the client
or gateway. Test socket keepalive/heartbeats, idle timeouts, and load-balancer
behavior on the real path. Compression or intermediate proxies can change
flushing behavior.

When a client disconnects, cancel the upstream and observe whether the running
request/KV disappear on the server. Avoid endless retries; use bounded attempts
with jitter and load/error classification. Non-idempotent tool actions require
a separate operation protocol supporting deduplication. [S17](28-sources.md)

## Resource limits and data

Bound input bytes, tokenized context length, output budgets, active requests,
and queue age, plus multimodal sizes, logprob volume, schema complexity,
and file access. Interpret token limits after actual template/tokenizer
processing. Native context limits do not replace HTTP-upload byte limits.

Prompts, media, responses, KV, and profiles can contain confidential data.
Default logs should omit request bodies; use bounded retention and controlled
debug access. KV offload stores potentially sensitive derived states and needs
its own deletion/access rules. A cache salt is not an authentication system
or encryption. [S06–S07, S27](28-sources.md)

## Readiness, draining, restart

Process started ≠ model loaded ≠ graph warmup complete ≠ representative request
works. Supplement health/readiness with a bounded synthetic request without
flooding the service with aggressive probes. During shutdown, reject or reroute
new requests, drain existing ones for a bounded interval, and cancel cleanly
after the deadline.

Monitor log rotation, free disk space, host RAM, GPU errors, restart count,
queues, and SLOs. Do not restart indefinitely after OOM and conceal a costly
cold-start loop. Keep the last working revision and configuration locally
available. See the [upgrade checklist](../templates/upgrade-checklist.md).
