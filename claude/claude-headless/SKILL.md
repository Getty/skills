---
name: claude-headless
description: "Use when running Claude Code headless — claude -p, JSON output, claude calling claude, or a nested run that hangs, denies a tool or picks the wrong model."
---

# Headless Claude Code

`claude -p "<prompt>"` runs one non-interactive turn-loop and exits. Calling it from
inside a running Claude Code session works — no environment cleanup needed. Facts below
verified against claude 2.1.261; when a flag misbehaves, `claude --help` is the
authority for the installed version.

## Matching the parent's model

A child does **not** inherit the parent session's model — it reads the saved user
default (`~/.claude/settings.json`, key `model`; this is where `/model` saves). To
guarantee the same model, pass it explicitly and verify:

1. The system prompt's environment block states the exact model ID — e.g.
   `MiniMax-M3-512k`, or `claude-opus-5-5` when on Claude. No environment variable
   carries it.
2. Pass `--model <exact-id>` using that **exact string**, verbatim. Do not substitute
   an Anthropic-family alias (`fable`, `opus`, `sonnet`, `haiku`) when the parent is on
   a different provider; those aliases resolve inside the Anthropic namespace only, and
   would silently swap the model.
3. Verify from the output: with `--output-format json`, the `modelUsage` object is
   keyed by the model ID that actually ran — assert it is the one you asked for.

```bash
claude -p "Reply with exactly one word: PONG" \
  --model MiniMax-M3-512k --output-format json \
  | jq -er '.result, (.modelUsage | keys[0])'
```

**Default to the model you're already on.** Switch to `fable` / `claude-fable-5-2` only
when the run's task sits at the frontier tier of skill `model-routing` — it is the most
expensive slot, and a one-shot `-p` call on it writes a fresh cache before it even
answers. The system prompt's "alternative models" list (typically the recent Claude
family plus Haiku) is the switch menu; your current model is often *not* on it when it
belongs to another provider. Pick the cheapest tier appropriate for the task, priced by
that provider's rate card, not Claude's.

## Permissions — decide before launch

A one-shot print run cannot ask. An unapproved tool call is denied (see
`permission_denials` in the JSON), so the run limps or stops instead of prompting.
Choose one:

- `--allowedTools "Bash(git *),Read,Edit"` — pre-approve exactly what the task needs
  (permission-rule syntax; the deny syntax is `--disallowedTools`).
- `--permission-mode <mode>` — `auto`, `dontAsk`, `acceptEdits`, `plan`,
  `bypassPermissions`.
- `--dangerously-skip-permissions` (= `bypassPermissions`) — only inside an isolated
  environment (container, throwaway VM), never on a working checkout you care about.

A run that should ask instead needs the stream-json channel and
`--permission-prompt-tool`: [references/stream-json.md](references/stream-json.md).

## What the child inherits

Settings resolve against the **child's cwd**, not the parent's session: managed → user
(`~/.claude/settings.json`) → project (`.claude/settings.json`) → local
(`.claude/settings.local.json`), plus the cwd's `CLAUDE.md`, skills, agents, and hooks.

- Run the child in the directory whose context it should have; `cd` is the main
  inheritance lever.
- `--setting-sources user,project,local` narrows which scopes load;
  `--settings <file-or-json>` injects overrides; `--bare` skips hooks, plugins, MCP,
  and CLAUDE.md discovery entirely — pass what it needs explicitly
  (`--append-system-prompt`, `--mcp-config`, `--agents`).
- Session-scoped state of the parent (its model, its conversation) never transfers;
  context the child needs goes into the prompt, the system-prompt flags, or files it
  can read.

## The child is a peer

A `-p` child is a full session, not an isolated command. It appears in
`claude agents --json` as `kind: interactive`, named after its directory, and can call
`ListAgents` and `SendMessage` to reach the session that started it and every other
session on the machine. So it can talk back while it works, not only through its exit
JSON, and you can talk to it. See `claude-cross-session`.

## Read on demand

- JSON result fields, `stream-json` output, `--json-schema`, several turns in one
  process over stdin (the single turn is a choice, not a limit), a print run that
  asks: [references/stream-json.md](references/stream-json.md).
- An agent on another host over ssh — somebody else's login, a Windows host, the
  base64-wrapped remote command: [references/ssh-hosts.md](references/ssh-hosts.md),
  with the channel from [references/stream-json.md](references/stream-json.md).
- Bounding a run (`--max-turns`, `--max-budget-usd`), resuming or continuing it,
  session persistence, background commands the child starts (killed right after its
  result), recursion detection: [references/guard-rails.md](references/guard-rails.md).

## Related

- `claude-cross-session` — when you do not want a result but a counterpart: starting a
  session elsewhere with `claude --bg` and talking to it while it runs.
- `getty-agent-team` — subagents *within* a session (briefing-preloaded); reach for
  headless spawning only when a separate process is genuinely needed: clean context,
  different cwd, CI, or another program driving Claude.
