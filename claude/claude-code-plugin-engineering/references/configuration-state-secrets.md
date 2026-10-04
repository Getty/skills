# Configuration, state, and secrets

## Choose the owner of every value

Classify values before choosing a file:

| Value | Recommended owner |
|---|---|
| Package behavior and schemas | Versioned plugin files |
| Endpoint, project selection, preferences | Explicit user configuration |
| API token or password | Credential storage; inject only into the consuming process |
| Runtime cache or generated environment | Plugin data directory |
| One invocation's work | Temporary request state |
| Shared business records | Application service with a real concurrency model |

Avoid discovering an endpoint or account by scanning unrelated personal configuration. Make missing required values produce a clear configuration result.

## Declare user configuration

The manifest's `userConfig` supports typed values with titles and help text. Sensitive options go to secure credential storage. Ordinary options go under `pluginConfigs`; interactive installation/configuration can collect them, while shell installation needs explicit supplied values. [User configuration](https://code.claude.com/docs/en/plugins/manifest-reference#user-configuration), [configuration commands](https://code.claude.com/docs/en/plugins/cli-reference#plugin-configure).

Example manifest fragment to merge into a real manifest:

```json
{
  "userConfig": {
    "service_url": {
      "type": "string",
      "title": "Service URL",
      "description": "HTTPS base URL of the evidence service",
      "required": true
    },
    "service_token": {
      "type": "string",
      "title": "Service token",
      "description": "Credential issued for the selected service",
      "sensitive": true,
      "required": true
    }
  }
}
```

Prefer the native stdin configuration route for secrets over command-line literals that may enter shell history. Do not log option objects while diagnosing a missing value.

## Keep interpolation context-aware

`${user_config.KEY}` is supported only in specified fields. Shell-form hook commands, monitor commands, and MCP `headersHelper` reject it. Use structured hook `args` or read `CLAUDE_PLUGIN_OPTION_<KEY>` from a hook's environment. Sensitive values do not interpolate into skill/agent text as raw secrets. Monitor processes do not receive the hook option variables. [Substitution contract](https://code.claude.com/docs/en/plugins/manifest-reference#reference-a-saved-value).

Inspect the executable boundary even when a value is valid JSON: JSON escaping does not make it safe for a shell. Keep shell-free argument arrays whenever possible; validate URLs and identifiers according to the application contract.

## Plan persistence and precedence

`${CLAUDE_PLUGIN_ROOT}` locates installed files and may change on update. `${CLAUDE_PLUGIN_DATA}` survives updates, but default final-scope uninstall can remove it. Treat cache as disposable and provide an explicit export/retention plan for irreplaceable state. [Loading and disk layout](https://code.claude.com/docs/en/plugins/loading#find-plugins-on-disk).

Plugin `settings.json` defaults currently affect only `agent` and `subagentStatusLine`; arbitrary settings do not become effective merely by being placed there. User and managed configuration may override plugin defaults. [Settings precedence](https://code.claude.com/docs/en/settings), [plugin defaults](https://code.claude.com/docs/en/plugins/components#default-settings).

Version the shape of your own stored data. Make migrations idempotent, retain a recoverable copy, and test an upgrade followed by a rollback. Avoid background downloads or package installation on every hook event; if bootstrapping is necessary, make its cost and failure explicit.
