![codex](../assets/codex.png)

# Codex skills

Working with the Codex CLI itself: driving it non-interactively, and reaching a
thread that already exists. Both are reference skills — nothing here is specific
to one project.

## [codex-headless](codex-headless/SKILL.md)

`codex exec` runs one non-interactive session and exits. What bites first is
stdin: `exec` accepts its prompt from an argument *or* from stdin, and with stdin
left open it waits for it anyway — a scripted run prints `Reading additional
input from stdin...` and hangs until you add `< /dev/null`.

Covers the JSONL events (`thread.started` carrying the `thread_id` you need for
everything else, `agent_message` for the answer, `turn.completed` for the usage),
the sandbox dial `read-only`/`workspace-write`/`danger-full-access`, the fact that
Codex expects a git repository, models being gated by the account — asking for
`gpt-5.1-codex` on a ChatGPT login fails the turn — and `exec resume`, which keeps
the thread's memory but accepts neither `--sandbox` nor `--cd`.

**Load when** running Codex non-interactively, resuming a thread, or when an exec
run hangs, refuses a model, or complains about a git repository.

## [codex-cross-session](codex-cross-session/SKILL.md)

Codex sessions do not talk to each other. They share a local app-server daemon
and a queue, and anything you send is a letter with no reply channel.

Covers `codex queue --thread … --message …` (accepted even for a finished thread,
parked in `~/.codex/queue_1.sqlite`, and played in *before* the next prompt when
the thread is picked up again), `codex agents` as an interactive browser with no
`--json`, the `remote-control start`/`pair`/`stop` daemon with its short-lived
pairing code, and the client side `--remote ws://…|wss://…|unix://…` with a bearer
token — an **address**, where Claude Code keys cross-machine reach to the account.

**Load when** sending a message to an existing thread, listing what runs, or
setting up Codex across hosts.
