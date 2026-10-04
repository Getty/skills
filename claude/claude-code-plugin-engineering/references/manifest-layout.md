# Manifest and package layout

## Start with an explicit manifest

Use `.claude-plugin/plugin.json` for metadata. Put component directories beside `.claude-plugin/`, not inside it. The manifest may be omitted for some auto-discovered packages; include one for a distributable plugin and for a mod. `name` is required when the manifest exists. Prefer a permanent kebab-case identifier. [Manifest contract](https://code.claude.com/docs/en/plugins/manifest-reference), [create guide](https://code.claude.com/docs/en/plugins/create).

```json
{
  "name": "change-companion",
  "version": "0.1.0",
  "description": "Inspect a change and organize evidence for review",
  "author": { "name": "Example maintainers" },
  "license": "MIT"
}
```

Use the license only after deciding the actual package license; this is a sample.

| Path at plugin root | Purpose |
|---|---|
| `skills/<name>/SKILL.md` | Instruction entry and nearby supporting files |
| `commands/<name>.md` | Existing command prompts |
| `agents/<name>.md` | Specialist definitions |
| `hooks/hooks.json` | Classic hooks and/or mod module declaration |
| `.mcp.json`, `.lsp.json` | Server connection declarations |
| `scripts/`, `assets/` | Implementation files used by components |
| `settings.json` | Supported plugin defaults |
| `workflows/`, `monitors/` | Optional orchestration and monitoring |

## Resolve custom paths deliberately

Custom component paths normally start with `./`, must exist, and remain inside the plugin. Forward slashes make manifest paths portable. The current merging contract is:

- Add to default discovery: `skills`.
- Merge with the default file: `hooks`, `mcpServers`, `lspServers`.
- Replace default discovery: `commands`, `agents`, `outputStyles`, `workflows`, `experimental.themes`, `experimental.monitors`.

The `agents` field names Markdown files, not directories. A hook file contains a `hooks` wrapper; an inline manifest hooks object contains the event map directly. Consult accepted shapes before mixing inline and file declarations. [Path and component schemas](https://code.claude.com/docs/en/plugins/manifest-reference#component-path-forms).

## Package a coherent unit

Use defaults until a concrete need justifies a custom path. Avoid duplicating a server or hook in both its default file and the manifest. Do not depend on `../shared` being present after installation. Include implementation files within the package or declare a real dependency.

Use `${CLAUDE_PLUGIN_ROOT}` for shipped resources. Place generated state elsewhere. A root `CLAUDE.md` is not a plugin-wide instruction injection mechanism; put reusable instructions into a skill and event behavior into an appropriate hook or mod. [Component behavior](https://code.claude.com/docs/en/plugins/components).

Run native validation for the target build and review warnings. A JSON parser proves syntax only. A manifest that appears to accept an unsupported permission key has not granted that permission.
