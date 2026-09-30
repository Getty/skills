# 13 — Weight and KV Quantization: Capacity Does Not Automatically Mean Speed

## Three separate layers

**Weights** account for much of model memory. **Activations and the compute
path** help determine which Tensor Core/kernel paths are available.
The **KV cache** grows with context and active sequences. A “4-bit model” does
not imply that KV also occupies 4 bits or that every computation uses 4 bits.
Scales, group metadata, unquantized layers, and temporary buffers remain.
[S12–S14](28-sources.md)

Prefer a compatible pre-quantized checkpoint before quantizing on a constrained
serving machine yourself. Quantization needs separate tools, calibration data,
test data, and often more peak memory than the finished model.
`--quantization` is not a universal converter for arbitrary weights.

## Selection matrix

| Path | Useful evaluation purpose | Boundaries |
|---|---|---|
| BF16/FP16 | Quality/compatibility baseline when it fits | High weight and KV requirements |
| AWQ/GPTQ/other supported W4A16 paths | Fit the model into less VRAM | GPU, kernel, and checkpoint format determine speed |
| FP8 weight/activation path | Suitable hardware and a validated fast kernel | Older chips do not all have the same native support |
| Blackwell-specific FP4 paths | Matching architecture and compatible checkpoint | Not equivalent to arbitrary INT4 or every format labeled FP4 |
| FP8 KV | More context/concurrency, less KV traffic | Validate scales, backend, and accuracy |
| GGUF | A specific supported model/format | No general equivalence to llama.cpp |

The official quantization matrix describes combinations, not “this format is
always fastest.” Initially record the automatic selection from startup logs;
force kernels only as a controlled deviation. [S12–S14, S31](28-sources.md)

## KV scales and long-context quality

Quantized KV needs suitable scales. The consulted documentation describes
both per-tensor and supported per-attention-head paths; the appropriate
calibration method depends on the backend. Default scales of 1 are not
automatically good for every model. Prefer artifacts calibrated with
representative data and verify scale loading in the log. Do not blindly copy
old dynamic-scale-calculation flags from tutorials. [S13](28-sources.md)

FP8 KV can reduce memory and transfer pressure. The old blanket claim “it only
saves memory and never improves latency” is too strong: supported newer
attention paths can also change computation. “Half the KV means twice the
tokens/s” is equally wrong. Small batches, weight bandwidth, kernel conversion,
and prefill can limit the overall benefit. Enable new KV dtypes such as
INT4/NVFP4 or other specialized paths only after explicit model/hardware/backend
verification; a value appearing in the global CLI does not imply universal
support. [S03, S13–S14](28-sources.md)

## A quality gate using your application

Use an unchanged model family, tokenizer, chat template, parser, sampling
configuration, and test-dataset version. Test separately: instruction following,
code/tool arguments, JSON schemas, numerical tasks, German-language text,
long-context retrieval, rare entities, and long reasoning chains. Do not
evaluate quality solely through a friendly example conversation.

Calibration data must not leak the later test set. Evaluate quality across
multiple tasks and, with stochastic sampling, multiple seeds. Changed parser
or stop rules alone can create apparent quantization errors; after a regression,
first inspect the complete configuration diff.

## A/B plan

First compare the same concurrency, input/output lengths, and load against
BF16 or a working reference quantization. Only then test the higher concurrency
range made possible by saved memory. Report **speed changes at the same load**
separately from **additional capacity from more KV**. Record quality, peak
memory, cache warmup, TTFT/TTFA/ITL, SLO goodput, and costs. Rollback means the
exact previous checkpoint and configuration, not merely a different dtype flag.
