# Advanced hook handlers and operational limits

Verified on 2026-10-04. Select a handler by the evidence it needs and the latency the event can tolerate.

## Handler selection

| Type | Suitable design intention | Evidence to require before release |
|---|---|---|
| `command` | Deterministic local parsing, transformation or process integration | Interpreter, argument handling, output schema, exit behavior |
| `http` | Shared service that evaluates an event | Authentication, response schema, outage behavior, bounded latency |
| `mcp_tool` | Reuse a configured service tool | Actual server/tool names, readiness, tool response contract |
| `prompt` | Judge information already supplied to the evaluator | Bounded rubric, adversarial fixtures, false-positive rate |
| `agent` | Gather additional evidence before judging | Tool availability, finite search, cost and cancellation limits |

The last two are model evaluations rather than deterministic validators. Agent hooks are experimental. Prompt/agent defaults are 30/60 seconds; agents have a 50-turn ceiling. [Handler overview](https://code.claude.com/docs/en/hooks-guide#how-hooks-work), [agent limits](https://code.claude.com/docs/en/hooks-guide#agent-based-hooks).

Prompt/agent eligibility currently includes `PermissionDenied`, `PostToolBatch`, `PostToolUse`, `PostToolUseFailure`, `PreToolUse`, `Stop`, `SubagentStop`, `TaskCompleted`, `TaskCreated`, `TeammateIdle`, `UserPromptExpansion`, and `UserPromptSubmit`. `PermissionRequest` accepts prompt hooks but skips agent hooks; prompt `ok: false` cannot deny that event. [Eligibility and response semantics](https://code.claude.com/docs/en/hooks#prompt-based-hooks).

Do not translate `ok: false` into one universal behavior. A prompt hook's `continueOnBlock` changes some events; stop evaluators can return `impossible`; agent hooks have neither option. `PermissionDenied` discards prompt/agent decisions; use a command for `retry`. Use the event's documented response table when constructing the rubric. [Prompt response schema](https://code.claude.com/docs/en/hooks#response-schema).

For model evaluation, distinguish “failed”, “insufficient evidence”, and “cannot be satisfied”. Demand evidence identifiers rather than confidence adjectives. Avoid embedding full transcripts when a short structured summary contains everything needed. Never instruct an evaluator to manufacture a success condition merely to unblock the session.

## HTTP and MCP

For HTTP, a denial is a successful HTTP response carrying the event's decision JSON; an HTTP error status is not a policy denial. Header interpolation needs `allowedEnvVars`. [HTTP hook contract](https://code.claude.com/docs/en/hooks-guide#http-hooks).

Design the service so replaying an evaluation is harmless. Use an application-owned request identifier, redact unnecessary content, and return a stable machine-readable reason. Test an empty body, malformed JSON, timeout, authentication rejection and a valid negative decision separately. These are different operational states even if a dashboard labels all of them “hook failed”.

An MCP handler declares `server`, `tool` and optional `input`. Plugin servers use `plugin:<plugin-name>:<server-name>` here. Launch-time `SessionStart` and all `Setup` MCP hooks are skipped because clients are unavailable; later session-start events can run them. Hooks do not initiate OAuth. [MCP lifecycle](https://code.claude.com/docs/en/hooks#mcp-tool-hook-fields).

Consequently, bootstrap prerequisites with a command handler. Do not make the first successful connection depend on an MCP hook that itself requires that connection. Inspect the actual returned tool text; a tool designed to answer conversationally may need a small adapter to emit hook decision JSON reliably.

## Background execution and deadlines

Command `async` work cannot gate the triggering action. Results arrive on a later turn; `asyncRewake` can wake an idle session on exit `2`. Plain `async` does not enforce the configured hook timeout; `asyncRewake` does. [Background contract](https://code.claude.com/docs/en/hooks#run-hooks-in-the-background).

Use background handlers for observations whose usefulness survives delay. Record the revision being evaluated so a late result is not attributed to newer files. Coalesce repeated requests and cap worker concurrency in your own implementation; create a cancellation and shutdown plan. A background test of revision A should never silently certify revision B.

Set explicit deadlines instead of inheriting defaults. SDK callback timeouts use seconds: most events default to 600; `UserPromptSubmit`, `PreModelSwitch` and `PostModelSwitch` to 30; `MessageDisplay` to 10. `SessionEnd` shares a 1.5-second budget, configurable up to 60. A timed-out SDK `PreToolUse` callback blocks the pending call, whereas command/HTTP/MCP hooks ordinarily leave it to normal permission processing. [SDK timeout behavior](https://code.claude.com/docs/en/agent-sdk/hooks#hook-timeout), [process timeout behavior](https://code.claude.com/docs/en/hooks#timeouts).

Include time for process startup, service lookup and result encoding in the budget. A timeout result should describe missing evidence, never success. For strict enforcement, choose an underlying control whose failure behavior meets the requirement; a hook's implementation timeout is not automatically a fail-closed policy.

## Managed deployments

`allowManagedHooksOnly` restricts permitted hook sources. Managed configuration also controls plugin sources and HTTP hook policy; inspect effective settings rather than assuming a local configuration file wins. [Managed controls](https://code.claude.com/docs/en/managed-settings#keys-only-a-managed-source-can-set), [settings precedence](https://code.claude.com/docs/en/settings#settings-precedence).

Document the required source, version, runtime and event for every distributed handler. If an organization blocks that source, report the incompatibility and offer the allowed deployment route. Keep a small acceptance matrix covering the target terminal, IDE, desktop or cloud environment: availability of the same event does not guarantee the same files, credentials, executable paths or interactive approval UI.
