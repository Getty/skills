# Portability and migration

Treat portability as a component-by-component migration, not a filename conversion.

## Claude-compatible input

OpenAI's conversion guide preserves reusable skill content, converts reusable command/agent instructions to skills, and requires adaptation of hook behavior. Claude installation prompts and `user_config` expansion are not OpenAI runtime features; prompt/agent hook handlers are not supported by Codex. Claude approvals/listings do not transfer. [Claude plugin conversion](https://developers.openai.com/plugins/guides/submit-claude-plugin)

| Existing component | Migration question |
|---|---|
| Skill instructions/resources | Are tool names, paths, invocation wording, and behavior portable? |
| Command Markdown | Can the workflow become a focused skill? |
| Agent definition | Is it reusable procedure or a host-specific agent configuration? |
| MCP server | Does the target connection/authentication path support it? |
| Hook | Does this event, handler type, and response work in the target runtime? |
| UI | Which standard and host extensions does it require? |
| Incoming channel | Is a supported event host or separately operated bridge required? |
| Installer settings | Where will persistent user configuration and secrets live? |

## Codex format migration

When adopting a portable manifest, move only the fields belonging to that format. Preserve package identity intentionally, map OpenAI-only settings into its extension, and update component configuration according to the actual schema.

Do not carry a deprecated field just because parsing succeeds. Compatibility acceptance, implemented behavior, and public submission support are different claims.

For older external-control integrations, the removed `codex mcp-server` route requires an app-server migration. [SDK](https://learn.chatgpt.com/docs/codex-sdk) Rework message lifecycle and approval handling; do not wrap old method names around a new transport and assume equivalence.

## Migration plan

Record the source version and destination version; map each capability to keep, adapt, replace, or omit; create a regression case for every retained workflow; and expose any lost capability to the user.

For multi-host distribution, share backend logic and portable resources where useful, but retain separate tested host adapters and package manifests. Avoid claiming that Agent Plugins, Agent Skills, or MCP compatibility implies identical Claude, Codex, and Hermes behavior.

Keep rollback possible until the destination has passed real installation and workflow tests.
