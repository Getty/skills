# Optional UI and OpenAI extensions

Keep the MCP result useful without a rendered component. Use UI when inspection, editing, navigation, or confirmation benefits from it.

Current ChatGPT UI guidance uses MCP Apps: associate a tool with `_meta.ui.resourceUri` and use the `ui/*` bridge. OpenAI-specific `window.openai` capabilities are optional extensions, and older output-template fields remain compatibility aliases. [MCP UI](https://developers.openai.com/plugins/build/chatgpt-ui)

OpenAI extensions additionally cover sidebar applications, conversation panels, plugin settings, file viewers/editors, deep links, context sharing, rich forms, and onboarding. Availability varies; composer mentions are currently desktop-specific. [Extensions](https://developers.openai.com/plugins/build/extensions)

## Design procedure

1. Define the same core operation as a tool that returns structured data.
2. Identify the exact interaction the UI adds.
3. Select standard MCP Apps methods before host-specific additions.
4. Feature-detect optional capabilities.
5. Design a readable headless result and an understandable unsupported-state view.
6. Test authorization and error handling through both the UI and agent tool path.

Do not trust a client-supplied record ID because it came from your own component. Apply the same server-side checks as for a model call.

Keep UI state distinct from authoritative business state. A selected row, open panel, or draft field can be client state; a committed release approval belongs in an authorized backend operation. Prevent a rerender or replay from duplicating a write.

## Verification

Test loading failure, missing resources, content security restrictions, small screens, keyboard interaction, expired connections, stale data, and interrupted writes.

Treat rendering support as its own compatibility claim. A CLI receiving structured results does not prove that it supports sidebar extensions. A browser component working in ChatGPT does not establish Codex IDE plugin support.

Use resource and UI diagnostics from [troubleshooting](https://developers.openai.com/plugins/deploy/troubleshooting). Avoid introducing an iframe or complex frontend for a simple text lookup.
