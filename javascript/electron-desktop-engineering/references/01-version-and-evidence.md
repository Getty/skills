# Version support, project intake, and evidence discipline

**Read when:** starting any Electron task, upgrading, or resolving contradictory guidance.

## Inventory the shipped runtime

Record the resolved Electron version, its bundled Chromium and Node versions, host/build Node version, OS/architecture targets, packager, updater, native modules, renderer framework, module format, signing channel, and distribution format. The build host's Node version is not the application's embedded Node version. Inspect package.json, lockfiles, Forge/builder/Vite configuration, preload entry points, and the actual packaged file layout.

Electron documents support for its latest three stable major release lines, with current maintenance releases within those lines. Refresh the release dashboard and support timeline when working. The retrieved dashboard did not provide a dependable exact stable major, so this skill deliberately does **not** assert a latest Electron version. Select a supported patched runtime only after current verification and compatibility tests.

## Evidence policy

Prefer installed declarations and runtime observations, version-specific API docs, official breaking-change/release/security notes, and reproducible tests. Distinguish development, unpackaged runtime, packaged unsigned, packaged signed, and installed-update tests. A BrowserWindow opening under a development server proves none of the later states.

Use `observed`, `source-reviewed`, `inferred`, and `unverified`. Record exact command, OS, architecture, runtime, artifact, exit status, and scope. Syntax checks and pure policy tests do not prove a Chromium sandbox or operating-system permission boundary. The supplied example is not a penetration-tested production shell.

## Stop conditions

Do not silently disable sandboxing, context isolation, certificate validation, signing checks, or update verification to resolve a build/test failure. Keep secure production fuses separate from a test launcher that requires different settings. Treat unsupported OS targets, unverified native ABI compatibility, and unknown update/signing behavior as explicit release blockers for that target while continuing other work.

## Evidence and navigation

Primary sources (reviewed 2026-10-15 unless marked as discovery pointers):

- [E02: Electron support timelines](https://www.electronjs.org/docs/latest/tutorial/electron-timelines)
- [E03: Electron release dashboard](https://releases.electronjs.org/) — discovery pointer; not substantively verified
- [E04: Electron process model](https://www.electronjs.org/docs/latest/tutorial/process-model)
- [E08: ES modules](https://www.electronjs.org/docs/latest/tutorial/esm)
- [S01: Agent Skills specification](https://agentskills.io/specification)

Procedures are original engineering recommendations. Verify API-specific changes against installed-version documentation.

[Topic index](00-index.md) · [Evidence policy](01-version-and-evidence.md) · [Source register](../SOURCES.md)
