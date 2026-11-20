# Guard rails and follow-ups

Read when a headless run must be bounded, continued later or kept from spawning itself,
or when the child may start background commands.

- `--max-turns <n>` and `--max-budget-usd <amount>` bound a runaway child.
- `session_id` from the JSON + `claude -p --resume <session-id> "<next>"` continues
  that conversation; `--continue` takes the most recent one. `--session-id <uuid>`
  picks the id up front. `--no-session-persistence` for fire-and-forget runs.
- Background Bash commands the child starts are killed ~5 s after its final result — a
  headless run must finish its work in the foreground.
- Inside any Claude Code Bash call, `CLAUDECODE=1` and `CLAUDE_CODE_SESSION_ID` are
  set — a script can detect it is being run *by* Claude and avoid spawning recursively
  by accident.
