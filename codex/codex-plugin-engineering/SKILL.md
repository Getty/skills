---
name: codex-plugin-engineering
description: "Use when building or debugging an OpenAI Codex plugin — plugin.json, .codex-plugin/, marketplace.json, hooks.json, plugin MCP — or choosing between plugin, Codex SDK and app-server."
---

# Codex Plugin Engineering

Build the smallest supported extension that completes the requested workflow. Keep this skill generic: derive account, operating system, repository, execution host, policy, and deployment choices from the task. Do not require another installed skill or a particular commercial service.

## Establish the target before designing

1. Identify the client and the machine or service running the agent. Record versions and orchestration mode using [the compatibility record](references/compatibility-record.md).
2. Read the relevant [surface map](references/surface-map.md). A plugin catalog listing does not prove that every bundled capability runs on every client.
3. Inspect available local CLI help, schemas, and relevant source without exposing credentials. Then open current official documentation from [the source registry](references/sources.md). Separate documented behavior, locally verified behavior, proposals, and unknowns.
4. Classify the request: reusable instructions, authenticated tools, lifecycle intervention, visual interaction, incoming events, or an application that controls Codex.
5. Choose the mechanism using the routing table. Explain a material limitation before implementing a workaround.
6. Deliver the implementation, validation evidence, supported environments, necessary setup, and remaining limits. Never present schema validation as a successful end-to-end runtime test.

Snapshot: **2026-10-04, Europe/Berlin**. Refresh version-sensitive facts when acting, especially host availability, hook contracts, manifest formats, command names, submission limits, and experimental protocols.

## Route by mechanism

| Requested outcome | Primary mechanism | Read |
|---|---|---|
| Installable collection of workflows and capabilities | Native plugin package | [Package formats](references/package-formats.md) |
| Discover, install, enable, update, or remove plugins | Marketplace plus host state | [Marketplaces](references/marketplaces.md) |
| Teach a repeatable task with references or scripts | Skill and optional metadata | [Skills and metadata](references/skills-metadata.md) |
| Repository conventions, project defaults, or execution policy | Instructions/configuration | [Instructions and config](references/instructions-config.md) |
| Connect a local process or remote service | MCP client configuration | [MCP connections](references/mcp-connections.md) |
| Add controlled operations and structured results | MCP server tool contracts | [Tool contracts](references/tool-contracts.md) |
| Connect user accounts or protect secrets | MCP authentication and backend authorization | [Authentication and secrets](references/auth-secrets.md) |
| React at supported agent lifecycle points | Reviewed runtime hooks | [Hooks](references/hooks.md) |
| Add a panel, rich form, viewer, or interactive result | MCP Apps and host extensions | [UI and extensions](references/ui-extensions.md) |
| React to external changes | Supported MCP Events host or separately operated bridge | [Events](references/events.md) |
| Build a custom Codex client | App-server protocol | [App-server](references/app-server.md) |
| Drive coding jobs from code or CI | Codex SDK or non-interactive CLI | [SDK and automation](references/sdk-automation.md) |
| Define execution and action boundaries | Host policy plus backend checks | [Security and approvals](references/security-approvals.md) |

Current native plugins include hooks; do not repeat older claims that Codex only supports skills and MCP. Conversely, an app-server client is not an in-process plugin API. See [current plugin architecture](https://developers.openai.com/plugins/concepts/plugins) and [app-server](https://learn.chatgpt.com/docs/app-server).

## Implement in a reproducible order

1. Write the intended inputs, output, side effects, success conditions, and excluded requests.
2. Select one distribution target first. Choose portable or compatibility format deliberately.
3. Implement one complete, small workflow before adding a broad tool catalog.
4. Keep workflow prose, backend authorization, runtime hooks, UI, and host policy in their respective layers.
5. Test the source component, then the installed package, then each claimed host.
6. Prepare migration and rollback alongside release changes.

Use [development workflow](references/development-workflow.md), [testing and evaluation](references/testing-evaluation.md), [distribution and release](references/distribution-release.md), and [debugging](references/debugging.md) for the corresponding phase. Use [portability and migration](references/portability-migration.md) when adapting existing plugins. Start from [design recipes](references/recipes.md) when the request is architectural.

## Preserve important boundaries

- Do not infer OpenAI runtime support from a Claude-compatible filename or familiar event name.
- Do not make skills or metadata the only enforcement of authorization, tenancy, or destructive-action limits.
- Keep secrets out of packages, prompts, example outputs, and diagnostic reports.
- Do not change global settings, managed requirements, or hook trust merely to make a failing example pass.
- Treat plugin source, marketplace entry, installed copy, enabled state, service connection, and hook trust as distinct states during diagnosis.
- Distinguish public directory submission requirements from private/local plugin capabilities.
- Do not silently install dependencies, publish packages, connect accounts, or send external messages beyond the user's authorization.
- Use the current SDK migration guidance for old `codex mcp-server` integrations; that command is removed in the documented baseline.

## Minimum delivery

Report the selected mechanism and why it fits; exact files changed; declared and observed host compatibility; source dates or version pins; tests actually run; required credentials or external setup; and how to disable or roll back the change. Include concrete unsupported behavior when it affects the request. Keep the complete implementation in the requested project, and avoid embedding personal environment assumptions in reusable packages.
