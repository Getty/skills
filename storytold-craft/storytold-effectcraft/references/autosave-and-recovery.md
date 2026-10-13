# Headless autosave, explicit saves and recovery

**Read when:** keeping agent work across MCP restarts or responding to a checkpoint warning.

Without `--autosave`, headless project changes remain in memory until explicitly saved. With `mcp --autosave`, a dirty mutation triggers a checkpoint before its reply is sent. Query calls do not rotate versions. A failed checkpoint can leave a successful edit in memory while returning a warning; explicitly save to a writable path before disconnecting.

Each MCP server has a separate session folder under the configured auto-save location. The server reports recovery information through initialization metadata and `get_project.autosave`. Previous dirty sessions are not automatically opened, since they may still belong to a running process. Recover by explicitly opening a selected checkpoint and saving it as a new named project.

The headless autosave flag does not change desktop preferences and is not the same as the desktop's interval/toggle policy. A bridged desktop owns its own auto-saves. Replacing a dirty project with open/new intentionally discards the current in-memory project; save first. A process killed before a reply can lose the last interrupted edit despite earlier successful checkpoints.

For long jobs keep three identities: the live project, the latest durable checkpoint, and the render's snapshot. After a transport failure inspect all relevant states before deciding whether an operation should be retried. Deliver a deliberately saved `.ecproj`, not merely an auto-save folder whose retention settings may later rotate files.

## Evidence

- [effect-agents](https://github.com/storytold/effectcraft/blob/main/docs/agents.md)
- [effect-mcp](https://github.com/storytold/effectcraft/blob/main/docs/mcp.md)
