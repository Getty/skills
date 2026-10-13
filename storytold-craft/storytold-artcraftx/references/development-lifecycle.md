# Development startup is not production automation

**Read when:** starting a local development copy or diagnosing reload behavior.

The repository documents a Node/npm, Rust and Tauri development environment and a Unix launcher at `./script/unix_dev.sh`. Read the current manifests/setup instructions for required versions rather than carrying a stale global toolchain pin into every installation.

The launcher selects an available loopback development port starting around the documented Vite default range; `ARTCRAFTX_DEV_PORT` can request a specific port. This serves the frontend/HMR workflow. It is not a generation REST endpoint, and port availability does not prove native IPC or backend authentication is ready.

Frontend changes can hot reload while native Rust changes require a restart. Such a restart can discard in-memory state. Do not use development reload behavior as a persistence guarantee for long-running or paid jobs. Record external job identity before restarting when the actual implementation provides it.

The development launcher owns the processes it starts; do not kill unrelated processes occupying a desired port. Stop the relevant dev session intentionally. Build/install/restart actions are distinct from ordinary read-only inspection and should be authorized in the user's environment.

For integration testing, separate frontend compilation, native startup, IPC dispatch, authenticated backend calls and result retrieval. Passing the first two does not establish the last three. The bundled evaluation cases check whether an agent preserves these distinctions; they are not claims that the application was run here.

## Evidence

- [artcraftx-readme](https://github.com/storytold/artcraftx/blob/main/README.md)
- [artcraftx-ipc](https://github.com/storytold/artcraftx/blob/98c2a48940aa0a54604637f665ee539c122fa707/crates/artcraftx/src/lib.rs)
