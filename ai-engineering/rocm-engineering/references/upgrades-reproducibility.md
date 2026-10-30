# Releases, upgrades and reproducible environments

Evidence baseline: checked 2026-10-30. The current AMD production documentation identifies ROCm Core SDK 10.1.0. Refresh this baseline before a new deployment; retain historical documentation for maintained older stacks.

## Contents

- [Recognize the release streams](#recognize-the-release-streams)
- [Account for TheRock packaging changes](#account-for-therock-packaging-changes)
- [Capture a reproducible manifest](#capture-a-reproducible-manifest)
- [Perform a staged upgrade](#perform-a-staged-upgrade)
- [Control compiled caches and extensions](#control-compiled-caches-and-extensions)
- [Restore and maintain](#restore-and-maintain)

## Recognize the release streams

Distinguish an AMD production release, a framework's upstream release, development/nightly artifacts, distribution-maintained packages and local source builds. A numerically larger package version does not establish that it belongs in the current environment.

Use the [release notes](https://rocm.docs.amd.com/en/latest/about/release-notes.html) to identify breaking changes and known issues that touch the workload. Use the [driver matrix](https://instinct.docs.amd.com/projects/amdgpu-docs/en/latest/compatibility/compatibility-matrix.html) for the host-driver pair. Drivers, SDK components, frameworks and firmware have separate version identities; record each.

Make an upgrade solve a concrete problem: a needed GPU target, a security/bug fix, an operator, a measured improvement, or an application's supported dependency range. Record the reason and the acceptance criterion before changing anything. Avoid combining a new kernel, driver, SDK, Python, framework, model revision and quantization format in one opaque transaction.

## Account for TheRock packaging changes

AMD's [transition guide](https://rocm.docs.amd.com/en/docs-10.1.0/about/transition-guide-TheRock.html) identifies Core SDK 7.14.0 as the first production TheRock-based release. In the 10.1.0 layout, core packages use the `amdrocm-` prefix and `/opt/rocm/core-10.1`; extras use `/opt/rocm/extras-10`. Package-manager installations provide compatibility symlinks through alternatives, while tarballs require explicit path/dependency handling. Package names are consolidated; legacy one-library package assumptions can fail. GPU-specific DEB/RPM suffixes and tarball family names are not always identical.

Use that guide as a mapping source rather than inventing package names from a GPU's `gfx` string. Inspect the chosen package's actual files and dependencies before updating build scripts or container layers. A script looking for `/opt/rocm-<version>` can fail even when the new SDK is installed correctly.

For migration work, inspect these classes of assumptions:

- Hardcoded SDK directories, library names and package names.
- CMake discovery variables, compiler wrappers and environment modules.
- Runtime library paths in service definitions and image entrypoints.
- Packaging rules that copy only selected `.so` files.
- Architecture filters used for wheels and custom extensions.
- Profiler command names, formats and database/schema consumers.

Use one coherent prefix per build/run environment. A compatibility symlink helps old paths resolve; it does not prove that all old build assumptions or ABIs remain valid.

## Capture a reproducible manifest

Record enough to recreate the environment without collecting secrets:

```yaml
captured_at: YYYY-MM-DD
purpose: representative workload and acceptance target
hardware:
  sku: exact observed model
  gpu_targets: [observed-gfx-target]
  logical_devices: observed count and partition layout
host:
  os: distribution and point release
  kernel: running release
  driver: running version and package source
  firmware: applicable OEM bundle or unknown
userspace:
  rocm_stream: production, legacy, nightly, distro, or source
  rocm_release: exact selected release
  install_prefix: resolved directory
  artifacts: package versions, hashes, or image digests
application:
  revision: immutable source or image revision
  python: version and environment path
  framework: exact build and source
  extensions: revisions, compiler and GPU targets
  model: immutable model/tokenizer revision
  precision: weights, activations, cache and accumulation
validation:
  correctness: test and result
  performance: workload parameters and measurements
  recovery: tested rollback or restart procedure
```

Treat this as a schema to fill with observations, not values to paste literally into a deployment report. Add only relevant environment variables and record their purpose. Do not capture all process environment variables, credential files or unrelated host configuration.

Retain package manifests, exact wheels or their verified acquisition recipe, base-image digests and build inputs. A `pip freeze` listing alone does not preserve wheel origin, GPU architecture coverage or the host driver. A local image tag alone does not preserve its immutable identity.

## Perform a staged upgrade

1. **Define success.** Choose a short representative correctness test, the workload sizes, precision, concurrency, performance envelope and restart behavior.
2. **Capture baseline.** Run the same measurements on the current environment. Separate cold startup/compilation from steady state.
3. **Resolve compatibility.** Verify the new tuple, release notes, framework build and required custom kernels. Include component deprecations and known issues.
4. **Prepare recovery.** Keep the old image/environment and bootable kernel where applicable. Record exact package reversal or snapshot restoration.
5. **Create the candidate.** Prefer a separate image, virtual environment or SDK prefix. Preview system package transactions before applying them.
6. **Test one unit.** Use one GPU/process first, then the intended topology and realistic load.
7. **Compare results.** Require numerical acceptance before a speed claim. Investigate large latency/memory changes with the same configuration.
8. **Roll out gradually.** Drain relevant workers, preserve checkpoints, monitor the candidate and retain a fast rollback route.

Do not require a host reboot for a pure isolated Python environment change. Do not omit a required reboot after replacing the active driver. State exactly which boundary changes and which running services are affected.

## Control compiled caches and extensions

Kernel and extension caches can depend on framework, compiler, target ISA and build settings. Preserve the original cache and use a new scoped directory when testing an upgrade; avoid deleting unrelated caches just to see whether the problem disappears.

Rebuild custom extensions when the relevant compiler/framework ABI or target set changes. Verify which build tool and headers were used. A cached extension that imports can still contain incompatible code objects or incorrect assumptions about the selected backend.

For performance comparisons, label:

- **Cold:** first model load and any compilation/autotuning.
- **Warm:** cache populated and inputs stabilized.
- **Sustained:** enough workload to reveal power, thermal, allocation and cleanup behavior.

Keep model versions, prompts/data, shape distribution and random-seed handling fixed where appropriate. A framework upgrade that selects a different kernel or precision policy can change accuracy and memory as well as speed.

## Restore and maintain

Rollback the smallest changed boundary first. Restore the prior application image or environment if the driver remains compatible. If the host changed, restore its documented driver/kernel configuration and reboot as needed. Re-run the baseline acceptance test; an import succeeding is not sufficient evidence of restoration.

Keep an explicit maintenance note for experiments: why a workaround exists, the exact affected tuple, its source, how to remove it and the condition that would trigger retesting. Do not let debug flags, gfx overrides, unconfined container settings or forced attention backends become unexplained permanent configuration.

Review the support matrix and relevant release notes when hardware, OS/kernel, driver, framework or workload requirements change. Refresh links and recorded access dates when using this skill for a new decision. Preserve the distinction between “documented by the vendor,” “measured on this system,” and “not yet verified.”
