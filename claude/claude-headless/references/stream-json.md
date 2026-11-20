# JSON output and the stream-json channel

Read when parsing a `--output-format json` result, streaming events, forcing structured
output, or holding several turns with one `claude -p` process.

## JSON output

`--output-format json` (requires `-p`) returns one object; the fields that matter:
`result` (the final text), `is_error`, `session_id` (feed to `--resume`),
`total_cost_usd`, `num_turns`, `stop_reason`, `modelUsage`, `usage` (token detail),
`permission_denials`. `--output-format stream-json` emits events as they happen and
additionally requires `--verbose`; `--json-schema <schema>` forces structured output.

## Staying in the conversation

The single turn is a choice, not a limit. `--input-format stream-json` keeps stdin
open, so one process takes several turns and remembers the earlier ones:

```python
p = subprocess.Popen(
    ["claude","-p","--input-format","stream-json","--output-format","stream-json",
     "--verbose","--replay-user-messages","--model","claude-haiku-4-5-20251001"],
    stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True, bufsize=1)

def say(text):                       # one message in
    p.stdin.write(json.dumps({"type":"user","message":{"role":"user",
        "content":[{"type":"text","text":text}]}}) + "\n")
    p.stdin.flush()                  # read stdout until type == "result"
```

`--replay-user-messages` echoes each message back so the driver knows it landed;
closing stdin ends the run. `--include-partial-messages` streams chunks as they arrive,
`--forward-subagent-text` surfaces what its subagents say. Both need
`--output-format stream-json`.

## Letting a print run ask

This channel is also the one way a print run can *ask*: point `--permission-prompt-tool`
at an MCP tool of your own and every tool decision comes to the driver as a question
instead of being silently denied.

Because the channel is a pipe, it survives ssh: [ssh-hosts.md](ssh-hosts.md).
