# Sources and compatibility

Reviewed: **2026-10-04, Europe/Berlin**. Sources are primary NousResearch documentation and source unless otherwise marked.

## Evidence baseline

Pinned Hermes source: [158fd638da1629c8e62caf9ade1515d162def8ab](https://github.com/NousResearch/hermes-agent/commit/158fd638da1629c8e62caf9ade1515d162def8ab), observed main commit dated 2026-10-03 UTC. Mutable docs were read alongside source. This pin is a reference baseline, not a required user version.

No live Hermes agent, production gateway, Telegram bot, or Desktop binary was operated while authoring this skill. Code examples are original, narrowly scoped illustrations of retrieved contracts. Host/API availability must be checked on the user's target build. In particular, documentation for current main can describe features newer than an installed release.

## Primary documentation registry

| Source | URL and purpose |
| --- | --- |
| Project identity | [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent) |
| Native plugin design | [Build a Hermes Plugin](https://hermes-agent.nousresearch.com/docs/developer-guide/plugins) — entry points, contracts, discovery, doctor, dependencies |
| Plugin operation | [Plugins](https://hermes-agent.nousresearch.com/docs/user-guide/features/plugins) — activation, permissions, install/pins |
| Event catalog | [Hooks](https://hermes-agent.nousresearch.com/docs/user-guide/features/hooks) — precise events and shell/gateway distinctions |
| Telemetry | [Observer Hooks](https://hermes-agent.nousresearch.com/docs/developer-guide/observer-hooks) — request/turn/session correlation |
| Behavior changes | [Middleware](https://hermes-agent.nousresearch.com/docs/developer-guide/middleware) — request/execution contracts |
| Child execution | [Subagent lifecycle](https://hermes-agent.nousresearch.com/docs/developer-guide/subagent-lifecycle-api) — parent context, handles, cancellation |
| Auxiliary inference | [Plugin LLM Access](https://hermes-agent.nousresearch.com/docs/developer-guide/plugin-llm-access) |
| Skills | [Creating Skills](https://hermes-agent.nousresearch.com/docs/developer-guide/creating-skills) |
| CLI | [Extending the CLI](https://hermes-agent.nousresearch.com/docs/developer-guide/extending-the-cli) |
| MCP | [MCP integration](https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp) |
| Inference providers | [Model provider](https://hermes-agent.nousresearch.com/docs/developer-guide/model-provider-plugin) |
| Memory | [Memory provider](https://hermes-agent.nousresearch.com/docs/developer-guide/memory-provider-plugin) |
| Context | [Context engine](https://hermes-agent.nousresearch.com/docs/developer-guide/context-engine-plugin) |
| Secrets | [Secret source](https://hermes-agent.nousresearch.com/docs/developer-guide/secret-source-plugin) |
| Images | [Image provider](https://hermes-agent.nousresearch.com/docs/developer-guide/image-gen-provider-plugin) |
| Video | [Video provider](https://hermes-agent.nousresearch.com/docs/developer-guide/video-gen-provider-plugin) |
| Search | [Web search provider](https://hermes-agent.nousresearch.com/docs/developer-guide/web-search-provider-plugin) |
| Browser | [Browser provider](https://hermes-agent.nousresearch.com/docs/developer-guide/browser-provider-plugin) |
| Terminal | [Terminal environment](https://hermes-agent.nousresearch.com/docs/developer-guide/terminal-environment-plugin) |
| Local app gating | [Application declarations](https://hermes-agent.nousresearch.com/docs/developer-guide/plugins/application-declarations) |
| Gateway | [Messaging Gateway](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/) |
| Adapter plugins | [Adding Platform Adapters](https://hermes-agent.nousresearch.com/docs/developer-guide/adding-platform-adapters) |
| Telegram | [Telegram guide](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/telegram) |
| Discord | [Discord guide](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/discord) |
| Slack | [Slack guide](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/slack) |
| WhatsApp linked device | [Bridge guide](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/whatsapp) |
| WhatsApp Business | [Cloud API guide](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/whatsapp-cloud) |
| Signal | [Signal guide](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/signal) |
| Official Desktop | [Desktop product guide](https://hermes-agent.nousresearch.com/docs/user-guide/desktop) |
| Native UI | [Desktop SDK](https://hermes-agent.nousresearch.com/docs/developer-guide/desktop-plugin-sdk) |
| Web UI | [Extending Dashboard](https://hermes-agent.nousresearch.com/docs/user-guide/features/extending-the-dashboard) |
| Distribution | [Catalog submission](https://hermes-agent.nousresearch.com/docs/developer-guide/plugins/catalog-submission) |
| Portable upstream format | [Agent Plugins](https://agent-plugins.org/) — portable specification, separate from native Hermes |

## Pinned source registry

Use the same commit for related files rather than mixing revisions. The links below deliberately retain that pin.

| Source path | Reason to inspect |
| --- | --- |
| [hermes_cli/plugins.py](https://github.com/NousResearch/hermes-agent/blob/158fd638da1629c8e62caf9ade1515d162def8ab/hermes_cli/plugins.py) | PluginContext, accepted hooks, native handlers, capabilities, injection |
| [hermes_cli/plugins_manifest.py](https://github.com/NousResearch/hermes-agent/blob/158fd638da1629c8e62caf9ade1515d162def8ab/hermes_cli/plugins_manifest.py) | Additive manifest parser and metadata |
| [hermes_cli/plugins_state.py](https://github.com/NousResearch/hermes-agent/blob/158fd638da1629c8e62caf9ade1515d162def8ab/hermes_cli/plugins_state.py) | Scoped settings, durable JSON, locking |
| [hermes_cli/middleware.py](https://github.com/NousResearch/hermes-agent/blob/158fd638da1629c8e62caf9ade1515d162def8ab/hermes_cli/middleware.py) | Execution-chain error and single-use behavior |
| [hermes_cli/plugin_capabilities.py](https://github.com/NousResearch/hermes-agent/blob/158fd638da1629c8e62caf9ade1515d162def8ab/hermes_cli/plugin_capabilities.py) | Actual declared capability IDs and enforcement mapping |
| [hermes_cli/platform_actions.py](https://github.com/NousResearch/hermes-agent/blob/158fd638da1629c8e62caf9ade1515d162def8ab/hermes_cli/platform_actions.py) | Narrow verbs, supported platforms, process/profile gates |
| [gateway/session.py](https://github.com/NousResearch/hermes-agent/blob/158fd638da1629c8e62caf9ade1515d162def8ab/gateway/session.py) | Canonical session key and persistence boundary |
| [gateway/platforms/event.py](https://github.com/NousResearch/hermes-agent/blob/158fd638da1629c8e62caf9ade1515d162def8ab/gateway/platforms/event.py) | MessageEvent and source metadata |
| [gateway/platforms/base.py](https://github.com/NousResearch/hermes-agent/blob/158fd638da1629c8e62caf9ade1515d162def8ab/gateway/platforms/base.py) | Adapter lifecycle and native handler wiring |
| [plugins/platforms/telegram/adapter.py](https://github.com/NousResearch/hermes-agent/blob/158fd638da1629c8e62caf9ade1515d162def8ab/plugins/platforms/telegram/adapter.py) | Current Telegram implementation/location |
| [tools/send_message_tool.py](https://github.com/NousResearch/hermes-agent/blob/158fd638da1629c8e62caf9ade1515d162def8ab/tools/send_message_tool.py) | Host outbound helpers and absent normal model registration |
| [Desktop contribution context](https://github.com/NousResearch/hermes-agent/blob/158fd638da1629c8e62caf9ade1515d162def8ab/apps/desktop/src/contrib/plugin.ts) | Native PluginContext and plugin interface |
| [Desktop contribution types](https://github.com/NousResearch/hermes-agent/blob/158fd638da1629c8e62caf9ade1515d162def8ab/apps/desktop/src/contrib/types.ts) | Contribution fields and nonreactive when semantics |
| [Desktop runtime loader](https://github.com/NousResearch/hermes-agent/blob/158fd638da1629c8e62caf9ade1515d162def8ab/apps/desktop/src/contrib/runtime-loader.ts) | Local load, module evaluation, enablement, error isolation |
| [Desktop SDK exports](https://github.com/NousResearch/hermes-agent/blob/158fd638da1629c8e62caf9ade1515d162def8ab/apps/desktop/src/sdk/index.ts) | Public import inventory |
| [Desktop root reconciliation](https://github.com/NousResearch/hermes-agent/blob/158fd638da1629c8e62caf9ade1515d162def8ab/apps/desktop/electron/desktop-plugins-root.ts) | App-level local root and unified copies |
| [Desktop plugin API client](https://github.com/NousResearch/hermes-agent/blob/158fd638da1629c8e62caf9ade1515d162def8ab/apps/desktop/src/api/plugins.ts) | Connection/profile REST and OAuth socket limitation |
| [Plugin events](https://github.com/NousResearch/hermes-agent/blob/158fd638da1629c8e62caf9ade1515d162def8ab/hermes_cli/plugin_events.py) | Event validation and per-process delivery |

## Known moving boundaries

- Overview pages contain stale hook counts. Use the actual event catalog and accepted set; do not hardcode a count.
- Older paths for Telegram and split core helpers no longer identify current implementations. Prefer documented facades over private imports.
- Native and portable MCP examples can use different historical name spellings. Discover actual names from the target host.
- The Desktop docs' minimal interface omits some additive source fields; source also maps an additional development JSX runtime import. Examples here use the conservative documented import subset.
- Desktop `when()` is not an independent reactive subscription, and disabled module inventory may still evaluate ESM before skipping registration.
- Standalone gateway/cron events do not imply Desktop delivery. OAuth remote plugin sockets need a fallback.
- Manifest schema version, advisory API metadata, package version, backend version, Desktop build, and portable-spec version are separate.
- Portable-format publication labels have differed between the rendered specification and versioned source. Check schema/implemented subset rather than inferring support from a label.

## Refresh procedure

Capture the user's target versions. Read the linked relevant docs, resolve a current immutable source revision, compare the actual interfaces, then run a behavioral test on each requested surface. Update only changed references and their support evidence; preserve old-state compatibility notes.

Treat this skill's recommendations as engineering judgment unless explicitly tied to an upstream contract. Do not convert an untested inference or a source-only capability into a deployed support guarantee.

