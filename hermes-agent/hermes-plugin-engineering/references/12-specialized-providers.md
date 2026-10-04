# Specialized providers

Use the provider interface that owns the resource. Avoid implementing a second independent tool when the desired behavior is a replacement backend for an existing Hermes capability.

| Extension | Primary guide | Verify before coding |
| --- | --- | --- |
| Image generation/editing | [Image provider](https://hermes-agent.nousresearch.com/docs/developer-guide/image-gen-provider-plugin) | `ImageGenProvider`, `ctx.register_image_gen_provider`, input modalities, reference-image limits, output/error helpers |
| Video generation | [Video provider](https://hermes-agent.nousresearch.com/docs/developer-guide/video-gen-provider-plugin) | Generation/polling contract, long-running jobs, output lifecycle |
| Web search/extraction | [Search provider](https://hermes-agent.nousresearch.com/docs/developer-guide/web-search-provider-plugin) | Search versus extraction, normalized results, fallback and provider selection |
| Browser session backend | [Browser provider](https://hermes-agent.nousresearch.com/docs/developer-guide/browser-provider-plugin) | Session creation, CDP endpoint ownership, reconnect, closing remote resources |
| Terminal environment | [Terminal provider](https://hermes-agent.nousresearch.com/docs/developer-guide/terminal-environment-plugin) | Environment lifecycle, workspace/files, command behavior, timeouts, cleanup |
| Speech | [Plugin extension map](https://hermes-agent.nousresearch.com/docs/user-guide/features/plugins) | Config-driven command provider versus Python TTS/transcription registrar |

These are independent extension contracts. Availability of an image backend does not imply that a messaging platform can deliver its output or that the selected model accepts images.

## Provider selection method

Identify the existing tool and its expected result envelope. Read the installed ABC and a matching maintained implementation. Implement the minimal required members, then opt into optional capabilities only when the backend supports them.

Keep provider identifiers stable. Scope state and credentials to the active profile. Make availability checks fast and passive, and keep initialization separate from operations that allocate billable resources.

## Media flow

For image/audio/video work, record the complete path: input reference, download/cache, preprocessing, provider call, local/remote output, agent-visible result, and channel delivery. A path on a remote gateway is not a path a local Desktop renderer can read.

Use artifact references with explicit lifetimes. Avoid buffering unbounded media in memory. Test invalid MIME, unsupported format, oversized input, cancelled generation, expired URLs, and partial upload.

Speech input involves transcription before the agent receives text. Speech output involves synthesis and channel-specific attachment formatting after generation. A `pre_transcription` hook can steer documented transcription fields; it is not a universal audio-filter API.

## Execution environment flow

For remote terminals and cloud browsers, design ownership: who creates a resource, who pays, what survives interruption, and who deletes it? Preserve the host approval path before actions execute. A custom environment must not silently replace the configured account or convert a denied command into remote execution.

## Minimal practical fallback

Use a command-configured speech tool when its argv template expresses the backend cleanly. Use MCP when the capability already has a suitable server. Use a native provider when replacing the host's existing backend is the actual objective. Keep unsupported features visible instead of claiming every provider has feature parity.

