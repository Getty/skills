# Messaging gateway: routing, identity, and delivery

Treat the [messaging gateway](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/) as a long-running runtime with adapters, admission, session routing, agent execution, and delivery. It is not merely another visual client.

## Follow one request

Trace the adapter's platform update into `MessageEvent`, admission/authorization, command or agent dispatch, session lookup, tool execution, and final response. Record profile, platform, account/workspace scope, chat, thread/topic, sender, platform update ID, message ID, and resulting session identifiers.

Use the [normalized event type](https://github.com/NousResearch/hermes-agent/blob/158fd638da1629c8e62caf9ade1515d162def8ab/gateway/platforms/event.py) and [session-key builder](https://github.com/NousResearch/hermes-agent/blob/158fd638da1629c8e62caf9ade1515d162def8ab/gateway/session.py). Do not manually concatenate identifiers. DMs, shared groups, per-user groups, threads, Slack workspaces, and profiles do not use identical keying.

A stable routing key and a conversation's session ID are different. Resets/compression/resumption can change the latter without changing the visible chat. Persist intended routing identity, not an ephemeral Desktop UI session ID.

## Dispatch interception

`pre_gateway_dispatch` is a native plugin hook before normal authorization/pairing at this snapshot. It can skip or rewrite text; an “allow” result does not grant authentication or override downstream policy. Keep pre-auth work bounded and free of unauthorized side effects.

A normalized `gateway_platform_event` is a different observer surface dispatched after the gateway's applicable authorization check. Prefer it when the feature only needs supported platform events. Consult [native handlers](16-native-channel-handlers.md) before adding raw SDK callbacks.

## Conversation injection

The [native injection implementation](https://github.com/NousResearch/hermes-agent/blob/158fd638da1629c8e62caf9ade1515d162def8ab/hermes_cli/plugins.py) accepts `ctx.inject_message(content, role="user", session_key=...)`. Non-CLI use needs an existing durable key and explicit `allow_gateway_injection`. TUI/Desktop and messaging use separate host injector slots.

A successful boolean means accepted for scheduling, not completed work or delivered output. Do not promote an external event to an internal trusted command. Distinguish injecting context for one turn from waking the agent with a new message.

## Outbound messaging

The [send implementation](https://github.com/NousResearch/hermes-agent/blob/158fd638da1629c8e62caf9ade1515d162def8ab/tools/send_message_tool.py) deliberately does not register `send_message` as a normal model-callable tool at this pin. Host-driven CLI send, cron delivery, notifier paths, and opt-in server integrations are distinct.

Do not recreate a generic model-callable outbound tool merely because old examples mention one. Design the requested delivery through the supported host path and explicit target/authorization.

The gateway's response ledger provides recovery with at-least-once semantics. It does not make a plugin's external business action exactly-once. Use external operation IDs and durable idempotency for actions that might repeat.

## Process boundary

A cron job may run outside the gateway process. Platform plugins needing that delivery path must implement the documented standalone sender. An in-memory adapter reference cannot serve another process. Likewise a gateway hook does not automatically broadcast to Desktop; use a backend data/event bridge with an explicit owner.

