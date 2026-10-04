# MCP servers inside a plugin

## Separate protocol from deployment

An MCP server supplies operations; the plugin supplies discovery, configuration, and usage instructions. Choose a process for local resources or a remote service for centralized state. Verify protocol and authentication independently before debugging packaging. [MCP integration](https://code.claude.com/docs/en/mcp).

Example `.mcp.json`:

```json
{
  "mcpServers": {
    "evidence": {
      "command": "node",
      "args": ["${CLAUDE_PLUGIN_ROOT}/server/index.js"],
      "env": { "EVIDENCE_STATE_DIR": "${CLAUDE_PLUGIN_DATA}" }
    }
  }
}
```

This declares a connection; it does not create the script or prove Node and its dependencies exist. Supply those requirements.

## Verify host names

For plugin `change-companion`, server `evidence`, and tool `lookup`, the server is `plugin:change-companion:evidence` in `/mcp`, while the tool is `mcp__plugin_change-companion_evidence__lookup`. Use the tool name in permissions and classic hook matchers. Use the server name where the MCP tool-hook schema asks for a server. [Plugin-provided servers](https://code.claude.com/docs/en/mcp#plugin-provided-mcp-servers).

Check `/mcp` for transport and authentication status, then make one harmless call with an expected result. Connection does not prove application authorization or result quality.

## Design the server contract

Give each tool a narrow schema and a clear effect. Separate reads from writes requiring authorization. Return structured data and understandable errors; avoid unbounded responses. Include operation identifiers for retryable writes.

For stdio, reserve stdout for protocol messages and send diagnostics to stderr. For HTTP, document endpoint, timeout, credential source, tenant selection, and refresh behavior. Do not commit tokens to headers or logs.

A `.mcpb` or older `.dxt` bundle is another packaging route. Required bundle configuration must be supplied before startup. A remote MCP endpoint is needed for hosts unable to launch the local process. [Bundles and cross-product behavior](https://code.claude.com/docs/en/plugins/components#include-a-packaged-mcpb-server).

## Reconnect and test failure paths

An applied reload can retain unchanged server configurations, reconnect changed ones, and disconnect removed servers. Editing implementation behind unchanged configuration does not prove a running process restarted. [Reload behavior](https://code.claude.com/docs/en/plugins/components#server-names-tool-names-and-reloads).

Test missing executable, invalid configuration, unavailable endpoint, expired credentials, malformed results, cancellation, and scoped-name mismatch. Identify transport, authentication, tool permission, and application failures separately. When porting hosts, keep the service where possible and adapt host registration and authentication.
