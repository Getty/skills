---
name: codex-cross-session
description: "Use when reaching a Codex session that already exists — codex queue to send it a message, codex agents to see what runs, the app-server daemon, remote-control start/pair, --remote ws:// or unix://, or a queued message that never seems to arrive."
---

# Reaching Other Codex Sessions

Codex sessions do not talk to each other. They share a **daemon** — one local
app-server that owns the running threads — and a **queue** that holds messages
until a thread picks them up. Anything you send is a letter, never a
conversation: there is no reply channel back to the sender.

Facts below verified against codex-cli 0.153.0; the remote paths in the last
section are read from the CLI contract and not measured against a second host.

## The queue is a letterbox

```bash
codex queue --thread <uuid|thread-name> --message "Mach erst die Tests grün"
# Queued message 01a06fe5-…-53c3bfdd324d for thread 01a06fe4-…-7423bb04ccc0.
```

The thread does **not** have to be running. A message for a finished thread is
accepted and parked in `~/.codex/queue_1.sqlite` (table `queued_items`), and the
next time that thread is picked up the message is played in **before** whatever
prompt you pass then. Measured: queue "merke dir 99" onto a stopped thread, then
`codex exec resume <id> "nenne alle Zahlen"` — the run answers the queued
message first, then the new prompt with both numbers, and the queue is empty
after.

That ordering is the whole design. Use the queue for an instruction that must
land before the next turn, never for a question you want answered now — nothing
comes back to you, and nothing tells you it was read except the emptied queue
and the thread's own transcript.

The thread id comes from `thread.started` in `codex exec --json`
(see `codex-headless`); a thread name works in its place.

## Seeing what runs

`codex agents` browses the sessions on the shared local app-server daemon. It is
an interactive browser — **there is no `--json`**, so it is for you to look at,
not for a script to parse. When a script needs the id, keep the `thread_id` from
the run that created it.

## The daemon, and what "remote" means here

```bash
codex remote-control start --json
# {"mode":"daemon","status":"connected","serverName":"reuben",
#  "environmentId":"env_e_…","daemon":{"remoteControlEnabled":true,
#  "socketPath":"~/.codex/app-server-control/app-server-control.sock",…}}
codex remote-control pair --json     # {"pairingCode":"…","expiresAt":1788584345}
codex remote-control stop
```

`start` brings up the daemon and connects it; `serverName` defaults to the
hostname. `pair` mints a **short-lived** pairing code — it expires, so mint it
when you are about to use it.

The client side is an address, not an account:

```
--remote ws://host:port | wss://host:port | unix://PATH
--remote-auth-token-env <ENV_VAR>     # bearer token, by env var name
```

This is the significant difference from Claude Code, where cross-machine reach
is keyed to the *account* and a host you can ssh into gives you nothing by
itself (see `claude-cross-session`). Here the daemon is addressable, so a
tunnel — `ssh -L` onto the remote app-server, then `--remote ws://127.0.0.1:…` —
reaches a Codex that belongs to somebody else's login. Verify that path before
relying on it; it is the one part of this skill not measured.

## Codex as a tool for another agent

`codex mcp-server` runs Codex as an MCP server over stdio, which is how another
agent uses Codex as one of its tools rather than as a peer. That is a different
relationship from everything above and belongs in the client's MCP config.

## Related

- `codex-headless` — creating threads with `codex exec`, the JSONL events, and
  where the `thread_id` comes from.
- `claude-cross-session` — the same problem in Claude Code, solved with a live
  socket mesh and real two-way messages instead of a queue.
