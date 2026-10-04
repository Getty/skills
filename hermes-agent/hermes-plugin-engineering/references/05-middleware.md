# Middleware

Use middleware when a plugin must alter a request or wrap execution. Use observers for reporting. The supported [middleware contract](https://hermes-agent.nousresearch.com/docs/developer-guide/middleware) exposes four kinds:

| Kind | Input | Return |
| --- | --- | --- |
| `tool_request` | `tool_name`, effective `args`, `original_args`, context | `{"args": complete_replacement}` or `None` |
| `llm_request` | effective `request`, `original_request`, context | `{"request": complete_replacement}` or `None` |
| `tool_execution` | effective arguments and `next_call` | The tool result expected by Hermes |
| `llm_execution` | effective provider request and `next_call` | The provider result expected by Hermes |

Request middleware runs before downstream host checks. Tool execution wrappers run after the ordinary pre-execution approval/guardrail path. Preserve original and effective values in redacted diagnostics.

## Safe, bounded shaping example

This original callback only changes the plugin-owned tool from [tools](03-tools-and-commands.md), and preserves all other arguments:

```python
def normalize_text_request(tool_name, args, **kwargs):
    if tool_name != "text_metrics_count":
        return None
    value = args.get("text")
    if not isinstance(value, str):
        return None
    return {
        "args": {**args, "text": value.replace("\r\n", "\n")},
        "source": "text-metrics",
        "reason": "normalize line endings",
    }

def register(ctx):
    ctx.register_middleware("tool_request", normalize_text_request)
```

This is a middleware fragment to combine with a real plugin registration; it does not register the tool itself. Decide whether newline normalization changes the intended metric before adopting it.

## Execution semantics

The [implementation](https://github.com/NousResearch/hermes-agent/blob/158fd638da1629c8e62caf9ade1515d162def8ab/hermes_cli/middleware.py) tracks single-use downstream execution. Call `next_call(args)` for tools or `next_call(request)` for provider calls once, or deliberately return a valid short-circuit result. Do not call it repeatedly for retries or split one tool call into several hidden side effects.

Middleware errors are not a dependable enforcement boundary: the host can continue the base chain. Once a downstream result exists, a wrapper's later exception must not cause re-execution. Preserve downstream exceptions as failures instead of converting them to a successful empty result.

## Design constraints

Treat request replacements as complete payloads, not JSON patches. Verify provider mode: Responses API input and chat-completion messages are different schemas. Preserve streaming objects, tool-call IDs, error behavior, and cancellation.

Do not mutate a security-relevant path, command, URL, or account inside execution middleware after the user's approval covered different arguments. Move that rewrite to request middleware. For workflow expansion, expose an explicit composite operation or use host-managed child execution with its own audit and permission boundaries.

Test chaining with another plugin, an exception before downstream execution, an exception after execution, cancellation, denied actions, and both streaming/non-streaming model calls.

