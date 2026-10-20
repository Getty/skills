# Release pipeline, supply chain, provenance, and CI

**Read when:** automating packaging/publishing or reviewing release risk.

## Reproducible pipeline inputs

Commit the correct lockfile and pin the build environment through the repository's established mechanism. Record Electron, embedded runtime, package-manager, bundler, native compiler, packager, and signing-tool versions. Separate dependency installation, compilation, tests, packaging, signing, publishing, and release promotion into auditable stages.

Review newly introduced install/build scripts and downloaded prebuilt binaries. Untrusted forks/pull requests must not receive signing or publication credentials. Keep artifact upload destinations constrained and use least-privilege credentials. A successful package-manager audit is not comprehensive supply-chain verification.

## Artifact controls

Generate a file/dependency inventory and retain checksums, license notices, source revision, test results, and platform verification records. Inspect for secrets, development server references, debug ports, incorrect fuses, and accidentally included files. Sign only artifacts produced by the intended workflow after required review gates.

Use separate candidate and production channels. Promote the already-verified artifact rather than rebuilding subtly different bytes after approval, where the tooling permits that workflow. Keep release metadata and binaries consistent and test that consumers receive the intended version.

## Acceptance

Perform a clean build on each required target runner, launch packaged artifacts, validate signatures/fuses, and run update tests from the previous installed release. Simulate failed signing, failed upload, partial publication, and revoked credentials. Define who can pause rollout and how incident evidence is retained. Do not call a pipeline reproducible merely because it has a YAML file; state which outputs and external dependencies were actually reproduced or verified.

## Evidence and navigation

Primary sources (reviewed 2026-10-15 unless marked as discovery pointers):

- [E22: Electron Forge](https://www.electronforge.io/)
- [E24: electron-builder](https://www.electron.build/)
- [E19: Code signing](https://www.electronjs.org/docs/latest/tutorial/code-signing)
- [E12: Fuses](https://www.electronjs.org/docs/latest/tutorial/fuses)
- [E02: Electron support timelines](https://www.electronjs.org/docs/latest/tutorial/electron-timelines)

Procedures are original engineering recommendations. Verify API-specific changes against installed-version documentation.

[Topic index](00-index.md) · [Evidence policy](01-version-and-evidence.md) · [Source register](../SOURCES.md)
