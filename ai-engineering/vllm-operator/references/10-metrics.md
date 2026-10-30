# 10 — Prometheus, Dashboards, and GPU Telemetry

## Inventory the running exporter first

`/metrics` is an internal endpoint. Names and semantics evolve. The consulted
documentation sometimes lists counter families without `_total`; Prometheus
exposition may add that suffix. Read **HELP, TYPE, and samples from the target
instance** rather than blindly importing old dashboard JSON. [S08](28-sources.md)

```bash
python scripts/metrics_inventory.py --url http://127.0.0.1:8000/metrics \
  --out metrics-inventory.json
# Alternatively, read an existing safely collected scrape without networking:
python scripts/metrics_inventory.py --file scrape.prom --out inventory.json
```

The script stores names, types, and help text, not label values. When needed,
it reads the API key from `VLLM_API_KEY`. Check locally whether the target
server actually protects metrics with its API key; an API key is no substitute
for network isolation.

## Five dashboard views are enough to start

| View | Relevant documented families | Decision |
|---|---|---|
| User SLOs | Client TTFT, TTFA, E2E, errors/rejections, SLO goodput | Is the service fulfilling its purpose? |
| Engine latency | `time_to_first_token_seconds`, `inter_token_latency_seconds`, `request_time_per_output_token_seconds`, queue/prefill/decode histograms | Where does waiting occur? |
| Pressure | `num_requests_running`, `num_requests_waiting`, `num_requests_waiting_by_reason`, `kv_cache_usage_perc`, `num_preemptions` | Is saturation/recomputation approaching? |
| Work and cache | `prompt_tokens`, `generation_tokens`, `prefix_cache_hits`, `prefix_cache_queries`, external-cache families, `request_prefill_kv_computed_tokens` | How much work is actually avoided? |
| Hardware and host | GPU/VRAM/RAM utilization, power/clocks/temperature, CPU, IO pressure, network/PCIe | Compute, bandwidth, CPU, or thermal limit? |

vLLM families have a `vllm:` prefix. Not every family exists for every engine
or feature. Do not blindly substitute the old `time_per_output_token_seconds`
for the documented `inter_token_latency_seconds`. KV occupancy in
`kv_cache_usage_perc` is documented as a fraction: 1 means 100%.
Cache hits/queries count tokens here, not “requests with any hit.”
[S08](28-sources.md)

## PromQL patterns — verify against a local scrape

```promql
# Server TTFT p95; preserve model boundaries, do not average p95 values.
histogram_quantile(0.95,
  sum by (le, model_name) (
    rate(vllm:time_to_first_token_seconds_bucket[5m])
  )
)

# Output tokens/s (only if the counter is exposed with this name).
sum by (model_name) (rate(vllm:generation_tokens_total[5m]))

# Token-weighted APC hit rate; meaningless when there are zero queries.
sum by (model_name) (rate(vllm:prefix_cache_hits_total[5m]))
/
sum by (model_name) (rate(vllm:prefix_cache_queries_total[5m]))
```

Labels are illustrative: check `model_name` against your exporter and preserve
a low-cardinality service/pool label when monitoring multiple services.
Histogram bucket boundaries must be compatible across compared instances.
The [rule template](../configs/prometheus-rules.yml) makes assumptions explicit
and does not replace validation with `promtool`. Display `NaN`/missing series
as “no data,” not as apparently perfect zero latency.

## Per-request metrics use a different measurement boundary

With `--enable-per-request-metrics`, the consulted documentation describes,
among other fields: `time_to_first_token_ms` starting at scheduling,
**excluding queue time**; `generation_time_ms` from the first to the last
generated output token; `queue_time_ms`; and `mean_itl_ms`, undefined for only
one token. `tokens_per_second` uses time since scheduling and therefore includes
prefill; it is not simply pure decode speed. Test field availability and streaming
responses at the actual endpoint. This feature adds CPU work. [S09](28-sources.md)

Client TTFT includes additional components: connection establishment, gateway,
tokenization, scheduling wait, transport, and buffering. A favorable engine
number cannot disprove poor user latency. Always put the unit, ms or s, in
panel names.

## Operations and privacy

Initially collect NVIDIA telemetry through `nvidia-smi`; add a suitable exporter
as needed. GPU utilization does not mean “95% optimal.” Memory-controller load,
SM load, clocks, and thermal/power throttling can indicate different bottlenecks.
Sampling resolution affects whether brief spikes are visible at all.
Leave unsupported sensors as unknown; a container may not see all host data.

Do not use prompts, user IDs, full URLs, trace IDs, or session IDs as metric
labels. Keep cardinality low, agree retention, and protect access. Base alerts
on sustained user-facing violations or pressure, not one cache miss.
`num_requests_waiting > 0` alone is not an outage.
