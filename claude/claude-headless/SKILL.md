---
name: claude-headless
description: "Use when running Claude Code headless — claude -p/--print, --output-format json, claude calling claude, tool approval, or a nested run that hangs, denies a tool, or picks the wrong model."
---

# Headless Claude Code

`claude -p "<prompt>"` runs one non-interactive turn-loop and exits. Calling it
from inside a running Claude Code session works — no environment cleanup
needed. Facts below verified against claude 2.1.234; when a flag misbehaves,
`claude --help` is the authority for the installed version.

## Matching the parent's model

A child does **not** inherit the parent session's model — it reads the saved
user default (`~/.claude/settings.json`, key `model`; this is where `/model`
saves). To guarantee the same model, pass it explicitly and verify:

1. The system prompt's environment block states the exact model ID — e.g.
   `MiniMax-M3-512k`, or `claude-fable-5` when on Claude. No environment
   variable carries it.
2. Pass `--model <exact-id>` using that **exact string**, verbatim. Do not
   substitute an Anthropic-family alias (`fable`, `opus`, `sonnet`, `haiku`)
   when the parent is on a different provider; those aliases resolve inside
   the Anthropic namespace only, and would silently swap the model.
3. Verify from the output: with `--output-format json`, the `modelUsage`
   object is keyed by the model ID that actually ran — assert it is the one
   you asked for.

```bash
claude -p "Reply with exactly one word: PONG" \
  --model MiniMax-M3-512k --output-format json \
  | jq -er '.result, (.modelUsage | keys[0])'
```

**Default to the model you're already on.** The frontier tier
(`fable` / `claude-fable-5`) is the most expensive slot in the Anthropic
lineup and a reliable way to set your token budget on fire for no good
reason — a one-shot `-p` call on `fable` writes a fresh cache before it
even answers. Escalate to `fable` only when the task genuinely needs
frontier reasoning; for everything else, let the parent's tier stand.

The system prompt's "alternative models" list (typically the recent Claude
family plus Haiku) is the switch menu — your current model is often *not*
on that list when it belongs to another provider. Pick the cheapest tier
appropriate for the task; per-token pricing varies by provider, so use that
provider's rate card, not Claude's.

## JSON output

`--output-format json` (requires `-p`) returns one object; the fields that
matter: `result` (the final text), `is_error`, `session_id` (feed to
`--resume`), `total_cost_usd`, `num_turns`, `stop_reason`, `modelUsage`,
`usage` (token detail), `permission_denials`. `--output-format stream-json`
emits events as they happen; `--json-schema <schema>` forces structured
output.

## Permissions — decide before launch

Print mode cannot ask. An unapproved tool call is denied (see
`permission_denials`), so the run limps or stops instead of prompting. Choose
one:

- `--allowedTools "Bash(git *),Read,Edit"` — pre-approve exactly what the task
  needs (permission-rule syntax; the deny syntax is `--disallowedTools`).
- `--permission-mode <mode>` — `auto`, `dontAsk`, `acceptEdits`, `plan`,
  `bypassPermissions`.
- `--dangerously-skip-permissions` (= `bypassPermissions`) — only inside an
  isolated environment (container, throwaway VM), never on a working checkout
  you care about.

## What the child inherits

Settings resolve against the **child's cwd**, not the parent's session:
managed → user (`~/.claude/settings.json`) → project (`.claude/settings.json`)
→ local (`.claude/settings.local.json`), plus the cwd's `CLAUDE.md`, skills,
agents, and hooks. Consequences:

- Run the child in the directory whose context it should have; `cd` is the
  main inheritance lever.
- `--setting-sources user,project,local` narrows which scopes load;
  `--settings <file-or-json>` injects overrides; `--bare` skips hooks,
  plugins, MCP, and CLAUDE.md discovery entirely — pass what it needs
  explicitly (`--append-system-prompt`, `--mcp-config`, `--agents`).
- Session-scoped state of the parent (its model, its conversation) never
  transfers; context the child needs goes into the prompt, the system-prompt
  flags, or files it can read.

## Guard rails and follow-ups

- `--max-turns <n>` and `--max-budget-usd <amount>` bound a runaway child.
- `session_id` from the JSON + `claude -p --resume <session-id> "<next>"`
  continues that conversation; `--continue` takes the most recent one.
  `--no-session-persistence` for fire-and-forget runs.
- Background Bash commands the child starts are killed ~5 s after its final
  result — a headless run must finish its work in the foreground.
- Inside any Claude Code Bash call, `CLAUDECODE=1` and
  `CLAUDE_CODE_SESSION_ID` are set — a script can detect it is being run *by*
  Claude and avoid spawning recursively by accident.

## Related

- `getty-agent-team` — subagents *within* a session (briefing-preloaded);
  reach for headless spawning only when a separate process is genuinely
  needed: clean context, different cwd, CI, or another program driving Claude.
