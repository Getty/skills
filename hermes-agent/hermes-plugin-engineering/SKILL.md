---
name: hermes-plugin-engineering
description: "Use when extending NousResearch Hermes Agent — a plugin, tool, hook, middleware, provider, gateway or Telegram adapter, or a Desktop/Dashboard extension."
---

# Hermes Plugin Engineering

## Operating method

Treat this as an engineering map. Load only the references needed for the current integration. Keep the implementation generic: derive profiles, paths, credentials, hosts, and channel identifiers from the target deployment.

1. Identify the product and build: NousResearch **Hermes Agent**, official Desktop if applicable, backend revision, frontend build, Python/dependency manager, OS, active profile, and local versus remote connection. Start with [identity and surfaces](references/01-identity-and-surfaces.md).
2. State the intended behavior and where it must execute. Select an extension point before designing a package: agent tool, command, observer, middleware, provider, messaging adapter, native channel handler, Desktop contribution, dashboard contribution, or external MCP server.
3. Check the relevant primary source and the target build. The dated snapshot in [sources and compatibility](references/25-sources-and-compatibility.md) is an orientation baseline, not a claim about every installed release.
4. Write an extension contract: inputs, return shape, process, lifecycle, profile/session identity, permission checks, persistent state, dependencies, failure behavior, and testable acceptance criteria.
5. Implement the smallest end-to-end slice. Keep import/registration fast; validate untrusted inputs; use public host facades instead of private agent references.
6. Test in an isolated profile/home with deliberate negative cases. Verify the actual requested surfaces, restart/reconnect, missing capabilities, and concurrent sessions. See [evaluation](references/23-evaluation-and-release-checks.md).
7. Package with an immutable source reference, documented support matrix, and reversible state migration. Report what was exercised, what was source-verified, and what remains unverified.

## Select the extension point

| Need | Prefer | Read |
| --- | --- | --- |
| Let the model perform a new operation | Native tool or MCP server | [Tools](references/03-tools-and-commands.md), [MCP](references/09-mcp-integration.md) |
| Add explicit user actions | Session command or CLI subcommand | [Commands](references/03-tools-and-commands.md) |
| Observe costs, tools, sessions, requests | Observer hooks | [Hooks](references/04-hooks-and-observers.md) |
| Rewrite arguments or wrap execution | Middleware | [Middleware](references/05-middleware.md) |
| Supervise child agents or background work | Public lifecycle service and supervised tasks | [State and lifecycle](references/06-state-and-lifecycle.md) |
| Provide reusable instructions | Agent Skill, native bundled skill, or portable package | [Skills and portability](references/08-skills-and-portable-packages.md) |
| Add inference, memory, compression, media, browser, or terminal service | Corresponding provider interface | [Model](references/10-model-and-llm-providers.md), [Memory/context](references/11-memory-and-context-providers.md), [Other providers](references/12-specialized-providers.md) |
| Connect a new messaging network | Platform adapter plugin | [Gateway](references/13-gateway-routing.md), [Adapter authoring](references/14-platform-adapter-authoring.md) |
| Add a Telegram button/reaction/topic workflow | Narrow native handler or platform action | [Telegram](references/15-telegram.md), [Native handlers](references/16-native-channel-handlers.md) |
| Integrate another existing messaging channel | Reuse its adapter; verify channel-specific contract | [Other channels](references/17-other-messaging-platforms.md) |
| Add native desktop panes, actions, or pages | Official Desktop SDK | [Desktop](references/18-desktop-sdk.md), [Remote/events](references/19-desktop-backend-and-events.md) |
| Add web admin tabs or shell slots | Dashboard SDK | [Dashboard](references/20-dashboard-sdk.md) |

## Preserve the real boundaries

- General Python plugins are trusted in-process extensions. Capability grants guard particular host APIs; they do not create an operating-system sandbox.
- Keep plugin discovery, enablement, dependency preparation, toolset exposure, provider selection, and channel activation separate. Finding a package proves none of the later steps.
- Use the active Hermes home/profile and the host's session identifiers. Do not route by display name, global current working directory, or a hand-built session-key string.
- A messaging gateway, a Desktop renderer, a Desktop backend, a dashboard server, a cron process, and an MCP child are different runtimes. Sharing files does not create shared memory or an event bus.
- Distinguish normalized, authorized channel observers from native SDK handlers. A raw Telegram callback is not automatically an authenticated gateway command.
- Keep tool-request rewrites before the host approval boundary. Middleware callback failures are generally skipped; preserve downstream failures and do not treat middleware as an authorization boundary.
- Distinguish context injection, scheduling an agent turn, sending a platform message, and notifying a UI. Choose the API that performs the requested operation.
- Do not claim cross-host compatibility from a similarly named manifest field. Native Hermes, portable Agent Plugins, Claude Code, Codex, Desktop, and Dashboard have separate contracts.
- When an interface is absent on the target build, select a supported fallback or state the required upgrade/core change. Never invent a registration method.

