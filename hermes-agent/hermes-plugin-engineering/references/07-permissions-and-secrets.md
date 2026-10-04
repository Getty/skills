# Permissions, approvals, and secrets

Enabled Python plugins execute in the agent process. Host capability gates protect supported facades; they do not prevent arbitrary trusted Python from using the operating system. Desktop renderer plugins likewise have app-level authority. Treat installation and execution as a code-trust decision.

## Independent gates

The [capability registry](https://github.com/NousResearch/hermes-agent/blob/158fd638da1629c8e62caf9ade1515d162def8ab/hermes_cli/plugin_capabilities.py) defines actual grant IDs. At this snapshot these include built-in tool override, host-owned LLM provider/model/agent/profile/task overrides, and `gateway.platform_actions`.

Declare only required capabilities. Probe `ctx.has_capability(id)` and degrade explicitly when absent. Unknown capability strings are not a way to acquire future powers.

Keep these separate:

| Permission | Scope |
| --- | --- |
| `plugins.enabled` | Load general plugin code |
| Toolset/platform exposure | Make tools available to an agent surface |
| Capability grant | Permit a specific host facade behavior |
| `mcp_allowlist` | Permit a plugin to call named configured MCP servers |
| `allow_gateway_injection` | Permit non-CLI conversation injection |
| Platform sender/chat policy | Admit messaging users and conversations |
| External OAuth/service scopes | Authorize the underlying service operation |
| Desktop enable preference | Register local UI contributions |

The last two plugin-specific grants above remain separate from the declared-capability registry at this snapshot. Consult the [native implementation](https://github.com/NousResearch/hermes-agent/blob/158fd638da1629c8e62caf9ade1515d162def8ab/hermes_cli/plugins.py).

## Human approval transport

A transport registered with `ctx.register_approval_transport(name, present_fn)` changes where an existing approval request is presented. It must return the request-bound `request.respond(choice)` result. The host still owns policy, scope, timeout, persistence, and final authorization. Enabling the plugin is separate from selecting `security.approval.transport`. Read the [approval transport contract](https://hermes-agent.nousresearch.com/docs/user-guide/features/plugins#approval-transports).

Do not use observer return values to pre-answer approvals, and do not translate a timeout into consent. Bind interactive buttons to the authenticated actor, exact request, target profile, allowed choices, and expiry.

## Secret handling

Use profile-scoped host credential resolution. For platform adapters, the [adapter guide](https://hermes-agent.nousresearch.com/docs/developer-guide/adding-platform-adapters) provides `get_scoped_secret` and `extra_or_secret`; raw global environment reads can select another profile under gateway multiplexing.

For an external vault, implement the [SecretSource interface](https://hermes-agent.nousresearch.com/docs/developer-guide/secret-source-plugin). The source fetches values; the orchestrator owns ordering and environment application. Startup fetches must not prompt. Bound helper execution, restrict inherited variables, and keep bootstrap credentials protected.

Do not put secrets in manifests, committed MCP environment blocks, Desktop JS, query strings, telemetry, or plugin-state examples. Native code may still read process environment; a friendly facade is not an isolation guarantee.

## Cross-surface policy design

Run business authorization in the backend even if a button is hidden or a slash command is restricted. Consider a user invoking the HTTP endpoint or native callback directly. Validate sender, account, chat/topic, requested operation, and target resource together; none of those identifiers is interchangeable.

