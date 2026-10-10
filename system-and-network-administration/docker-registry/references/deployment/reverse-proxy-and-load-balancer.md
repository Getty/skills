# Reverse proxies, load balancers, and upload correctness

> Read when: placing a registry behind ingress/TLS termination or scaling frontends.

A registry reverse proxy must support large, long-lived uploads and preserve the advertised scheme/host and Location semantics. A green `/v2/` check exercises almost none of the upload path. Validate methods, request-body limits/buffering, transfer timeouts, Authorization forwarding, and blob redirects.

Terminate TLS in one deliberately designed layer and ensure upstream/forwarded scheme is accurate. Keep the backend private when TLS terminates at the proxy. The externally visible registry hostname and token-service audience must remain consistent with image references.

## Load balancing

Multiple registry replicas need a supported shared storage backend, consistent configuration/auth policy, and the same configured HTTP secret where upload-state signing requires it. Without the shared secret, an upload resumed on another replica can fail even though ordinary pulls work. Sticky sessions can mask a broken design rather than fixing it.

Health checks should distinguish liveness, API response, storage reachability, and authorized manifest access. Do not configure a load balancer to mark a deliberately authenticated `/v2/` response unhealthy solely because it is 401. Conversely, do not accept every 401 from any proxy as proof that the registry backend works.

## Failure tests

Start an upload, route subsequent requests to a different replica, drain/restart one instance, and finish the upload. Test object-store redirects from outside the registry network. Confirm error status/body survives the proxy and that access logs redact tokens and presigned URLs.

Tune timeouts from representative layer sizes and bandwidth rather than copying web-application defaults. Set explicit rate/connection limits so a large CI wave cannot exhaust the proxy's buffers or file descriptors. Record whether buffering stores image bytes on proxy disk and include that disk in capacity monitoring.

## Primary sources

- [Distribution reverse-proxy recipe](https://distribution.github.io/distribution/recipes/nginx/)
- [Distribution configuration](https://distribution.github.io/distribution/about/configuration/)
- [Deploy a registry](https://distribution.github.io/distribution/about/deploying/)
- [Distribution S3 storage driver](https://distribution.github.io/distribution/storage-drivers/s3/)
