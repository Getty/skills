---
name: codex-headless
description: "Use when running the Codex CLI non-interactively — codex exec, its JSONL events, resuming or forking a thread by id, sandbox and approval settings, an exec run that hangs on stdin, refuses a model, or complains about a git repository."
---

# Headless Codex

`codex exec "<prompt>"` runs one non-interactive session and exits. Facts below
verified against codex-cli 0.153.0; when a flag misbehaves, `codex exec --help`
is the authority for the installed version.

## The stdin trap

`exec` takes its prompt from an argument **or** from stdin, and announces
`Reading additional input from stdin...` either way. With a prompt already given
and stdin left as an open pipe that never closes, it waits on that pipe. Close
it and the run is unambiguous:

```bash
codex exec --json -s read-only "Antworte mit genau einem Wort: PONG" < /dev/null
```

Piping deliberately is the other half of the same rule: with a prompt argument
*and* piped stdin, the pipe is appended as a `<stdin>` block.

## JSONL events

`--json` prints one event per line. The shape that matters:

```json
{"type":"thread.started","thread_id":"01a06fe4-3c80-72f0-ad06-b75fdffd45ad"}
{"type":"turn.started"}
{"type":"item.completed","item":{"id":"item_0","type":"agent_message","text":"PONG"}}
{"type":"turn.completed","usage":{"input_tokens":15689,"cached_input_tokens":12160,
 "output_tokens":6,"reasoning_output_tokens":0}}
```

Take the answer from the `agent_message` item, the cost from `turn.completed`,
and **the `thread_id` from `thread.started`** — that id is the handle for
everything below. Failures arrive as `error` and `turn.failed`, both carrying
the provider's message. `-o <file>` writes just the final message to a file,
and `--output-schema <file>` constrains the model's final response.

## Where it runs and what it may do

- `-C/--cd <DIR>` sets the working root; `--add-dir` adds writable directories.
- **Codex expects a git repository** and stops outside one — `--skip-git-repo-check`
  when that is deliberate.
- `-s/--sandbox` is the permission dial: `read-only`, `workspace-write`,
  `danger-full-access`. `--approve-for-me` routes approvals through automatic
  review under `workspace-write`;
  `--dangerously-bypass-approvals-and-sandbox` drops both and belongs only in an
  externally sandboxed environment.
- `--ephemeral` keeps the run out of the session files;
  `--ignore-user-config` and `--ignore-rules` narrow what is loaded.

## Models

`-m/--model` takes the provider's own id, and the account decides what is
allowed: with a ChatGPT login, asking for `gpt-5.1-codex` fails the turn with
*"not supported when using Codex with a ChatGPT account"* — after a warning
about missing model metadata that looks harmless and is not. Leave `-m` off to
take the configured default unless a specific model is the point. `--oss` with
`--local-provider lmstudio|ollama` runs against a local provider instead.

## Continuing a thread

```bash
codex exec resume <thread-id|thread-name> "<next prompt>" --json
```

The thread keeps its id and its memory — turn two still knows what turn one was
told. `--last` picks the most recent recorded session; `codex exec fork` starts
a new thread from an old one.

**`resume` accepts neither `-s/--sandbox` nor `-C/--cd`.** Sandbox and working
root are decided when the thread is created; a resumed turn cannot widen or
narrow them. Plan the sandbox at `exec` time.

It does take `--skip-git-repo-check`, and needs it just as much as `exec` does:
outside a repository a resume stops with `Not inside a trusted directory and
--skip-git-repo-check was not specified` — on stderr, so a script filtering for
JSON events sees an empty run and no reason.

## Related

- `codex-cross-session` — reaching a thread that already exists: `codex queue`,
  the shared app-server daemon, and driving Codex on another host.
- `claude-headless` — the same job for Claude Code, with a genuinely different
  permission model and a bidirectional stdin channel Codex has no equivalent
  for.
