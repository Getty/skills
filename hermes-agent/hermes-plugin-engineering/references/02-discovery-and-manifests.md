# Discovery, manifests, and activation

Use a native directory package for Hermes-specific behavior. A minimal layout is `plugin.yaml` beside `__init__.py` with `register(ctx)`; split handlers, schemas, assets, and skills when that makes maintenance clearer.

```yaml
name: text-metrics
version: "1.0.0"
description: Deterministic text metrics for agent workflows
```

This is a manifest example, not a complete plugin. Supply the implementation in [tools and commands](03-tools-and-commands.md). The official [plugin guide](https://hermes-agent.nousresearch.com/docs/developer-guide/plugins) describes native and portable package admission.

## Keep six steps distinct

1. **Discover:** resolve the package and parse its manifest.
2. **Prepare dependencies:** use the owner's Hermes package-management workflow.
3. **Enable:** admit executable general plugin code.
4. **Register:** import the plugin and call its entry point.
5. **Expose:** make its tools available in the selected platform/toolsets.
6. **Activate services:** select providers and connect channels that the extension contributes.

Inspect `hermes plugins list` before guessing the effective plugin key. Category layouts can produce qualified identifiers.

General discovery considers bundled, user, trusted project, and entry-point sources; later sources normally win a name collision. General/user plugins are opt-in through `plugins.enabled`; `plugins.disabled` overrides an allow entry. Project discovery additionally requires `HERMES_ENABLE_PROJECT_PLUGINS=true`. Bundled infrastructure has exceptions. See the [user plugin reference](https://hermes-agent.nousresearch.com/docs/user-guide/features/plugins).

Memory providers have their own discovery and earlier-wins collision policy. Model/context providers also have specialized selection. Do not carry general-plugin precedence into those systems.

## Manifest precision

The [pinned manifest parser](https://github.com/NousResearch/hermes-agent/blob/158fd638da1629c8e62caf9ade1515d162def8ab/hermes_cli/plugins_manifest.py) accepts additive metadata including manifest version, advisory API/dependency metadata, Python requirements, configuration schema, and declared capabilities. Missing `manifest_version` retains the legacy file format. Do not invent a mandatory global `PLUGIN_API_VERSION` or treat a manifest number as a runtime feature guarantee.

Use the installed parser/validator for optional fields. In particular, dependency declarations and `requires_plugins` do not prove another integration is active or compatible. Probe the runtime and produce an actionable diagnostic.

## Registration discipline

Keep module import and `register(ctx)` cheap and deterministic. Avoid network calls, credential prompts, daemon launch, pip installation, or long scans there. Defer optional SDK imports to the operation that needs them. Register one coherent tool family and explain its toolset.

Check returned registration handles where the API supplies them. A warning/rejected duplicate registration can leave a plugin loaded with no usable tool. Use unique names, and require explicit host authorization before overriding built-ins.

Treat reload as a lifecycle transition, not an invitation to retain global callbacks indefinitely. Use host cleanup facilities and test with two profiles in one process.

