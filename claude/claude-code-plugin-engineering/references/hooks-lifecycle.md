# Hook lifecycle and event selection

Verified against official documentation on 2026-10-04. Treat this as a design map; check the installed Claude Code version before using newer events. The [event inventory](https://code.claude.com/docs/en/hooks#hook-events) owns each event's schema.

## Choose the invariant before the event

Write down the condition the extension must preserve, the last point at which it can affect that condition, and what should happen when the condition cannot be checked. Then choose the narrowest event.

| Design intention | Starting event | Implementation question |
|---|---|---|
| Inspect one proposed operation | `PreToolUse` | Which exact tool and argument schema are in scope? |
| Answer an approval request | `PermissionRequest` | Who authorized this decision, and how is that authority represented? |
| Interpret a completed operation | `PostToolUse`, `PostToolUseFailure` | What evidence identifies this particular execution? |
| Evaluate the combined result of parallel work | `PostToolBatch` | Is the assessment meaningful only after the entire batch? |
| Check a submitted or expanded prompt | `UserPromptSubmit`, `UserPromptExpansion` | Should rejection preserve an actionable explanation? |
| Check completion | `Stop`, `SubagentStop` | What finite, observable completion condition is missing? |
| Track session and context transitions | `SessionStart`, `SessionEnd`, `PreCompact`, `PostCompact` | Does the work require live state or only a durable record? |
| Integrate host changes | `ConfigChange`, `CwdChanged`, `DirectoryAdded`, `FileChanged` | Could the handler itself cause another matching event? |

This selection table is engineering guidance, not a complete capability matrix. Look up task, teammate, worktree, notification, elicitation, instruction-loading, model-switch and display events when those are the actual integration point. Avoid treating an event name as proof that every handler type or decision field is accepted. [Lifecycle reference](https://code.claude.com/docs/en/hooks#hook-lifecycle).

## Filtering correctly

General matcher rules: omitted, empty or `*` means all; letters, digits, underscores, hyphens, spaces, commas and pipes select exact names or comma/pipe-separated exact alternatives. Other characters select unanchored JavaScript regex. Thus `Edit|Write` is exact; anchor regex when necessary. `FileChanged` and `StopFailure` have narrower exact-name rules; file-watch registration additionally interprets literal filenames. [Matcher rules](https://code.claude.com/docs/en/hooks#matcher-patterns).

For each hook, record its filter field: tool name, agent type, event subtype, or none. A tool matcher is not a filename matcher. Inspect arguments in the handler when correctness depends on paths, content or several conditions. A handler's `if` uses one permission-rule expression and is evaluated only on tool events; using it on another event suppresses that handler. [Handler filters](https://code.claude.com/docs/en/hooks#common-fields).

Test a filter with positive and negative examples, including names that contain the intended name as a substring. Use an observed MCP tool name in a fixture; plugin-scoped server names differ from bare server configuration keys. Do not construct a test that simply repeats the same matching implementation.

## Composition and termination

Matching handlers execute concurrently. A sibling denial does not cancel other handlers; permission decisions combine as `deny > defer > ask > allow`. Competing input rewrites are nondeterministic because the last completion wins. [Combination rules](https://code.claude.com/docs/en/hooks-guide#combine-results-from-multiple-hooks), [limitations](https://code.claude.com/docs/en/hooks-guide#limitations).

Give each mutable resource one writer. Keep observational hooks free of irreversible side effects. For shared logs, choose atomic appends or an explicit collector; for generated files, use temporary files and atomic replacement. Correlate work by session, agent and tool-use identifiers rather than assuming completion order matches invocation order.

A stop condition should make progress possible and have a finite escape condition. Inspect `stop_hook_active` before issuing another continuation. [Stop-loop troubleshooting](https://code.claude.com/docs/en/hooks-guide#stop-hook-hits-the-block-cap).

For example, a completion check can request one missing test result, remember the relevant revision, and then assess that result. Repeating “verify everything” without recording what changed creates an unbounded loop. An unavailable dependency should produce a bounded explanation, not an instruction to retry indefinitely.

## Policy boundary

Ordinary `PreToolUse` approvals do not override deny or ask rules. Mods have a different permission interception layer; do not infer their authority from command-hook behavior. [Permission integration](https://code.claude.com/docs/en/permissions#extend-permissions-with-hooks).

If the invariant is filesystem or network isolation, implement it in the applicable permission and sandbox controls. Use the hook to explain, enrich or coordinate that policy. For the process protocol, read [command contracts](hooks-command-contracts.md); for model, HTTP, MCP and background handlers, read [advanced hooks](hooks-advanced.md).
