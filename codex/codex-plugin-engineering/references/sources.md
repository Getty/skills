# Primary source registry

Verification snapshot: **2026-10-04, Europe/Berlin**. These are current official documentation pages opened during authoring, not frozen specifications. Refresh relevant pages and the target installation before implementing. The references in this skill provide original workflow guidance and short summaries, not copied documentation.

## Product, packaging, and distribution

| Source | Consult for |
|---|---|
| [Plugin architecture](https://developers.openai.com/plugins/concepts/plugins) | Components and division of responsibilities |
| [Plugins by surface](https://learn.chatgpt.com/docs/plugins) | Host availability, installation, new-session behavior |
| [Package your plugin](https://developers.openai.com/plugins/build/plugins) | Portable/compatibility formats, marketplaces, path rules, bundled hooks |
| [Developer commands](https://learn.chatgpt.com/docs/developer-commands) | Current plugin and marketplace CLI syntax |
| [Workspace plugin management](https://learn.chatgpt.com/docs/enterprise/plugin-management) | Admin imports, policy, app references, update semantics |
| [Submission](https://developers.openai.com/plugins/deploy/submission) | Public directory process, server limitations, review/update paths |
| [Submission requirements/errors](https://developers.openai.com/plugins/deploy/submission-errors) | Exact validation and listing requirements |

## Skills and host configuration

| Source | Consult for |
|---|---|
| [Build skills in Codex](https://learn.chatgpt.com/docs/build-skills) | Discovery, local scope, metadata, invocation |
| [Build plugin skills](https://developers.openai.com/plugins/build/skills) | Workflow/resource structure and tool dependencies |
| [AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md) | Instruction discovery and precedence |
| [Config basics](https://learn.chatgpt.com/docs/config-file/config-basic) | Runtime layers and trusted project scope |
| [Configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference) | Exact keys, plugin policy, managed and cloud scope |
| [Rules](https://learn.chatgpt.com/docs/agent-configuration/rules) | Command policy and supported scope |
| [Hooks](https://learn.chatgpt.com/docs/hooks) | Event contracts, trust, coverage, failure semantics |
| [Agent approvals/security](https://learn.chatgpt.com/docs/agent-approvals-security) | Sandbox, approval modes, retired options |

## Tools, authentication, UI, and events

| Source | Consult for |
|---|---|
| [Codex MCP connections](https://learn.chatgpt.com/docs/extend/mcp) | STDIO/HTTP, config, OAuth, tool filtering |
| [MCP server concepts](https://developers.openai.com/plugins/concepts/mcp-server) | Tool/resource relationship and transport |
| [Define tools](https://developers.openai.com/plugins/plan/tools) | Contract design and annotation meaning |
| [Build MCP server](https://developers.openai.com/plugins/build/mcp-server) | Tool registration, results, server instructions |
| [Authentication](https://developers.openai.com/plugins/build/auth) | OAuth, resource discovery, client registration |
| [MCP Apps UI](https://developers.openai.com/plugins/build/chatgpt-ui) | UI bridge, standard fields, compatibility aliases |
| [OpenAI extensions](https://developers.openai.com/plugins/build/extensions) | Panels, sidebar, viewers, rich forms, host limits |
| [MCP Events](https://developers.openai.com/plugins/build/mcp-events) | Cloud event availability and draft protocol integration |
| [Plugin security/privacy](https://developers.openai.com/plugins/guides/security-privacy) | Data minimization and trust boundaries |
| [Docs MCP](https://developers.openai.com/learn/docs-mcp) | Optional official documentation connector |

## Integration, testing, and migration

| Source | Consult for |
|---|---|
| [App-server](https://learn.chatgpt.com/docs/app-server) | Generated schemas, handshake, turns, approvals, streaming |
| [Codex SDK](https://learn.chatgpt.com/docs/codex-sdk) | Programmatic threads and removed MCP-server mode |
| [Non-interactive mode](https://learn.chatgpt.com/docs/non-interactive-mode) | CLI automation, event output, structured results |
| [Connect and test](https://developers.openai.com/plugins/deploy/connect-chatgpt) | Component and installed-plugin evaluation |
| [Troubleshooting](https://developers.openai.com/plugins/deploy/troubleshooting) | Server, discovery, UI, auth diagnostics |
| [Claude plugin conversion](https://developers.openai.com/plugins/guides/submit-claude-plugin) | Supported conversions and nonportable components |

## Maintenance rules

Prefer a current detailed reference to a historical launch announcement for present support. Distinguish a parser accepting a field from implemented behavior. Use generated app-server schemas tied to the selected binary.

For libraries or adjacent protocols, follow primary links from the relevant official guide and verify the actual dependency version. Do not turn community examples, repository issues, or unreleased branches into supported product promises.

Preserve a short evidence record for changed claims. Update the affected reference and its compatibility notes together; avoid scattering a new global assumption through every file.
