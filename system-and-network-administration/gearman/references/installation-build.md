# Installation, builds, and reproducibility

Read when setting up a machine, image, CI build, or development environment. Evidence: [G4, G8, G13, S4](sources.md). Commands below are procedures, not a promise that every distribution offers identical packages.

## Package installation path

On Debian-family systems first inspect package metadata for `gearman-job-server`, `gearman-tools`, and `libgearman-dev`. Select only the roles needed: daemon, CLI tooling, development headers, and the language binding are separate concerns. Obtain change approval before installing or enabling services. Package installation can auto-start a daemon; establish binding/firewall policy before exposing it.

After installation capture `command -v gearmand`, `gearmand --version`, `gearmand --help`, `gearman -H`, and `gearadmin --help`. Check package service units with the service manager rather than guessing their names. Verify supported queue plugins from this exact executable; a database installed on the host does not make a missing Gearman plugin appear.

## Source build path

Select a tagged release, record its resolved commit, verify the release archive against an independently obtained expected hash/signature, and retain the original archive. Generated release tarballs and GitHub source snapshots can differ: the latter may require bootstrapping Autotools files. Follow that tag's README/build instructions; do not invent configure switches from an older article.

Install a compiler, build tools and the detected dependencies for libevent, UUID support, Boost components, and chosen storage backends. For native TLS explicitly examine the `--enable-ssl` path and the configure result. Inspect `./configure --help`, configure output, and the generated feature summary. Build with a bounded job count appropriate to the machine, run upstream tests, and use staged packaging rather than overwriting an existing production installation.

A reproducible record contains archive hash, compiler, libc, dependency package versions, configure invocation, compile/test logs, install prefix, linked libraries, image digest, and failed/skipped tests. Copy runtime shared libraries and CA material into the final image deliberately. A successful C link does not prove the runtime loader finds the intended libgearman.

## Platform boundaries

Treat Linux as the reference deployment environment for these assets. On Windows, prefer an isolated Linux VM, WSL environment, or Linux container runtime for the daemon unless a specific native distribution is independently verified. A Windows client can connect over the protocol without the daemon being native. macOS packaging and SSL/backend capabilities also require inspection.

## Safe first start

Start an isolated foreground daemon on loopback and a non-production port. Confirm the actual listening socket; perform binary ECHO; register a test worker under a test-only function; submit one job; check result and queue cleanup. Only then enable persistence and verify restart/replay. TLS, multi-server routing and service integration are later acceptance gates, not assumptions inherited from this initial test.

The included distribution-based Dockerfile is a **lab build**, not a pinned 2.1.0 image. See [systemd/containers](systemd-containers.md) for its explicit limitations.
