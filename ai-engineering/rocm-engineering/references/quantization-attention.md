# Quantization, attention and optimized kernel selection

Evidence checked: 2026-10-30. Recheck the exact engine release and GPU architecture before treating a method as supported. Read [hardware.md](hardware.md) for device capabilities and [pytorch.md](pytorch.md) for the baseline runtime.

## Contents

- [Separate the compatibility questions](#separate-the-compatibility-questions)
- [Resolve quantization support per engine](#resolve-quantization-support-per-engine)
- [Qualify a quantized model](#qualify-a-quantized-model)
- [Select attention by semantics and dispatch](#select-attention-by-semantics-and-dispatch)
- [Understand the kernel libraries](#understand-the-kernel-libraries)
- [Run a controlled comparison](#run-a-controlled-comparison)
- [Handle unsupported paths](#handle-unsupported-paths)

## Separate the compatibility questions

For each optimization, answer all of these:

1. Can the hardware represent or accelerate the required datatype?
2. Does the compiler/runtime/library provide the necessary operation for this `gfx` target?
3. Does the installed framework or engine integrate that implementation?
4. Does it handle this model's tensor layout, head dimensions, group size, masks and sequence lengths?
5. Does the selected artifact contain the required code objects or a working compilation path?
6. Does the result meet the workload's accuracy, throughput, latency and memory objectives?

A model format such as GGUF or a quantization algorithm such as GPTQ is not a single kernel. Storage dtype, accumulation dtype, activation dtype and KV-cache dtype may all differ. Lower-bit storage can save capacity while dequantization overhead makes execution slower for a particular batch size.

Treat "FP8 supported" with particular care: distinguish its concrete format and scale convention, weight-only versus activation quantization, prequantized versus dynamic execution, and native versus converted arithmetic. For FP4/MXFP4/NVFP4, inspect the actual implementation rather than inferring incompatibility or support solely from a vendor name. Do not infer optimized support on RDNA from an Instinct demonstration.

## Resolve quantization support per engine

Use the engine's own versioned table, implementation source and a local test. Current primary sources illustrate why a single universal AMD checklist is misleading:

| Component | Observation at the evidence date | Operational consequence |
| --- | --- | --- |
| bitsandbytes | Maintained installation guide documents ROCm features and platform-specific target lists | Check the wheel and operation; do not repeat a historical CUDA-only rule |
| vLLM | Its generic quantization table marks some AMD paths unavailable, including AWQ/GPTQ/bitsandbytes, while listing others such as FP8 and GGUF | A library or another engine supporting a method does not prove this vLLM integration supports it |
| SGLang | Its AMD guide describes AWQ and additional quantization paths, with implementation-specific limits | Select its ROCm implementation rather than a Marlin-dependent path |
| AMD Quark | Provides quantization/export tooling | Verify that the deployment engine consumes that precise export format and scale layout |

Sources: [bitsandbytes installation](https://huggingface.co/docs/bitsandbytes/installation), [vLLM quantization](https://docs.vllm.ai/en/latest/features/quantization/), [SGLang AMD support](https://docs.sglang.io/docs/hardware-platforms/amd_gpu), [AMD model quantization](https://rocm.docs.amd.com/projects/ai-ecosystem/en/latest/optimization/model-quantization.html).

These observations are intentionally scoped, not permanent prohibitions. Tables may lag a new implementation or differ from a vendor-maintained branch. If source and documentation disagree, record the exact release/commit, inspect dispatch and test the requested method. Label the result experimental or locally validated until the support evidence is clear.

Do not copy an old package index from a conceptual quantization tutorial into a current ROCm environment. A tutorial can still explain a method while its AutoGPTQ wheel or API example belongs to a much older release. Resolve maintained implementations and artifacts independently.

## Qualify a quantized model

Before downloading a large candidate or starting calibration, inspect metadata: base model and revision, quantization method, bits, group size, scale granularity, zero-point convention, activation order, excluded layers, compute dtype, format version and intended runtime. Confirm tokenizer and chat-template compatibility.

Use the following acceptance sequence:

1. Establish a reference model or a trusted higher-precision checkpoint.
2. Load the candidate with explicit logged kernel selection. Verify that the engine did not choose CPU execution or a different dtype unexpectedly.
3. Test representative short and long contexts, multilingual or domain inputs where relevant, and structured outputs/tool use if required.
4. Compare task metrics and intermediate logits where available; do not infer accuracy from one plausible chat answer.
5. Measure loading peak, steady-state memory, KV-cache capacity and temporary dequantization workspaces.
6. Benchmark the target concurrency and prompt/output distribution, then repeat after a clean restart.

For post-training calibration, use representative input distributions and sequence lengths, keep a held-out evaluation set, and retain calibration recipe and data provenance. A calibration set tuned only to a benchmark may not represent deployment. For quantization-aware or adapter training, verify the backward and optimizer paths separately from inference.

For KV-cache quantization, compare long-context retrieval and generation quality as well as memory. Weight quantization and KV quantization are independent changes; test them separately before combining them. Keep scale artifacts with the model and ensure the engine interprets them as intended.

## Select attention by semantics and dispatch

Start from a correct baseline such as standard PyTorch scaled-dot-product attention. Record batch size, query and KV lengths, number of query/KV heads, head dimension, causal or arbitrary masks, dropout, tensor dtype and strides. Include backward when training.

[PyTorch's SDPA interface](https://docs.pytorch.org/docs/2.14/generated/torch.nn.functional.scaled_dot_product_attention.html) may choose among available implementations. Backend eligibility depends on inputs, so one successful shape does not validate all shapes. Use backend-selection controls for diagnosis and benchmarks, but do not leave a forced backend in production when the workload can produce unsupported inputs.

Distinguish these cases:

- The optimized kernel is unavailable, and dispatch falls back correctly.
- The kernel is selected but fails compilation or launch on this target.
- The kernel executes but produces unacceptable error for this mask/dtype/shape.
- The kernel is correct but slower because the workload is too small or transfer/launch costs dominate.
- A forward kernel works while the required backward, dropout or variable-length path is missing.

Verify mask semantics carefully. A Boolean mask convention can differ between APIs, and a subtle causal-mask mistake may still produce fluent language. Compare explicit small cases where expected attention behavior is known. Test padded and unpadded sequences, GQA/MQA and boundary lengths required by the model.

## Understand the kernel libraries

| Layer | Role | Avoid this assumption |
| --- | --- | --- |
| rocBLAS / hipBLASLt | Dense linear algebra and selectable algorithms | Every shape/dtype uses the same tuned algorithm |
| MIOpen | Neural-network primitives | A successful GEMM validates convolution or its backward path |
| Triton | Kernel programming and compilation | A CUDA-oriented Triton kernel is automatically performant and correct on AMD |
| AOTriton | Ahead-of-time kernel artifacts used by integrations | An installed artifact necessarily contains the target and variant needed |
| Composable Kernel / CK Tile | Kernel implementations and composition | All CK users share the same GPU/shape support matrix |
| AITER | AMD operator collection integrating multiple kernel approaches | Enabling one environment variable optimizes every model on every AMD GPU |
| FlashAttention package | Attention implementations with backend-specific coverage | Every FlashAttention generation has identical AMD and NVIDIA support |

[AITER's project](https://github.com/ROCm/aiter) describes its multi-backend operator collection. Pin it as part of the engine environment and inspect the actual operators used. An Instinct-optimized fused MoE or MLA implementation may require another path on Radeon even when AITER itself imports.

The [FlashAttention project](https://github.com/Dao-AILab/flash-attention) documents separate AMD CK and Triton implementations and their supported features. Its Triton installation can interact with the installed Triton/AITER versions. Prefer the engine's tested combination; do not blindly replace a torch-matched Triton package to satisfy a newer extension. Use published options for an existing system Triton/AITER only after verifying their version compatibility.

For ComfyUI, consult [diffusion-video.md](diffusion-video.md). The application's attention selection and VAE path add another dispatch layer beyond the library's own eligibility checks.

## Run a controlled comparison

Create an experiment record with baseline, candidate, fixed inputs, expected numerical tolerance, metric and rollback. Keep driver, model revision, tensor shapes and load distribution fixed unless one is the variable under test.

Run correctness before throughput. Include warm-up and synchronize at timing boundaries. Separate kernel microbenchmarks from end-to-end application measurements, and report compile/tune time. Capture actual backend names, precision, peak allocated/reserved memory, latency distributions and repeated-run variance. For training, include gradient error and convergence checks; for inference, include task accuracy and quality limits.

Reject optimization claims that depend only on theoretical TFLOPS, compressed checkpoint size or a single favorable shape. A useful result states which workload improved, by how much, at what memory/quality cost and under which software tuple.

## Handle unsupported paths

Choose among a supported fallback operator, another engine/backend, rebuilding a documented target, or a scoped port. Preserve a correct baseline and state the performance cost if known. A `gfx` override may bypass an identification check but cannot create missing instructions, guarantee numerical correctness or supply a validated kernel. Never present it as a general fix for quantization or attention support.

Report the exact boundary: unsupported model format, missing engine integration, missing architecture code object, unsupported operator shape/dtype, or failed local validation. That precision makes the next action concrete and avoids replacing the entire ROCm stack for an application-level limitation.
