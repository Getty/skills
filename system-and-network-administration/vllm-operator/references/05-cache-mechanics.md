# 05 — Caches: What Is Reused and What Is Not

| Cache | Contents | Primarily helps with | Cost / boundary |
|---|---|---|---|
| Model/download cache | Weight files, tokenizer | Restarting without downloading again | Disk; no speedup for ongoing token generation |
| Compile/kernel cache | Compiled artifacts | Repeated startup/warmup | Version- and architecture-specific |
| CUDA Graph replay | Recorded execution structure | Launch overhead for matching shapes | GPU memory, capture, padding |
| Active KV cache | Context states of active sequences | Autoregressive decode | Grows/varies with context |
| APC | Reusable prefix states | Repeated prefill of an identical prefix | Resident blocks, eviction, identity |
| External KV cache | Offloaded states | Larger reusable working set | Copies, RAM/NVMe/network |
| Multimodal processor/encoder cache | Preprocessing results or features | Repeated media | Additional CPU/GPU/IPC budgets |
| Response/semantic cache | Completed responses | Avoiding an entire model request | Outside generic APC; correctness/ACLs |

References: [S04–S07, S24, S32](28-sources.md). These distinctions prevent,
for example, presenting a warm HF download cache as successful prefix caching.

## APC works with prefix identity

In the conventional block model, keys depend on preceding prefix states and
the tokens of the corresponding section. Additional identities, such as adapters
or media, must also match. Similar meaning is not a hit. An identical paragraph
after different preceding tokens is not automatically reusable. [S06](28-sources.md)

The historically simple explanation “only complete physical blocks” no longer
covers every new implementation: newer configurations can separate match
granularity from physical block size, particularly for hybrid models. Check
`prefix_match_unit`, cache groups, and actual reported hits. Even with a
completely identical prompt, do not blindly expect 100% reuse; boundary positions
and required logits can cause additional computation. [S03, S29](28-sources.md)

## Effects and opportunity costs

A warm prefix primarily shortens the prefill computation required. Response
tokens still have to be generated, and attention still has to access the
necessary context states. With a long output and a short prompt, the overall
gain may therefore be small. Under queue overload, waiting can hide a local
prefill improvement. [S05](28-sources.md)

In normal operation, APC uses the same limited memory space as other KV usage.
Inactive cached blocks are reusable and evictable; reboots and evictions can
eliminate hits. Artificially keeping many rarely needed prompts warm can displace
useful work. This is a cost tradeoff to test, not a general recommendation
to prewarm everything.

## Cache benchmarking as an experiment

A: A first long prompt with an unchanged system/tool prefix.
B: The same request immediately afterward.
C: The same long prefix with a different question at the end.
D: A small change very early in the prefix.
E: Repeat A after enough unrelated load.

With the same model, template, sampling, and comparable queue conditions,
compare client TTFT, prefill time, local/external cached tokens, and KV pressure.
B alone does not prove the effect: the first run can also include compilation
warmup. Warm up the engine first, then test cache states separately.
Never reset a production server's cache without permission.

## The most important misconceptions

Temperature 0 does not make a prefix hit more likely; the relevant input tokens
and cache identities must match. JSON key order in the outer HTTP body matters
only when it changes the rendered model prompt. A stable `request_id` is not
a cache ID. Do not treat provider fields such as `cache_control` or
`prompt_cache_key` as vLLM APC controls without verification.
External caching and replica routing are separate layers.
