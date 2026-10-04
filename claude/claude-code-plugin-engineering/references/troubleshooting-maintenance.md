# Troubleshooting and maintenance

## Start with the first failing stage

Capture the exact error, command or user action, host/build, plugin identity/version, source and effective scope. Reproduce once with the smallest relevant component. Avoid deleting caches or reinstalling everything before understanding whether the fault is acquisition, loading, runtime, or behavior. The official [troubleshooting catalog](https://code.claude.com/docs/en/plugins/troubleshooting) groups errors by those stages.

| Symptom | First useful check | Next discriminating experiment |
|---|---|---|
| Shell rejects `/plugin` | Was a session command entered in the shell? | Use `claude plugin ...` or the proper host UI |
| Plugin not found | Marketplace registered, entry name, catalog freshness | Inspect the catalog and qualified ID |
| Installed but component absent | Effective enablement, version, loading errors | Fresh session or supported reload |
| Works with local path only | Resolved root and packaged contents | Install the actual distributed artifact |
| Script cannot start | Interpreter, argv, cwd, permissions, dependency provisioning | Run a fixture in the same environment |
| Hook loads but never fires | Exact event, matcher, `if`, and supported handler type | Trigger one known event and inspect input |
| Hook reports success but no effect | Event output schema and timing | Inspect decision/result in the host, not only script exit |
| MCP never connects | Command/transport, configuration, credentials, clean stdout | Minimal protocol startup and explicit reconnect |
| LSP missing or wrong | Binary, extension mapping, server config, indexing scope | One fixture file in the intended language |
| Skill never selected | Namespaced visibility and task description | Compare manual invocation with natural phrasing |
| Mod draws nothing | Host drawing support, render site, dimensions, guard refusal | Text fallback plus native UI test |
| Channel receives nothing | Server connection, activation, sender pairing, routing | One permitted synthetic inbound event |

This table is a diagnostic sequence, not proof of a cause. Change one relevant condition and observe the effect before changing another.

## Use observability without exposing secrets

Inspect the plugin list, reload summary, component status, and the host's debug output. Use `claude --debug` only when appropriate for the task and retain the relevant error/context rather than dumping transcripts or environment variables. The [configuration debugging guide](https://code.claude.com/docs/en/debug-your-config) helps distinguish instructions, settings, model context, and tool availability.

For hooks and servers, separate human logs from machine protocol output. For mods, record whether a handler ran, forwarded, short-circuited, was refused, or was skipped. A log line saying a module loaded can precede a policy refusal; confirm the effective outcome. For channels, retain event IDs and routing decisions with content minimized to what diagnosis needs.

## Common misleading repairs

- Bumping a marketplace version while the plugin manifest still pins an unchanged version may not replace a cached copy.
- Editing a cached file can disappear on a later install and hides the actual source defect.
- Reloading does not necessarily restart an unchanged MCP server; headless reload has additional limits.
- Returning an arbitrary JSON object does not make it valid for every hook event.
- Installing an LSP config does not itself install the language server binary.
- Disabling managed policy to make a local experiment pass changes the problem instead of validating deployment.

Resolve these with [loading/version behavior](loading-versioning-development.md), [hook contracts](hooks-command-contracts.md), [LSP setup](lsp-code-intelligence.md), and [trust boundaries](permissions-trust.md).

## Maintain a compact compatibility record

For each release, keep the plugin version/source commit, minimum host build, tested host/OS/provider combinations, component contracts used, runtime requirements, state migration, meaningful test results, and rollback route. Record links and review dates for fast-changing features such as mods, channels, native evals, and custom manifest fields.

When a feature stops working, compare the target's `--help`, validation output, generated mod types, release notes, and current primary documentation. Decide whether the defect is in the package, an older host, a changed external service, policy, or documentation. Mark unresolved contradictions explicitly and prefer the target runtime's reproducible behavior over an untested inference.

Retire obsolete compatibility workarounds once no supported target needs them. Keep examples small and internally consistent; a copied old config can otherwise outlive the explanation that once made it correct. Refresh the [source registry](sources.md) when changing a contract, not merely its review date.
