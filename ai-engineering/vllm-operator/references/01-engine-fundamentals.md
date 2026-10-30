# 01 — From HTTP Request to Token

## The execution model

A request roughly passes through the network/gateway, API validation, chat
rendering and tokenization, optional media preprocessing, scheduler, prefill,
decode, and detokenization/streaming. Depending on the version, the frontend,
engine, and GPU workers run as separate processes. A GPU can therefore be idle
while an HTTP request takes a long time. Background: [S17, S39](28-sources.md).

**Prefill** computes states for the input. A new long context can involve
substantial parallel matrix computation. **Decode** extends sequences
autoregressively. At small batch sizes, a single decode step can be heavily
limited by memory movement and launch overhead. This is a bottleneck hypothesis,
not a universal classification: architecture, context, batch size, quantization,
and kernels can shift the dominant bottleneck.

**Continuous batching** means completed sequences free capacity and new work
can enter ongoing iterations. It does not imply unlimited concurrency or
guaranteed fairness. More simultaneous sequences amortize work but require
KV memory and can reduce per-user speed. [S04](28-sources.md)

## PagedAttention and KV

Attention uses the keys and values of earlier positions. The KV cache avoids
fully recomputing these states for every token. Block-based management addresses
the data logically without requiring a large contiguous allocation for each
request's maximum context from the outset. This makes memory more usable;
it does not eliminate attention computation.

In a conventional full-attention model, state requirements grow with active
context tokens. A GQA model can have substantially fewer KV heads than query
heads. Sliding-window and hybrid models require a different memory model.
See [04](04-memory-capacity.md) and [S29](28-sources.md).

An allocated KV pool is not the same as data currently used by active requests.
Free, reusable, pinned, and actively referenced blocks have different meanings.
A high VRAM reading after startup is therefore not evidence of a leak.
Consider activity, pool occupancy, and preemption together.

## Three practical cost models

**Request latency:**

```text
Client TTFT ≈ network/proxy + rendering/tokenization + queue + prefill + first decode/flush
Client E2E ≈ client TTFT + remaining generation + final transport/completion
```

These sums are a diagnostic model. Stages can overlap, and specific metrics
can use different starting points. Adding the p95 values of individual stages
does not produce the p95 of total latency.

**Memory:**

```text
Available budget = weights + runtime/graphs/activations + KV + media + reserve
```

**Utilization:** A GPU percentage does not guarantee useful throughput.
Recomputation, padding, or unsuitable kernels can keep a GPU busy while it
produces few SLO-compliant answers.

## Consequences for small systems

A small model with enough KV budget can usefully serve more concurrent users
than the largest model that barely starts. A larger prompt not only creates
prefill work but can also reduce available concurrency until the request ends.
A long reasoning output occupies resources even while the interface shows
nothing yet.

Start troubleshooting with a timeline and three questions: Is work waiting?
Is computation happening? Are data being transferred? Derive an experiment
from the answers rather than maximizing batch size or memory allocation blindly.

## Naming trap

Engine **V1** is not the same as **Model Runner V2**. The v0.29.0 release listing
names MRV2 as the default with exceptions. Older statements about V0 swapping,
speculation, or metric names may no longer apply. [S01, S39](28-sources.md)
