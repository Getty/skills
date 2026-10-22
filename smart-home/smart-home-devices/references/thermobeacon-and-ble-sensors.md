# ThermoBeacon and Bluetooth environmental sensors

## Establish the actual device

Core ThermoBeacon lists SensorBlue **WS03, WS07 and WS08** and discovers them through HA's Bluetooth integration. These may be sold under other retail labels; compare the actual protocol and device identity, not the Amazon title alone. [HA ThermoBeacon](https://www.home-assistant.io/integrations/thermobeacon/).

| Family | Route to evaluate | Check |
| --- | --- | --- |
| SensorBlue / ThermoBeacon WS03, WS07, WS08 | ThermoBeacon | Advertisement visibility, readings, battery and freshness |
| Xiaomi Bluetooth thermometers | Exact Xiaomi BLE protocol/integration or documented alternate firmware | Model, encryption bind key and native versus modified firmware |
| Govee temperature/humidity products | Govee Bluetooth supported list | Active scan requirement and exact model |
| SwitchBot environmental sensors | SwitchBot Bluetooth supported list | Encryption/model, proxy support, cloud provisioning if applicable |
| Airthings air-quality sensors | Airthings BLE for supported Bluetooth mode | Active connection requirements; SmartLink mode is different |
| Sensirion gadgets | Sensirion BLE | Supported versus untested models |

BLE advertisements and active GATT connections have different resource/range needs. Use `smart-home-radio` for receiver placement and proxy design; do not assume a single adapter in a metal server cabinet covers the house. [HA Bluetooth](https://www.home-assistant.io/integrations/bluetooth/).

## Diagnose the observation chain

1. Record local display or reference reading, time and placement.
2. Verify Bluetooth receiver health and whether the raw advertisement is visible.
3. Determine whether an advertisement is parsed into the expected HA sensor.
4. Compare HA last update, value and availability; a stored number can remain unchanged legitimately or be stale.
5. Move a single test receiver/sensor temporarily to separate range from parsing problems.
6. Test physical stimulus and recovery after HA restart, then restore normal placement.

Avoid changing sensor firmware, integration and receiver at the same time. Do not use “nearby Bluetooth devices detected” as proof that this sensor's particular packets were received. A sensor can transmit a battery/identity packet more often than its measurement packet.

## Calibration and automation

Use a stable comparison interval and similar placement before setting an offset. Keep air temperature away from solar heating, radiators, electronics and drafts when the goal is room temperature. Preserve raw data while investigating spikes; do not hide a parsing problem behind aggressive smoothing. Automations that control heating or ventilation should include freshness and plausibility bounds, plus a fallback if no valid measurement arrives.

Temperature/humidity do not directly establish mold, CO2, occupancy or air safety. Use separate measured quantities when the task requires them. A displayed decimal precision is not sensor accuracy.

## Firsthand evidence

A report opened **2025-03-06** described periodic invalid ThermoBeacon values after moving from HA **2025.2.5** to **2025.3.0**, using a Brifit-branded device and Raspberry Pi 5 Bluetooth. It closed as a duplicate of issue 139917; the report alone does not prove a current regression or bad hardware. [Core issue 139972](https://github.com/home-assistant/core/issues/139972).

When an upgrade aligns with a measurement fault, compare the parser/integration change and raw packet behavior before buying new sensors. Follow the linked root issue to verify the actual fix version; record unknown where not established.

## Expansion examples

Airthings BLE documents a choice between Bluetooth and SmartLink modes, with active connection support required for local readings. Sensirion BLE lists specific gadgets, including one marked untested. Preserve those distinctions in buying advice. [Airthings BLE](https://www.home-assistant.io/integrations/airthings_ble/), [Sensirion BLE](https://www.home-assistant.io/integrations/sensirion_ble/).
