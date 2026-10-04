# Marketplaces, installation, and state

Use this for local development, team catalogs, and installation diagnosis.

## Catalog shape

Repo catalogs use `.agents/plugins/marketplace.json`; personal catalogs use the corresponding directory under the user home. Local source paths resolve against the marketplace root. Installed local packages run from a cache copy. [Packaging](https://developers.openai.com/plugins/build/plugins)

Original repo example:

```json
{
  "name": "engineering-tools",
  "interface": {"displayName": "Engineering Tools"},
  "plugins": [
    {
      "name": "release-review",
      "source": {"source": "local", "path": "./plugins/release-review"},
      "policy": {
        "installation": "AVAILABLE",
        "authentication": "ON_INSTALL"
      },
      "category": "Productivity"
    }
  ]
}
```

Use this structure in a repository where `plugins/release-review/` contains the package.

## CLI workflow

Current commands include:

```sh
codex plugin marketplace add ./engineering-marketplace
codex plugin marketplace list --json
codex plugin list --available --json
codex plugin add release-review@engineering-tools --json
codex plugin list --json
```

Use `codex plugin marketplace upgrade engineering-tools` to refresh a configured Git marketplace, and `codex plugin remove release-review@engineering-tools` to remove an installed package. Inspect `--help` before automating version-sensitive options. [Developer commands](https://learn.chatgpt.com/docs/developer-commands)

Do not execute installation or removal merely because this reference contains commands; apply them to the user's requested operation.

## Track distinct states

| State | Evidence to collect |
|---|---|
| Catalog entry | Source type, catalog name, resolved source location |
| Available package | Valid manifest and component paths |
| Installed package | Installed path, version, source revision |
| Enabled package | Effective host/workspace/project state |
| Usable tools | MCP connection, authentication, tool discovery |
| Usable hooks | Host support and trust of the current hook definition |

Compare source and installed content when edits seem ineffective. Editing an installed cache file creates an untracked fix that an update can replace; fix the authoring source.

Workspace GitHub import has its own administration and access policies. It does not inherit repository installation/authentication policy fields. [Workspace management](https://learn.chatgpt.com/docs/enterprise/plugin-management)

Pin team releases to reviewed revisions. Keep development catalogs separate from release catalogs, and make rollback select known content rather than an unbounded branch head.
