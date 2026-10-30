# 02 — Capabilities, Combinations, and Limits

## Compatibility is an intersection

```text
Working feature = release ∩ platform ∩ model architecture ∩ task
                  ∩ quantization format ∩ attention backend ∩ parallelism
                  ∩ template/parser ∩ API behavior
```

A check mark in a model list does not replace this verification. Record a status
and test for each combination in `templates/compatibility-matrix.md`.
The following map describes feature families, not a guarantee for every piece
of hardware. [S02, S12, S14, S18](28-sources.md)

| Family | vLLM's role | Important boundary / evidence |
|---|---|---|
| Text/chat generation | Online and offline, streaming, sampling | Check chat template and stop/EOS behavior |
| Structured output | Constrain model output with a schema/grammar | Syntactic validity does not imply factual correctness |
| Tools | Structure and parse tool outputs | Model quality and parser; tool permissions are a separate concern |
| Reasoning | Model-dependent separation/streaming of reasoning and answer | No universal switch makes every model reasoning-capable |
| Embeddings/pooling | Suitable models for embeddings, scores, classification, etc. | Not every generator is a good embedder |
| Vision/audio/video | Model-dependent input/output paths | Check media limits, encoders, processors, and APIs |
| Prefix caching | Reuse compatible KV prefixes | Requires an exact prefix and matching cache identity |
| External KV | CPU/other tiers, connectors, transfer | Not unlimited fast GPU memory |
| Quantization | Execute supported weight and KV formats | A supported format and a fast kernel are separate requirements |
| Speculative decoding | Verify proposals, generate multiple tokens per step | Support, acceptance, extra memory, and load determine the outcome |
| LoRA | Serve multiple adapters for a compatible base model | Not automatic fine-tuning |
| Multi-GPU | TP/PP/DP/EP and context-specific distribution | Check topology, model partitionability, and collectives |
| Monitoring | Metrics, traces, profilers, specialized KV/graph metrics | Overhead, privacy, and metric migration |
| Lifecycle | Model loading, sleep, restore, weight replacement in specialized workflows | Not a complete multi-model orchestrator |
| RL integration | Rollouts/inference and weight transfer for training systems | Optimizers/backpropagation belong to the training stack |

Details: [S17–S26, S28, S33, S38](28-sources.md).

## Treat API boundaries as version-dependent

Chat Completions, Completions, and Responses are different contracts.
The consulted vLLM documentation also describes an Anthropic Messages
integration and Responses with MCP tools. This does **not** imply identical
support for every cloud API feature, billing field, session semantic, or SDK.
Proxies in particular must test unknown-field handling, streaming events,
and usage fields. [S17, S34–S36](28-sources.md)

“vLLM never executes tools” would be too broad: ordinary chat tool calling
produces tool calls for the application; explicitly configured Responses/MCP
integrations can include additional tool-execution paths. Allow these paths
only after an isolated functional test and with a separate security model.

## What is not included automatically

vLLM does not make a weak model more knowledgeable, provide reliable long-term
agent memory, deliver a universal RAG pipeline, or guarantee freedom from
hallucinations. Raising a context limit does not train better long-context
capability. A structured tool call proves neither correct arguments nor safe
execution.

A single serving process does not replace a full product gateway with tenant
quotas, billing, retry budgets, prioritization, dataset versioning, and quality
evaluation. Surrounding projects may provide these functions; for a small
server, initially add only what is actually needed.

## Decision order

First “correct answers and API behavior,” then “fits with a reserve,” then
“good single-request performance,” then “good load curve,” and finally
“additional specialized optimizations.” For an unsupported feature, provide
an alternative and an explicit `not verified` status, not an invented CLI flag.
