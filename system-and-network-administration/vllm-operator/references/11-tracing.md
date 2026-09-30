# 11 — OpenTelemetry and End-to-End Request Traces

## What a trace should show

The useful chain is **client → gateway → tokenization/scheduling → model work
→ stream at the client**. Timestamps for tool execution and retrieval help
distinguish whether vLLM or the application is making the user wait.
A single span for the whole request does not provide this separation.
Not every vLLM version exports every internal phase and process as a separate
span by default. Open a sample trace first and compare its boundaries with
logs and metrics. [S10](28-sources.md)

## Getting started locally

The consulted reference uses `--otlp-traces-endpoint`. For a local collector
using OTLP/gRPC, add, for example, the following to an already working serving
setup:

```bash
export OTEL_SERVICE_NAME=vllm-local
export OTEL_EXPORTER_OTLP_TRACES_PROTOCOL=grpc
export OTEL_EXPORTER_OTLP_TRACES_INSECURE=true  # Local testing without TLS ONLY
# Append to the existing validated startup command:
# --otlp-traces-endpoint grpc://127.0.0.1:4317
```

`4317`/gRPC and `4318`/HTTP-Protobuf are different transports. For HTTP, check
the URL required by the exporter, including `/v1/traces`. Inside a container,
`127.0.0.1` refers to **that container**, not another one.
The [collector configuration](../configs/otel-collector.yaml) is a local
diagnostic example with debug export, not a persistent trace backend.
For remote transport, add TLS, authentication, access controls, and defined
retention. [S10](28-sources.md)

The consulted vLLM examples do not universally require the old manually pinned
OpenTelemetry package lists. Check installed dependencies and the image instead
of arbitrarily installing old SDK versions into a working image.

## Propagate context correctly

Send a W3C `traceparent` from a real client span and propagate it through the
gateway; use optional `tracestate` only under your trust/privacy policy.
Do not put API keys or prompts in baggage. Keep the client span open until
the stream is fully consumed or cancelled, not merely until response headers
arrive. Mark timeouts and cancellations as statuses/events.

The `stream_probe.py --trace` probe creates and records a syntactically valid
correlation header. **It does not export a client span itself.** A complete
trace tree needs actual client/gateway instrumentation. A random request-ID
header is not automatically a trace either.

Useful bounded attributes: deployment revision, model alias, workload class,
prompt/completion token counts, cache class, result status, and queue/prefill
time where available. Include end-user identity only after an explicit privacy
decision; never silently attach the entire request body.

## Detail level and sampling

Start by collecting a few ordinary request spans. `--collect-detailed-traces`
with `model`, `worker`, or `all` can provide more detailed timing while adding
work or synchronization costs. Verify supported values and actual spans against
the target version. This is an experiment, not a free always-on switch.
[S03, S10](28-sources.md)

Head sampling may miss rare slow requests; tail sampling can select based on
completed traces but needs memory itself and initially processes more data.
Before broad deployment, measure collector capacity, export queues, drop
counters, and failure behavior. Even with downsampling, collector backlog must
remain bounded and must not dominate inference.

## Four diagnostic questions

**Late client, fast server?** Check DNS/TLS, proxy buffering, network, client
reader, and event parser. **Long queue?** Check admission, scheduler, KV, and
preemption. **Slow prefill?** Check input length, cache misses, CPU tokenizer,
multimodal encoder, and large prefill steps. **Stuttering decode?** Check batch
mix, memory bandwidth, long steps, communication, and thermal limits;
for kernel analysis, see [Profiling](12-profiling.md).

Acceptance: compare tracing off, light tracing, and detailed tracing under
identical warmup and load profiles. Record changes in CPU, TTFT p95, E2E,
throughput, and export loss. Do not invent a universal overhead percentage.
