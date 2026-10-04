# Primary sources and update strategy

## Checkpoint and precedence

Reviewed on **2026-10-04, Europe/Berlin**. This skill synthesizes current official Claude Code documentation and selected official repositories. It is a navigation and engineering guide, not a frozen copy of those sources. Examples labeled original were composed for this skill.

For an implementation, reconcile the target's `claude --version`, command help, validation output, and generated mod types with current documentation. Do not assume a current feature exists on an older installation. Where a guide and a detailed event schema differ, inspect the specific schema and a controlled runtime observation; report remaining uncertainty. Source links below were opened during authoring, either directly or through their indexed canonical/redirected page.

## Packaging, installation, and distribution

| Primary source | Refresh when changing |
|---|---|
| [Documentation index](https://code.claude.com/docs/llms.txt) | Page locations and newly added extension surfaces |
| [Plugin overview](https://code.claude.com/docs/en/plugins/overview) | Package role and component support |
| [Create a plugin](https://code.claude.com/docs/en/plugins/create) | Authoring workflow and local development |
| [Manifest reference](https://code.claude.com/docs/en/plugins/manifest-reference) | Fields, paths, merge rules, feature gates |
| [Plugin components](https://code.claude.com/docs/en/plugins/components) | Skills, agents, hooks, MCP, LSP, binaries, options |
| [Install and manage](https://code.claude.com/docs/en/plugins/install) | Host-specific installation and activation |
| [CLI reference](https://code.claude.com/docs/en/plugins/cli-reference) | Commands, flags, reload behavior, exits |
| [Loading reference](https://code.claude.com/docs/en/plugins/loading) | Cache, scope precedence, runtime packages, versions |
| [Dependencies](https://code.claude.com/docs/en/plugins/dependencies) | Dependency versions and marketplace boundaries |
| [Publish](https://code.claude.com/docs/en/plugins/publish) | Identity, release strategy, distribution |
| [Create a marketplace](https://code.claude.com/docs/en/plugins/create-marketplace) | Catalog structure and local testing |
| [Marketplace reference](https://code.claude.com/docs/en/plugins/marketplace-reference) | Source types, strictness and metadata |
| [Host a marketplace](https://code.claude.com/docs/en/plugins/host-marketplace) | Git/URL/private hosting and updates |
| [Official plugin repository](https://github.com/anthropics/claude-plugins-official) | Concrete package examples and ownership |

## Skills, agents, hooks, tools, and messaging

| Primary source | Refresh when changing |
|---|---|
| [Skills](https://code.claude.com/docs/en/skills) | Frontmatter, invocation, arguments, context and migration |
| [Subagents](https://code.claude.com/docs/en/sub-agents) | Tools, nesting, background execution, worktrees and memory |
| [Hook reference](https://code.claude.com/docs/en/hooks) | Event inputs/results, matching, handler types, exits, timeouts |
| [Hook guide](https://code.claude.com/docs/en/hooks-guide) | Operational examples and lifecycle composition |
| [Agent SDK hooks](https://code.claude.com/docs/en/agent-sdk/hooks) | SDK callbacks, output mapping and timeout differences |
| [MCP](https://code.claude.com/docs/en/mcp) | Transport, namespacing, configuration, authentication |
| [Workflows](https://code.claude.com/docs/en/workflows) | Agent composition, replay and runtime restrictions |
| [Channels](https://code.claude.com/docs/en/channels) | Preview eligibility, providers, activation and official bridges |
| [Channel reference](https://code.claude.com/docs/en/channels-reference) | MCP notifications, metadata, replies and permission relay |
| [Agent SDK plugins](https://code.claude.com/docs/en/agent-sdk/plugins) | Local plugin paths and initialization diagnostics |

## In-process mods

| Primary source | Refresh when changing |
|---|---|
| [Mods overview](https://code.claude.com/docs/en/plugins/mods/overview) | Version gate, host surface support, authority |
| [Create a mod](https://code.claude.com/docs/en/plugins/mods/create) | Module layout, loading and generated types |
| [Mod reference](https://code.claude.com/docs/en/plugins/mods/reference) | Registration, event results, APIs and runtime limits |
| [Event middleware](https://code.claude.com/docs/en/plugins/mods/events) | Forwarding, rewriting, retries, short-circuits and permission flow |
| [Use the mods API](https://code.claude.com/docs/en/plugins/mods/api) | Tools, commands, model calls, timers, IO and session messaging |
| [Interface](https://code.claude.com/docs/en/plugins/mods/interface) | Render sites, native elements, UI events and state lifetime |
| [Test a mod](https://code.claude.com/docs/en/plugins/mods/test) | Native kit, stubs, clocks, UI tests, policy tests |
| [Manage mods](https://code.claude.com/docs/en/plugins/mods/admin) | Guard options, managed identity, execution order and policy |
| [Published declaration file](https://github.com/anthropics/claude-code/blob/main/mods/types/claude-code.d.ts) | Public API detail; compare with target-generated declarations |

## Trust, operation, and evaluation

| Primary source | Refresh when changing |
|---|---|
| [Plugin security](https://code.claude.com/docs/en/plugins/security) | Executable authority and review boundaries |
| [Permissions](https://code.claude.com/docs/en/permissions) | Tool rules, hooks and mod permission interaction |
| [Settings](https://code.claude.com/docs/en/settings) | Configuration scope and precedence |
| [Managed settings](https://code.claude.com/docs/en/managed-settings) | Deployment and organization-enforced controls |
| [Organization plugins](https://code.claude.com/docs/en/plugins/org) | Allow/block rules, seed deployment, first-query readiness |
| [Plugin evals](https://code.claude.com/docs/en/plugin-evals) | Suite format, baselines, cost, report publication |
| [Measure cost and usage](https://code.claude.com/docs/en/plugins/measure) | Context footprint and measured behavior |
| [Troubleshoot plugins](https://code.claude.com/docs/en/plugins/troubleshooting) | Exact error messages and layer-specific remedies |
| [Debug configuration](https://code.claude.com/docs/en/debug-your-config) | Loaded configuration, context and diagnostic surfaces |

## Selected feature gates to recheck

| Capability | Documented checkpoint |
|---|---|
| `userConfig.options` | v2.1.271+; older builds can reject that schema |
| Noninteractive `/reload-plugins` | v2.1.260+; no MCP connection changes there |
| Native plugin evals | v2.1.269+ |
| Account-synced plugin loading | v2.1.273+ and applicable authentication/host conditions |
| Bundled workflow-authoring skill | v2.1.248+ |
| Mods enabled by default | v2.1.287+; managed controls still apply |
| LSP `requestTimeout` setting | v2.1.288+ |
| Channels | Research preview with provider, organization and activation constraints |
| Monitors and themes | Experimental component surfaces |

This is a selected list, not a complete minimum-version calculation. A plugin's effective minimum is the newest requirement among its essential features. Prefer optional feature detection or an explicit version error to accepting a configuration the target silently ignores.
