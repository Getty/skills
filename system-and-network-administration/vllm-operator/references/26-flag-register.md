# 26 — Flag Register: Effects and Consequences

**Not a complete copy-and-paste configuration.** These tables connect the
consulted feature families with decisions. Before execution, check
`vllm serve --help=all` (or `--help` when necessary) and structured configuration.
Do not mix values from `stable`/`latest` with old V0 tutorials; many defaults
are derived from hardware or usage. Sources: [S03, S45](28-sources.md), plus
the relevant subject reference.

## Identity, model, and API

| Option/family | Effect | Consequence/gate |
|---|---|---|
| Positional model / `--revision` | Model and weight revision | Record the exact revision rather than a moving main |
| `--tokenizer`, `--tokenizer-revision` | Tokenization | Must match template/model/cache |
| `--served-model-name` | API alias(es) | Not a new model; account for metrics aliases |
| `--dtype` | Base weight/compute dtype | Hardware/quantization path; start with auto |
| `--quantization` | Select a supported quantization path | Checkpoint and kernel must match |
| `--generation-config` | Model/vLLM generation defaults | Make quality/sampling changes explicit |
| `--chat-template` | Conversation serialization | Roles, tools, BOS/EOS, cache identity |
| `--enable-auto-tool-choice`, `--tool-call-parser` | Parse automatic tool selection | Model/parser/template contract |
| `--reasoning-parser` | Process reasoning fields | Model-dependent; measure TTFA separately |
| `--structured-outputs-config` | Configure the constraint backend | Check schema features/cold start/CPU |
| `--trust-remote-code` | Allow third-party code from model integration | Only after explicit code/supply-chain review |
| `--enable-prompt-embeds` | Accept embeddings as input | Shapes/trust; not a public default |

## Memory and caching

| Option/family | Effect | Consequence/gate |
|---|---|---|
| `--max-model-len` | Context limit | Input + output; does not train long-context capability |
| `--gpu-memory-utilization` | Executor's GPU memory-budget fraction | No hard protection from other processes |
| `--kv-cache-memory-bytes` | Explicit KV budget | Check documented precedence over automatic profiling |
| `--kv-cache-memory` | Alternative appearing in newer guidance | Use **only** when the local CLI actually recognizes it |
| `--kv-cache-dtype` | KV format | Scales, kernel, model quality; not the weight dtype |
| `--block-size` | KV allocation block | Backend-dependent; padding/sharing/connector alignment |
| `--enable-prefix-caching` | APC | Reusable prefill, not a response cache |
| `--prefix-caching-hash-algo` | Hashing/serialization path | Choose cryptography/determinism deliberately for tenants |
| Request field `cache_salt` | Sharing namespace | Trusted gateway; not an authentication substitute |
| `--kv-offloading-size` | External CPU KV budget | Check the applicable summed-across-TP semantics |
| `--kv-offloading-backend` | Native/LMCache path | Options/versions are not all interchangeable |
| `--kv-transfer-config` | Connector/transfer configuration | Separate stores, security, failure testing |
| `--cpu-offload-gb` | Weight-offload budget | Potential recurring transfers/host pressure |
| `--offload-backend` | Weight-offload implementation | auto/prefetch/uva, etc.; only locally supported paths |
| `--disable-hybrid-kv-cache-manager` | Affect hybrid-aware allocation | Do not blindly set for presumed compatibility |

## Scheduler and parallelism

