# Model providers and host-owned LLM calls

Distinguish three tasks: calling the user's selected model for an auxiliary operation, registering a new inference backend, and changing the main agent's request/execution. These map to `ctx.llm`, provider profiles, and middleware respectively.

## Auxiliary calls

Use the [Plugin LLM Access API](https://hermes-agent.nousresearch.com/docs/developer-guide/plugin-llm-access). The host owns active provider/auth resolution. Sync and async chat/structured variants return text, optional parsed content, usage, and attribution.

```python
async def summarize_for_status(ctx, text):
    if not isinstance(text, str) or len(text) > 12000:
        raise ValueError("status input exceeds the supported limit")
    result = await ctx.llm.acomplete(
        messages=[
            {"role": "system", "content": "Summarize the supplied activity in one sentence."},
            {"role": "user", "content": text},
        ],
        max_tokens=100,
        purpose="status-summary",
    )
    return result.text
```

This is an auxiliary-call fragment, not a conversation manager. Do not assume streaming, tool loops, or inherited full history. Explicitly bound inputs and usage. For structured calls, handle missing/invalid parsed output and validate required application fields independently.

Model/provider/auth-profile overrides require the appropriate grants; default use of the selected configuration does not authorize silent account switching. Use an audit purpose that identifies the feature without including user content.

## Inference provider plugins

The [provider guide](https://hermes-agent.nousresearch.com/docs/developer-guide/model-provider-plugin) uses `providers.base.ProviderProfile` and `providers.register_provider`. This loader is distinct from ordinary `register(ctx)`. Use `kind: model-provider` for applicable installed directory packages so discovery selects the right system.

Declare the actual wire API, endpoint, authentication strategy, model catalog, and supported metadata. An OpenAI-compatible HTTP endpoint does not guarantee every OpenAI request field, reasoning control, tool format, or image path.

Register canonical model IDs and truthful capabilities. Missing capability metadata means unknown, not necessarily unsupported. Provider-wide wire capability and per-model ability are different facts.

## Provider engineering checklist

Test non-streaming and streaming responses, tool invocation/results, empty output, structured-output failures, truncation, retries, rate limits, credential refresh, and cancellation. Preserve provider-native error evidence without exposing tokens.

Use the host's existing credential/auxiliary configuration mechanisms. Keep model catalog fetches bounded and provide a deliberate fallback when discovery is unavailable. Do not invent valid model IDs.

For an existing backend needing only a custom endpoint, configuration may be enough. Add a provider plugin when discovery/authentication/wire quirks justify it. Add a core transport only when the supported provider interface cannot truthfully express the protocol.

