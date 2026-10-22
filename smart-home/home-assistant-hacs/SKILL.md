---
name: home-assistant-hacs
description: "Use when installing, updating, removing or debugging HACS or a Home Assistant custom integration, card or theme — custom repositories, a card that fails to load (\"Custom element doesn't exist\"), frontend resources, Mushroom, Bubble Card, card-mod, Adaptive Lighting, LocalTuya, Tuya Local, SonoffLAN, the HACS Marketplace transition."
---

# Home Assistant HACS

Treat HACS as a distribution/lifecycle layer for community code. Evaluate each installed project and its exact version separately.

Research snapshot: **2026-10-22**. HACS documentation already describes a **2026.11 Marketplace transition**; this is forward-looking at this snapshot. Determine the installed released version before choosing a procedure.

## Route the task

| Task | Load |
| --- | --- |
| Explain HACS versus Apps, install/configure, version gate | [Lifecycle and terminology](references/lifecycle-terminology.md) |
| Choose useful projects by requirement | [Curated extension catalog](references/curated-extensions.md) |
| Cards, resources, browser errors and frontend compatibility | [Frontend debugging](references/frontend-debugging.md) |
| Adaptive Lighting, thermostat wrappers, Scheduler ownership | [Lighting and climate extensions](references/lighting-climate.md) |
| Tuya/Sonoff/Govee native versus custom routes | [Device bridges](references/device-bridges.md) |
| Update, restore, disable, remove, trust review | [Upgrade and recovery](references/upgrade-recovery.md) |
| Firsthand incidents and resolution status | [Community evidence](references/community-evidence.md) |
| Refresh authoritative sources | [Source index](references/sources.md) |

Use `home-assistant-operator` for host/backups/backend diagnosis; `home-assistant-automations` for control logic; `smart-home-devices` for exact products. Installing a custom integration cannot manufacture a device protocol or unsupported capability.

## Evaluate before installing

1. State the feature missing from native HA or an existing integration.
2. Identify the correct repository owner, project, release, type, supported HA version, and hardware/API dependencies.
3. Review release notes, recent maintenance, unresolved relevant issues, and install/uninstall requirements. Stars and download counts do not prove reliability.
4. Compare built-in capabilities first. Avoid a custom component when native HA meets the requirement without losing a needed feature.
5. Map the blast radius: backend code runs within HA; frontend code runs in authenticated browser sessions; external bridges have separate credentials/storage.
6. Preserve a restorable checkpoint, install one coherent change, configure it through its documented surface, and verify an actual use case plus a fallback.

## Keep boundaries clear

- A repository download is not necessarily a configured integration or working dashboard resource.
- HAOS Apps (formerly add-ons), HACS custom integrations, frontend cards, vendor cloud services, and AppDaemon programs are different objects.
- HACS availability on Container does not provide Supervisor/Apps management.
- A custom repository needs the expected structure/type; any arbitrary GitHub repository is not automatically installable.
- Default catalog inclusion is not a promise that every version works on this installation or that HA core maintainers support its code.
- Treat LocalTuya, Tuya Local, and Tuya's native cloud integration as different projects. Tuya Zigbee devices paired directly do not require Tuya Wi-Fi keys.
- Run only one active controller for the same thermostat/light behavior unless a precise handoff is designed.
- Do not automatically update every custom dependency in a working home at once.

## Return a concrete decision

Provide project/repository, reason it is needed, dependency graph, tested version/installation scope, setup steps, verification, maintenance owner, rollback, and evidence gaps. When recommending an extension, explain which feature is gained and which new operating responsibility is introduced.