## Reference map

Every reference is directly reachable here.

| Reference | Load when |
| --- | --- |
| [01 Identity and surfaces](references/01-identity-and-surfaces.md) | Resolving what “Hermes” or “gateway” means and which process owns an extension |
| [02 Discovery and manifests](references/02-discovery-and-manifests.md) | Building package structure, activation, collision rules, or dependency metadata |
| [03 Tools and commands](references/03-tools-and-commands.md) | Writing model tools, user commands, and safe dispatch |
| [04 Hooks and observers](references/04-hooks-and-observers.md) | Choosing lifecycle events, timing, returns, or telemetry |
| [05 Middleware](references/05-middleware.md) | Rewriting requests and wrapping tool/provider execution |
| [06 State and lifecycle](references/06-state-and-lifecycle.md) | Async tasks, cleanup, profiles, state, or supervised child agents |
| [07 Permissions and secrets](references/07-permissions-and-secrets.md) | Capabilities, approval routing, credential scopes, or secret providers |
| [08 Skills and portable packages](references/08-skills-and-portable-packages.md) | Bundling knowledge, using taps, or sharing portable components |
| [09 MCP integration](references/09-mcp-integration.md) | Connecting servers, controlling exposure, or calling MCP from a plugin |
| [10 Model and LLM providers](references/10-model-and-llm-providers.md) | Host-owned auxiliary calls versus registering inference providers |
| [11 Memory and context providers](references/11-memory-and-context-providers.md) | Replacing memory/compression or preserving session evidence |
| [12 Specialized providers](references/12-specialized-providers.md) | Image, video, speech, browser, terminal, or search backends |
| [13 Gateway routing](references/13-gateway-routing.md) | Admission, identity, dispatch, persistence, injection, and outbound delivery |
| [14 Platform adapter authoring](references/14-platform-adapter-authoring.md) | Supporting a new messaging platform without a core fork |
| [15 Telegram](references/15-telegram.md) | Bots, DMs, groups, topics, files, voice, streaming, and access controls |
| [16 Native channel handlers](references/16-native-channel-handlers.md) | Telegram SDK handlers, Slack actions, platform events, and reactions |
| [17 Other messaging platforms](references/17-other-messaging-platforms.md) | Channel-specific capabilities and external service requirements |
| [18 Desktop SDK](references/18-desktop-sdk.md) | Official native Desktop contributions and trust/enablement |
| [19 Desktop backend and events](references/19-desktop-backend-and-events.md) | Remote connections, plugin APIs, sockets, polling, and local UI installation |
| [20 Dashboard SDK](references/20-dashboard-sdk.md) | Browser administration extensions and shared Python backends |
| [21 Packaging and distribution](references/21-packaging-and-distribution.md) | Installation, dependency admission, catalog submission, upgrades, and rollback |
| [22 Troubleshooting](references/22-observability-and-troubleshooting.md) | Diagnosing discovery, dispatch, leaks, missing UI, and cross-profile faults |
| [23 Evaluation and release checks](references/23-evaluation-and-release-checks.md) | Acceptance tests and evidence needed for support claims |
| [24 Worked design recipes](references/24-worked-design-recipes.md) | Selecting and composing extension surfaces for a concrete feature |
| [25 Sources and compatibility](references/25-sources-and-compatibility.md) | Primary URLs, pinned code, known documentation differences, and refresh workflow |

## Deliver the result

For implementation work, include the package, exact installation target, activation steps, tested version/surface matrix, required permissions, state location, and upgrade/rollback notes. For architecture work, provide the chosen API contracts, alternatives that fit the task, and a proof plan.

Use “implemented,” “tested,” “documented,” and “inferred” accurately. A schema check or fake context test does not establish real gateway, Telegram, or Desktop behavior.
