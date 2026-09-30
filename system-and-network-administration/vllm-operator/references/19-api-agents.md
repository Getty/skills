# 19 — APIs, Tool Calling, Reasoning, and Fast Agent Loops

## “Compatible” means a tested contract, not identical product features

vLLM provides model- and version-dependent OpenAI-compatible APIs, plus the
integrations described in the consulted documentation for Responses and
Anthropic Messages/Claude Code. Explicitly test the SDK, endpoint, stream
events, token usage, unknown fields, and session semantics. A proxy between
protocols must preserve these distinctions, not merely rewrite the URL and
model name. [S17, S34–S36](28-sources.md)

Create a small contract matrix: `/v1/models`, chat/completion, required
Responses/Messages behavior, streaming, cancellation, errors, tool calls,
usage, cache usage, reasoning, and JSON Schema. Expose only required endpoints.
The package's probe tests **Chat Completions SSE**, not every protocol.

## The tokenizer and chat template are part of the model

A conversation is serialized into tokens before inference. Roles, BOS/EOS,
tool definitions, generation prompts, and reasoning markers must match the
model. A server can start correctly yet produce poor answers or broken tools
because of an incorrect template. Pin the template and tokenizer revision
alongside the model revision. [S17–S18, S20–S21](28-sources.md)

A model's `generation_config.json` can change sampling/default behavior.
This package's baseline deliberately uses `--generation-config vllm` where
supported by the target CLI and explicit request parameters. This does not
eliminate every model-specific requirement; when model defaults are necessary,
restore them explicitly and document them rather than diagnosing a quality
regression as “server slow/broken.” [S17](28-sources.md)

## Tool calling

The parser, template, and model must agree on tool syntax. Enable automatic
tool choice and model-specific parsers only after consulting the applicable
table; do not guess a parser name from a similar model name. Tests must include:
no tool needed, one tool, multiple tools, incorrect/missing arguments, long
arguments, streaming fragments, and a tool response in the next turn.
[S20](28-sources.md)

In the normal chat path, vLLM produces structured tool calls; the application
validates arguments, checks permissions, and executes them. Explicit
Responses/MCP integrations can add server-side tool paths. Isolate these
separately, with authentication/network allowlists, timeouts, and human approval
for relevant side effects. Do not assume everything is harmless text.
[S36](28-sources.md)

For agents, **time to successful task completion** matters, not merely a fast
tool call. A smaller, faster model can cause more error/retry rounds. Measure
model time, tool/retrieval time, number of rounds, success rate, total cost,
and visible progress.

## Structured outputs and logprobs

JSON Schema, grammar, regex, and choice paths are version- and backend-dependent
capabilities. Check `structured_outputs` fields against local API documentation;
do not arbitrarily mix them with older `guided_*` examples. Schema
precompilation, complex grammars, and constrained decoding can change cold
start, CPU work, and per-token work. Still validate syntactically correct JSON
semantically and against permissions. [S19](28-sources.md)

Logprobs, prompt logprobs, and large top-k responses can increase computation,
serialization, and network overhead. Request only what is needed, and do not
confuse interpretation of logprobs with calibrated confidence in factual truth.
Beam/multiple samples consume additional resources; do not enable them as a
supposedly cheap improvement without measurement. [S03, S17](28-sources.md)

## Reasoning and streaming

Reasoning parsers can separate internal model fields from the visible answer.
A model may already be generating substantial output while the user still
sees no actual answer. Track TTFT and TTFA separately; verify token budgets
and cancellation behavior per model. There is no universal `reasoning_effort`
with identical effects on every open-weight model. [S21](28-sources.md)

Consume streams without proxy buffering, tolerate fragmentation, and evaluate
usage through the end of the stream. A network chunk or role event is not a
token. On timeout/cancellation, terminate the upstream; then check whether
the engine slot and KV are also released. Blind retries after a partially
executed tool can duplicate side effects.

## Cache-friendly agent prompts

Stable system content and tools first; volatile timestamps, changing IDs,
and retrieval results later where semantically appropriate. Do not randomize
tool order or JSON serialization. Check cache success through actual tokens
and metrics, not “the text looks the same.” Context compaction can save work
while invalidating the old prefix; measure both effects. Use
[cache layout](06-cache-layout-isolation.md) guidance rather than prompt
restructuring that damages quality.
