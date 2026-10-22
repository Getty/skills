# Inventory and exact identity

## Identity record

Capture the following using labels, vendor UI, integration diagnostics, Zigbee interview, or a read-only API response:

- Manufacturer, retail name, regional SKU, hardware revision and current firmware.
- Transport and bridge: Wi-Fi/Ethernet, Zigbee, Z-Wave, BLE, Thread, DECT; exact hub/coordinator and firmware.
- Software path and versions: native integration domain, custom repository/release, Zigbee2MQTT converter or ZHA quirk, server and broker where applicable.
- Stable identity: serial/IEEE/MAC/vendor ID stored privately; full Tuya manufacturer signature rather than `_TZ…` shorthand.
- Functions: sensor data, commands, button events, energy, calibration, scenes, firmware updates and restrictions; distinguish required from optional.
- Ownership and operation: native schedules, manual override, power-loss state, cloud requirements, last successful observation, responsible person.

Use `assets/device-record.json` in the parent skill as a seed. Unknown values must remain null or explicitly unknown.

## Avoid destructive identity collection

Export diagnostics before re-pairing; pairing may replace IDs, reset bindings and discard a working vendor path. Redact credentials, tokens, coordinates, internal addresses and camera endpoints before sharing externally. Retain the exact model/fingerprint and version needed to investigate.

Do not infer a radio from a brand: Philips, Tuya, SONOFF, Xiaomi and others sell incompatible product families. A capability through a bridge does not prove that capability exists through Matter or direct Zigbee.

Use vendor references plus the [HA integration catalog](https://www.home-assistant.io/integrations/) and [Zigbee2MQTT supported devices](https://www.zigbee2mqtt.io/supported-devices/) to investigate support.
