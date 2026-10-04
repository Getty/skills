# Build a custom client with app-server

Choose app-server when the product must own its UI, thread navigation, approvals, streaming, or orchestration around Codex.

The documented interface uses request/response and notification messages over supported transports. Initialize each connection, acknowledge with `initialized`, then start/resume a thread and start turns. Generate schemas from the target binary; experimental fields require opt-in. [App-server](https://learn.chatgpt.com/docs/app-server)

## Version-bound schema generation

```sh
codex app-server generate-ts --out ./generated/codex
codex app-server generate-json-schema --out ./generated/codex
```

Keep the generated schema version tied to the executable used in production.

Original initialization message:

```json
{
  "id": 1,
  "method": "initialize",
  "params": {
    "clientInfo": {
      "name": "release_console",
      "title": "Release Console",
      "version": "0.1.0"
    }
  }
}
```

Wait for the response, send the documented initialization acknowledgment, and then use the schema to construct thread/turn requests. Do not copy a fixed model ID into a generic integration.

## Client responsibilities

Implement request correlation, stream parsing, cancellation, reconnect policy, and separation of transport failure from failed agent work. Persist thread identifiers only under the correct account and workspace.

Handle server-initiated approval and elicitation requests as explicit product interactions. Do not auto-approve them merely to avoid a stalled stream. Distinguish read-only viewing from authority to issue new turns or modify a thread.

Design for partial progress: a disconnected client does not prove that an external tool did nothing. Reconcile operation state before retrying a mutation.

If remote access is required, choose authenticated secure transport and a deployment boundary that protects the running agent. Do not expose an unauthenticated listener as a plugin backend.

## Relationship to plugins

A plugin contributes packaged capabilities to a supported host. App-server lets an external program interact with Codex. An application can use both, but installing a plugin does not grant arbitrary app-server control.

The current documentation removes `codex mcp-server` and the standalone server binary; use app-server for integrations that previously depended on them. [SDK migration notice](https://learn.chatgpt.com/docs/codex-sdk)
