# Author a platform adapter

Use the [platform plugin path](https://hermes-agent.nousresearch.com/docs/developer-guide/adding-platform-adapters) for community or product-specific channels. Reserve edits to the built-in registry/config/UI for a genuine core contribution.

## Contract

Subclass `gateway.platforms.base.BasePlatformAdapter`. Implement connection, disconnection, and sending; use optional typing/chat-info/media behavior only when supported. Normalize inbound updates into `MessageEvent` and call `self.handle_message(event)` so gateway policy and session routing remain in the path.

Register with `ctx.register_platform` and the actual `PlatformConfig`/registry signature in the target build. The registrar has many optional capabilities; copy only those needed from the current API.

Keep the manifest `kind: platform`. Keep heavy SDK imports lazy. A platform plugin can be deferred until the gateway/send path needs it; if it also exposes CLI-usable client tools, inspect the documented `provides_tools` plus `tools.py:register_tools(ctx)` mechanism.

## Implementation sequence

1. Define a canonical platform identifier and sender/chat/thread mapping.
2. Implement a passive dependency/config check.
3. Read secrets with the scoped helper and construct the SDK client at connection time.
4. Convert one real inbound text fixture into a normalized event.
5. Route it through host authorization and confirm the session key.
6. Send one reply to the correct chat and topic with an explicit result.
7. Add shutdown/reconnect, cancellation, attachment, rate-limit, and duplicate-update handling.
8. Add configuration/status/setup integration through registrar callbacks.

The [base adapter source](https://github.com/NousResearch/hermes-agent/blob/158fd638da1629c8e62caf9ade1515d162def8ab/gateway/platforms/base.py) is the baseline for optional hooks and lifecycle. Do not fabricate SDK objects in normalized observer payloads.

## Authentication and profile isolation

Distinguish SDK login, gateway sender allowlisting, channel restrictions, and action-specific permissions. Do not make `check_fn` install packages or send network requests simply to render status.

Use `get_scoped_secret`, `extra_or_secret`, and supported YAML/env bridge helpers. One multiplexed gateway can host several bot identities; caching a default-profile token in a module global can route another profile's actions to the wrong account.

Acquire any required scoped bot/token lock and release it on shutdown. Multiple pollers for the same Telegram-style bot identity can conflict even if each is independently healthy.

## Delivery and integration

Declare message limits and chunking semantics. Preserve thread/reply identifiers and distinguish unsupported media from transient upload failure. For cron outside the live gateway, register `standalone_sender_fn`; for direct host send, verify target parsing and validation callbacks.

A platform's registrar integrates configuration and routing; it does not implement its SDK or service policy. Keep acknowledgement deadlines, retry rules, rate limits, and API versions in platform-specific references. Test another profile and a second concurrent chat before claiming the adapter is ready.

