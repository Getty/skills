# 09 — TTFT, ITL, TPOT, and Reliable Load Tests

## Define measurement boundaries first

| Quantity | Meaning in this skill | Common misinterpretation |
|---|---|---|
| Client TTFT | Start of sending until the first meaningful model delta reaches the client | Counting the first HTTP byte or an empty role event as a token |
| First-answer latency / TTFA | Start of sending until the first visible answer-content delta | Treating reasoning tokens as the start of the actual answer |
| Queue time | Waiting time within the explicitly selected queue | Forgetting client/proxy queues |
| ITL | Spacing between actual generated tokens at the chosen measurement boundary | Equating SSE chunk spacing with token spacing |
| TPOT | Time from the first to the last output token / subsequent output tokens | Reporting total time/N, including prefill, as pure decode performance |
| E2E | Start of sending until the result has been fully consumed | Cutting off network/usage/final-event time |
| SLO goodput | Work successfully delivered within all required limits per unit time | Counting every emitted token regardless of errors |

A stream chunk can contain several tokens, only metadata, or just part of a
tool structure. The included probe therefore calls its intervals **delta gaps**,
not ITL. Exact token timing requires appropriate server-side instrumentation
or clearly documented benchmark definitions. [S08–S09, S15–S17](28-sources.md)

For a single output token, TPOT is undefined. Missing values remain
`null`/“unknown,” not zero. Reasoning may appear in a separate field, in content,
or not be emitted at all; a parser error can distort TTFA measurements.
Never mix streaming and non-streaming results in an unlabeled series.

## Two load models instead of one “tokens/s” figure

**Saturation with bounded concurrency:** a fixed number of clients keeps work
available. This exposes batch/memory effects, but the actual offered rate falls
when the server slows down. Real users waiting ahead of the load generator are
not automatically measured.

**Independent arrivals:** new requests arrive at a finite rate or according to
a timestamped trace. This makes overload visible. When a semaphore delays
sending, record its wait separately or include it in user latency. A configured
rate of “100/s” does not prove the generator actually sent 100/s. Check the
generator's CPU and network. [S15–S16](28-sources.md)

## Required matrix for a small instance

| Dimension | Minimum useful variants |
|---|---|
| Input | Short chat, medium document, long realistic context |
| Output | Short tools/JSON, typical answer, long reasoning/code output |
| Reuse | Cold prefix, identical warm prefix, similar but different prefixes |
| Load | Single request, normal concurrency, SLO knee, burst |
| State | Warm model, cold compilation/graph phase separately, cache after eviction |
| Quality | Real tasks, tools, structured output, long context, language |

Specify numeric lengths in the workload contract. Do not automatically execute
every combination: start with a few representative profiles, then targeted
bottleneck experiments. Random tokens test serving mechanics, not language
quality. `--ignore-eos` is useful for controlled output lengths but does not
represent the behavior of every production request. [S16](28-sources.md)

## Tools in the package

```bash
# Stream semantics only, not load. MODEL_ALIAS must match the API.
python scripts/stream_probe.py --model MODEL_ALIAS \
  --payload configs/client-request.json --repeat 2 --out probe.json

# Default: a plan, no requests. --model also provides the tokenizer source.
python scripts/bench_sweep.py --model MODEL_REPO_OR_LOCAL \
  --served-model-name MODEL_ALIAS --mode saturation \
  --concurrency 1,2,4,8 --input-len 1024 --output-len 128 \
  --num-prompts 200 --out experiments/saturation

# Start with --execute only after approval; separate arrival experiment:
python scripts/bench_sweep.py --model MODEL_REPO_OR_LOCAL \
  --served-model-name MODEL_ALIAS --mode arrival --rates 0.5,1,2 \
  --input-len 1024 --output-len 128 --num-prompts 300 \
  --out experiments/arrival
```

Before execution, the sweep checks local help, uses `subprocess` without a
shell, and records the actual commands in its plan. A model alias is not
necessarily a valid Hugging Face tokenizer name. Model/tokenizer downloads,
requests, and GPU time may incur costs during execution. For strictly
reproducible tests, use a local revision-pinned tokenizer/model snapshot;
a moving repository name may otherwise load different tokenizer files.
The wrapper does not silently invent a benchmark revision flag.
API keys are not written to the plan.

For APC, additionally use the official `prefix_repetition` dataset or your own
constant prefixes. Do not present a prefix-repetition test as general production
throughput. Establish the same warmup and cache state for each comparison;
do not expose GPU cache-reset endpoints publicly.

## Analysis and statistical honesty

For each run, preserve the version/hardware/model manifest, input/output
distribution, seed, arrival model, achieved rate, duration, warmup, errors,
and all SLOs. Run multiple repetitions; report mean and variation in goodput
alongside latency distributions. A p99 from 100 requests depends on very few
observations; measure longer and show uncertainty for reliable tails.
Successful requests alone can produce an overly favorable picture.

Do not average p95 values from different instances. Aggregate compatible
histograms appropriately or analyze raw observations together. Do not compare
different prompt distributions as though they were equivalent. Alternate A/B
order to identify temperature, power limits, caches, and competing load as
confounders.

**Approval gate:** quality maintained; SLO goodput improved or costs reduced
at the same SLO; no new instability; rollback reproduces the baseline.
