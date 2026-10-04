# Native channel handlers and platform actions

Use normalized host events whenever they meet the requirement. Use native SDK handlers when the feature needs a channel-specific event or interaction that the normalized surface does not express.

## Three different contracts

| Surface | Data/access | Authority |
| --- | --- | --- |
| `gateway_platform_event` | Normalized dictionaries for implemented events | Host-authorized observer; no raw bot handle |
| `ctx.platform_actions` | Narrow reactions/thread-title operations | Explicit capability, active profile, connected supported adapter |
| `register_platform_handler` / convenience registrars | Native SDK application/client at connection time | Trusted native integration; author must preserve auth/routing |

The [native plugin source](https://github.com/NousResearch/hermes-agent/blob/158fd638da1629c8e62caf9ade1515d162def8ab/hermes_cli/plugins.py) registers handlers, while the [base adapter](https://github.com/NousResearch/hermes-agent/blob/158fd638da1629c8e62caf9ade1515d162def8ab/gateway/platforms/base.py) wires factories into the live client.

`register_platform_handler(platform, factory)` calls `factory(native, adapter)`. Import optional SDKs inside the factory. Treat the adapter as host-owned; do not replace core methods or directly mutate global session state.

## Telegram

`ctx.register_telegram_handler(factory)` is the Telegram convenience API. PTB dispatches only the first matching handler in a group. Scope callback patterns to the plugin; an unrestricted callback-query handler can consume Hermes' own approval/clarification buttons.

For a real action button:

1. Store the action proposal in the backend with a random short reference.
2. Bind it to the intended profile, bot, sender, chat/topic, action, and expiry.
3. Register only the plugin's callback prefix.
4. Acknowledge within the channel's requirement, then authorize the actual actor.
5. Atomically consume the proposal/idempotency key before the side effect.
6. Deliver a bounded outcome through the correct chat/topic.
7. Reject unknown, expired, duplicate, or differently scoped references.

A callback arriving through Telegram is not proof that canonical gateway command policy ran. Do not reconstruct a powerful command from untrusted button text.

## Slack and other native SDKs

`ctx.register_slack_action_handler(action_id, callback)` wires a Bolt action callback. Acknowledge promptly and perform expensive work outside the acknowledgement path. Verify workspace/team/account scope, not just user ID.

The generic native factory currently receives different types for Telegram, Discord, Slack, Matrix, Teams, DingTalk, and LINE; some adapters provide no native object. Read the actual adapter before assuming parity. Reconnect may recreate the client, so handler wiring and cleanup must be idempotent.

## Narrow platform actions

The [platform-action implementation](https://github.com/NousResearch/hermes-agent/blob/158fd638da1629c8e62caf9ade1515d162def8ab/hermes_cli/platform_actions.py) exposes async `add_reaction` and `set_thread_title` for supported Telegram/Discord paths. The gate is `gateway.platform_actions`; calls return structured success/error and resolve the active profile's adapter.

Do not generalize these verbs to sending arbitrary messages, deleting content, banning users, or every platform. Handle `gateway_unavailable`, missing/disconnected adapter, denied capability, unsupported action, and service failure explicitly. A standalone CLI process normally has no live gateway adapter to act through.

