# Permissions, execution authority, and trust

## Review effects at the correct boundary

| Mechanism | Boundary to inspect |
|---|---|
| Skill or agent instructions | Influence on model decisions; declared tool availability and host permission flow |
| Classic hook process | The process's operating-system access plus event-specific decision semantics |
| Local MCP or LSP server | Process authority and server-side access controls; tool calls have additional host rules |
| Remote MCP server | Remote service identity, credentials, scopes, and authorized operations |
| Mod | In-process API access, middleware effects, organization guard policy, and downstream effects |
| Channel | Sender authorization, session selection, data exposure, reply authority, and any separate permission relay |

Do not call a plugin sandboxed merely because Claude's Bash tool is sandboxed. Hook, server, and mod execution can use the installing user's authority outside that tool sandbox. Inspect the actual process/API capabilities and the data they can reach. [Plugin security](https://code.claude.com/docs/en/plugins/security).

## Make permission behavior an explicit contract

Record which operations are automatic, which reach the host's permission flow, and which need service-side authorization. A text instruction saying “ask first” is useful guidance but cannot constrain a process independently. Model tool permissions also do not automatically constrain a mod's direct filesystem/process API calls.

Classic hooks have event-specific authority. An observational event cannot undo a completed tool action; a process exit is not a universal veto. In-process `tool.check` middleware can influence a wider permission path, including some ordinary asks and nonmanaged hook blocks. A managed `PreToolUse` block remains authoritative in the documented mod flow. Read [classic decision contracts](hooks-command-contracts.md), [permission extensions](https://code.claude.com/docs/en/permissions#extend-permissions-with-hooks), and [mod permission behavior](https://code.claude.com/docs/en/plugins/mods/events#approve-or-deny-a-tool-call) before promising enforcement.

Define failure behavior for absent code, load refusal, missing interpreter, dependency failure, malformed input, timeout, and service unavailability. “Return deny on exceptions” covers only exceptions the handler actually receives. If the host skips a handler that fails to start, a script cannot turn that into a reliable external policy boundary.

## Apply organization controls precisely

Marketplace allowlists constrain acquisition sources; they are not a substitute for reviewing each plugin's executable content. Separate marketplace restrictions, enabled plugin settings, sideload restrictions, hooks policy, mod policy, and external network/identity policy. Check the effective managed settings in the actual host instead of weakening local settings until loading succeeds. [Organization controls](https://code.claude.com/docs/en/plugins/org), [managed settings](https://code.claude.com/docs/en/managed-settings).

Current mod administration has a built-in guard. Its `allowManagedModsOnly` option belongs under managed `pluginConfigs["cc-plugin-sec-default@builtin"].options`, not at the settings root. Where the guard loads, deny rules normally remain authoritative for model tool calls; its separate override option changes that policy. Do not enable the override merely to make a test pass.

A mod counts as the organization's own only when the documented managed enablement and directory deployment conditions hold: an absolute local-directory marketplace and its relative, in-place plugin source. A remotely cached plugin does not become a managed mod solely because managed settings enable it. If defining `prependPlugins`, preserve the built-in guard in the list when its protections are intended. `disableAllHooks` can also disable managed enforcement hooks; it is broader than disabling user mods. [Exact guard configuration and deployment](https://code.claude.com/docs/en/plugins/mods/admin).

These controls govern Claude Code. Use service credentials, operating-system isolation, access controls, or a policy service when the requirement must remain true outside the host or when plugin code itself is not trusted.

## Keep the review concrete

For a plugin under review, follow data from the initiating input to each external effect. Inspect scripts, modules, configured server commands, dependency resolution, executable paths, update behavior, and credential handling. Static mod capability output is evidence of declared API use; it does not establish that all downloaded or launched code is harmless.

For generated files, prefer bounded writes and a recoverable update. For external mutations, retain the target, authorization context, idempotency key where available, result identity, and partial-failure details. For messages, distinguish drafting, scheduling, sending, receiving, and relaying approval. A capability to send is not authorization to choose a recipient or publish content.

Retest materially changed authority after an update. Keep review output about observed capabilities and concrete risks; avoid generic warnings that do not affect the requested design.
