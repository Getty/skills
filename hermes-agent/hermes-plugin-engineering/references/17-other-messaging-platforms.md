# Other messaging platforms

Use the official [messaging index](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/) to identify currently supported adapters. Choose the specific channel guide rather than transferring Telegram settings to another platform.

| Platform | Verified integration shape | Extension design implication |
| --- | --- | --- |
| [Discord](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/discord) | Bot, gateway connection, DMs/channels/threads, attachments and voice paths | Check intents, role/user/channel permissions, thread identity, and bot-loop behavior |
| [Slack](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/slack) | Bolt Socket Mode with bot and app-level tokens | Preserve team/workspace identity; distinguish slash commands and Block Kit callbacks |
| [WhatsApp bridge](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/whatsapp) | Baileys-based linked-device Node bridge | Own pairing/session persistence and bridge lifecycle; this is not the Business Cloud API |
| [WhatsApp Business](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/whatsapp-cloud) | Meta Cloud API and webhook integration | Verify webhook authentication, account registration, message-window/template rules, and current API version |
| [Signal](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/signal) | External signal-cli HTTP daemon, inbound SSE and JSON-RPC send | Own daemon availability and account/session storage separately from Python |
| Other adapters in the index | Teams, email, SMS, Matrix and additional regional services use their own contracts | Verify supported current plugin, delivery mode, service scopes, SDK, and setup instructions individually |

The rows identify architectural differences, not exhaustive feature parity. Live calls and file sending can require permissions beyond basic text.

## Choose the lowest necessary layer

Reuse a platform's configuration for mentions, allowed users, channel-specific model/prompt behavior, and voice settings when available. Reuse session commands for explicit user actions. Add a native handler for unsupported channel events. Build a new adapter only for an unrepresented transport.

For a business integration independent of chat transport, put the operation behind a tool/backend service and expose thin channel-specific presentation. This avoids separate implementations of the same authorization and idempotency in Telegram, Slack, and Desktop.

## Cross-channel identity

Do not equate matching display names, email-like strings, or phone formatting with a shared identity. Require an explicit mapping if a workflow needs continuity across services. Use workspace/team IDs as part of Slack identity; preserve group/thread scopes elsewhere.

Chat visibility, agent tool permissions, and access to an external business system are separate. A user admitted to Slack chat does not automatically have the right to administer the backend service.

## Format and delivery fallback

Design one semantic outcome and several presentation adapters: text summary, structured attachment, button where supported, or link to an authenticated UI. Keep the necessary action accessible when rich UI is unavailable.

Test rate limits, message-length splitting, attachment limits, edit/reaction permissions, missing native APIs, network loss, and delivery acknowledgement. Avoid a universal “send any object to any platform” abstraction that silently discards unsupported fields.

