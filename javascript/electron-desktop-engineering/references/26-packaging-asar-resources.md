# ASAR, resources, filesystem layout, and packaging boundaries

**Read when:** packaging assets/native files or diagnosing production-only path failures.

## ASAR is a packaging format

ASAR can group application files, but it is not encryption and not by itself a strong integrity/authorization boundary. Native modules, helper executables, and APIs needing real filesystem paths can require unpacked resources. Read the selected Electron/packager behavior instead of assuming every filesystem operation treats an archive exactly like a directory.

## Resource map

Classify application code, immutable UI assets, native binaries, templates, user data, cache, logs, and secrets. Only application-controlled immutable resources belong in the trusted code/asset path. User documents must not become loadable scripts merely because they share a directory. Resolve resources relative to packaged locations, not cwd.

Define inclusion/exclusion patterns and inspect the final archive/unpacked tree. Exclude source secrets, private test fixtures, unnecessary maps, and accidental development files. Preserve licenses/notices and required native dependencies. Check path case sensitivity and Unicode on all claimed platforms.

## Integrity and modification

ASAR integrity verification and related fuses can strengthen packaging when correctly configured on supported targets, but unpacked content and other resources need their own review. Apply fuse changes and all code/resource transformations before final signing. Post-sign modifications can invalidate the release's trust properties.

## Acceptance

Open the packaged app from a different working directory and an installation path with spaces. Test native modules, worker files, icons, templates, and external helpers. Verify missing files fail with useful sanitized diagnostics. Attempt an application-asset request for an unlisted user file and ensure it is denied. Record actual archive integrity/fuse/signature checks rather than claiming them from a configuration flag alone.

## Evidence and navigation

Primary sources (reviewed 2026-10-15 unless marked as discovery pointers):

- [E17: ASAR archives](https://www.electronjs.org/docs/latest/tutorial/asar-archives)
- [E35: ASAR integrity](https://www.electronjs.org/docs/latest/tutorial/asar-integrity)
- [E16: Native Node modules](https://www.electronjs.org/docs/latest/tutorial/using-native-node-modules)

Procedures are original engineering recommendations. Verify API-specific changes against installed-version documentation.

[Topic index](00-index.md) · [Evidence policy](01-version-and-evidence.md) · [Source register](../SOURCES.md)
