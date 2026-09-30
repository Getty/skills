# 04 — Memory, Context, and Actual Concurrency

## Weights are only the first calculation

For a dense model with P parameters, `P × bits/8` is a **raw baseline**.
Scales, zero points, unquantized layers, padding, and backend structures add
overhead. MoE models generally also store currently inactive experts unless
those experts are explicitly distributed or offloaded differently.

| Parameters | Raw BF16/FP16 (GiB) | Raw 8-bit (GiB) | Raw 4-bit (GiB) |
|---|---:|---:|---:|
| 8 billion | 14.90 | 7.45 | 3.73 |
| 14 billion | 26.08 | 13.04 | 6.52 |
| 32 billion | 59.60 | 29.80 | 14.90 |
| 70 billion | 130.39 | 65.19 | 32.60 |

Calculated with 1 GiB = 2³⁰ bytes. These are **not measured GPU memory footprints**.
Quantization and architecture boundaries: [S12–S14, S18](28-sources.md).

## KV for homogeneous full-attention MHA/GQA

```text
KV_bytes_per_token = 2 × layers × kv_heads × head_dim × bytes_per_element
KV_total ≈ KV_bytes_per_token × sum of resident context tokens
```

The factor 2 represents keys and values. Use `num_key_value_heads`, not blindly
`num_attention_heads`. Padding and block rounding increase actual requirements.
With 32 layers, 8 KV heads, head dimension 128, and 2 bytes per element, the
result is **128 KiB per token**. 8,192 resident tokens therefore require
**1 GiB of KV**; four independent sequences of this size require about 4 GiB.
The example model is synthetic.

Shared prefix blocks can reduce physical requirements. For worst-case capacity,
initially calculate without sharing. For an optimized plan, count the **union
of physically distinct blocks**, not simply all logical prompt lengths.
Additional output grows on top of the prompt.

## Where the formula does not apply

MLA can use different latent cache dimensions. Mamba/SSM models store states
rather than a conventional complete KV history. Hybrid models combine layer
and cache groups; sliding attention keeps different token counts resident.
Quantized KV scales and specialized layouts change the calculation.
`capacity.py` is therefore explicitly a full-attention calculator with manually
confirmed parameters only. [S29, S13](28-sources.md)

With TP, KV cannot always simply be divided by GPU count: KV heads may be
replicated, partitioning may have architectural constraints, and additional
processes need memory. Use the engine's per-rank reports; the calculator does
not model automatic TP/PP/DCP partitioning.

## Practical budget

```text
KV_budget = permitted GPU budget
            − weights
            − activations/temporary workspaces
            − CUDA Graphs/runtime
            − encoders/adapters/other GPU processes
            − safety reserve
```

`gpu_memory_utilization` is an executor memory budget, not a target for GPU
compute utilization or a global isolation mechanism. An explicit
`kv_cache_memory_bytes` overrides the corresponding automatic derivation;
it does not eliminate other memory consumers. [S03](28-sources.md)

A high value can retain APC longer and prevent preemptions but tolerate fewer
memory spikes. A lower value can make startup more stable but shrinks the KV
pool. For an OOM, first determine whether it occurs during weight loading,
profiling, graph capture, media encoding, or under load.

## Do not confuse capacity with the context limit

`max_model_len` limits one sequence, `max_num_seqs` limits concurrently scheduled
sequences, and `max_num_batched_tokens` sets a scheduler-iteration budget.
None alone specifies the “number of supported users.”

Planning sequence: estimate weights → read actual startup capacity → apply the
p50/p95/p99 input-plus-output distribution → measure SLOs under load → adjust
reserves. The largest successful individual prompt is not capacity evidence for
concurrent agents. For unified memory, also check host/container RAM and swap.

## Example invocation

```bash
python scripts/capacity.py --gpu-gib 24 --utilization 0.85 \
  --parameters-b 8 --weight-bits 4 --weight-overhead 1.15 \
  --runtime-gib 3 --reserve-gib 1 --layers 32 --kv-heads 8 \
  --head-dim 128 --kv-bits 16 --context-tokens 8192 --block-size 16
```

All values, including the 15% weight overhead, are **chosen assumptions**.
The result is a rough memory-based bound, not a performance SLO.
