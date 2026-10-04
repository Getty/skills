# Package formats and manifests

Select one canonical authoring format. Use a compatibility overlay only for an identified consumer.

## Portable package

The current portable entry point is root `plugin.json`, with fixed root `skills/` and optional `mcp.json`. OpenAI-specific settings belong under `extensions.com.openai`. An inline OpenAI object replaces the compatibility overlay; the two are not merged. Relative component paths resolve from the plugin root. [Packaging](https://developers.openai.com/plugins/build/plugins)

Original minimal example:

```json
{
  "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
  "name": "release-review",
  "version": "0.1.0",
  "description": "Review a proposed software release against its evidence."
}
```

Add `skills/release-review/SKILL.md`; start from the skill example in [skills and metadata](skills-metadata.md).

For a remote dependency, an original portable `mcp.json` example is:

```json
{
  "$schema": "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json",
  "mcpServers": {
    "release-records": {
      "type": "streamable-http",
      "url": "https://releases.example.com/mcp"
    }
  }
}
```

Replace the example endpoint before execution. The schema and transport spelling are verified in [submission examples](https://developers.openai.com/plugins/deploy/submission).

## Codex compatibility package

A compatibility-only bundle uses `.codex-plugin/plugin.json`; place its resources at the plugin root:

```json
{
  "name": "release-review",
  "version": "0.1.0",
  "description": "Review a proposed software release against its evidence.",
  "skills": "./skills/"
}
```

A compatibility manifest can reference `.mcp.json`, whose documented HTTP example uses `mcpServers.<name>.url` without the portable schema declaration. Do not mechanically rename portable MCP files. [Compatibility ingestion](https://developers.openai.com/plugins/deploy/submission-errors)

## Design checks

Use a stable package identity and a distinct version for every distributable content change. Decide whether the package needs credentials, persistent state, executable scripts, or a deployed backend before publishing it.

Keep package identity separate from skill names and tool names. A consistent namespace helps readers, but those identifiers serve different contracts. Do not add guessed fields such as universal plugin dependencies, arbitrary runtime classes, or automatic execution permissions.

Validate examples against the target format and then load the package in the target host. A minimal authoring manifest is not a complete public listing.
