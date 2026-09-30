# 27 — Glossary and Formulas

| Term | Meaning in this package |
|---|---|
| Prefill | Process input tokens and build initial states/KV |
| Decode | Generate new tokens autoregressively; context grows |
| PagedAttention | Block-based KV management/use instead of large contiguous reservations |
| Continuous batching | Requests can enter/finish between execution steps |
| APC | Automatic prefix caching: reuse compatible prefix-related state |
| KV | Attention key/value states, not model weights |
| Weight offload | Make model weights available through GPU/host memory paths |
| KV offload | Move/restore KV states through external memory tiers |
| Compile cache | Reusable compilation artifacts, not response/prompt tokens |
| TTFT | Time to first token; always specify the measurement boundary |
| TTFA | Here: time to first visible answer content, not just reasoning |
| ITL | Inter-token latency; actual token timing or an explicitly labeled proxy measure |
| TPOT | Time per output token after the first token; not E2E/N |
| E2E | Entire measured request duration, including final stream completion at the client |
| Goodput | Work successfully delivered within the agreed SLOs per unit time |
| SLO | Testable service-quality objective, e.g. p95 client TTFT under a specified load |
| Admission control | Bounded admission instead of an unlimited queue |
| Preemption | Interrupt running work, potentially resume later through recomputation |
| Recomputation | Recompute required states instead of retrieving them from cache/memory |
| MHA/GQA | Attention with many KV heads or grouped/shared KV heads |
| MLA/SSM/hybrid | Different state/memory models; the simple KV calculator is not universal |
| Dense/MoE | Dense activation versus selected experts; active parameters ≠ all resident weights |
| TP/PP/DP/EP | Tensor/pipeline/data/expert parallelism |
| P2P | GPU-to-GPU transfers; verify actual topology/support |
| Quantization | Lower precision/representation with format/kernel/quality conditions |
| Speculation | Propose candidate tokens and have the target verify them |
| CUDA Graph | Recorded execution path with its own shape/memory behavior |
| LoRA | Adapter for a compatible base model; not an independent full model |
| Unified memory | Here, Spark's shared physical memory, not an additional VRAM pool |
| OTLP | Telemetry transport, including gRPC or HTTP-Protobuf |
| Span/trace | Timed segment/related distributed execution; not a universal kernel measurement |
| SSE | Server-sent events; event/chunk boundaries are not tokenization boundaries |
| Saturation knee | Region where additional load sharply worsens latency/errors |

## Calculation models

```text
Rawweights_bytes ≈ total_parameters × weight_bits / 8
KV_bytes_per_token = 2 × layers × kv_heads × head_dim × kv_bits / 8
KV_sequence_bytes = ceil(context_tokens / block_size) × block_size × KV_bytes_per_token
```

The KV formula applies only to homogeneous full MHA/GQA attention with similar
layers. Metadata, scales, padding, runtime, graphs, and other buffers are not
automatically fully included. Do not use it to claim fit for TP/MLA/SSM models.
Context tokens include input and the planned output budget; shared APC can
change actual requirements.

```text
TPOT ≈ (last_output_token_time − first_output_token_time) / (N − 1)
Little's law: mean_requests_in_system = arrival_rate × mean_residence_time
Transfer_time_lower_bound ≈ bytes / effectively_achievable_bandwidth
```

TPOT applies only for N > 1 and a consistent token/measurement definition.
Little's law requires a stable system with consistent boundaries. The transfer
formula ignores latency, setup, conversion, contention, and lack of overlap.
Manufacturer peak bandwidth is not measured effective bandwidth.

`1 GB = 10^9 bytes`, `1 GiB = 2^30 bytes`. In the calculator, “8B parameters”
means eight billion, not eight gibiparameters. Convert physical manufacturer
capacities into actually reported bytes/GiB. Calculations explain orders of
magnitude, not hardware compatibility or achievable tokens/s.

Further primary sources: [S03–S16, S22–S30](28-sources.md).
