---
name: smart-home-radio
description: "Use when a Zigbee, Thread, Matter, Bluetooth or Z-Wave network misbehaves or changes — pairing fails, devices drop off, ZHA or Zigbee2MQTT, coordinator migration, routers and binding, Zigbee OTA, Matter commissioning, Thread border routers, IPv6, BLE proxies, EnOcean."
---

# Smart Home Radio

Identify the failing layer before changing the network. A successful radio join does not establish application compatibility, and a visible entity does not prove current physical state.

## Establish a baseline

1. Capture exact radio/controller model, firmware, owning process, HA and relevant server versions.
2. Record network owner, transport, channel where available, credentials/backup location, device fingerprint and power/sleep behavior. Keep keys private.
3. Reproduce one symptom with a timestamp and an expected result. Check whether it affects one device, one router branch, one vendor, or the whole network.
4. Inspect physical placement, interference, power, service logs and protocol-specific evidence. Change one variable at a time.
5. Retest the original symptom and reconnect behavior before escalating to reset, migration or firmware changes.

## Load the relevant reference

| Task | Reference |
|---|---|
| Mesh roles, placement, capacity and coexistence | [zigbee-design.md](references/zigbee-design.md) |
| ZHA pairing, quirks, events and maintenance | [zha.md](references/zha.md) |
| Zigbee2MQTT adapters, MQTT, converters and exposes | [zigbee2mqtt.md](references/zigbee2mqtt.md) |
| Matter commissioning, Thread, fabrics and IPv6 | [matter-thread.md](references/matter-thread.md) |
| BLE proxies, advertisements and active connections | [bluetooth.md](references/bluetooth.md) |
| Z-Wave, EnOcean and other RF | [zwave-and-other-radios.md](references/zwave-and-other-radios.md) |
| Diagnose failures and migrate with rollback | [troubleshooting-and-migration.md](references/troubleshooting-and-migration.md) |
| Dated firsthand experiences and primary sources | [evidence-and-sources.md](references/evidence-and-sources.md) |

## Enforce the important boundaries

- Give one Zigbee coordinator to one owning stack. Run ZHA and Zigbee2MQTT on separate coordinators/networks when both are required. Do not confuse radio multiprotocol firmware with two Zigbee applications sharing ownership.
- Match the actual device fingerprint. Preserve Tuya manufacturer strings and supported converter/quirk evidence; never equate every TS0601 with one device.
- Keep a Thread border router, Matter controller, Matter fabric, and Zigbee coordinator conceptually separate. Do not disable IPv6 to repair Matter.
- Distinguish BLE active scanning from active GATT connections. A proxy is not a Bluetooth Classic audio adapter.
- Back up before changing channel, network credentials, coordinator firmware or pairing. Do not invent a universal seamless ZHA ↔ Zigbee2MQTT migration.
- Verify exact-model OTA warnings before offering an update. In particular inspect the current TS0201 device entry for matching variants.
- Preserve healthy Hue and FRITZ networks unless a feature-driven migration has been chosen. Routers on a different Zigbee network do not extend the target mesh.

Route DECT/FRITZ to `fritzbox-operator`, vendor identity to `smart-home-devices`, BLE firmware/MQTT to `smart-home-esphome-mqtt`, and higher-level behavior to `home-assistant-automations`.

Report observations, likely layer, discriminating test, bounded fix and recovery. Research baseline: **2026-10-22**; verify the installed release and exact hardware before using changing advice.
