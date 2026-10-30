# Frameworks, graph runtimes and interoperability

Evidence checked: 2026-10-30. Apply [compatibility.md](compatibility.md) to every framework independently; a supported Core SDK target does not guarantee a framework wheel for that target.

## Contents

- [Choose the runtime boundary](#choose-the-runtime-boundary)
- [JAX](#jax)
- [TensorFlow](#tensorflow)
- [ONNX Runtime and MIGraphX](#onnx-runtime-and-migraphx)
- [Other array and compiler ecosystems](#other-array-and-compiler-ecosystems)
- [Exchange tensors without hiding ownership](#exchange-tensors-without-hiding-ownership)
- [Validate a migration](#validate-a-migration)

## Choose the runtime boundary

Start from the application and its required operations. Determine whether it needs eager Python execution, autograd, ahead-of-time graph inference, a native C/C++ API or an accelerator-independent model representation. Use a framework's supported AMD route instead of translating package names by analogy with CUDA.

| Requirement | Candidate route | Evidence required before selection |
| --- | --- | --- |
| Research models and custom training | ROCm PyTorch or AMD's JAX plugin | Model operators, backward kernels, compiler and device support |
| Existing TensorFlow application | AMD ROCm TensorFlow build | TensorFlow/Keras/Python tuple and GPU matrix |
| Deploy an ONNX graph | ONNX Runtime with MIGraphX EP | Provider plugin availability, opset/shape coverage and actual node placement |
| Native graph inference | MIGraphX | Supported operators, precision, dynamic shapes and C++/Python interfaces |
| Portable desktop inference | Application's HIP, Vulkan or DirectML backend | That backend's capabilities; these paths are not interchangeable ROCm validations |
| AMD NPU deployment | Ryzen AI/Vitis AI path applicable to the NPU | Separate device, toolchain, model and driver support |

Treat vendor examples as recipes for their recorded GPU/software tuple. A worked Instinct example does not prove Radeon or APU support; a working PyTorch wheel on Windows does not prove a Windows wheel for another framework.

## JAX

JAX uses an AMD-maintained ROCm plugin. Current JAX installation documentation distinguishes system-ROCm installation from architecture-specific TheRock pip extras. It also distinguishes native Linux support, native Windows absence and experimental WSL2 use. The plugin's ROCm version must match its published compatibility mapping; a generic `pip install jax` may leave the application running on CPU. See [JAX installation](https://docs.jax.dev/en/latest/installation.html) and [AMD's JAX installer](https://rocm.docs.amd.com/projects/ai-ecosystem/en/latest/frameworks/jax/install.html).

Resolve `jax`, `jaxlib`, PJRT/plugin packages, Python, ROCm and the target together. Do not mix a classic `/opt/rocm` installation with TheRock plugins that require a different library layout. Prefer the documented pinned container when reproducing an upstream bug; then isolate whether the application or environment introduces the difference.

Prove device placement and finish asynchronous work before reporting success:

```python
import jax
import jax.numpy as jnp

devices = jax.devices()
print(devices)
gpus = [d for d in devices if d.platform == "gpu"]
assert gpus, "No GPU backend; do not accept a CPU fallback"
x = jax.device_put(jnp.arange(64, dtype=jnp.float32).reshape(8, 8), gpus[0])
y = jax.jit(lambda a: a @ a.T)(x)
y.block_until_ready()
assert bool(jnp.isfinite(y).all())
print(y.devices())
```

Confirm the selected GPU is the intended AMD device from inventory and backend metadata. Add an independent numerical reference before accepting correctness. Measure tracing/compilation separately from execution. For training, add gradient and optimizer tests; for multi-device work, inspect the mesh, sharding and collective results. Repeated retracing can dominate performance even when the GPU runtime is healthy.

JAX, PyTorch and TensorFlow may each reserve substantial memory. First reproduce failures with one framework per process. If coexistence is required, configure each framework's allocator deliberately and test both startup orders. Do not label a second-framework OOM as a driver incompatibility until reservation and live allocations are measured.

## TensorFlow

Use the AMD build named by [the TensorFlow installer](https://rocm.docs.amd.com/projects/ai-ecosystem/en/latest/frameworks/tensorflow/install.html), with the exact supported Python and GPU selection. At the evidence date, AMD publishes ROCm-specific TensorFlow packages; an ordinary CUDA-oriented TensorFlow recipe is not a replacement.

Begin with physical-device enumeration:

```python
import tensorflow as tf

print(tf.__version__)
print(tf.sysconfig.get_build_info())
gpus = tf.config.list_physical_devices("GPU")
assert gpus, "No TensorFlow GPU found"
tf.config.set_soft_device_placement(False)
with tf.device("/GPU:0"):
    a = tf.reshape(tf.range(64, dtype=tf.float32), (8, 8))
    b = tf.linalg.matmul(a, a, transpose_b=True)
print(b.device)
assert bool(tf.reduce_all(tf.math.is_finite(b)).numpy())
```

Require build metadata and inventory to identify the ROCm implementation. Disable soft placement during diagnosis to expose unsupported operations instead of silently benchmarking CPU work. Add model-specific ops, gradients, mixed precision and distributed tests only as needed. Do not assume a SavedModel produced with one custom operator package is deployable without that operator's compatible implementation.

Keep Keras, TensorFlow, protobuf, NumPy and Python constraints in the environment record. Solve an import failure at this layer before changing GPU firmware or host drivers.

## ONNX Runtime and MIGraphX

The legacy `ROCMExecutionProvider` was removed beginning with ONNX Runtime 1.23. Current migration work should target the [MIGraphX Execution Provider](https://onnxruntime.ai/docs/execution-providers/MIGraphX-ExecutionProvider.html), not perpetuate the old provider name. The [legacy provider notice](https://onnxruntime.ai/docs/execution-providers/ROCm-ExecutionProvider.html) documents that removal.

The ROCm 10.1.0 AMD recipe uses an `onnxruntime-ep-migraphx` plugin and requires a pip-installed MIGraphX dependency. Its provider must be explicitly registered before provider enumeration. A system MIGraphX installation alone does not satisfy that plugin's Python package dependency. Follow [AMD's ONNX Runtime guide](https://rocm.docs.amd.com/projects/ai-ecosystem/en/latest/inference/onnxruntime.html) for the exact package tuple and version-specific differences.

For that plugin model, validate registration explicitly:

```python
import onnxruntime as ort
import onnxruntime_ep_migraphx as plugin

names = plugin.get_ep_names()
paths = plugin.get_library_paths()
assert len(names) == len(paths), "Unexpected provider plugin metadata"
for name, path in zip(names, paths):
    ort.register_execution_provider_library(name, path)
assert "MIGraphXExecutionProvider" in ort.get_available_providers()
```

Older monolithic builds and newer plugin builds need different setup; do not copy registration or soname workarounds across releases blindly. Build a session using the required provider first, enable profiling and inspect graph node placement. Merely seeing MIGraphX in `get_available_providers()` does not prove the expensive nodes were assigned to it.

Before conversion, record input/output names, shapes, dynamic axes, dtypes, opset, preprocessing and postprocessing. Test minimum, typical and maximum shapes. Compare model outputs against the original framework using representative data and tolerances, then inspect CPU fallback and host/device copies. Include graph compilation and cache reuse in startup measurements; separate them from steady-state inference.

## Other array and compiler ecosystems

For CuPy, Numba, Triton, OpenMP offload, SYCL and domain libraries, inspect the current project's own AMD backend support. Similar array syntax does not imply interchangeable binaries or identical coverage. Distinguish source portability from a supported installation package and from performant execution on the selected architecture.

For a Python package with native code, inspect its build files, dependencies and tests for HIP or another AMD-capable backend. Record unsupported CUDA-specific functionality such as a particular PTX kernel, TensorRT integration or vendor-specific collective path. Replacing the package or implementing a portable operator can be more reliable than attempting to translate a complete compiled dependency chain.

## Exchange tensors without hiding ownership

Treat DLPack or another exchange interface as a contract about device, lifetime, dtype, strides and synchronization. It is not a vendor translation layer. Check whether the producer and consumer operate on the same physical GPU and compatible runtime, whether a copy occurs, and who owns the buffer after exchange. Avoid reusing storage while an asynchronous consumer still depends on it.

For any zero-copy claim, measure transfer activity and validate aliasing intentionally. Check contiguous and non-contiguous inputs, ownership after deletion of the producer, and cross-stream ordering. If the API or package requires a copy, record its latency and peak-memory cost rather than concealing it inside an end-to-end number.

## Validate a migration

Produce a capability table with columns for import, device discovery, target operators, numerical parity, gradients, compilation, multi-GPU and deployment packaging. Mark untested cells explicitly. Preserve the smallest failing graph or operator and environment manifest. State whether a limitation belongs to the GPU, ROCm runtime, framework build, provider, exporter or application; each boundary suggests a different remedy.
