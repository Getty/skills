# Skills and portable packages

Use a skill for reusable instructions, reference navigation, and scripts/assets the agent can consult. Use executable plugins for tool handlers or runtime behavior. A skill can explain a workflow, but it does not grant a gateway permission or install a Desktop pane.

The official [skill authoring guide](https://hermes-agent.nousresearch.com/docs/developer-guide/creating-skills) defines Hermes' Agent Skills conventions. Keep the entry file short and direct the model to specific references by task. Make examples generic and keep secrets outside the package.

## Native bundled skills

Use the native `ctx.register_skill(name, path)` contract after verifying the target signature. Keep paths relative to `__file__`, not the process working directory. Native plugin skills are qualified by their owning plugin and read through the host's skill facilities. Treat installed bundle files as immutable; store editable results elsewhere.

Do not rely on a guessed sanitized namespace. List skills from the running host and invoke the returned qualified name. Account for a disabled plugin or inactive provider removing its skills from discovery.

For shared repositories or organization catalogs, use the existing skills/tap facilities. Packaging instructions as a Python plugin solely to copy files adds unnecessary installation behavior.

## Portable Agent Plugins

Hermes' [portable compatibility adapter](https://hermes-agent.nousresearch.com/docs/developer-guide/plugins#portable-agent-plugins-v1-packages) accepts supported Agent Plugins v1 components from a root `plugin.json`, skills under `skills/`, and MCP definitions in `mcp.json`. At the baseline it supports stdio and Streamable HTTP entries; legacy SSE is skipped by this portable adapter even if other native MCP paths support it.

This is a subset, not evidence that all native hooks, subagents, UI extensions, permissions, or manifests from another agent host work in Hermes.

Use [the canonical portable specification](https://agent-plugins.org/) when authoring the shared package, and check the Hermes loader for its implemented subset. Keep host-specific features in clearly named extensions or separate packages. Do not transcribe a Claude Code plugin directory into `plugin.json` and call that migration.

## Names, paths, and trust

Hermes validates fixed component locations and path containment. Portable skills get a deterministic namespace; MCP server names can conflict with user configuration or another package. Inspect warnings and actual registered names.

Use `PLUGIN_ROOT` for package assets and `PLUGIN_DATA` for host-managed writable data only where the specification/runtime defines them. MCP environment mappings are visible package data, so they are unsuitable for committed secrets.

Choose full native packaging when the feature requires Hermes-specific lifecycle or frontend APIs. Choose portable packaging when the common denominator genuinely satisfies the desired task. Test the same package independently in every claimed host.

