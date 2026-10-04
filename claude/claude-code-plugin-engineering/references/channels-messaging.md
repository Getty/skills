# Channels, chat bridges, and messaging

## Define the bridge boundary

A channel delivers external events into an already-running Claude Code session. It is distinct from polling with an MCP tool or creating a new cloud task. Channels remain a research preview: authentication, provider support, organization enablement, and allowlists apply. Current examples include Telegram, Discord, and iMessage. [Channels overview](https://code.claude.com/docs/en/channels).

At this checkpoint, channel authentication uses a claude.ai account or Anthropic Console API key; Bedrock, Google Cloud's Agent Platform, and Microsoft Foundry routes are unsupported. Team and Enterprise use requires organization enablement. Recheck these preview limits before designing a deployment around them.

For another messaging platform, implement the platform-facing adapter separately from the Claude Code channel protocol. Do not infer support for an arbitrary platform from the existence of an MCP server.

## Protocol map

| Direction | Contract |
|---|---|
| Declare channel capability | MCP experimental capability `claude/channel` |
| Inbound event | `notifications/claude/channel` with `content` and an optional string-valued `meta` map |
| Reply | A server-defined MCP tool that sends to the intended conversation |
| Optional permission relay | Separate `claude/channel/permission` capability and request/verdict notifications |

Metadata keys have protocol restrictions. Treat metadata as routing input, not proof of identity. Implement authentication before emitting a channel event. [Channel protocol](https://code.claude.com/docs/en/channels-reference).

Example application envelope before protocol conversion:

```json
{
  "platform": "example-chat",
  "account_id": "configured-account",
  "conversation_id": "test-room",
  "sender_id": "verified-sender",
  "event_id": "event-001",
  "text": "Show the latest build result"
}
```

This is an original internal adapter shape, not Claude Code's channel schema. Verify all identifiers against the authenticated platform event; then map only required fields to `content` and `meta`.

## Activate deliberately

A plugin's `channels` entry binds to one of its MCP server keys. Registration alone does not enable inbound delivery. During preview, production activation is restricted to an effective allowlist. Custom development uses the documented `--dangerously-load-development-channels` route for `plugin:` or `server:` targets. [Preview activation](https://code.claude.com/docs/en/channels#research-preview).

Use a test bot and conversation first. Confirm the server is connected, the channel is registered, a permitted sender reaches the right session, and the reply returns to the correct conversation. Keep server authentication and user pairing separate.

## Make delivery reliable

Deduplicate platform event IDs, bound message size, handle rate limits, and record delivery state without exposing tokens. Keep per-conversation context from leaking across chats. Decide which attachments are accepted and where temporary files live. Make group-chat mention rules and reply threading explicit.

A channel event is not blanket permission for later tool calls or outbound messages. A permission relay uses correlated request IDs and explicit allow/deny responses; ordinary chat text must not be promoted to authorization. Test expired, replayed, unknown, and cross-user approval IDs. [Permission relay](https://code.claude.com/docs/en/channels-reference#relay-permission-prompts).

Do not advertise the session as a permanent messaging gateway. Define reconnection, offline queuing, retention, and what a sender sees while the host is unavailable. Keep those durable responsibilities in the bridge service where necessary.
