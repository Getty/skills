# A layout production loop with explicit checks

**Read when:** turning a brief into an editable layout and verified delivery.

Start with an explicit page size, page count/facing-page choice, margins, columns and bleed. Create or open the document, inspect its spreads and retain returned IDs. Build a small representative page first: one text story, a style hierarchy and an image/frame relationship. Render it and check content/geometry before replicating across a long publication.

Use `frame.create` and story tools with discovered schemas rather than reproducing mouse gestures. If a gesture is genuinely necessary, inspect tool state, screen/spread mapping and the pending dialog/selection first. UI-only view/window/help commands do not become usable in headless mode merely because `execute` accepts arbitrary command IDs.

At each major phase, inspect story overflow, missing links and fonts, page bounds and selection. Save a checkpoint before global typography changes, parent-page changes or large content replacements. On partial script failure, inspect the failed index, resulting objects and story contents before replaying the script; duplicate frames can be difficult to notice visually.

For final acceptance, save native, export delivery, reopen both where supported, compare text and structural counts, render every output page and review detail regions. Run the application's publication validator when applicable and record its scope. The file count, a successful validator and visual proof answer different questions and should be reported separately.

The supplied example script demonstrates document/frame construction. It is a native engine script, not an MCP request array; IDs returned by live creation must be bound before dependent edits that target those objects.

## Evidence

- [design-cli](https://github.com/storytold/designcraft/blob/main/apps/designcraft-cli/src/main.rs)
- [design-mcp](https://github.com/storytold/designcraft/blob/main/docs/mcp.md)
