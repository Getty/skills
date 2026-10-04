# Command-hook protocol and decisions

Verified on 2026-10-04. These are command-hook contracts, not SDK callback signatures or in-process mod APIs.

## Contents

- [Input and process invocation](#input-and-process-invocation)
- [stdout, stderr and exit status](#stdout-stderr-and-exit-status)
- [Original minimal Python example](#original-minimal-python-example)
- [Offline verification](#offline-verification)

## Input and process invocation

Read one JSON object from stdin. Common fields include `session_id`, `cwd`, `hook_event_name` and `transcript_path`; others depend on the event. `PreToolUse` supplies `tool_name`, `tool_input` and `tool_use_id`; `PermissionRequest` omits `tool_use_id`. Do not require optional fields universally. [Input schema](https://code.claude.com/docs/en/hooks#common-input-fields), [permission input](https://code.claude.com/docs/en/hooks#permissionrequest-input).

Example fixture, using deliberately synthetic paths:

```json
{
  "session_id": "fixture-session",
  "transcript_path": "/fixture/transcript.jsonl",
  "cwd": "/fixture/project",
  "hook_event_name": "PreToolUse",
  "tool_name": "Write",
  "tool_use_id": "fixture-tool",
  "tool_input": {"file_path": "/fixture/project/.env", "content": "demo"}
}
```

Use exec form to pass a plugin script as one argument:

```json
{
  "type": "command",
  "command": "python3",
  "args": ["${CLAUDE_PLUGIN_ROOT}/scripts/check_file.py"],
  "timeout": 5
}
```

With `args`, Claude Code spawns the executable directly; omitting it selects shell form. Choose the interpreter available on the target platform. Windows `.cmd` shims need a shell or their underlying script interpreter. [Command fields](https://code.claude.com/docs/en/hooks#command-hook-fields). Keep bundled code under `${CLAUDE_PLUGIN_ROOT}` and persistent state under `${CLAUDE_PLUGIN_DATA}`. [Plugin paths](https://code.claude.com/docs/en/plugins-reference#environment-variables).

## stdout, stderr and exit status

| Output | Contract to design around |
|---|---|
| Exit `0`, no decision | No objection; ordinary permission processing continues. |
| Exit `0`, valid JSON object | Preferred structured response. |
| Exit `2` | Blocks only events with a blocking contract; it is not a universal veto. |
| Another exit code | Normally nonblocking without valid decision JSON; valid JSON can still control standard decision events. |

JSON is considered alongside exit status, including nonzero status. Use one intentional response path and one JSON object; keep diagnostics out of stdout. [Output guide](https://code.claude.com/docs/en/hooks-guide#read-input-and-return-output).

`PermissionRequest` requires `hookSpecificOutput.decision.behavior`; exit `2` alone does not deny it. `Stop` and `SubagentStop` use top-level `decision: "block"` with `reason` to request continuation. `PostToolUse` cannot reverse an executed operation. Worktree events and observational events have their own exceptions. Read the [per-event exit table](https://code.claude.com/docs/en/hooks#exit-code-2-behavior-per-event) and [decision fields](https://code.claude.com/docs/en/hooks#decision-control) before attaching a generic error wrapper.

For `PreToolUse`, place `permissionDecision` and `updatedInput` inside `hookSpecificOutput` with `hookEventName: "PreToolUse"`. Decisions include `allow`, `deny`, `ask` and `defer`; input replacement without a decision still follows normal permission evaluation. [Decision and rewrite contract](https://code.claude.com/docs/en/hooks#pretooluse-decision-control).

`defer` ignores `updatedInput`. It is honored only in noninteractive `-p` runs with one tool call in the turn; interactive sessions and multi-call batches ignore it with a warning. [Deferral limits](https://code.claude.com/docs/en/hooks#defer-a-tool-call-for-later).

This is control over the pending call. It does not define a general split/merge API for replacing one call with an arbitrary sequence. If a product needs several ordered operations, expose a composite tool or use an explicit workflow/host integration with its own state model.

## Original minimal Python example

This example illustrates a narrow file-name policy for `Write` and `Edit`. It neither executes tool input nor grants permission. It is suitable for local fixture tests before registration.

```python
import json
import sys
from pathlib import PurePosixPath


def decide(event):
    if not isinstance(event, dict):
        raise ValueError("object required")
    if event.get("hook_event_name") != "PreToolUse":
        return {}
    if event.get("tool_name") not in {"Write", "Edit"}:
        return {}
    args = event.get("tool_input")
    if not isinstance(args, dict):
        raise ValueError("tool_input must be an object")
    value = args.get("file_path")
    if not isinstance(value, str) or not value or "\x00" in value:
        raise ValueError("file_path must be a nonempty path")
    path = PurePosixPath(value.replace("\\", "/"))
    if path.name == ".env" or ".git" in path.parts:
        return {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason":
                    "This file is outside the example edit policy."
            }
        }
    return {}


def main():
    try:
        result = decide(json.load(sys.stdin))
    except (ValueError, TypeError):
        print("The example hook could not validate its input.", file=sys.stderr)
        return 2
    print(json.dumps(result, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

The policy is intentionally limited: it checks lexical path components, not symlink targets, filesystem races or alternate tools. Define those requirements before adapting it into an enforcement mechanism. Missing interpreters and hung processes are different failures from rejected input; explicit error handling inside a script cannot repair a process that never starts.

## Offline verification

Exercise `decide` with the fixture above, an ordinary source file, an unrelated event, malformed `tool_input`, Windows separators, and a path containing an apostrophe. Verify the exact response object and that the input object is unchanged. Separately verify malformed JSON exits `2` with a diagnostic on stderr and no stdout payload.

Only then register the hook in a disposable project and inspect the actual host event. A successful direct script test proves the script's branches; it does not prove loading, matching, permission precedence or host timeout behavior. Keep that distinction in the plugin's validation report.
