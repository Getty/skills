# Scientific computing and the ROCm library ecosystem

Evidence checked: 2026-10-30. Check API, precision, architecture, and OS support at the individual component level. An umbrella SDK listing is not proof that a specific routine or datatype has an optimized implementation on the target GPU.

## Contents

- [Select the programming layer](#select-the-programming-layer)
- [Choose a library by operation](#choose-a-library-by-operation)
- [Integrate and validate numerical code](#integrate-and-validate-numerical-code)
- [Use OpenMP and Fortran](#use-openmp-and-fortran)
- [Scale beyond one device](#scale-beyond-one-device)
- [Maintain the build](#maintain-the-build)

## Select the programming layer

Start from the application's existing parallel model and measured hotspot. Prefer a maintained application backend or a numerical library over rewriting a proven solver as custom kernels. Use HIP when explicit kernel and memory control is required; OpenMP target when extending directive-based C/C++/Fortran code; a maintained portability framework when the project already depends on it. Verify the framework's exact ROCm backend and release rather than assuming all standard C++ parallel code offloads.

The ROCm Core SDK supplies the main runtime, compilers, math, and communication components. The ROCm HPC SDK is a separate packaging scope and currently lists hipTensor and rocALUTION. Resolve those scopes before concluding that an absent Core SDK package was abandoned. [ROCm HPC SDK 10.1.0](https://rocm.docs.amd.com/en/docs-10.1.0/components/hpc-sdk/index.html).

## Choose a library by operation

| Need | Candidate | Decision and validation detail |
| --- | --- | --- |
| Dense vector/matrix operations | [rocBLAS](https://rocm.docs.amd.com/projects/rocBLAS/en/latest/), hipBLAS | Check layout, strides, scalar pointer mode, batching, and accumulation type |
| Flexible/tuned GEMM and epilogues | [hipBLASLt](https://rocm.docs.amd.com/projects/hipBLASLt/en/latest/) | Check exact dtype/layout/epilogue combination and required workspace |
| Factorization, decomposition, dense solves | [rocSOLVER](https://rocm.docs.amd.com/projects/rocSOLVER/en/latest/), [hipSOLVER](https://rocm.docs.amd.com/projects/hipSOLVER/en/latest/) | Check routine coverage, pivots/status, conditioning, and residuals |
| Sparse matrix operations | [rocSPARSE](https://rocm.docs.amd.com/projects/rocSPARSE/en/latest/), hipSPARSE | Choose format and index width; include conversion and analysis cost |
| Sparse iterative-solver application layer | rocALUTION in the HPC SDK | Check preconditioner, convergence, matrix formats, and current packaging |
| FFTs | [rocFFT](https://rocm.docs.amd.com/projects/rocFFT/en/latest/), [hipFFT/hipFFTW](https://rocm.docs.amd.com/projects/hipFFT/en/latest/) | Check normalization, strides, batching, plan/workspace lifetime, and API subset |
| Random-number generation | [rocRAND](https://rocm.docs.amd.com/projects/rocRAND/en/latest/), hipRAND | Specify generator, seed, subsequences, and reproducibility scope |
| Scan, reduction, sort, device primitives | [rocPRIM](https://rocm.docs.amd.com/projects/rocPRIM/en/latest/), hipCUB, [rocThrust](https://rocm.docs.amd.com/projects/rocThrust/en/latest/) | Measure temporary storage, synchronization, and algorithm ordering |
| Low-level matrix-tile operations | [rocWMMA](https://rocm.docs.amd.com/projects/rocWMMA/en/latest/) or Composable Kernel | Check tile shape, supported ISA/dtype, register pressure, and fallback |
| Tensor contractions | hipTensor in the HPC SDK | Check contraction layout, type combinations, and plan reuse |
| Host-driven collectives | RCCL or ROCm-aware MPI | Choose according to application semantics and tested transport |
| GPU-initiated communication | [rocSHMEM](https://rocm.docs.amd.com/projects/rocSHMEM/en/latest/) | Understand symmetric allocation, ordering, and device-side synchronization |

The `hip*` wrappers can aid source portability across documented backends; they do not convert arbitrary vendor binaries or ensure identical routine coverage, numerical behavior, and performance. For example, hipSOLVER wraps backend LAPACK implementations; hipFFT uses GPU-visible buffers, while hipFFTW exposes a selected FFTW-like interface with a different memory contract. Read the actual API rather than relying on similar names.

## Integrate and validate numerical code

1. Identify the mathematical contract: shape, layout, dtype, error tolerance, sparsity pattern, determinism, and expected output.
2. Build a small CPU/reference result and a GPU implementation with explicit error handling. Check every allocation/library status and synchronize before inspecting results.
3. Allocate buffers and reusable workspace once when possible. Distinguish algorithm selection/planning cost from repeated execution.
4. Keep data resident across several operations. Measure end-to-end speed including copies and format conversion; a fast library call can lose overall when inputs bounce between CPU and GPU.
5. Test realistic and adversarial cases: zero/empty dimensions where supported, odd sizes, transposed/strided data, ill-conditioned matrices, extreme values, and large indices.
6. Scale the representative workload, then profile its actual bottleneck. Do not optimize a synthetic square GEMM when the application performs small irregular sparse operations.

Use residual/error criteria appropriate to the algorithm: normalized solve residuals, reconstruction errors, conservation laws, or known FFT round trips. Bitwise identity is a stronger requirement than acceptable numerical error and is not implied by a fixed random seed. Specify which operations and software/hardware revisions are expected to be deterministic.

Match handles and streams to the intended device, and obey library lifetime/thread-safety rules. Avoid sharing a mutable handle across host threads without an explicit supported pattern. Query workspace requirements instead of guessing that a routine uses no temporary GPU memory.

## Use OpenMP and Fortran

Select the ROCm-provided compiler and runtime explicitly; a system `clang`, `flang`, or `gfortran` binary may have different targets and libraries. ROCm's OpenMP documentation describes GPU offload and partial support across successive OpenMP standards. Inspect support for the constructs used, rather than advertising complete compatibility with the newest standard. [ROCm OpenMP guide](https://rocm.docs.amd.com/projects/llvm-project/en/latest/conceptual/openmp.html).

A compilation pattern for an existing C++ source is:

```bash
# Set ROCM_CLANGXX to the selected compiler and GPU_ARCH to the verified gfx target.
"${ROCM_CLANGXX:?set compiler path}" -O2 -fopenmp --offload-arch="${GPU_ARCH:?set verified gfx target}" simulation.cpp -o simulation
OMP_TARGET_OFFLOAD=MANDATORY ./simulation
```

This is a template, not a claim that `simulation.cpp` exists or has been GPU-tested. Confirm device execution within a target region using `omp_is_initial_device()` as part of the program's validation. A host-only or explicitly host-targeted region is not caught merely by expecting mandatory GPU offload. [LLVM OpenMP offload flags](https://openmp.llvm.org/CommandLineArgumentReference.html).

Keep target data resident across timesteps and make mapping lifetimes explicit. Unified/shared-memory behavior depends on hardware and runtime/XNACK support; it does not make remote memory bandwidth equivalent to local HBM. Use explicit copies as a diagnostic baseline. For Fortran interoperability, distinguish compiler offload support, C bindings to numerical libraries, and a separate helper project such as hipfort; verify each one's current packaging.

## Scale beyond one device

Use MPI for an MPI-oriented application, RCCL for supported collective-centric GPU communication, and rocSHMEM when GPU-initiated fine-grained communication fits the algorithm. rocSHMEM's symmetric heap and ordering model are programming constraints, not transparent distributed malloc. Review its supported network backend and deployment prerequisites. [rocSHMEM overview](https://rocm.docs.amd.com/projects/rocSHMEM/en/latest/).

Verify ROCm-aware MPI using GPU buffers, not only host-buffer benchmarks. Open MPI 5.0.x documents UCX as its supported ROCm transport; compiling an application with `mpicxx` does not prove the linked UCX has GPU support. [Open MPI ROCm guidance](https://docs.open-mpi.org/en/v5.0.x/tuning-apps/networking/rocm.html).

Report both strong scaling at fixed total work and weak scaling at fixed work per device when relevant. Include convergence or numerical quality, not only iteration duration. A different preconditioner or stopping criterion can invalidate an apparent speedup. Use [the multi-GPU guide](multi-gpu-networking.md) for topology and collective acceptance.

## Maintain the build

Pin compiler, SDK, component versions, architecture targets, and source revisions. Discover package-provided CMake configuration/targets instead of hardcoding every library path. Keep host and device compilation flags distinct, and confirm the runtime libraries loaded by the final binary match the tested installation.

Current math-library repositories commonly live in `ROCm/rocm-libraries`, while runtime/communication projects can live in `ROCm/rocm-systems`; follow each component's authoritative repository link. Preserve required licenses and notices when redistributing binaries. Treat rebuilds after compiler, library, or architecture changes as numerical-validation events, then compare performance only after the results pass.
