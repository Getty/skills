# 06 — Agent Prompts, Stable Prefixes, and Isolation

## Prompt layout for recurring work

A useful starting point is:

```text
stable system rules
consistently serialized tool definitions
stable project/document context, where semantically appropriate
previous unchanged conversation history
new question, new observation, dynamic time/request data
```

This is an application architecture, not a vLLM requirement. Do not compromise
the semantic instruction hierarchy for cache hits. Required current-time
information can go in a suitable dynamic position; incorrect or stale information
must not be retained for performance reasons.
Reuse fundamentals: [S05–S06](28-sources.md).

Stable tool ordering and consistent serialization help where the chat template
renders them as text/tokens. A proxy must not insert random IDs, timestamps,
or changing tool descriptions before a large stable prefix on every call.
Equivalent JSON semantics do not imply an identical tokenized prompt.

## Multi-turn conversations are not automatically append-only

Some templates close assistant messages differently from the output already
generated. Tool results, reasoning blocks, compaction, changed system prompts,
or additional BOS/EOS markers can alter earlier tokens. Inspect the **rendered
token sequence**, not just the chat JSON. Always test prefix stability with
exactly the same tokenizer, template, and template options. [S17, S20–S21](28-sources.md)

For a RAG call, newly retrieved documents are often dynamic. Stabilizing their
order must not distort relevance or source attribution. With ordinary APC,
an identical document section after a different query is not a freely
positionable cached fragment. Specialized external reuse/blending methods are
separate extensions that require evaluation, not a standard guarantee.

## Tenant boundaries

`cache_salt` limits reuse to requests with a matching salt. Use a namespace
derived by the gateway for a tenant or trust group; do not blindly accept
an arbitrary user-supplied value. The same salt within a legitimate group enables
sharing; different salts reduce cross-tenant reuse. [S06](28-sources.md)

A salt is not authentication, encryption, or complete side-channel protection.
Hardware and scheduling remain shared. Strict isolation may require separate
processes/GPUs. For external KV, additionally plan access control, TTL/deletion,
transport, disk permissions, and versioning.

Cryptographic hashing is the conservative multi-tenant choice. Do not treat
faster non-cryptographic variants as a free optimization. The CLI documents
SHA and xxHash variants; check support and defaults locally. [S03](28-sources.md)

## Replicas: affinity with an escape route

Round-robin routing can distribute related requests across cold cache pools.
A stable routing decision based on model, tenant, and session/prefix group can
help. It must not permanently bind requests to an overloaded replica.

Practical design: select a preferred replica; check queue/deadline limits;
fail over to a healthy peer under overload; mark the cold cache as an expected
consequence. Affinity and cache salts solve different problems. A cache-aware
router requires actual cache/queue information or a clearly identified heuristic.

## Test matrix

Test matching/different salts; LoRA changes; tokenizer/template changes;
media IDs with unchanged and changed content; cache eviction; replica changes;
and session compaction. Expected outcome: no incorrect response reuse,
no mixed-up media, and explainable changes in hit rate.
Never weaken privacy boundaries to improve a global hit-rate figure.
