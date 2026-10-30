# Native Windows and WSL2

Evidence baseline: 2026-10-30. AMD's current Core SDK documentation is 10.1.0. Native Windows, WSL2, older HIP SDK installations and older Radeon ROCm releases must be treated as separate configurations.

## Contents

- [Choose the execution environment](#choose-the-execution-environment)
- [Understand current WSL scope](#understand-current-wsl-scope)
- [Build a native Windows workflow](#build-a-native-windows-workflow)
- [Build a WSL workflow](#build-a-wsl-workflow)
- [Diagnose the right layer](#diagnose-the-right-layer)
- [Evaluate alternative backends](#evaluate-alternative-backends)

## Choose the execution environment

| Environment | Check first | Avoid assuming |
| --- | --- | --- |
| Native Windows | Exact supported GPU, Windows release, AMD driver, SDK/framework artifact | Linux tool and collective-library parity |
| WSL2 | Windows GPU driver, WSL version, Linux guest, supported ROCm WSL route | Native Linux kernel-driver installation or full profiling support |
| Native Linux | GPU/OS/kernel/driver/framework qualification | A WSL workaround is appropriate |
| Windows application with another backend | The application's DirectML/Vulkan/OpenCL requirements | Its GPU support implies ROCm support |

Start from the [unified compatibility matrix](https://rocm.docs.amd.com/en/latest/compatibility/compatibility-matrix.html), then the exact framework's guide. A general “Windows supported” banner cannot answer whether an application with custom kernels, distributed communication and profiling will work.

For historical deployments, keep the documentation version aligned with the installed stack. Old guidance that only selected ROCm components were available on Windows describes that release; it must not be generalized indefinitely. Equally, newer Windows artifacts do not retroactively qualify an old GPU/driver combination.

## Understand current WSL scope

The [10.1.0 release notes](https://rocm.docs.amd.com/en/latest/about/release-notes.html) label the TheRock WSL2 integration a **technical preview**. It packages `librocdxg`, detects `/dev/dxg`, and targets Ubuntu DEB packages and Python wheels. That launch excludes RPM packaging and KFD-dependent profiling/debugging tooling. Keep this specific scope separate from earlier WSL release paths and their support labels. Recheck the release notes before claiming these restrictions still apply to a later release.

The host Windows driver remains part of the execution path. Installing a Linux `amdgpu-dkms` package inside WSL is not the native-Linux solution transplanted into WSL. A missing `/dev/kfd` in WSL does not by itself diagnose a broken installation; verify the expected DXG path for the chosen release.

## Build a native Windows workflow

Collect the exact OS build, installed display driver, GPU SKU and Python version. A targeted PowerShell inventory is preferable to dumping all system state:

```powershell
Get-CimInstance Win32_VideoController |
  Select-Object Name, PNPDeviceID, DriverVersion
Get-Command python -ErrorAction SilentlyContinue
python --version
```

Do not use the `AdapterRAM` field as authoritative capacity for large GPUs. Confirm memory through the supported runtime or application.

1. Select the Windows driver linked by the chosen ROCm release; consult its own [release notes](https://www.amd.com/en/resources/support-articles/release-notes/RN-RAD-ROCM-10-01.html), including supported devices and known issues.
2. Choose a native Windows artifact for the precise GPU family and framework. A Linux wheel or tarball is not portable merely because it contains HIP code.
3. Use a clean Python environment or a separate SDK prefix. Record the executable resolving `python`, the wheel index and the final package list.
4. For C++ development, use the toolchain required by that build. Inspect compiler/linker discovery and avoid mixing incompatible MSVC, MinGW, MSYS and Linux libraries.
5. Configure paths for the current process first. Persistent system-wide PATH changes can shadow another SDK or application.
6. Run a supported HIP device query and a small framework operation, then test the real custom extensions and model.

TheRock's [Windows development status](https://github.com/ROCm/TheRock/blob/main/docs/development/windows_support.md), checked on the baseline date, lists missing components including RCCL, ROCr/`rocminfo`, AMD SMI and ROCm profiling/debugging tools, while many compiler/math components build. Treat that as component-development evidence and confirm the release artifact's contents. Do not make a Linux `rocminfo` or RCCL command the mandatory acceptance test for native Windows.

For a source build, pin the repository and submodule revisions, satisfy long-path and compiler requirements, and run the project's environment validation before a large build. Building a component is not equivalent to proving the whole framework's Windows execution path.

## Build a WSL workflow

First inspect the host with Microsoft's documented [WSL commands](https://learn.microsoft.com/en-us/windows/wsl/basic-commands):

```powershell
wsl --version
wsl --status
wsl --list --verbose
```

Inside the intended guest, inspect:

```bash
cat /etc/os-release
uname -r
ls -l /dev/dxg
python3 --version
```

Resolve the exact GPU, Windows driver, WSL guest and ROCm combination before installation. Follow the WSL-selected branch of [AMD's current install guide](https://rocm.docs.amd.com/en/latest/install/rocm.html). If maintaining an older `roc4wsl` or separately built `librocdxg` setup, identify that path explicitly before upgrading; do not layer both approaches blindly.

Use a clean virtual environment and the matching framework artifact. Keep development files and large compilation caches on a filesystem suited to the Linux tools; measure filesystem overhead if data loading is slow. Record WSL VM memory limits and host memory pressure when diagnosing an out-of-memory condition.

Validate enumeration, a bounded GPU calculation and the representative model. Compare a suspected WSL-specific issue with a known-good native environment only when one is available; do not infer that all AMD hardware is broken from one preview backend failure.

Treat a WSL shutdown or driver update as an operation affecting running sessions. Preserve active work and use the authorized maintenance scope. Recheck the loaded driver and guest state after restarting.

## Diagnose the right layer

| Symptom | First checks |
| --- | --- |
| GPU absent in native Windows | Driver branch, exact device qualification, selected runtime artifact |
| No `/dev/dxg` in WSL | WSL2 status, Windows GPU driver, guest context |
| Python imports but GPU unavailable | Wheel OS/ABI/backend, library resolution, GPU-target coverage |
| Custom extension fails | Windows build support, compiler/linker, CUDA-specific code |
| Multi-GPU code expects RCCL | Native Windows component support and framework distributed implementation |
| Profiler unavailable in WSL | Release-specific tooling restrictions before reinstalling |
| Hang or reset after working enumeration | Small reproducer, exact release known issues, host and guest logs |
| Works in one shell only | Different Python, PATH, SDK prefix or virtual environment |

Do not run an indefinite telemetry/event command as a health check. Current release notes contain WSL-specific known issues; choose bounded queries and preserve a way to stop a reproducer.

## Evaluate alternative backends

An application may offer Vulkan or DirectML on hardware that lacks a suitable ROCm configuration. Evaluate that backend on its own requirements, operator coverage, precision, memory use and performance. Do not describe it as a ROCm installation, and do not assume equivalent training or distributed features.

If the task concerns the Ryzen NPU, route to [Ryzen AI](https://ryzenai.docs.amd.com/en/latest/) and its supported deployment flow. A backend switch is a concrete engineering tradeoff: state which features are preserved, which need testing, and how to return to the original environment.
