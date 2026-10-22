# Integration development

Check maintained native integrations, bridges, and reusable libraries first. Keep vendor protocol logic in a library and HA entities/lifecycle in the integration.

## Specify the contract

List exact models/firmware, local/cloud transport, authentication, discovery, polling/push, rate limits, entities, commands, unavailable behavior, and reconnect behavior. Include an unsupported case. Brand matching alone must not report successful compatibility.

Validate `manifest.json` fields and custom integration version against the current schema. [Manifest](https://contributors.home-assistant.io/core/integrations/manifest/).

## Lifecycle

Use config flows for device/service setup, distinguish auth/network failures, prevent duplicates, and support reauth/reconfigure where relevant. Preserve stable unique IDs and migrate stored schemas explicitly. [Config entries](https://contributors.home-assistant.io/core/integrations/config-entries/), [reauth helpers](https://developers.home-assistant.io/blog/2024/10/21/reauth-reconfigure-helpers/).

Use async I/O or a documented executor boundary. Share one fetch across dependent entities with a coordinator; avoid one poll per entity. Prefer reliable protocol push. Never turn unknown telemetry into a plausible measurement. [Fetching data](https://contributors.home-assistant.io/core/integrations/fetching-data/).

Unload listeners, subscriptions, clients, tasks, and platforms. `entry.async_on_unload` callbacks alone do not replace the required unload interface. [Unload contract](https://developers.home-assistant.io/docs/core/integration-quality-scale/rules/config-entry-unloading/).

## Entity/action design

Choose domains by semantics: a momentary button is not a persistent switch. Do not fake device capability through optimistic state writes. Preserve units, supported features, and stable device association. Keep runtime data per config entry rather than a global shared client. Follow current action registration rules so unavailable targets produce clear failures. [Runtime data](https://developers.home-assistant.io/blog/2024/04/30/store-runtime-data-inside-config-entry/), [action registration](https://developers.home-assistant.io/docs/core/integration-quality-scale/rules/action-setup).

## Verification

Cover setup/duplicate/auth/network flows, unload/reload, reconnect, stale/unavailable data, command serialization, and stored-schema migration. Use sanitized protocol fixtures and deterministic clocks. Preventing a false heater action after reconnect matters more than tests mirroring a helper's implementation.

Run the repository's current focused tests, linters, hassfest/schema validation, and integration checks. Importing Python is insufficient proof of compatibility. Publish an actual HA version range and rollback guidance; use `home-assistant-hacs` for distribution lifecycle.
