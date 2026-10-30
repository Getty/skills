# PyTorch on ROCm

Evidence checked: 2026-10-30. Use the compatibility record for the actual machine before applying an installation example. Recheck moving package selectors when changing versions.

## Contents

- [Select one coherent build](#select-one-coherent-build)
- [Understand the CUDA naming](#understand-the-cuda-naming)
- [Prove execution and correctness](#prove-execution-and-correctness)
- [Introduce precision and compilation](#introduce-precision-and-compilation)
- [Handle extensions and dependency changes](#handle-extensions-and-dependency-changes)
- [Diagnose by the first failing layer](#diagnose-by-the-first-failing-layer)
- [Record the result](#record-the-result)

## Select one coherent build

Resolve GPU SKU, real `gfx` target, OS, Python ABI, driver, ROCm build, PyTorch and application requirements together. A framework import is weaker evidence than a supported matrix entry and a successful representative operator test.

[AMD's PyTorch installer](https://rocm.docs.amd.com/projects/ai-ecosystem/en/latest/frameworks/pytorch/install.html) now exposes TheRock-based packages with device extras, including PyTorch 2.14.0 for ROCm 10.1.0. These extras select architecture-specific kernels and runtime dependencies. Preserve the exact package set emitted for the selected platform; do not substitute an upstream wheel with a similar version number. Native Windows availability is real, but framework, compiler and distributed features still require individual verification.

Installation procedure:

1. Read the selected application release's PyTorch constraints first. A serving engine may require an older PyTorch than AMD's newest standalone release.
2. Choose a version-pinned AMD container or an isolated Python environment. Keep experimentation outside an existing working environment.
3. Select the GPU and OS in the installer; retain the URL parameters or an exported record of the selection. A text extraction may include commands for several mutually exclusive selections.
4. Resolve the published Python/torch/torchvision/torchaudio tuple. Install only the companion libraries the application needs, while retaining their documented matching versions.
5. Capture a dependency resolution report; inspect subsequent application installs for attempted replacement of torch, Triton or ROCm dependencies.
6. Run `python -m pip check`, then the execution checks below. A satisfied Python resolver cannot verify GPU kernel compatibility.

Example of the **observed 10.1.0 package syntax**, after the matrix confirms the machine is suitable:

```bash
# In a fresh environment with a supported Python version, for real gfx1100.
python -m pip install --index-url https://stable.repo.amd.com/rocm/whl-next/ \
  'torch[device-gfx1100]==2.14.0+rocm10.1.0'
python -m pip check
```

This is a scoped example, not a policy to upgrade every installation. For a different target, select its published extra; `device-all` increases download and disk requirements and does not confer official support on every GPU. The operating-system GPU driver remains a separate prerequisite. Development headers and a compiler may still be needed for custom extensions.

## Understand the CUDA naming

ROCm PyTorch intentionally retains the `torch.cuda` API and `cuda` device strings. Use `torch.version.hip` to distinguish a HIP build; `torch.cuda.is_available()` alone does not identify the vendor. Do not replace `cuda` with `rocm` or `hip` in tensor placement. Distributed GPU communication normally retains the backend name `nccl` while using RCCL in a compatible ROCm build. These are compatibility interfaces, not evidence that CUDA binaries execute on AMD. See [PyTorch 2.14 HIP semantics](https://docs.pytorch.org/docs/2.14/notes/hip.html).

```python
import torch

assert torch.version.hip is not None, "Expected a ROCm/HIP PyTorch build"
assert torch.cuda.is_available(), "HIP build loaded, but no usable GPU is visible"
print(torch.__version__, torch.version.hip, torch.cuda.device_count())
for index in range(torch.cuda.device_count()):
    p = torch.cuda.get_device_properties(index)
    print(index, p.name, getattr(p, "gcnArchName", "unknown"), p.total_memory)
```

Run this in the exact interpreter, container, service account and device-visibility context used by the application. Notebook kernels, system services and interactive shells often resolve different environments. If the machine contains multiple AMD devices, inspect all of them rather than choosing the first `gfx` string in a diagnostic output.

## Prove execution and correctness

Use [the bundled smoke test](../scripts/torch_smoke.py) and inspect its `--help` for the current options. Require an actual HIP GPU and explicit pass/fail results; never count a CPU fallback as ROCm validation.

Progress through four stages:

1. **Small FP32 allocation and GEMM:** compare output with an independently computed reference, synchronize to expose asynchronous failures and record the device used.
2. **Required operators and dtypes:** test the application's convolution, normalization, sparse, FFT or attention operations as relevant. A matmul success does not validate every library.
3. **Backward and optimizer step:** require finite loss and gradients, and confirm at least one intended parameter changed. Inference success does not validate backward kernels.
4. **Representative workload:** use real shapes, sequence lengths, strides, masks and batch sizes. Include a second iteration so compilation and allocator initialization are not mistaken for steady-state behavior.

Set tolerances according to dtype and reduction depth. Check both absolute and relative error; relative error is unstable near zero. Compare intermediate tensors when the final application output looks plausible but numerical drift is suspected. For a CPU reference, reproduce the same input values and semantics instead of generating unrelated random tensors on each device.

## Introduce precision and compilation

Establish a working eager baseline before enabling `torch.compile`, fused optimizers, custom attention or reduced-precision kernels. Change one dimension at a time and keep a repeatable baseline command.

Use `torch.autocast(device_type="cuda", dtype=...)` for a verified precision path. Treat BF16 availability, efficient BF16 arithmetic and model numerical suitability as separate checks. FP16 frequently needs gradient scaling during training; BF16 does not automatically need the same policy. Avoid combining automatic mixed precision with unreviewed blanket conversions of every model tensor. The [AMP examples](https://docs.pytorch.org/docs/2.14/notes/amp_examples.html) define the relevant lifecycle and optimizer interaction.

For compilation, distinguish:

- capture failure or graph breaks;
- compiler/Triton/code-object generation failure;
- generated-kernel numerical error;
- correct execution with excessive compilation time or repeated recompilation;
- correct steady-state execution that is slower for this shape distribution.

Preserve a minimal failing shape, input dtype/stride, actual backend, compiler version and traceback. Compare eager with compiled output before measuring performance. Run warm and cold measurements separately; a short-lived process can lose more to compilation than it gains from optimized execution. Do not assume an inference graph implies supported backward graph capture or every collective is graph-safe.

## Handle extensions and dependency changes

A package may contain Python code, portable ATen calls, a HIP implementation, generated Triton kernels or CUDA-only PTX/CUBIN. Classify each compiled dependency before installing it. `pip install` success proves neither the existence nor selection of its ROCm implementation.

For a HIP extension:

1. Pin its source revision and compatible PyTorch/compiler versions.
2. Confirm the build system recognizes ROCm and uses the intended SDK, especially with pip-based SDK layouts.
3. Build for the real target list. Do not use an architecture override to disguise a missing code object.
4. Inspect the resulting library dependencies and kernel targets using the project's documented tools.
5. Test import, operator execution, backward where needed, and output equivalence in the deployment environment.

PyTorch's [C++ extension reference](https://docs.pytorch.org/docs/2.14/cpp_extension.html) describes its extension machinery; a particular third-party extension may impose additional restrictions. Keep extension caches scoped to the tested torch/compiler/architecture combination. After changing the toolchain, rebuild the affected extension rather than deleting every cache indiscriminately.

## Diagnose by the first failing layer

| Observation | Next evidence to collect |
| --- | --- |
| `torch.version.hip` is absent | Interpreter path, wheel origin, package dependency resolution |
| HIP build exists but no GPU is visible | Host/runtime visibility, device access, container mapping, compatible driver |
| Allocation works but first GEMM fails | GPU target, code objects, loaded math-library paths, required device extras |
| FP32 succeeds but BF16/FP16 fails | Exact operator, dtype and target support; reference comparison |
| Eager succeeds and compiled fails | Minimal compiled reproducer, Triton/compiler versions, graph-break evidence |
| Application install breaks a previously working smoke test | Before/after package manifest and replacement of torch or ROCm libraries |
| Growing memory after repeated requests | Live tensor ownership, retained autograd graphs, allocator reserved versus allocated bytes |
| Failure appears only under multiple processes | Per-process device assignment, memory headroom, collectives and inherited environment |

`empty_cache()` cannot release tensors still referenced by Python or make an undersized GPU fit a larger live working set. Treat allocator tuning as a measured hypothesis after understanding the allocation pattern.

## Record the result

Return the exact software tuple, support classification, device identities, successful operators/dtypes, untested features, minimal reproduction and rollback environment. Include benchmark shapes, synchronization method, warm-up, repetitions, peak memory and error tolerances. Report "basic ROCm execution verified" separately from "this model and training/serving path validated."