| Option/family | Effect | Consequence/gate |
|---|---|---|
| `--max-num-seqs` | Active sequences per step | Batch amortization versus KV/ITL |
| `--max-num-batched-tokens` | Token work per iteration | Prefill speed versus step duration/decode smoothness |
| `--max-num-scheduled-tokens` | Limit scheduling budget | Includes room for additional speculative work |
| `--enable-chunked-prefill` | Split long prefills | Support/activation depend on model/usage |
| `--max-num-queued-reqs` | Limit in-flight requests (waiting + running) | Despite the name, not just the queue; 503 at the limit |
| `--max-num-queued-tokens` | Conservative prefill token backlog | Native TTFT admission control, not a tenant quota |
| `--scheduler-reserve-full-isl` | Check complete input fit before admission | Less over-admission, potentially more initial waiting |
| `--watermark` | Keep a fraction of KV blocks free for admission | Reserve versus immediately usable capacity |
| `--scheduling-policy` | fcfs/priority | No automatic fair allocation among customers |
| `--async-scheduling` | Decouple host/scheduler work | Check the support matrix and measure effects |
| `--stream-interval` | Bundle multiple tokens per stream emission | Less host work versus larger visible deltas/TTFT |
| `--tensor-parallel-size` | Tensor distribution | Head divisibility, collectives, P2P |
| `--pipeline-parallel-size` | Distribute layer stages | Pipeline bubbles, load balance |
| `--data-parallel-size` / DP family | Replication/DP execution | Check routing, processes, and model-specific path |
| `--enable-expert-parallel` / EP family | MoE expert distribution | All-to-all/network/expert balance |

## Kernels, multimodal workloads, and adapters

| Option/family | Effect | Consequence/gate |
|---|---|---|
| `--attention-backend` or the applicable backend configuration | Attention implementation | Check CLI/release form; no universal kernel choice |
| `--enforce-eager` | Force eager execution instead of the graph path | Diagnostic; can increase runtime costs |
| `--compilation-config` | Compilation/capture parameters | Startup time, graph memory, shape coverage |
| `--speculative-config` | Proposal/verification method | Acceptance, extra memory, quality, and load |
| `--limit-mm-per-prompt` | Modality counts/conditions | Model/API syntax; also bound bytes/duration |
| `--mm-processor-cache-gb` | CPU multimodal processing cache | Not GPU KV; account for process multiplication |
| `--allowed-local-media-path` | Allow local media files | Minimal safe path; no sensitive mounts |
| `--enable-lora`, `--lora-modules` | Adapter serving | Compatible base model and controlled artifacts |
| `--max-loras`, `--max-lora-rank`, `--max-cpu-loras` | Adapter capacities | Do not confuse active and resident adapters |
| `--enable-sleep-mode` | Allow memory-release paths | Secure drain/wake and any development endpoints |

## Observability and access

| Option/family | Effect | Consequence/gate |
|---|---|---|
| `--host`, `--port`, `--uds` | Network/socket binding | Private/loopback first; account for namespaces |
| `--api-key` | Authenticate certain API paths | **Not all** paths are protected; check `/invocations`, among others |
| `--enable-prompt-tokens-details` | Additional prompt usage | Test usage/cache fields at the actual endpoint |
| `--enable-per-request-metrics` | Request timings in responses | Queue boundaries/units, CPU costs |
| `--per-request-spec-decode-metrics` | Acceptance metrics | Experimental format, additional data/overhead |
| `--otlp-traces-endpoint` | OTLP export | gRPC/HTTP, TLS, collector backpressure |
| `--collect-detailed-traces` | More detailed model/worker timing | Potentially expensive/blocking; enable only after measurement |
| `--profiler-config` | PyTorch/other profiler paths | Internal start/stop functions and large trace files |
| `--kv-cache-metrics`, `--kv-cache-metrics-sample` | Sample KV residency | Overhead, statistics prerequisite, sampling effects |
| `--cudagraph-metrics` | Observe capture/padding paths | Additional diagnostic data |
| `--enable-layerwise-nvtx-tracing` | Layer/shape NVTX | Documented limitation with CUDA Graphs |
| `--jit-monitor-mode`, `--jit-monitor-verbose` | Observe compilation after warmup | Warnings/logs can become expensive |
| `--enable-log-requests`, `--enable-log-outputs` | Request/output logging | Privacy; DEBUG can include prompts |
| `--disable-log-stats` | Affect statistics collection/output | Dependent metrics may be missing |

## Upgrade trap

Do not silently remove an unavailable flag when that would remove the intended
safety/SLO property. Stop the experiment, identify the required semantics,
and choose a demonstrably equivalent alternative. Record new defaults or
`auto` choices in logs. Repeat quality, cancellation, isolation, and load tests
after API, backend, or cache-layout changes.
