# Supervision, systemd and containers

This chapter describes deployment templates in this package, not a vendor-supported production configuration. Gearmand option evidence: [G4, G9–G11](sources.md). Inspect the exact binary's help before using a template.

## Service manager contract

Run gearmand in the foreground under the supervisor. Do not combine daemonization with a supervisor expecting the foreground process. Separate server and worker units so they have independent identities, limits, logs and restart policy. Bind only to intended interfaces; create the required user and state directories deliberately.

The example server unit uses a local SQLite queue and a persistent state directory. It is a single-owner example, not a highly available database design. The worker unit uses the bundled Python demonstration. Both require adaptation of paths, installed packages, function names and local security policy. Enabling or restarting a unit is an operational mutation; this skill does not perform it automatically.

Graceful worker stop means stop acquiring work, finish the current bounded assignment, then exit. Give the service manager a sufficient termination window; after the window, forced termination can cause redelivery or uncertain effects. A signal flag alone cannot stop an unbounded external call. Distinguish worker-drain procedures from server shutdown procedures.

## Container contract

The Dockerfile installs the distribution's packaged gearmand. It does **not** promise that Debian's package equals the 2.1 source-review baseline. Capture the built package version and feature set; choose an explicit source build or package pin when 2.1 behavior is required. Resolve and pin image digests and package versions after your own validation, rather than inventing a digest here.

The Compose sample keeps the published native listener on host loopback, uses a private service network and a persistent queue volume. The worker consumes the common JSON function. It has no external durable result store unless configured; a persisted server queue is not that store. The image includes the diagnostic scripts but starts no jobs during build.

Do not put secrets into image layers, command-line arguments or committed Compose files. Use a read-only root filesystem where supported, explicit writable volumes, a non-root identity and measured memory/CPU limits. Do not mistake a container restart policy for recovery of in-memory queue state.

## Verification before deployment

Build in a controlled environment; record image/package metadata; run ECHO and an end-to-end job; test signal handling, writable-directory restrictions, backend persistence/replay, network isolation and TLS boundary. Confirm that the health check is bounded and non-mutating. Run worker kill/retry and unknown-outcome tests before relying on automatic restarts.

Deployment API background: [O1–O3 and verification caveats](sources.md).
