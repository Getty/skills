# MCP integration

Prefer MCP for an external tool service that should be reusable across agent hosts or isolated in another process. Prefer a native Hermes plugin when the feature needs Hermes lifecycle, profile integration, UI contributions, or provider replacement.

The [MCP guide](https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp) documents native `mcp_servers` configuration, stdio/remote transports, tool filtering, authentication, discovery, and reload.

## Configuration shape

A deliberately generic stdio configuration:

```yaml
mcp_servers:
  catalog:
    command: /absolute/path/to/catalog-mcp
    args: ["--read-only"]
    tools:
      include: ["lookup_item"]
```

Replace the executable and arguments with a real server contract; this does not install or implement that server. Use separate executable and argument tokens. Avoid shell interpolation of user input.

Choose stdio for a local child lifecycle; choose remote transport when the service belongs on another host. Determine who owns credentials and process cleanup. An authenticated remote MCP service is not necessarily the same account as the messaging sender or active Hermes profile.

## Availability and exposure

Separate successful handshake, registered tool schema, toolset exposure, credential availability, and successful execution. Resource/prompt helpers depend on server capabilities. Do not assume every MCP server exposes resources or prompts.

Use include/exclude filters to keep a bounded tool surface. Discover actual registered names instead of constructing them: overview docs and current portable/runtime code have used different underscore conventions. A hardcoded name from an old example can silently select nothing.

For many servers, consider lazy discovery from a valid schema cache and bounded startup concurrency. Measure startup memory and first-use latency separately. Make the service's idle recycling safe for subscriptions, stateful sessions, and in-flight operations.

## Calling MCP from a plugin

The [native `ctx.call_mcp` implementation](https://github.com/NousResearch/hermes-agent/blob/158fd638da1629c8e62caf9ade1515d162def8ab/hermes_cli/plugins.py) reuses Hermes' MCP connection machinery. Its per-plugin `mcp_allowlist` is default-deny.

```yaml
plugins:
  entries:
    text-metrics:
      mcp_allowlist: ["catalog"]
```

Then a plugin operation can call `ctx.call_mcp("catalog", "lookup_item", {"id": item_id})`. Check the returned `ok`, `result`, `error`, and possible truncation marker. The call is synchronous; do not block an event loop with a slow server. The grant is server-level, not proof of per-tool or read/write scope.

A plugin allowed to call one server should not open an independent connection to bypass the host policy, timeout, or account routing.

## Application-backed servers

For an MCP server that controls a local desktop application, inspect [application declarations](https://hermes-agent.nousresearch.com/docs/developer-guide/plugins/application-declarations). Presence/version/GPU declarations and connection readiness are separate gates. At this snapshot the declaration parser's existence does not mean arbitrary YAML is automatically loaded; verify the loader integration. This is local application integration, not the native Hermes Desktop UI SDK.

