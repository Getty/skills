# Mod event middleware and tool composition

## Use event-specific contracts

Mod handlers receive `$`, immutable event `e`, and `next`. Calling `next(e)` continues the chain. Passing a changed copy rewrites the downstream event; returning an event-specific result without `next` handles it directly. Awaiting `next` permits result inspection. These are actual middleware semantics, unlike the classic hook result protocol. [Mod event guide](https://code.claude.com/docs/en/plugins/mods/events).

| Event family | Engineering use | Contract lookup |
|---|---|---|
| `tool.call` | Observe, change arguments, refuse, or provide a result | Tool event input/result types |
| `tool.check` | Review the permission decision | Decision shape and managed-policy precedence |
| `tool.describe` | Change the model-facing tool description | Description and deferred-loading fields |
| `prompt.submit` | Rewrite, add context, or drop submitted input | Prompt result shape |
| `turn.step` | Observe or configure an individual model request | Async generator, model/effort, streaming result |
| `agent.offer`, `agent.spawn` | Control offered agents or spawning | Pinned identity and permission fields |
| `session.receive`, `session.send` | Handle inter-session delivery | Origin, identity, consumed/delivery result |
| `classic.<Event>` | Reach classic lifecycle events | Classic payload contract |

Look up the chosen event in the [current event inventory](https://code.claude.com/docs/en/plugins/mods/reference#events) and then the generated types. This map is not an exhaustive writable-field schema.

## Preserve semantics when composing actions

For one logical task requiring several operations, prefer an explicit composite tool with its own input/output schema. Its implementation can orchestrate supported tool or MCP calls and return an aggregate result with each sub-operation's status. This is an engineering pattern; it is not a claim that classic hooks expose a tool-call-array replacement API.

Before implementing retries or fan-out, answer:

1. Which operation is idempotent, and how is duplicate execution detected?
2. Does each downstream action still receive the intended permission check?
3. How does cancellation stop unfinished actions?
4. How are failed and successful partial results represented?
5. Which result identity is visible to the model and audit log?

The guide explicitly documents repeated `next(e)` for retrying a failed tool. Do not repeat a write merely because its response was lost. A synthetic `{ result: ... }` replaces execution; label it accurately. [Tool-call behavior](https://code.claude.com/docs/en/plugins/mods/events#guard-or-change-a-tool-call).

## Register commands and tools deliberately

Register a native command or tool during `session.start`, before the first prompt. A registered mod tool uses a different naming form from a plugin-bundled MCP server: `mcp__<plugin>__<tool>`. Provide a schema and handle the full tool name. An immediate native command may run while the model is working. [Registration API](https://code.claude.com/docs/en/plugins/mods/api#add-a-command-or-a-tool).

Keep native-command input validation outside model prompting. Do not let a display command unexpectedly submit a turn or send external messages. Reserve command names and handle registration conflicts without losing all remaining initialization.

## Make failure behavior intentional

A mod handler that throws or times out is normally skipped. A gate that must refuse on internal failure needs a supported `.catch` result before any action is forwarded. If `next` already ran, an error message must not claim the action never happened. Distinguish pre-action rejection from post-action observation failure. [Error handlers](https://code.claude.com/docs/en/plugins/mods/events#when-a-hook-throws-or-times-out).

Multiple mods can rewrite the same event. Test composition with another observer and another rewriter. Preserve immutable identity fields from the generated types; do not attempt to change the caller's agent identity or inherited permission state. Put authoritative policy at the protected host or service boundary rather than relying on an incidental user-mod load order.
