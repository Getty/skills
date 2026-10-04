# Lifecycle hooks

Read the selected event contract before implementing a handler. Do not infer behavior from a familiar Claude event name or a field accepted by a parser.

Contents: [Input](#input-contract), [example](#original-configuration-and-response), [outputs](#output-and-failure-contract), [engineering](#engineering-procedure).

Current events include `SessionStart`, `SessionEnd`, `SubagentStart`, `SubagentStop`, `UserPromptSubmit`, `PreToolUse`, `PermissionRequest`, `PostToolUse`, `PreCompact`, `PostCompact`, `Stop`, and `Interrupt`. Command and MCP-tool handlers exist; prompt/agent handlers are not supported. Review non-managed hooks with `/hooks`; matching command handlers can run concurrently. [Hooks](https://learn.chatgpt.com/docs/hooks)

## Input contract

A command receives one JSON object on stdin. Relevant documented fields are:

| Field | Type / applicable events |
|---|---|
| `session_id` | String; subagent events use the parent session ID |
| `transcript_path` | String or null; do not assume a stable transcript file format |
| `cwd` | Working-directory string |
| `hook_event_name` | Event-name string |
| `model` | Active model string, Codex extension |
| `turn_id` | String on turn-scoped events |
| `permission_mode` | String on `SessionStart`, tool/prompt, subagent, `Stop`, and `Interrupt` events; not universal |
| `tool_name`, `tool_input` | Tool events; canonical tool name and JSON arguments |
| `tool_use_id` | Tool-call ID on `PreToolUse` and `PostToolUse` |
| `tool_response` | JSON tool result on `PostToolUse` |

For Bash and `apply_patch`, inspect `tool_input.command`; MCP input contains the tool arguments. Do not assume `tool_input.description` exists. [Common and event-specific inputs](https://learn.chatgpt.com/docs/hooks#common-input-fields)

## Original configuration and response

A plugin can use default `hooks/hooks.json`; OpenAI-specific overrides and path rules follow [packaging](https://developers.openai.com/plugins/build/plugins).

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "^mcp__release_records__apply_release_change$",
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"${PLUGIN_ROOT}/hooks/check_release.py\"",
            "timeout": 10
          }
        ]
      }
    ]
  }
}
```

Resolve the actual exposed tool name before using that matcher. An original denial response is:

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "The change lacks a reviewed release identifier."
  }
}
```

## Output and failure contract

| Handler result | Documented meaning |
|---|---|
| Exit `0`, empty stdout | Successful no-op; continue |
| Exit `0`, supported JSON | Interpret the selected event's fields |
| `PreToolUse`: exit `2` + stderr | Deny the pending supported tool; stderr provides the reason |
| `PostToolUse`: exit `2` + stderr | Replace the completed tool's result with feedback; no rollback |
| `Stop` / `SubagentStop`: exit `2` + stderr | Request continuation; it does not mean “reject the completed turn” |
| Plain text stdout | Added context for session/subagent start and prompt submission; ignored by tool events; invalid for `Stop`, `SubagentStop`, and `Interrupt` |

`PreToolUse` JSON uses `hookSpecificOutput.permissionDecision`; rewriting requires `allow` plus `updatedInput`. `PermissionRequest` uses `hookSpecificOutput.decision.behavior` with `allow` or `deny`; no decision preserves the ordinary approval flow. [Event output contracts](https://learn.chatgpt.com/docs/hooks#pretooluse)

Treat unsupported output carefully: `PreToolUse` fields such as `permissionDecision: "ask"` or `continue: false` fail the hook and allow the tool to continue. `PermissionRequest`'s reserved rewrite fields instead fail closed. Do not use one generic output object for every event.

Command timeouts use seconds and default to `600`; `Interrupt` defaults to one second and is limited to three. Background hooks cannot block, approve, rewrite, or continue the triggering operation. [Background execution](https://learn.chatgpt.com/docs/hooks#run-hooks-in-the-background)

The documentation does not establish a universal fail-closed rule for arbitrary command crashes, non-`2` exit codes, timeouts, or malformed JSON. Test those exact cases on the target release; never substitute “the hook failed” for an explicit denial. MCP-hook missing-server, callback-error, timeout, and malformed-response cases can leave the operation running. [MCP execution and managed hooks](https://learn.chatgpt.com/docs/hooks#mcp-tool-hooks)

## Engineering procedure

- Capture a benign real event before writing the handler.
- Validate field types and bound input size. Keep diagnostic output distinct from protocol output.
- Test no-op, explicit denial, exit `1`, malformed JSON, unsupported fields, timeout, duplicate invocation, and simultaneous hooks.
- Check actual side effects and the returned tool result after every failure test.
- Verify matcher coverage: hosted tool paths are not universally covered, and `write_stdin` does not rerun prechecks.
- Make audit/cleanup idempotent; guard stop-hook continuations against endless loops.
- Keep critical authorization in the backend or host policy.

Do not implement shell-command policy with a naive substring blacklist. Prefer narrow structured operations. Do not advertise arbitrary call splitting, merging, loop replacement, or complete auditing merely because lifecycle hooks exist. Consult the source for managed-only policy, context limits, and remaining per-event constraints.
