# MCP tool contracts and server design

Build tools around meaningful user actions. Keep read, draft, and commit operations distinguishable.

The plugin server exposes named tools with explicit inputs, optional structured output schemas, descriptions, and annotations. Server instructions provide cross-tool guidance. Results can include `structuredContent`, model-readable `content`, and client-only `_meta`. [Server implementation](https://developers.openai.com/plugins/build/mcp-server)

## Original contract sketch

This JSON is an application design artifact, not a host manifest:

```json
{
  "name": "get_release",
  "inputSchema": {
    "type": "object",
    "properties": {
      "release_id": {"type": "string", "minLength": 1}
    },
    "required": ["release_id"],
    "additionalProperties": false
  },
  "annotations": {
    "readOnlyHint": true,
    "destructiveHint": false,
    "openWorldHint": false
  }
}
```

The annotation choices assume a read-only lookup within a bounded private release store. Change them if actual behavior differs. Annotations do not replace backend access checks. [Tool design](https://developers.openai.com/plugins/plan/tools)

## Define before implementing

For each tool, specify its tenant/account context, accepted identifiers, pagination, maximum input/output sizes, error types, retries, side effects, and audit evidence.

Example decomposition:

- `find_release` resolves a human description to candidate stable IDs.
- `get_release` reads one authorized record.
- `prepare_release_change` produces a reviewable proposed change.
- `apply_release_change` performs the authorized mutation using a revision check.

These names and decomposition are design suggestions; they are not built-in Codex tools.

Make mutations idempotent where feasible. Use resource versions or equivalent conflict detection when a prior read can become stale. Return an operation receipt rather than merely saying “done.”

Treat returned documents and messages as untrusted data. Do not convert content retrieved from an external record into new agent instructions. Keep explanations compact and provide stable handles for follow-up reads.

Start with one SDK implementation supported by the project's dependency policy. Read its current primary documentation before writing executable server code; this reference deliberately avoids freezing an SDK's evolving import paths.
