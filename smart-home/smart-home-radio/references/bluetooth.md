# Bluetooth LE and proxy diagnosis

## Resolve the communication mode

| Mode | What must work | Typical implication |
|---|---|---|
| Passive advertisements | Radio reception + correct decoder/key | Many sensors do not consume active connection slots |
| Active scanning | Scanner sends scan requests | Different from maintaining a GATT connection |
| Active GATT connection | Supported proxy/adapter + free connection + authentication | Locks/controllers and some sensors may need this |
| Bluetooth Classic | Separate profile/stack | HA BLE proxies do not supply arbitrary audio/headset forwarding |

The [HA Bluetooth integration](https://www.home-assistant.io/integrations/bluetooth/) supports BLE. Identify the actual device integration: ThermoBeacon, Xiaomi, Govee and a Zengge controller can require different decoders and connection modes despite all being nearby Bluetooth devices.

## Inspect the path end to end

Record adapter/proxy model, firmware, HA version, integration, device model, RSSI/advertisement age and whether an active connection is needed. Test a sensor near one known-good receiver. Determine whether the radio packets arrive but parsing fails, or no packets arrive at all.

For local adapters, inspect host support, permissions and VM/Container passthrough rather than granting broad privileges reflexively. For remote proxies, verify their HA native API connection separately from their BLE connection. MQTT-only proxy firmware does not replace the HA native API transport used by the proxy.

## Size active connection capacity

The current [ESPHome Bluetooth proxy documentation](https://esphome.io/components/bluetooth_proxy/) makes capacity platform-dependent: ESP32 defaults to three active slots and permits configuration subject to memory and BLE limits. Advertisement reception is not restricted to that count. Do not repeat an old “maximum three Bluetooth devices” claim.

A permanently connected lock can occupy a slot continuously; an advertising thermometer may occupy none. Measure contention and latency before increasing slots. More connections can increase memory pressure. Prefer a supported Ethernet proxy when it serves a concrete stability/placement need; test rather than promising universal superiority.

Default scan parameters are a baseline. Aggressively lengthening scan windows can harm coexistence or power/temperature behavior. Record configuration before experimenting.

## Use firmware evidence properly

In [ESPHome issue #18614](https://github.com/esphome/esphome/issues/18614), an ESP32-WROOM proxy's API/Wi-Fi remained connected while active BLE failed after a 2026.8.0 rebuild; the reporter's same-hardware 2026.7.2 comparison worked. The issue closed via a fix. Treat this as a good diagnostic pattern, not advice to downgrade every proxy to that old release.

Capture a controlled before/after result with the same placement, YAML and target device. Prefer the supported released fix once verified. Avoid updating every proxy at once; leave one known-good observation point.

## Handle identifiers and encryption

Do not assume a rotating BLE address identifies a different physical device. Some encrypted sensor formats need a vendor binding key; others do not. Follow the exact integration's provisioning method and do not search strangers' networks or guess secrets. Redact keys and precise household presence data in shared diagnostics.
