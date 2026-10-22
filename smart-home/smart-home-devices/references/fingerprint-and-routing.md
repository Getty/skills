# Device identification and route selection

## Establish identity before compatibility

Separate **retail identity** (brand, article number, EAN/ASIN, country), **hardware identity** (revision, radio module, supply), **protocol identity** (Zigbee model/manufacturer, BLE advertisement, Matter vendor/product ID, Wi-Fi API model), and **software identity** (firmware, HA Core, integration/library/converter version). Record each independently. A reseller can change the internal device without changing the listing title.

For Zigbee, download the device signature or interview from the existing controller. Capture `modelID`, exact `manufacturerName`, endpoints, input/output clusters, firmware build and selected converter/quirk. Preserve null suffixes or unusual characters in a machine-readable export. Pairing success means network admission; it does not establish usable clusters or data-point mappings. Tuya's project documentation explicitly requires fingerprints when reused model IDs have differing data points. [Zigbee2MQTT Tuya support](https://www.zigbee2mqtt.io/advanced/support-new-devices/02_support_new_tuya_devices.html).

## Choose a route for the required feature

| Route | Establish before choosing | Typical hidden dependency to test |
| --- | --- | --- |
| Native HA vendor integration | Exact product is supported; determine transport and entity list | Local control may still need cloud authentication or startup |
| Existing vendor bridge | Bridge generation/API and exposure of each child device | Vendor scenes, OTA and remotes may work differently through a generic bridge |
| Direct Zigbee ZHA/Z2M | Exact signature and feature support in installed release | Migration needs re-pairing; a Zigbee device belongs to one network |
| Matter | Actual device/bridge certification and firmware; HA supported clusters | Vendor-specific effects, energy or events may be absent |
| HomeKit Device | Device is a HomeKit accessory and available to pair | Existing HomeKit pairing may need removal; Thread is not automatically Matter |
| Bluetooth | Exact advertisement/protocol; passive versus active operation | Proxy supports advertisements but may lack the required active connection |
| MQTT | Broker, topic schema, discovery, command/state/availability paths | Retained state can look fresh when the physical device is gone |
| Custom integration | Repository identity, maintenance, version and dependencies | Installing via HACS does not certify compatibility or security |

HomeKit Device imports accessories into HA; HomeKit Bridge exports HA entities. Matter bridges expose supported child capabilities, not every proprietary API. Use the existing route when it meets the task unless a measured limitation warrants migration. [HA HomeKit Device](https://www.home-assistant.io/integrations/homekit_controller/), [HA Matter](https://www.home-assistant.io/integrations/matter/).

## Gather only the missing evidence

- For a lamp: label plus existing HA device info, supported color modes, available effects and power-on behavior.
- For a plug: exact SKU, rated load type, firmware, power/energy units, counter reset behavior and current integration.
- For a sensor: physical model, battery/power source, report interval, trigger semantics, stale-data behavior and local alarm capability.
- For a thermostat: heating system, valve/boiler role, setpoint owner, measured-temperature source and vendor schedule behavior.
- For a hub: firmware, child-device list, exposed endpoint types, backup method and local access path.

Do not collect credentials to answer a model-selection question. A screenshot of a product label should have serial numbers, MACs and pairing codes masked when shared publicly.

## Pilot acceptance procedure

Create a before/after record for one unit. Observe initial state without commands. Make a safe reversible change; confirm the physical result and the reported state independently. Exercise a manual control and inspect the event. Temporarily interrupt only the dependency under test, within the task's authorization, and observe whether the device, bridge, HA and recovery behave as expected. Keep safety alarms, access controls and heating protection operational while testing.

For a migration, preserve old entity names, dashboards, scenes and controller backups. Map old to new entities explicitly and disable duplicate control paths before enabling new automations. Do not delete the old route until the new route passes the actual use case.

## Evidence labels

Use `verified-documentation`, `verified-local-observation`, `firsthand-report`, `inference`, `unknown`, or `unsupported-in-tested-version`. A protocol's theoretical capability is not proof of a product's implementation. A model absent from a supported list is unverified unless the project explicitly rejects it. State “not verified for this exact revision” where that is the actual result.
