# Tools and commands

Choose a model tool for an operation the agent may select, a session slash command for an explicit user's action, and a CLI subcommand for setup or multi-option administration. These entry points have different invocation and identity contexts.

The [native plugin API](https://github.com/NousResearch/hermes-agent/blob/158fd638da1629c8e62caf9ade1515d162def8ab/hermes_cli/plugins.py) supplies `register_tool`, `register_command`, `register_cli_command`, and `dispatch_tool`. Built-in development in `tools/` is a separate core contribution path.

## Complete minimal tool plugin

Put the manifest from [discovery](02-discovery-and-manifests.md) beside this original `__init__.py` example:

```python
import json

SCHEMA = {
    "name": "text_metrics_count",
    "description": "Count characters and whitespace-separated words in supplied text.",
    "parameters": {
        "type": "object",
        "properties": {"text": {"type": "string", "maxLength": 20000}},
        "required": ["text"],
        "additionalProperties": False,
    },
}

def count_text(args, **kwargs):
    value = args.get("text")
    if not isinstance(value, str) or len(value) > 20000:
        return json.dumps({"ok": False, "error": "text must be at most 20000 characters"})
    return json.dumps({
        "ok": True,
        "characters": len(value),
        "words": len(value.split()),
    })

def register(ctx):
    ctx.register_tool(
        name="text_metrics_count",
        toolset="text_metrics",
        schema=SCHEMA,
        handler=count_text,
    )
    ctx.register_command(
        "textmetrics",
        handler=lambda raw: count_text({"text": raw}),
        description="Count characters and words in supplied text.",
    )
```

The schema description is what the model sees. Handler validation remains necessary even if the model or an upstream JSON-schema validator checks input. This example has no I/O, secrets, side effects, or dependencies; it establishes a narrow baseline.

For an asynchronous handler, check the installed `register_tool(..., is_async=True)` contract. Do not return a coroutine accidentally from a synchronous registration.

## Production operation design

Define input limits, error categories, deadlines, cancellation, idempotency keys, and output bounds before adding network/file actions. Return machine-readable errors that distinguish refused, unavailable, failed, and successful outcomes. Do not turn a partial write into success.

Use `check_fn` and declared environment requirements for availability, while keeping probes passive. Missing credentials should produce a setup instruction, not silent substitution of another account.

## Commands

The [CLI extension guide](https://hermes-agent.nousresearch.com/docs/developer-guide/extending-the-cli) describes terminal subcommands. A session `register_command` handler accepts the raw argument string and may be async. A `register_cli_command` setup function builds an argparse parser; the handler receives its Namespace. Built-in command names take precedence.

When a command needs host tool execution, prefer `ctx.dispatch_tool(name, args)` over direct imports of private dispatch helpers. Verify inherited workspace/model behavior on the target surface. A raw SDK handler is outside this path; gateway command authorization does not automatically protect it.

For child-agent orchestration, consult the explicit lifecycle service in [state and lifecycle](06-state-and-lifecycle.md) rather than assuming a command handler always has a live parent agent.

