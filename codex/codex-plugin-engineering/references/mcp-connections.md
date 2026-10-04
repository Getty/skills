# MCP connections and deployment choices

Choose how the host reaches the server before designing authentication.

| Connection | Suitable use | Operational questions |
|---|---|---|
| Local STDIO | Tools near local files or installed programs | Process owner, interpreter, paths, environment, shutdown |
| Remote Streamable HTTP | Shared service or managed backend | TLS, authorization, uptime, timeouts, deployment |
| Supported private tunnel | Private backend reached from a hosted client | Tunnel availability, workspace association, private routing |

Direct Codex MCP supports STDIO and Streamable HTTP. CLI, desktop, and IDE can share configuration on the same Codex host. Hosted plugin connections have a separate setup path. [MCP](https://learn.chatgpt.com/docs/extend/mcp)

## Original direct-host configuration

```toml
[mcp_servers.release-records]
url = "https://releases.example.com/mcp"
bearer_token_env_var = "RELEASE_RECORDS_TOKEN"
enabled_tools = ["find_release", "get_release"]

[mcp_servers.local-index]
command = "python3"
args = ["/absolute/path/to/local-index/server.py"]
env_vars = ["INDEX_ROOT"]
```

Replace example paths/endpoints and provision only the named variables. Do not print their values. Keep the token source appropriate to the host.

Use `codex mcp list`, `codex mcp login <name>` for OAuth-capable servers, and `/mcp` to inspect active connections. Server options include initialization/tool timeouts, required startup, enablement, and tool filters; consult the current reference before adding policy knobs. [MCP configuration](https://learn.chatgpt.com/docs/extend/mcp)

## Deployment design

For a local process, keep protocol output separate from diagnostics. Pin dependencies, avoid interactive installation during launch, and handle cancellation and child-process cleanup.

For HTTP, use stable service identity and explicit health diagnostics. Distinguish transport reachability, protocol negotiation, authentication, tool discovery, and handler success. A TCP connection alone verifies none of the later stages.

Developer-mode testing can use public HTTPS or Secure MCP Tunnel. The public plugin submission route still has its own endpoint requirements. [Connection testing](https://developers.openai.com/plugins/deploy/connect-chatgpt)

Do not equate “localhost” across desktop, containers, SSH sessions, remote execution, and hosted orchestration. Identify the network namespace in which the connecting process runs.
