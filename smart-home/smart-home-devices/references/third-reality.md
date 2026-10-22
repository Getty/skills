# THIRDREALITY

## Exact model: 3RSPE01044BZ

Preserve the exact identifier `3RSPE01044BZ`. Zigbee2MQTT has an exact entry describing a Zigbee/BLE power-monitoring plug, exposing switching, power/energy/current/voltage/frequency/power-factor, power-on behavior, LED brightness, energy reset and countdown controls. OTA is listed. These are converter capabilities; firmware and the installed Z2M release still govern availability. [Exact device definition](https://www.zigbee2mqtt.io/devices/3RSPE01044BZ.html).

Do not replace this identity with a newer plug SKU or assume that a BLE feature means a generic HA Bluetooth integration can control it. If using ZHA, inspect the actual signature and quirk supported by that HA release independently; Z2M support is not a ZHA support guarantee.

## Product-family map

| Family | Route to investigate | Required distinction |
| --- | --- | --- |
| Regional Zigbee power plugs | ZHA or Zigbee2MQTT | Socket/voltage region, power metering, firmware and reset behavior |
| Matter plugs/controllers/garage accessories | Matter for the exact model | Transport and exposed endpoints; do not infer from Zigbee products |
| Temperature, contact, motion, leak and air-quality sensors | Exact Zigbee or Matter device entry | Powered router versus sleepy end device; which values are real sensors |
| Buttons, mechanical switch actuators and lighting | Exact device definition | Event semantics, physical fit, local binding and startup state |
| Hubs and bridges | Manufacturer documentation and exposed bridge interface | Hub ownership, cloud dependency and child feature coverage |

Use the manufacturer's current product categories as discovery, then verify an individual SKU. The catalog includes plugs, switches, sensors, controllers, lighting and hubs; market and protocol availability differ. [Manufacturer catalog](https://www.thirdreality.com/).

## Plug acceptance and measurement

Build a per-plug record with firmware, converter version, circuit/use, required control and energy unit. Do not reset accumulated energy to “fix” a scaling discrepancy. Compare a steady resistive reference load and a representative appliance cycle against an independent meter; current × voltage is apparent power and equals real power only with the corresponding power factor. Check the power and cumulative energy channels separately.

Measure message rate while outputs are on and off. Pilot one or two plugs before applying reporting changes to the whole batch. A setting successfully written to a reporting table does not prove the device obeys it in every operating state. Protect Zigbee button latency and battery-device delivery from excessive metering traffic.

## Firsthand evidence

- **2025-11-10, Z2M 2.6.3, firmware v1.00.98, SLZB-06M:** an owner reported excessive power/energy for a dishwasher on two units and compared with a separate meter. The issue is closed; this collection does not establish a general fix or a failure rate. [Issue 29573](https://github.com/Koenkk/zigbee2mqtt/issues/29573).
- **2026-03-09, Z2M 2.9.1, plug firmware 1.01.01, SLZB-06M:** an owner of 20 units reported improved response after reducing reporting, then high-rate reporting when plugs were off. The captured issue remained open. Inspect the latest discussion before acting. [Issue 31332](https://github.com/Koenkk/zigbee2mqtt/issues/31332).

These reports justify targeted checks for this exact model. They do not imply that a batch of these plugs necessarily overloads a network or that every firmware shares the problem.

## Recovery and changes

Keep an inventory of IEEE address aliases, firmware and parent network before updates. Pilot firmware with representative measurement and latency checks. If settings are ignored, preserve the before/after trace and escalate with the model signature rather than repeatedly writing clusters. A factory reset is a last diagnostic step because it discards network membership and may break automation references.
