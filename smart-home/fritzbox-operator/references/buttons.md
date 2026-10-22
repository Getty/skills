# Control 400/440 buttons, URL actions, and HA webhooks

## Recognize the integration boundary

A Control 440 can operate native FRITZ functions even when its button events are unavailable in HA. The [current native SmartHome documentation](https://www.home-assistant.io/integrations/fritzbox/) explicitly distinguishes auxiliary sensor exposure from main event-based device functionality. Polling a last-press timestamp is not equivalent to a reliable event stream: repeated presses between reads can collapse, and timestamps may not encode every gesture.

A firsthand [February 2026 blueprint report](https://community.home-assistant.io/t/fritz-smart-control-440-blueprint-webhook/981706) demonstrates assigning FRITZ “call URL” templates to 440 buttons and directing them to HA webhooks. That is a separate FRITZ-native event-to-HTTP route, not a feature added to the `fritzbox` integration. The blueprint author describes two configured views and custom double-click handling; do not generalize those choices into hardware guarantees.

## Establish a single harmless button

1. Check that the actual FRITZ!OS offers the relevant URL/comfort-function template and method selection.
2. Select one unused button/view or preserve its original assignment before changing it.
3. Create a unique high-entropy webhook ID in HA.
4. Make the webhook write a harmless test notification or invoke a known lighting scene.
5. Configure the exact local HA origin and method in the FRITZ template, then assign it to the physical button.
6. Confirm one press produces exactly one expected automation trace before adding more mappings.

Verify reachability from the router. A hostname resolving on a laptop may not resolve for FRITZ's outgoing request. A proxy login page, certificate error, guest network, or blocked router-to-HA route can prevent delivery. Avoid public URLs when the local route suffices.

## A current YAML pattern

This is one automation body for the editor. Replace the example ID with a generated secret before using it, and choose an actual target. The dummy value is deliberately not a usable deployment secret.

```yaml
alias: FRITZ button test
mode: single
triggers:
  - trigger: webhook
    webhook_id: REPLACE_WITH_A_UNIQUE_RANDOM_SECRET
    allowed_methods:
      - GET
    local_only: true
conditions: []
actions:
  - action: persistent_notification.create
    data:
      title: FRITZ button test
      message: A configured FRITZ button reached Home Assistant.
```

Configure the FRITZ URL as `http://<local-ha-address>:8123/api/webhook/<generated-secret>` only when that matches the actual HA listener. Use HTTPS when configured. HA does not enable GET by default; specify it if the router template sends GET. Prefer POST if the actual sender supports it. HA webhooks rely on secrecy of the ID rather than ordinary HA token authentication. See [HA webhook documentation](https://www.home-assistant.io/docs/automation/trigger/#webhook-trigger).

## Expand deliberately

For many buttons, use either distinct webhook IDs or a fixed, validated command selector. Query parameters arrive in `trigger.query`; form/JSON bodies use different fields. Allowlist symbolic commands such as `livingroom_scene`; never accept arbitrary action names, entity IDs, shell commands, or target URLs from the request.

Keep debouncing and gesture recognition explicit. A double-click detector must define its timing window and single-click delay; it cannot simultaneously guarantee immediate single-click execution and wait indefinitely for a second click. Do not apply toggle twice if a duplicate request is delivered. An explicit scene or on/off command is often easier to reason about than repeated toggles.

Document the mapping as physical unit → view → button → FRITZ template → webhook/command → HA action. Keep the old assignment for rollback. Show labels matching the physical action so another household member can use the device without understanding the integration.

Do not use an unauthenticated bearer webhook as an unrestricted control entry point for unlocking, alarm disarming, or dangerous actuators. For those operations, use a separate authenticated design with an explicit authorization policy. The ordinary lighting/webhook route remains useful without broadening its authority.
