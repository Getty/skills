# Build toolchains, CMake and TheRock

Evidence baseline: 2026-10-30. Build against a selected SDK/component revision; development documentation can describe features not present in a released compiler.

## Contents

- [Separate target identities](#separate-target-identities)
- [Compile an application](#compile-an-application)
- [Diagnose ABI and library resolution](#diagnose-abi-and-library-resolution)
- [Choose a source build deliberately](#choose-a-source-build-deliberately)
- [Make builds reproducible](#make-builds-reproducible)

## Separate target identities

Record exact product, runtime `gfx` target, ISA features where relevant, and artifact architecture family. These are not interchangeable strings. An artifact family such as `gfx110X-all` groups targets for packaging; a compiler `--offload-arch` argument usually names a concrete accepted target such as `gfx1100`. Verify accepted values in the selected compiler/release.

When building in a container or CI without GPU access, automatic target detection may produce the wrong/default target. Set intended deployment targets explicitly. Including more targets increases artifact size and compile time; it cannot add hardware instructions absent from a device.

HIP code is compiled by an appropriate Clang-based toolchain; `hipcc` is a driver interface. A host C++ compiler can compile host-only integration but does not thereby compile GPU kernels. See [HIP compilers](https://rocm.docs.amd.com/projects/HIP/en/latest/understand/compilers.html) and [Clang HIP support](https://clang.llvm.org/docs/HIPSupport.html).

## Compile an application

Start with the [bundled HIP program](../assets/hip-smoke/hip-smoke.hip). Use [HIP programming](hip-programming.md) for a single-command `hipcc` build. For the bundled CMake project, select the actual SDK compiler and target:

```bash
# Templates: replace both paths/target from the installed SDK and GPU.
ROCM_HIP_COMPILER=/absolute/path/to/selected/sdk/bin/amdclang++
ROCM_TARGET=gfx1100
cmake -S assets/hip-smoke -B build-hip-smoke \
  -DCMAKE_HIP_COMPILER="$ROCM_HIP_COMPILER" \
  -DCMAKE_HIP_ARCHITECTURES="$ROCM_TARGET" \
  -DCMAKE_BUILD_TYPE=Release
cmake --build build-hip-smoke --parallel 2
ctest --test-dir build-hip-smoke --output-on-failure
```

The compiler path is intentionally not assumed from `/opt/rocm`; verify the installed layout and platform. Native CMake HIP language support uses an appropriate compiler executable rather than blindly pointing `CMAKE_HIP_COMPILER` at a `hipcc` wrapper. For an existing project, follow its own supported CMake integration; do not mix legacy `FindHIP` and native-language routes without understanding ownership.

CMake caches the compiler on initial configuration. Use a new build directory when switching SDK, compiler, platform or fundamental architecture configuration. `HIPCXX` influences initial selection, not an already configured cache. See [CMake HIPCXX](https://cmake.org/cmake/help/latest/envvar/HIPCXX.html) and [HIP architectures](https://cmake.org/cmake/help/latest/variable/CMAKE_HIP_ARCHITECTURES.html); check the installed CMake's versioned docs when it differs from current documentation.

## Diagnose ABI and library resolution

If compilation succeeds but loading fails, collect the exact executable/module, build provenance, runtime loader errors, selected SDK and Python/framework ABI. Distinguish a missing shared library from an undefined symbol, absent GPU code object or kernel launch failure.

For a trusted Linux artifact, inspect ELF metadata without running it:

```bash
readelf -d ./hip-smoke
readelf -h ./hip-smoke
```

Resolve `NEEDED`, RPATH/RUNPATH and actual library origins using tools appropriate to the platform. Windows DLL lookup needs native diagnostics; ELF commands do not apply. Do not repair mismatches by creating global symlinks to a differently versioned library or prepending every installed SDK to `LD_LIBRARY_PATH`.

Keep compiler, headers, runtime, math libraries and extension ABI coherent. A new framework wheel may bundle its own runtime and target-specific libraries; a system-wide SDK is not automatically the one it loads. A development SDK is still needed if the extension build actually compiles HIP code. A container includes userspace, not a private replacement for its host kernel driver.

API source compatibility, host ABI and device-code compatibility are independent. For major upgrades, consult component release notes, rebuild affected extensions and rerun numerical tests. Do not infer compatibility from matching the first digit of version strings.

## Choose a source build deliberately

Use TheRock when modifying ROCm, targeting an explicitly supported custom configuration, reproducing a component bug or needing an artifact unavailable as a release. First inspect [TheRock](https://github.com/ROCm/TheRock), its pinned revision's build instructions, release artifact documentation and support files. A successful source build on an alternative distribution does not create vendor validation.

A full stack build can consume substantial disk, RAM and time; the fetched project overview gives roughly 200 GB and multi-hour build expectations. Treat that as planning evidence, then size the chosen components, targets and debug configuration. The [environment guide](https://github.com/ROCm/TheRock/blob/main/docs/environment_setup_guide.md) warns that outer build parallelism does not necessarily bound nested component builds. Monitor actual compiler/linker concurrency and host memory rather than assuming `-j2` is a global limit.

Use this sequence:

1. Select release tag/commit and record submodule/component revisions.
2. Choose a documented build environment and compiler/tool versions for that revision.
3. Limit components and target families to the requirement; inspect available CMake options instead of guessing names.
4. Resolve required dependency and binary-artifact downloads through their documented source and preserve hashes.
5. Build in a dedicated prefix/output directory, leaving the working production SDK intact.
6. Run component tests and a real target-machine application test.
7. Produce a relocatable or packaged artifact only through a supported route; verify loader paths after relocation.

Consult [TheRock development guidance](https://github.com/ROCm/TheRock/blob/main/docs/development/development_guide.md) for incremental component work. Read repository-local contributor instructions and skills when editing that repository; they supplement this operator-level workflow.

## Make builds reproducible

Retain source revisions, patch set, dependency origins, tool versions, target list, configure arguments, build logs and package checksums. Separate build and run environments and document which system libraries remain external. Keep architecture targets in cache keys with compiler/framework versions.

For air-gapped environments, stage the exact released artifacts and dependencies on a connected machine, verify integrity, then test the offline install on a representative host. Do not assume a warm compiler cache is portable between drivers, GPU generations or framework revisions. See [upgrades](upgrades-reproducibility.md).

If no compiler or GPU is available locally, label source/syntax review separately from compilation and hardware execution. Do not claim the bundled CMake example was compiled merely because its configuration was inspected.
