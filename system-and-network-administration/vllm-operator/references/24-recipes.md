# 24 — Concrete Startup and Tuning Recipes

All numbers here are **unmeasured starting points**. No recipe installs
drivers, rents hardware, or loads a model without your execution instruction.
The target installation must offer the flags used. The scripts do not
automatically modify existing server configurations.

## Recipe A: a small single-GPU baseline

Assume Linux or a suitable container, a compatible model, and enough VRAM.
Choose the model revision deliberately; for a local snapshot, record its
provenance in the manifest. Optionally set `MODEL_ALIAS`; otherwise it defaults
to `local-model`.

```bash
export MODEL='ORG/EXACT-MODEL'           # Replace; not an executable example model.
export MODEL_REVISION='EXACT-COMMIT'    # Replace; do not permanently use main.
bash scripts/serve_single.sh             # Prints the plan only.
bash scripts/serve_single.sh --execute   # Loads/serves after explicit approval.
```

The template binds to loopback and starts without remote-code trust, offload,
speculation, a forced kernel, or public administrative access. It sets 8,192
context tokens, 0.85 memory utilization, eight active sequences, and 2,048
batched tokens as a hypothesis; adjust these after checking capacity.
Context includes input **and** output. `GPU_MEMORY_UTILIZATION` is not
OS-level protection against other GPU processes. [S03–S04, S17](28-sources.md)

After startup, inspect the log for the actual backend/KV budget, `/health`,
the model list, and a short chat probe. Then run real quality tasks.
On OOM, consult [Diagnostics](23-troubleshooting.md) first rather than
arbitrarily increasing memory flags.

## Recipe B: demonstrate APC

With an existing server, exactly the same request, and no other load:

```bash
python scripts/stream_probe.py --model local-model \
  --payload configs/cache-request.json --repeat 3 --out apc-probe.json
```

The first run is not necessarily cold if the instance already knows these
tokens. Establish a cold state through a planned test restart or a genuinely
new prefix that remains constant afterward. Do not hide production-cache resets
inside the test. The example prefix is deliberately longer than a short greeting
but is not a quality dataset. [S05–S06](28-sources.md)

When the local CLI offers `--enable-prompt-tokens-details`, use it to check
the corresponding usage extension. Request `include_usage` in the stream.
When `prompt_tokens_details.cached_tokens` is missing, the value remains
unknown; also inspect prefix counters and actually computed prefill tokens.
[S17, S45](28-sources.md)

A/B: APC on/off with constant warmup; identical prefixes; different prefixes;
cache after eviction; multiple tenants with separate salts. Verify content
correctness remains unchanged. Bound output length, or decode can dominate
the timing comparison. Cache hit rate alone is not a speed result.

## Recipe C: high interactive throughput

Plan the official benchmark sweep first, then execute it. Use three concurrency
values around a plausible region and at least one arrival profile. Change only
**one** server parameter at a time: `MAX_NUM_SEQS`, then
`MAX_NUM_BATCHED_TOKENS`. Use a new results directory and warmup for each
configuration. [S15–S16](28-sources.md)

When queues/preemptions rise and p95 worsens, stop increasing concurrency.
Newer native admission controls `--max-num-queued-reqs` and
`--max-num-queued-tokens` can be added after local verification: the first
limits in-flight requests; the second conservatively bounds the prefill token
backlog. The documented overflow behavior is 503. They do not replace tenant
quotas or deadline policies. [S45](28-sources.md)

## Recipe D: CPU KV offload only after an APC baseline

Assume sufficient **actually available host RAM** and a compatible platform.
Choose one variant, not two competing settings simultaneously:

```bash
# Additional locally verified flags at server startup:
# --kv-offloading-size 4 --kv-offloading-backend native
# OR:
# --kv-transfer-config "$(cat configs/kv-offload-native.json)"
```

Four GiB is an illustrative budget; in the documented native path, it applies
across TP workers combined. It is not extra GPU KV/weight memory or a blanket
Spark RAM gain. Measure APC-only against external caching under the same
reuse, load, and eviction conditions. Test store failure and a cold store.
[S03, S07](28-sources.md)

## Recipe E: metrics and light tracing

Adapt the Prometheus template to the process/container network and check it
with `promtool`. Validate the collector template locally; it writes diagnostic
data only and provides no trace-search interface. Add OTLP to the existing
server startup, then use `stream_probe.py --trace` for correlation.
Instrument a complete client span separately. Try detailed traces only after
measuring the simple configuration. [S08–S10, S41, S43](28-sources.md)

## Recipe F: two cards

Model fits on one GPU → compare two independent instances against TP=2.
Model fits only when distributed → check TP/PP with the actual topology;
do not simply divide raw weights by two. Do not assign identical
`CUDA_VISIBLE_DEVICES` values to replicas intended to be separate.
Give each process its own port and memory allocation.
See [Multi-GPU](15-multi-gpu.md).

## Recipe G: Spark or a small rental

Spark: start with the official GB10/Arm playbook, then change the model or
quantization; never blindly reuse a single-x86 image. Rental: record budget
approval, private access, storage lifecycle, boot/load/warmup costs, and the
exit check. See [Spark](17-dgx-spark.md) and [Costs](18-rented-gpus-costs.md).

## Recipe H: quality regression after tuning

Return to the exact previous model/tokenizer/template/parser/quantization
revision. Reproduce the baseline with the same requests. Then change only
weight quantization, KV quantization, the kernel, or sampling defaults.
Validate before measuring further load. Infrastructure gains without the
required quality do not constitute a successful optimization.
