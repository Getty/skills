# Curated extension catalog

Reviewed 2026-10-22. This is a requirement-driven shortlist, not a popularity ranking or recommendation to install everything. Open the linked upstream README/releases before choosing a version.

| Project and primary source | Use when | Check before adopting |
| --- | --- | --- |
| [Mushroom](https://github.com/piitaya/lovelace-mushroom) | Consistent configurable dashboard cards are wanted | Template-card generation, themes/CSS compatibility, native Tile alternative |
| [Bubble Card](https://github.com/Clooos/Bubble-Card) | Compact controls/popups fit the household workflow | Mobile navigation, extra module dependencies, resource version |
| [button-card](https://github.com/custom-cards/button-card) | Highly configurable entity controls/layouts are needed | JavaScript templates, tap/hold behavior, maintainability |
| [card-mod](https://github.com/thomasloven/lovelace-card-mod) | A specific styling requirement exceeds supported card options | DOM/shadow-tree changes, module/resource loading, CSS fragility |
| [auto-entities](https://github.com/thomasloven/lovelace-auto-entities) | Dynamic lists such as unavailable devices or low batteries are useful | Filter semantics, empty lists, duplicate entries, target card compatibility |
| [ApexCharts Card](https://github.com/RomRider/apexcharts-card) | More analytical history plots are required | Point counts/browser load, aggregation, experimental features |
| [Scheduler Card](https://github.com/nielsfaber/scheduler-card) + [Scheduler Component](https://github.com/nielsfaber/scheduler-component) | Household-editable action schedules need a UI | Both frontend and backend, schedule persistence, controller conflicts |
| [Adaptive Lighting](https://github.com/basnijholt/adaptive-lighting) | Time-dependent brightness/color temperature is useful | Supported light modes, manual takeover, bridge routines, update traffic |
| [Better Thermostat](https://github.com/KartoffelToby/better_thermostat) | Room sensor/window inputs should augment supported TRVs | Exact adapter, calibration mechanism, stale sensor fallback |
| [Versatile Thermostat](https://github.com/jmcollin78/versatile_thermostat) | Richer heating policy over a supported actuator type is needed | Selected over-switch/over-climate/valve mode, sensor freshness, safety state |
| [LocalTuya](https://github.com/rospogrigio/localtuya) | A supported Tuya Wi-Fi device should be controlled locally | Exact project/fork, local key/protocol/DPs, simultaneous clients |
| [Tuya Local](https://github.com/make-all/tuya-local) | The device matches a maintained local Tuya definition | Exact device profile, firmware/DP signature, key retrieval route |
| [SonoffLAN](https://github.com/AlexxIT/SonoffLAN) | Supported stock eWeLink devices need LAN/cloud integration | Device-specific LAN support, account/region, bridge versus direct Zigbee |
| [Govee2MQTT](https://github.com/wez/govee2mqtt) | Native Govee paths lack a required supported feature | Separate service/broker, actual LAN/cloud path, credentials and rates |

## Select a minimal set

For a mixed home, start with native dashboards and native vendor integrations. Add a card family only for a concrete presentation need; add a backend wrapper only when it resolves a real control gap. A visually rich frontend does not improve the reliability of device transport.

For simple editable weekly on/off windows, first evaluate the native [Schedule helper](https://www.home-assistant.io/integrations/schedule/). It provides time blocks and state for automations. Scheduler Card plus Component is a different choice when household users need the project's action-scheduling interface; installing both is not necessary merely to have a weekly schedule.

For each selected project record repository, version, HA compatibility, install type, dependent entities/services, backup boundary, and fallback. Evaluate release activity and relevant issues in context: one well-maintained small integration can fit better than a large project with an unsupported model.

## Match to the example household

Auto-entities can help expose selected unavailable/low-battery devices across the inventory. Analytical plots can compare room sensors and thermostat response. Adaptive Lighting is a candidate for chosen Hue/compatible lights only after manual controls are tested. A thermostat wrapper is a per-room experiment, not a blanket upgrade for all FRITZ! 301/302 devices. Tuya/Sonoff custom routes apply to the actual transport, not every product carrying the brand.
