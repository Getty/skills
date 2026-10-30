# Native Linux installation and validation

Evidence baseline: 2026-10-30, ROCm Core SDK 10.1.0. This is a workflow for producing a host-specific installation plan. Resolve repository URLs, package versions and hardware selectors from the chosen release before executing mutations. Use [windows-wsl.md](windows-wsl.md) for WSL; its driver path differs.

## Contents

- [Choose the installation boundary](#choose-the-installation-boundary)
- [Inventory before changing packages](#inventory-before-changing-packages)
- [Select and validate the driver](#select-and-validate-the-driver)
- [Install one coherent userspace](#install-one-coherent-userspace)
- [Configure access and discovery](#configure-access-and-discovery)
- [Verify from the bottom up](#verify-from-the-bottom-up)
- [Recover a failed installation](#recover-a-failed-installation)

## Choose the installation boundary

| Need | Practical route | Host requirement |
| --- | --- | --- |
| Run a validated ML application | A versioned framework container | Compatible loaded GPU driver and device access |
| Develop HIP or use system libraries | Distribution package manager | Compatible driver plus selected runtime/development packages |
| HPC modules, multiple SDKs or no root access | A release tarball in an isolated prefix | Administrator-provided compatible driver |
| Isolated Python workflow | The documented framework and ROCm wheel route | Compatible driver; correct Python and GPU artifact |
| Controlled offline or guided install | Release-specific runfile or staged repository | Verified prerequisites and explicit driver/userspace choice |

The [AMD installation guide](https://rocm.docs.amd.com/en/latest/install/rocm.html) provides platform-dependent instructions for these methods. Follow one selected branch. A flattened rendering can include commands for several mutually exclusive configurations; do not concatenate them.

Prefer the smallest boundary that satisfies the task. A container workload does not normally require installing the entire host SDK. Installing a development SDK is useful when compiling extensions; it does not establish that an arbitrary Python wheel uses that SDK.

## Inventory before changing packages

Capture only relevant system facts, avoiding an indiscriminate environment dump:

```bash
cat /etc/os-release
uname -r
lspci -nnk
id
ls -l /dev/kfd /dev/dri
command -v hipcc
command -v rocminfo
```

Missing commands or device nodes are observations, not grounds to install everything. In a container, distinguish the container's distribution from the host's kernel and driver. In a VM, establish whether a GPU or virtual function has actually been assigned.

On a Debian-family system, inspect relevant packages and candidates:

```bash
dpkg-query -W -f='${binary:Package}\t${Version}\n' 'amdrocm*' 'rocm*' 'hip*' 'amdgpu*'
apt-cache policy amdgpu-dkms
```

An unmatched package pattern may produce a nonzero exit code. Record it as absent. On RPM-family hosts, use the corresponding `rpm -qa` and repository queries. Check repository configuration for overlapping vendor, distro and legacy ROCm sources before selecting packages.

Record the existing bootable kernel and recovery route before a driver/kernel change. On a remote system, make sure recovery does not depend on the GPU driver being replaced. Preserve workload configuration and model/checkpoint directories independently from package operations.

## Select and validate the driver

Separate the running kernel driver from ROCm userspace. The [driver compatibility matrix](https://instinct.docs.amd.com/projects/amdgpu-docs/en/latest/compatibility/compatibility-matrix.html) permits specific cross-version combinations; equal release numbers are not required. Select a documented combination for the exact GPU and OS.

For the current selected AMD installation branches, Instinct/Radeon use the documented AMD GPU driver route, whereas supported Ryzen APU branches use the specified inbox kernel driver. Do not apply an Instinct DKMS recipe to an APU simply because both execute HIP. Follow [AMD's selected install instructions](https://rocm.docs.amd.com/en/latest/install/rocm.html) and the hardware matrix together when their prose differs in detail.

For a DKMS deployment, verify matching headers and development files for the intended kernel. AMD's [driver prerequisites](https://instinct.docs.amd.com/projects/amdgpu-docs/en/docs-31.60.0/install/detailed-install/prerequisites.html) describe this dependency. Inspect module-build errors before repeatedly reinstalling packages. A package installation can succeed while module compilation or loading fails.

After a driver change, follow its reboot requirement and re-check the running state. Use `modinfo amdgpu` to inspect the available module and relevant kernel logs to check what loaded; these answer different questions. If module-signature enforcement blocks loading, follow the distribution's supported signing/enrollment process. Do not make disabling Secure Boot a generic installation step.

## Install one coherent userspace

Resolve the current package family and layout using [upgrades-reproducibility.md](upgrades-reproducibility.md). Legacy `rocm-*` recipes and current `amdrocm-*` packages are not interchangeable. Select runtime, development or full-suite packages intentionally. Choose all required GPU targets for a heterogeneous host; architecture-specific packaging trades size for coverage.

For a package-manager plan, provide:

1. The exact vendor repository for the chosen distribution/version and release stream.
2. The signing-key source and repository-scoped key configuration.
3. Package names and exact candidate versions from live metadata.
4. A package transaction preview, including removals and driver changes.
5. The installation command and the validation/recovery steps.

For example, after setting verified values in the same shell, preview an APT transaction:

```bash
: "${ROCM_PACKAGE:?Set the verified package name}"
: "${ROCM_PACKAGE_VERSION:?Set the verified package version}"
apt-get --simulate install "${ROCM_PACKAGE}=${ROCM_PACKAGE_VERSION}"
```

Use the identical package/version pair for the authorized installation. Do not silently replace it with an unpinned meta-package when the candidate cannot be found. Explain whether repository retention requires staging the artifacts for future restoration.

For tarballs, inspect the archive layout and checksum/signature information before extracting into a new empty versioned directory. Do not extract over a working SDK. Configure an environment module or process-scoped wrapper using the actual extracted prefix. Test its binaries before making any global path change.

For wheels, create a clean virtual environment with the Python version required by the selected build. Use the framework guide's index and dependencies, record hashes where available, then run `python -m pip check`. Do not resolve a dependency conflict by installing an unrelated CPU or CUDA wheel over the intended ROCm build.

## Configure access and discovery

Inspect the ownership and mode of `/dev/kfd` and the relevant render nodes. Grant the intended account access through the documented groups or a deliberately scoped device policy. AMD documents `render` and `video` groups; a fresh session may be required to receive changed supplementary groups. Avoid making all GPU devices world-writable as a default fix.

Verify tool resolution with `command -v` and inspect the selected prefix. A global `LD_LIBRARY_PATH` containing several SDKs can create a mixed runtime. Prefer one project environment; add only required directories and preserve unrelated existing values. For a service, place the environment in its service configuration instead of relying on an interactive shell startup file.

## Verify from the bottom up

Use a short acceptance ladder:

1. **Host:** GPU appears at the expected PCI address; driver loaded; no new initialization/reset errors.
2. **Runtime:** supported device-query tool identifies the intended GPU, target and memory.
3. **Access:** the actual service user can enumerate and execute; root-only success is insufficient.
4. **Framework:** installed build identifies its HIP backend and runs a small numerical operation on the GPU.
5. **Application:** representative operators and extensions execute correctly with expected precision.
6. **Operational:** restart, bounded sustained load and resource cleanup work.

Capture expected/observed results and stop at the first failing layer. `hipcc --version` confirms compiler discovery, not GPU execution. A successful `rocminfo` query confirms discovery, not framework or model correctness. See the skill's smoke scripts for a bounded execution check.

## Recover a failed installation

Identify the last successful layer and the exact transaction. Restore the previous application environment first when the host driver remains healthy. For driver failures, use the recorded boot/recovery route and the original driver's removal/install procedure. Preview package removals; broad wildcard removal can affect graphics and unrelated applications.

Keep the broken environment's relevant logs and package manifest for comparison. Do not copy random shared libraries between SDK prefixes to make an import succeed. Re-run the same acceptance ladder after restoration and report which part of the stack is now verified.
