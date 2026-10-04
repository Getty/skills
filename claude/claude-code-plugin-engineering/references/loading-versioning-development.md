# Loading, versions, and local development

## Diagnose three independent states

| State | What it establishes | What it does not establish |
|---|---|---|
| Declared/enabled | Settings select a plugin in a scope | Files are present or trusted |
| Fetched/cached | A version exists on disk | Its components loaded into this session |
| Active | The session reports the component | The external server or behavior works |

Capture the plugin's qualified identity, source, version, effective scope, resolved root, and load errors. Do not edit install registries or cache metadata to manufacture a success state. They are useful diagnostic records; use supported commands for changes. [Loading reference](https://code.claude.com/docs/en/plugins/loading).

## Start with an in-place development copy

```bash
claude --version
claude plugin validate ./change-companion --strict
claude --plugin-dir ./change-companion
```

Inside the interactive session, use `/reload-plugins` after changes when necessary and inspect its summary. Local mod development has additional watching/reloading behavior; verify it with [mod authoring](https://code.claude.com/docs/en/plugins/mods/create). Keep a fresh-session check for startup and cleanup behavior.

`--plugin-dir` is repeatable and can load a plugin directory or ZIP. Current builds also accept a folder containing child plugins; that support is version-sensitive and does not mean every arbitrary marketplace layout is recursively scanned. Session-only plugins use the `@inline` identity and ordinarily override an installed plugin of the same name; managed selection can take precedence. Pass the same session flag when using `plugin list` to inspect that copy. [Session flags and precedence](https://code.claude.com/docs/en/plugins/cli-reference#flags-that-load-a-plugin-for-one-session).

Do not assume `.claude/plugins/` is an auto-discovery directory. Skills-directory plugins have a separate documented discovery/trust model. Explicit paths are the least ambiguous route while authoring.

## Verify both in-place and cached loading

A local-directory marketplace with a relative plugin source loads that source in place. Many remote sources are copied into a version cache. Only distributable content reaches a cached installation; links to a sibling checkout or an undeclared build output often explain a local-only success. `${CLAUDE_PLUGIN_ROOT}` identifies the current code location; `${CLAUDE_PLUGIN_DATA}` is the persistent writable location. [Source copying and path containment](https://code.claude.com/docs/en/plugins/loading#where-plugin-files-live).

Recreate the install from its actual source in a disposable destination. Run from a project unrelated to the author's checkout, and include a path containing spaces. Confirm the script, interpreter, optional binary, configuration, and data directory independently. Do not patch the cached copy as the durable fix.

## Understand reload limits

Reloading updates active components, but a reload that changes MCP tools or the `LSP` tool may stop with a prompt-cache warning. Use `/reload-plugins --force` only when accepting that specific cache consequence. An unchanged MCP configuration need not restart a changed server executable. Reconnect or start a new session when the server implementation itself must restart.

Noninteractive/headless reload support requires v2.1.260 or later and a command entered directly into that session. A remotely relayed command can be rejected. In those sessions, reload does not connect or disconnect plugin MCP servers; start a new session for that change. [Reload contract](https://code.claude.com/docs/en/plugins/cli-reference#reload-plugins).

## Version and package-runtime behavior

For most source types, an explicit plugin manifest version outranks a marketplace entry version; when both are absent, resolution depends on source type. Claude.ai-hosted and command sources have their own rules. An unchanged computed version generally leaves a cached copy unchanged. Treat code version, data schema version, dependency range, and minimum host version as four different values. [Version computation](https://code.claude.com/docs/en/plugins/loading#versions-and-updates).

Current cached installs can install Node dependencies when the plugin root has `package.json` and a supported lockfile. Recognized candidates include text `bun.lock`, `npm-shrinkwrap.json`, and `package-lock.json`; Yarn, pnpm, binary Bun locks, workspace dependencies, or native lifecycle builds need another provisioning design. The automatic step uses constrained frozen resolution and disables lifecycle scripts; it is not a general build system. In-place local-directory marketplace loading does not perform that install into the source tree. [Runtime dependency contract](https://code.claude.com/docs/en/plugins/loading#nodejs-package-dependencies).

Declare the interpreter/package manager users need. If a separate setup command or hook provisions a data-directory environment, make it idempotent, versioned, interruptible, and visibly fail when it cannot complete. Do not run an unrequested package bootstrap merely to inspect a plugin.

## Repeatable headless deployment

Prepare source access, enabled settings, configuration, and runtime dependencies before the first request. Background installation can otherwise make an enabled plugin absent from an early query. The organization guide documents `CLAUDE_CODE_SYNC_PLUGIN_INSTALL=1` and seeded caches for applicable CI/container deployments. A seed alone does not select a plugin for use. [Organization deployment](https://code.claude.com/docs/en/plugins/org).

Record the observed active components at startup and fail clearly when a required component is missing. Keep credentials out of images, transcripts, and source-controlled example settings. Preserve state across updates and understand cleanup before uninstalling the final scope; see [configuration and state](configuration-state-secrets.md).
