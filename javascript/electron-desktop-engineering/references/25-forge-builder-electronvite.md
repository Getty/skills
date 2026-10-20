# Electron Forge, electron-builder, electron-vite, and build ownership

**Read when:** selecting or repairing build/package tooling.

## Separate responsibilities

A bundler compiles application code; a packager assembles runtime/resources; a maker/installer step creates distribution artifacts; publishing uploads release assets; an updater consumes a compatible feed. Forge, electron-builder, and electron-vite occupy different combinations of this workflow. Inspect the existing repository and choose one clear owner for each step.

Do not run two independent packagers over each other's outputs without a documented reason. For Forge's Vite plugin, check the current plugin status/configuration and generated main/preload/renderer entry behavior. For electron-vite, verify how its outputs feed the chosen packager. For electron-builder, inspect target-specific packaging/signing/update configuration rather than assuming defaults fit every OS.

## Configuration review

Map source entries to emitted files, preload path, asset base, native externals, ASAR inclusion/unpacking, extra resources, architecture, signing, and publishing. Keep development-only origins/tools out of production. Avoid copying credential-bearing configuration into the artifact. Prefer environment/secret-provider references with CI access controls for signing/upload credentials.

Native rebuild ownership must be explicit to avoid building against the wrong runtime or rebuilding inconsistently at multiple stages. Test resource paths after packaging, not only in the bundler output directory.

## Acceptance

Build from a clean checkout with the committed lockfile. Inspect unpacked contents, then launch the packaged artifact without a development server. Exercise native addons, custom protocol, worker assets, preload bridge, and the target installer. Compare the output manifest against expected inclusions and exclusions. Document signing/publishing steps as unexecuted until actual authorized credentials and target runners have been used.

## Evidence and navigation

Primary sources (reviewed 2026-10-15 unless marked as discovery pointers):

- [E22: Electron Forge](https://www.electronforge.io/)
- [E23: Forge Vite plugin](https://www.electronforge.io/config/plugins/vite)
- [E24: electron-builder](https://www.electron.build/)
- [E25: electron-vite](https://electron-vite.org/guide/)

Procedures are original engineering recommendations. Verify API-specific changes against installed-version documentation.

[Topic index](00-index.md) · [Evidence policy](01-version-and-evidence.md) · [Source register](../SOURCES.md)
