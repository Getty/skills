# Telegram

Use the existing Telegram adapter for ordinary bot conversations, commands, attachments, and topics. Add a native plugin only for behavior that configuration or a skill cannot express.

Read the current [Telegram guide](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/telegram), then inspect the target build's [adapter](https://github.com/NousResearch/hermes-agent/blob/158fd638da1629c8e62caf9ade1515d162def8ab/plugins/platforms/telegram/adapter.py). At this pin Telegram lives under `plugins/platforms/telegram/`, not the older `gateway/platforms/telegram.py` path.

## Admission and identity

Configure the bot credential in the intended profile. Use numeric stable user IDs and explicit chat/group policy. Telegram privacy mode controls what updates the bot receives; Hermes allowlists control what it accepts. An incoming update can be absent before any plugin code runs.

Verify DMs, ordinary groups, supergroups, and forum topics separately. Group session policy and thread session policy are not identical. Use the host's source/session builder; preserve `thread_id` and reply metadata.

Current Hermes supports topic-to-skill bindings and DM topic/session management. Discover the running command/config surface rather than assuming the same configuration nesting across releases. A title is a label; use numeric topic/chat identifiers for routing.

## Files, voice, and streaming

Voice notes need a working transcription path; replies need synthesis only if voice output is requested. Photo, file, audio, and document handling have separate download, format, size, and delivery constraints.

The streaming transport can use edit-based messages or private-chat drafts. Telegram draft previews do not have persistent message IDs; the final message is the durable reply. Group/topic paths can use another transport. Test cancellation and fallback without duplicating the completed answer.

Prefer readable bounded text and real file attachments for long structured output. Rich-message support, Markdown conversion, and client rendering vary by bot API/runtime/client; avoid promising identical output across Telegram mobile and desktop.

## Extension choices

| Need | Prefer |
| --- | --- |
| Add `/inspect` for an allowed user | `ctx.register_command` through canonical gateway dispatch |
| Load domain instructions in one topic | Topic/skill binding |
| Observe supported edits/reactions | `gateway_platform_event` |
| Add a scoped inline-button workflow | `register_telegram_handler` with explicit authorization |
| Add a reaction or rename supported topic | Capability-gated `ctx.platform_actions` |
| Supply generated files/voice | Existing media/provider and adapter delivery path |
| Display a management pane on a laptop | Separate Desktop contribution plus backend routes |

## Reliability and debugging

Distinguish `update_id`, `message_id`, topic ID, and Hermes session identity. Duplicate-update suppression is not durable exactly-once business execution. Reconnect/restart and preserved pending queues can replay work; use durable idempotency for plugin side effects.

Test missing allowlist, unauthorized DM, group mention/no-mention, two topics, edited input, oversized file, transcription failure, API flood control, disconnect during reply, and two pollers using the same bot token.

When Desktop configures Telegram, the bot logic still executes in the selected gateway/backend environment. A local UI plugin does not gain direct Telegram capability merely by displaying the settings.

