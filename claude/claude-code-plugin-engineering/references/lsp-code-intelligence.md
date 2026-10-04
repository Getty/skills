# LSP and code intelligence

## Configure an existing language service

Use LSP for language diagnostics and navigation. Package connection settings; do not promise every server capability is exposed by Claude Code. Check the actual server version and host operations.

Original minimal `.lsp.json`:

```json
{
  "go-project": {
    "command": "gopls",
    "args": ["serve"],
    "extensionToLanguage": { ".go": "go" }
  }
}
```

The file is a direct server-name map. `command` and `extensionToLanguage` are required; arguments belong in `args`. The plugin does not install the binary. A malformed `.lsp.json` can be skipped at runtime despite a successful manifest-only validation. [LSP component contract](https://code.claude.com/docs/en/plugins/components#lsp-servers).

## Verify the environment

Check that the process starts in the agent's environment. A binary in an interactive shell may be absent from an IDE-launched process. Confirm extension routing, project-root discovery, dependency metadata, and a diagnostic or symbol result on a small real project.

When servers claim the same extension, inspect which registered first. Remove the conflict or choose the intended provider instead of repeatedly reinstalling an unused server.

## Protocol and resource behavior

Current configuration accepts timeouts, restart controls, diagnostics, initialization options, and settings. Although the schema accepts `transport: "socket"`, the documented runtime uses stdio. Keep stdout clean. `requestTimeout` requires v2.1.288 or later. Unknown LSP configuration keys are errors. [LSP schema](https://code.claude.com/docs/en/plugins/manifest-reference#lspservers).

Set a restart budget. Repeated restarts cannot repair malformed protocol output or a missing dependency. Measure initialization separately from request latency; indexing may dominate a large project's first query.

## Acceptance cases

- Introduce a known type error in a disposable fixture and confirm it reaches the host.
- Resolve a symbol with an unambiguous definition and verify its location.
- Exercise routing with a second language plugin enabled.
- Start without the binary and check the startup diagnostic.
- Verify shutdown and crash recovery without accumulating server processes.

Use native compiler and behavioral tests for correctness gates. A successful LSP request does not prove the program builds or behaves correctly.
