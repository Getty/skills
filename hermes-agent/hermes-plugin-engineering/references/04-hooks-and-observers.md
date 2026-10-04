# Hooks and observers

Select an event by its actual firing boundary and return contract. The [event catalog](https://hermes-agent.nousresearch.com/docs/user-guide/features/hooks) covers agent/plugin hooks, config-driven shell hooks, and separate gateway directory hooks. Do not interchange their event names, manifests, or trust rules.

## Agent events

The [observer contract](https://hermes-agent.nousresearch.com/docs/developer-guide/observer-hooks) provides session, turn, API-attempt, tool, approval, streaming, and subagent telemetry. Accept keyword arguments and `**kwargs` for additive compatibility. Prefer explicit correlation identifiers to parsing compound strings.

| Boundary | Typical events | Design consequence |
| --- | --- | --- |
| User turn | `pre_llm_call`, `post_llm_call` | A turn can contain several model requests and tool calls |
| Provider attempt | `pre_api_request`, `post_api_request`, `api_request_error` | Join retries by attempt and turn identifiers |
| Auxiliary inference | `pre_auxiliary_call`, `post_auxiliary_call` | Account for non-main-loop model work separately |
| Tool operation | `pre_tool_call`, `post_tool_call` | Record blocked/cancelled/error outcomes too |
| Session identity | `on_session_finalize`, `on_session_reset` | Clean up identity-scoped state |
| Run completion | `on_session_end` | Do not assume the conversation identity was destroyed |
| Stream | `on_stream_start`, `on_stream_delta`, `on_stream_end` | Observe; do not reinterpret as a transform API |

Some older hooks accept control returns: pre-tool block/modify/approval escalation, pre-LLM context, and final-result transforms. Read the exact event contract before returning directives. `pre_command` is an observer at this snapshot; returning a block-shaped dictionary does not make it an authorization hook. The [pinned accepted events](https://github.com/NousResearch/hermes-agent/blob/158fd638da1629c8e62caf9ade1515d162def8ab/hermes_cli/plugins.py) are more reliable than a numeric hook count in an overview.

## Timing and failure policy

Do not generalize “all hooks fail open.” Ordinary observers isolate exceptions; timeout-bounded pre-tool callbacks and explicitly fail-closed shell gates have different behavior. Select a policy mechanism only after checking malformed output, timeout, callback exception, and cancellation in the target build.

Use request middleware for general argument transformations. Preserve the approval boundary by making it evaluate the effective operation.

## Shell and gateway hooks

Config `hooks:` entries launch subprocesses with a JSON request/response protocol. Validate the supported event, matcher semantics, timeout, and fail-closed option. Do not copy Claude Code JSON verbatim: superficially similar approval/block names can have different meanings.

Gateway directory hooks live under `$HERMES_HOME/hooks/<name>/` with `HOOK.yaml` and `handler.py`. Placement is their trust opt-in; `plugins.enabled` does not gate them. They are a separate gateway lifecycle facility, not a general plugin package.

## Observer implementation guidance

Keep callbacks short, avoid secrets/raw transcript export, and batch external telemetry outside the token path. Use bounded queues and report drops. Preserve terminal outcomes so a blocked operation closes its trace. Emit no operational side effect merely because a span exists. For UI delivery, use the process-aware design in [Desktop events](19-desktop-backend-and-events.md).

