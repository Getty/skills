# Debugging and observability

Start with the smallest observable failure, not a full environment reset.

## Triage matrix

| Symptom | First evidence | Likely boundary to inspect |
|---|---|---|
| Plugin absent | Catalog list, entry validation, resolved source | Discovery/distribution |
| Old behavior | Installed version and file content | Cached copy or stale conversation |
| Skill absent | Frontmatter, skill location, enabled state | Skill discovery |
| Tools absent | MCP initialization/authentication and catalog | Connection or tool metadata |
| Wrong tool chosen | Exact user wording and descriptions | Selection contract |
| Hook skipped | Runtime host, event, matcher, trust | Hook lifecycle |
| UI missing | Resource URI, renderer support, CSP diagnostics | Presentation |
| Writes denied | Connected identity, scopes, host decision | Authorization or policy |
| Duplicate writes | Job/event IDs and retry history | Idempotency |

Server discovery and schema checks apply broadly; widget and client-auth debugging must be interpreted for the named host. [Plugin troubleshooting](https://developers.openai.com/plugins/deploy/troubleshooting)

Use `codex doctor` for local installation/runtime diagnosis where supported. Use plugin/MCP listing commands to capture state rather than dumping entire configuration files. [Developer commands](https://learn.chatgpt.com/docs/developer-commands)

## Reproduction packet

Capture the smallest input, expected result, actual result, client/runtime version, package source/revision, connected account type, relevant policy outcome, and timestamps. Redact secrets and sensitive content.

Separate:
- process launch failure;
- protocol negotiation failure;
- authorization failure;
- schema validation failure;
- handler failure;
- agent selection failure;
- UI failure.

Fix one boundary at a time, then rerun the case that originally failed. Do not reinstall everything to repair a malformed input schema.

## Logs and metrics

Assign correlation identifiers across tool calls, backend operations, and event deliveries. Record duration and categorized failure, while minimizing raw prompts and record content.

For performance, measure discovery/startup separately from tool execution and model latency. A large tool catalog may create selection problems even when every individual handler is fast; narrow descriptions and eliminate redundant operations.

Do not treat a transcript file format as a durable integration API. Prefer documented events and generated protocol types for external clients.
