# Identity and surfaces

Evidence baseline: 2026-10-04 Europe/Berlin. The official project is [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent). “Hermes” can also mean Nous model families or unrelated software; identify the repository before using this skill.

The official [Hermes Desktop](https://hermes-agent.nousresearch.com/docs/user-guide/desktop) shares the agent core and settings with CLI/gateway, while providing its own native interface. The [Desktop SDK](https://hermes-agent.nousresearch.com/docs/developer-guide/desktop-plugin-sdk) and dashboard extension interface are separate.

## Capability and process matrix

| Surface | Extension ownership | What can execute there | Do not assume |
| --- | --- | --- | --- |
| CLI / noninteractive agent | Python agent process and active profile | Enabled tools, hooks, middleware, skills, configured MCP/providers | An interactive REPL exists during cron, tests, or headless runs |
| Messaging gateway | Long-running Python gateway and connected adapters | Agent turns, platform adapters, native handlers, channel observers, permitted platform actions | Desktop renderer contributions or an automatic Desktop event bridge |
| Telegram / Discord / other client | External service and client UI | Channel-native messages, attachments, buttons, supported interactions | Arbitrary React panes or Hermes filesystem access |
| Desktop renderer | Local native application's frontend | Registered Desktop panes/pages/actions/settings and local preferences | Installation beside a remote agent installs local JS |
| Desktop backend / serve / compute host | Selected Hermes backend | Python plugin API, agent work, host state, supported event transport | Same process as every gateway/cron invocation |
| Web Dashboard | Browser frontend plus dashboard Python server | Dashboard tabs/slots and backend plugin API | Desktop SDK modules execute unchanged |
| MCP server | External process or remote endpoint | MCP tools/resources/prompts | Native Hermes hooks, frontend contribution points, or host credentials |
| Portable Agent Plugin | Host-managed package adapter | Supported skills and MCP components | Full native Python/JS API portability |

The distinctions above combine the primary interfaces with process-level engineering reasoning. Treat them as a design checklist, then verify the running architecture.

## Establish a support claim

Record four versions independently: Hermes backend revision, Desktop build when present, external channel SDK/API, and plugin version. Record OS and install mode too. A current `main` source contract is not proof that a deployed older binary implements it.

Use a matrix such as:

| Target | Native tool | Gateway hook | Desktop UI | Evidence |
| --- | --- | --- | --- | --- |
| Target backend A | Tested / unavailable | Tested / not applicable | Not applicable | Exact revision + test |
| Desktop build B with backend A | Tested | Depends on gateway process | Tested | Build + connection mode |
| Remote backend C | Tested | Tested separately | Local frontend install required | Both host identities |

Avoid unchecked “works everywhere” badges. Probe optional methods, but also test their behavior: an accepted unknown manifest field or warned registration is not an implemented capability.

## Evidence precedence

Use target runtime and tests first, pinned source second, matching official docs third, and mutable overview pages last. Consult [sources](25-sources-and-compatibility.md) for known differences. Preserve uncertainty when release availability is not established.

