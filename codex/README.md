![codex](../assets/codex.png)

# Codex skills

Working with Codex itself: driving the CLI non-interactively, reaching a thread
that already exists, and building plugins for it. All three are reference skills —
nothing here is specific to one project.

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
Measured: an ssh tunnel onto the remote control socket reaches a Codex running
under somebody else's login, no shared account and no open port involved.

**Load when** sending a message to an existing thread, listing what runs, or
setting up Codex across hosts.

## [codex-plugin-engineering](codex-plugin-engineering/SKILL.md)

A plugin showing up in a catalog proves less than it looks. The visible client, the
service that orchestrates, the machine that executes and the connected identity are
four separate things, and a capability exists per surface: the CLI and the desktop
app take native plugins, the IDE extension takes standalone skills and directly
configured MCP, and cloud-orchestrated ChatGPT Work drops plugin hooks — connecting
a computer does not move the orchestration onto it.

Covers the two package formats — the portable root `plugin.json` with `skills/` and
`mcp.json`, and the `.codex-plugin/plugin.json` compatibility bundle with its own
`.mcp.json` spelling — marketplaces and host state, skills with their
`agents/openai.yaml` metadata, MCP connections, tool contracts and authentication,
and lifecycle hooks with their per-event output contracts: a familiar Claude event
name guarantees nothing, and an unsupported `PreToolUse` output fails the hook while
the tool runs anyway. Also MCP Apps UI, events, and the cases where the answer is
not a plugin at all but the Codex SDK or an app-server client.

Development workflow, testing, release, migration and debugging are split by phase
— 22 references, loaded one decision at a time, on a dated snapshot. Schema
validation is never reported as an end-to-end runtime test.

**Load when** building, testing, migrating or publishing a Codex plugin, deciding
between plugin, SDK and app-server, or when a plugin is listed but its hook, tool
or UI does not run on the target host.
