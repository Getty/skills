# Host portability and Agent SDK integration

## Define compatibility as several independent questions

For each target, establish package discovery, component support, runtime availability, authentication/provider, permissions, interaction surface, and lifecycle. A shared manifest or MCP protocol does not imply identical loading or UI behavior.

The current documented **mod** surface matrix is:

| Claude Code surface | Mod handlers | Mod drawing | Design consequence |
|---|---|---|---|
| CLI, integrated terminal, JetBrains terminal | Yes | Yes | Test terminal dimensions and interruption |
| Desktop app's Code tab, supported non-WSL session | Yes | Yes | Verify Desktop-supported elements |
| Desktop app's WSL session | No current plugin support | No | Declare the feature unavailable there |
| VS Code extension panel | Yes | No | Return useful text/tool behavior |
| Noninteractive `-p` or Agent SDK | Yes | No | No required prompt-pane interaction |
| Remote Control | Runs on the local host | Stays in the local terminal | Remote participants cannot rely on local drawings |
| Cloud session | If the plugin reaches the cloud environment | No | Verify cloud acquisition, runtimes, and credentials |

This matrix is specific to mods and the documented hosts, not a promise that every component or external binary works there. Mods require v2.1.287 or later, and policy can refuse them. Terminal-only and Desktop-only UI elements differ. [Authoritative surface table](https://code.claude.com/docs/en/plugins/mods/overview#where-mods-run), [UI element reference](https://code.claude.com/docs/en/plugins/mods/interface).

## Installation UI is not the runtime contract

The interactive terminal `/plugin` panel, shell `claude plugin ...` commands, Desktop plugin browser, and VS Code management dialog are different entry points. A cloud session has no interactive plugin browser. Do not tell a headless application to open `/plugin` as its installation strategy. Pre-provision the plugin through a supported route and check the active session. [Install by surface](https://code.claude.com/docs/en/plugins/install), [environment-specific command failures](https://code.claude.com/docs/en/plugins/troubleshooting#find-where-plugin-runs).

Distinguish Desktop's **Code tab** from other Claude Desktop, Cowork, or hosted Claude experiences. Some packages and skills can be shared, but executable component support, user configuration, trust, and distribution differ. For example, the current component reference rejects plugins containing top-level `bin/` in Claude.ai and Cowork. Check each target's own component contract before labeling a package portable. [Component restrictions](https://code.claude.com/docs/en/plugins/components#executables).

## Load plugins through the Agent SDK deliberately

The SDK plugin option currently accepts local paths only. Resolve the path in the application's working directory and fetch/install a marketplace package beforehand when needed. Do not pass a marketplace ID or expect `~` expansion as if it were a shell. [Agent SDK plugins](https://code.claude.com/docs/en/agent-sdk/plugins).

Illustrative TypeScript configuration, after the application supplies a verified absolute path:

```typescript
const options = {
  plugins: [{ type: 'local' as const, path: pluginDirectory }]
};
```

Pass this through the SDK's documented query options. Inspect the initialization result's plugin/component information and `plugin_errors`; an invalid path can be skipped while the overall session still starts. SDK callback hooks have their own signatures and timeout behavior; do not return a command hook's stdout text from a callback and assume equivalence. See [advanced hook distinctions](hooks-advanced.md).

A headless application needs a programmatic authorization and interaction design. Replace an essential drawing or human dialog with an explicit request/result contract, or fail clearly that the requested feature needs an interactive host. Do not silently autoapprove to compensate for an absent UI. Test startup without the plugin, load failure, cancellation, and the first request after installation.

## Port behavior across different agent products

When targeting Codex, Hermes, another MCP client, or a standalone application, extract four layers:

1. **Knowledge:** prompts, reference material, schemas, and examples with licensing preserved.
2. **Pure logic:** parsers, transformations, result validation, and idempotency handling.
3. **Service protocol:** independently hosted tools/data that the target can access.
4. **Host adapter:** manifests, hooks, events, permission integration, UI, and lifecycle.

Reuse the first three only where their contracts fit; implement and test the fourth for the target. Claude-specific command namespaces, hook outputs, mod APIs, channel activation, and organization settings are not generic agent standards. Do not treat a similarly named Hermes Gateway or Desktop feature as a Claude Code surface.

Create a compatibility table in the implementation with one row per supported host/version and cells for load, invoke, permissions, effects, state, UI, and shutdown. Leave untested combinations explicit. A truthful partial compatibility claim is more useful than a universal label backed by one CLI run.
