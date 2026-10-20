# Native addons, ABI compatibility, and packaged binaries

**Read when:** using SQLite, keychain modules, codecs, device libraries, or other native code.

## Inventory native dependencies

Record each direct/transitive native addon, supported Electron/runtime versions, OS/architecture targets, prebuild availability, build toolchain, license, and dynamic-library dependencies. Electron's embedded runtime can require modules built specifically for Electron rather than the host Node ABI. Node-API may reduce some ABI coupling, but do not treat it as proof of all Electron/platform compatibility.

Use the selected packager's documented rebuild flow and avoid contradictory independent rebuild commands. Verify which architecture is actually targeted, especially on cross-build hosts and universal macOS packaging. A successful `require()` in the build host's Node process is not an Electron runtime test.

## Packaging contract

Native binaries and helper executables may need unpacked paths outside ASAR. Resolve them through packaged resource locations, preserve required permissions, and include dependent libraries. Inspect the final artifact rather than assuming a glob captured every generated file. Sign relevant nested binaries before the final application signature as required by the target.

Treat prebuilt downloads as supply-chain artifacts: verify provenance, checksums/signatures where available, and exact version selection. Network access during install/build affects reproducibility and offline support. Avoid silently compiling against whichever local library happens to be installed.

## Acceptance

Launch and exercise the native feature on every supported OS/architecture in the packaged artifact. Test cold load, concurrency, shutdown, error paths, and upgrade. Check for missing shared libraries, architecture mismatch, incorrect ASAR placement, and permissions after installation. Keep a fallback or explicit unsupported-target message. Document actual tests separately from source review and from a successful JavaScript bundle build.

## Evidence and navigation

Primary sources (reviewed 2026-10-15 unless marked as discovery pointers):

- [E16: Native Node modules](https://www.electronjs.org/docs/latest/tutorial/using-native-node-modules)
- [E17: ASAR archives](https://www.electronjs.org/docs/latest/tutorial/asar-archives)
- [E22: Electron Forge](https://www.electronforge.io/)
- [E24: electron-builder](https://www.electron.build/)

Procedures are original engineering recommendations. Verify API-specific changes against installed-version documentation.

[Topic index](00-index.md) · [Evidence policy](01-version-and-evidence.md) · [Source register](../SOURCES.md)
