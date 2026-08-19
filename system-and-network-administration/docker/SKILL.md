---
name: docker
description: Use when writing or debugging Dockerfiles or docker-compose — image builds, layer caching, multi-stage, service wiring, or a stack that starts in the wrong order or cannot reach a service.
user-invocable: true
---

# Docker & Compose Reference

One skill for both: images are built with Docker, run together with Compose —
they ship as one workflow. This covers the decisions and traps, not the
basics.

## CLI generation

`docker compose` (v2, a docker plugin) is current; the standalone
`docker-compose` binary is the legacy v1 — scripts should call
`docker compose`. The top-level `version:` key in compose files is obsolete
and ignored; new files start directly with `services:`. The default project
name (container/network/volume prefix) is the directory name — override with
`name:` at the top level or `-p` when two checkouts of the same stack must
coexist.

## Dockerfile — the rules that pay rent

- **Order layers by change frequency.** Dependency manifests first
  (`COPY package.json .` → install → `COPY . .`), source last — otherwise
  every source edit invalidates the dependency layer and rebuilds the world.
- **Multi-stage** for anything compiled: build stage with toolchain,
  `COPY --from=build` into a slim runtime stage. The runtime image carries no
  compilers, no dev deps.
- **One `RUN` per logical step, cleanup in the same layer** —
  `apt-get update && apt-get install -y … && rm -rf /var/lib/apt/lists/*`
  in one command; a later `RUN rm` does not shrink earlier layers.
- **`USER` non-root** in the final stage; **`HEALTHCHECK`** if compose or an
  orchestrator should gate on readiness.
- `.dockerignore` is not optional: without it `.git`, local `node_modules`,
  and secrets ride into the build context (and bust the cache).
- `CMD ["exec", "form"]` — shell form wraps PID 1 in `/bin/sh`, which
  swallows SIGTERM and turns every stop into the 10 s kill timeout.
- `ARG` is build-time, `ENV` is runtime; an `ARG` value referenced in `ENV`
  is baked into the image — never route secrets through either (use
  `--mount=type=secret` / runtime env).

## Compose — service wiring

- **Startup order needs conditions, not just names.** Bare
  `depends_on: [db]` only orders *creation*. For "wait until ready":

  ```yaml
  services:
    app:
      depends_on:
        db:
          condition: service_healthy
    db:
      image: postgres:17
      healthcheck:
        test: ["CMD-SHELL", "pg_isready -U $${POSTGRES_USER}"]
        interval: 5s
        retries: 10
  ```

- **Services reach each other by service name** on the default network, at
  the *container* port — `ports:` is only for host access. `localhost`
  inside a container is the container itself; that's the classic
  "connection refused" in app→db URLs.
- **Named volumes vs bind mounts:** named volumes for data that belongs to
  the stack (declared under top-level `volumes:`, survive `down`, die with
  `down -v`); bind mounts for source code in dev. First-use of a named
  volume copies the image's existing content into it — later image changes
  to that path are shadowed by the volume.
- **Env precedence:** shell env > `--env-file`/`.env` > `environment:` >
  `env_file:` > image `ENV`. `.env` is read by *compose itself* for
  `${interpolation}` in the YAML; `env_file:` feeds the *container* — they
  are different mechanisms. `$$` escapes a literal `$` in YAML values.
- **Override files:** `compose.yaml` + `compose.override.yaml` merge
  automatically (the standard dev/prod split); explicit stacking with
  `-f base.yaml -f prod.yaml`. **`profiles:`** gate optional services
  (`--profile debug` / `COMPOSE_PROFILES`) — a service with a profile simply
  doesn't exist otherwise, also not as a `depends_on` target.
- `restart: unless-stopped` for long-running business stacks; `on-failure`
  for one-shot jobs.

## Debug ladder

`docker compose ps` (state + health) → `logs -f <svc>` → `exec <svc> sh`
(inspect from inside; test DNS with `getent hosts <other-svc>`) →
`docker inspect <ctr>` (mounts, env, health log, exit code) →
`docker compose config` (the *merged, interpolated* YAML — the truth after
overrides and `.env`). Exit 137 = OOM-kill or SIGKILL timeout; check
memory limits before blaming the app. `compose up -d --build` rebuilds on
run; `--force-recreate` when only env/config changed but containers must
pick it up.

## Related

- `kubernetes-concepts` — when a stack outgrows one host, this is the next
  rung; compose services map to Deployments+Services conceptually.
