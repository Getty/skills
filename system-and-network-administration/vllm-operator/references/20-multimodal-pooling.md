# 20 — Vision, Audio, Video, Embeddings, and Reranking

## Supported architecture plus the appropriate task

Multimodal or pooling capability belongs to the selected model/runner/API
combination. An endpoint name does not turn a text generator into a good
embedder or speech model. Consult the applicable supported-models, multimodal,
pooling, and speech-to-text references together.
[S18, S24–S25, S37](28-sources.md)

## Media make “prompt length” multidimensional

Image count, resolution/tiles, video frames, audio duration, sampling, and the
processor path affect CPU work, encoders, intermediate memory, and resulting
model work. Images can make a request with 200 text tokens expensive.
Alongside token limits, therefore bound bytes, counts, dimensions, duration,
and CPU preprocessing timeouts at the gateway/model level. Do not load
unbounded video frames. [S03–S04, S24](28-sources.md)

Set API/processor limits such as `--limit-mm-per-prompt` only with modality
keys appropriate to the model and locally verified syntax.
`--mm-processor-cache-gb` refers to a different cache from GPU KV. Depending
on worker/API-process architecture, host caches can require multiple copies
in memory. Measure multimodal encoder caches, processor caches, and decoder
prefix caches separately. [S03–S04](28-sources.md)

Use reuse through stable media IDs/UUIDs only when the applicable API supports
it and the identity genuinely belongs to the content. Prevent collisions,
stale media, and intentional cross-tenant ID reuse. Changing the resize or
processor path can affect cache compatibility.

## Media are also a security boundary

Server-side fetching of arbitrary media URLs can reach internal networks or
metadata services. Allowlists, a controlled fetcher, DNS/redirect controls,
and egress rules are important countermeasures. Allow local file paths only
within explicitly approved directories; do not expose sensitive mounts to
model input. Bound decompression, oversized-image, and long-audio risks with
size limits and parser isolation. [S24, S27](28-sources.md)

## Audio/video tests

For STT, check accuracy for your languages, accents, and noise conditions,
along with duration, segment boundaries, time to first transcript, and final
latency. The real-time factor `processing_time / audio_duration` is not chat
tokens/s. Streaming transcription and batch uploads are separate contracts;
not every model class supports both. Claim generative audio/speech output
only with specific model/endpoint evidence. [S37, S18](28-sources.md)

For vision/video, consider task quality, the image/frame pipeline, and decoder
versus encoder latency separately. Text-only load benchmarks do not demonstrate
multimodal capacity. Mixed loads can interfere through CPU, encoders, and shared
GPU memory.

## Embeddings, pooling, reranking

Suitable pooling models can provide embedding-specific outputs, classification,
scoring, or token pooling. Take embedding dimensions, normalization, pooling
method, prefix instructions, and maximum length from the model documentation.
A generative model with pooling can technically produce a vector without being
suitable for retrieval. [S25](28-sources.md)

Here, vLLM is the **inference service**, not the vector database, chunking
pipeline, or relevance evaluation. After changing the embedding model,
dimensions, or normalization, generally build a new compatible index; do not
silently mix incompatible vectors. Reranking cross-encoders score query-document
pairs; the number and length of pairs are separate load dimensions.

On small hardware, separate the generator and embedder/reranker by time or
into dedicated small processes/instances when shared VRAM causes OOM or
interference. A single standard serving process is not an arbitrary simultaneous
multi-base-model server. [S17–S18, S25](28-sources.md)

## Acceptance

Document modality-specific quality; actual CPU/encoder/decoder timing;
bytes, lengths, and counts; peak RAM/VRAM; cache types; errors from oversized
or invalid media; and rate limiting. Do not retain sensitive media as
permanent benchmark outputs. Reporting only text metrics would be incomplete.
