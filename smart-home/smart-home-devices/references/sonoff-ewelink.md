# SONOFF and eWeLink

## Separate brand, platform and transport

SONOFF is a hardware brand; eWeLink is an ecosystem used by multiple manufacturers and can also appear in a Zigbee manufacturer string. Choose integration by the actual transport and firmware, not by either name.

| Family | Candidate route | Check |
| --- | --- | --- |
| SNZB Zigbee sensors/buttons | ZHA or Zigbee2MQTT | Exact model/signature, reports, quirk/converter and battery behavior |
| Wi-Fi BASIC/MINI/POW/TH/DUAL families | Verified eWeLink LAN/cloud path, often SonoffLAN custom integration | Hardware generation, stock firmware LAN support, local credentials and region |
| Matter products | HA Matter | Exact product certification and exposed functions |
| USB/network Zigbee coordinators | Supported coordinator driver | Coordinator firmware is unrelated to sensor firmware |
| NSPanel, bridges, gateways and displays | Exact stock or replacement firmware project | Do not call every eWeLink hub a generic ZHA/Z2M coordinator |
| Wired temperature/soil probes | Host controller's integration | Probe is not necessarily independently networked |

SonoffLAN is community software for devices with original eWeLink firmware, offering local and/or cloud paths depending on the device. Check its supported-device list and selected mode. Do not claim every eWeLink device becomes permanently cloud-free. [SonoffLAN](https://github.com/AlexxIT/SonoffLAN).

## SNZB devices

For **SNZB-02P**, use the exact entry: temperature, humidity, battery and calibration are exposed by Z2M. Check report cadence and confirm a physical temperature/humidity change. Calibration should follow a stable reference comparison; a device placed near a radiator is not corrected by an arbitrary offset. [SNZB-02P](https://www.zigbee2mqtt.io/devices/SNZB-02P.html).

For **SNZB-01P**, single/double/long actions are documented. It sleeps and may need waking for configuration. The Z2M page explicitly describes direct binding that does not control devices/groups for the documented v2.2.0 behavior. Do not promise HA-independent button operation merely because a bind request succeeds. Test each press and build an HA automation where needed. [SNZB-01P](https://www.zigbee2mqtt.io/devices/SNZB-01P.html).

## Resolve MS01 before configuring it

`MS01` is ambiguous. A firsthand gateway report identifies **SONOFF MS01 / SNZB-03** as a Zigbee motion sensor, and the SNZB-03 device entry exposes occupancy. Separately, SONOFF sells an **MS01 wired capacitive soil-moisture probe** for TH Elite/TH Origin. The inventory's eWeLink context is insufficient to prove which is present. [Motion-sensor report](https://github.com/AlexxIT/XiaomiGateway3/issues/738), [SNZB-03 definition](https://www.zigbee2mqtt.io/devices/SNZB-03.html), [SONOFF MS01 probe](https://sonoff.tech/en-de/products/sonoff-ms01-smart-soil-moisture-sensor-with-rj9-adapter).

Inspect the device photo/label and current signature. A battery unit with Zigbee occupancy clusters follows the motion route; a cabled probe attached to a TH unit follows the host's sensor path. Do not configure irrigation from a model string.

## Reporting and practical tests

A 2025-07-07 report on Z2M 2.5.1 and Ember firmware 8.0.2 described failed binding while changing SNZB-02P reporting. It closed as stale/not planned, which does not establish a fix. [Issue 27919](https://github.com/Koenkk/zigbee2mqtt/issues/27919). Check battery/wake state, radio delivery and actual write acknowledgment before inferring a device cannot support reporting changes.

Keep the original interval and threshold. Change one sensor, observe real reports, then decide whether its battery/latency tradeoff fits the task. For motion, test entry, stillness, clear delay and retrigger behavior. For a button, test debouncing and avoid an unsafe action on an ambiguous long-press sequence.

For TH/probe irrigation, retain a maximum run duration and an independent manual stop; stale moisture must not trigger indefinite watering. For relays and energy monitors, use the installed product's electrical instructions and an appropriate installer where mains work is involved.
