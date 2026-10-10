# Docker Engine and BuildKit registry clients

> Read when: Docker or a build worker ignores mirror/auth/TLS settings.

Docker Engine's `registry-mirrors` configuration is primarily the Docker Hub mirror mechanism, not a universal rewrite of every arbitrary registry. Set it on the daemon that performs the pull. Preserve existing daemon settings, validate the updated configuration, and apply reload/restart according to the option and installed release.

```json
{
  "registry-mirrors": ["https://hub-cache.example.com"]
}
```

This is a fragment for an existing configuration, not an instruction to overwrite `daemon.json`. An explicitly named private registry is still addressed by that authority. `docker login registry.example.com` credentials and daemon CA trust solve different parts of the connection.

## Separate builders

A `docker-container` or remote BuildKit builder can have its own mirror and CA configuration. Updating the host Engine may not affect base-image pulls performed inside that worker. Inspect the builder driver/endpoint and apply its supported registry configuration. CLI login credentials can be forwarded through build sessions, but that does not install a CA or change worker DNS.

## Diagnostic split

Compare normal `docker pull` with a build that fetches the same base image. If one succeeds and the other fails, inspect worker-side DNS, proxy settings, trust, credential/session flow, and mirror policy. Do not add `insecure-registries` blindly when the actual failure is in a separate builder.

Test cold and warm pulls, an approved private image, a rejected unauthorized image, and upstream failure. Record the actual authority and digest. Engine API `X-Registry-Auth` and build `X-Registry-Config` are client-to-daemon headers; they are not registry configuration keys or direct bearer-token challenge responses.

## Primary sources

- [Docker Hub mirror configuration](https://docs.docker.com/docker-hub/image-library/mirror/)
- [Docker daemon configuration](https://docs.docker.com/engine/daemon/)
- [Docker registry certificate trust](https://docs.docker.com/engine/security/certificates/)
- [Multi-platform build and image structure](https://docs.docker.com/build/building/multi-platform/)
- [Engine-specific registry auth header](https://raw.githubusercontent.com/moby/moby/v28.5.2/api/types/registry/authconfig.go)
