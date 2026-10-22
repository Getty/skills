# Select the control and transport path

## Compare by the actual requirement

| Technology/path | Useful for | Required proof and tradeoff |
|---|---|---|
| Ethernet / PoE + native API | Cameras, fixed hubs, gateways | Exact-model API, power budget and local authentication |
| Wi-Fi + native API | Plugs, meters, appliances | Local API versus cloud-only; reconnect/sleep behavior and AP capacity |
| Zigbee via ZHA | Integrated sensor/light network | Exact device features or quirk; one owner per coordinator |
| Zigbee via Zigbee2MQTT | Detailed converter/exposes management | Exact fingerprint; broker/service lifecycle |
| Matter over Wi-Fi/Ethernet | Standard local IP control | Required device type/features in product and HA |
| Matter over Thread | Low-power IP devices | Matter controller, Thread border router and IPv6 path |
| HomeKit Device | Import supported HomeKit accessories | Pairing ownership, transport and supported characteristics |
| HomeKit Bridge | Export HA entities to Apple Home | Deliberate exposure and avoidance of re-import loops |
| BLE advertisement / active GATT | Sensors, some locks/curtains | Decoder/key, passive versus active behavior, proxy support |
| DECT ULE / HAN FUN | FRITZ heating and smart devices | FRITZ model, compatibility and exposed API functions |
| Z-Wave | Region-specific sensor/actuator networks | Region, security keys, inclusion and migration support |
| EnOcean | Energy-harvesting controls/sensors | Controller, radio region and supported equipment profile |
| 433 MHz / proprietary RF | Legacy switches, weather sensors | Exact protocol and receive/transmit support; feedback may be absent |
| KNX | Established building automation | KNX/IP interface, group addresses, data types and keys |
| Modbus | Meters, inverters, HVAC | Register map, address convention, endian/scaling and permitted writes |
| DALI, BACnet, proprietary HVAC | Lighting/building plant | Verified gateway and maintained integration; no generic support promise |

Primary supported paths: [ZHA](https://www.home-assistant.io/integrations/zha/), [Zigbee2MQTT](https://www.zigbee2mqtt.io/guide/getting-started/), [Thread](https://www.home-assistant.io/integrations/thread/), [HomeKit Device](https://www.home-assistant.io/integrations/homekit_controller/), [HomeKit Bridge](https://www.home-assistant.io/integrations/homekit/), [Z-Wave](https://www.home-assistant.io/integrations/zwave_js/), [EnOcean](https://www.home-assistant.io/integrations/enocean/), [RFXtrx](https://www.home-assistant.io/integrations/rfxtrx/), [KNX](https://www.home-assistant.io/integrations/knx/), [Modbus](https://www.home-assistant.io/integrations/modbus/).

## Avoid category errors

- Matter is an application protocol; Thread is an IPv6 transport. A Thread logo alone does not establish Matter; a Matter device may use Wi-Fi.
- A Thread border router routes traffic; a Matter controller owns the application relationship. A Zigbee coordinator is neither by default.
- Wi-Fi is a network, not evidence for a local API. An API gateway may require a cloud account.
- MQTT is messaging infrastructure; a broker does not understand an arbitrary product. Discovery and payload semantics must be implemented.
- HomeKit Device imports; HomeKit Bridge exports.
- Bluetooth proxy support is not Bluetooth Classic audio forwarding.
- Zigbee 3.0 does not guarantee every manufacturer-specific function in every stack.

## Select for an existing mixed installation

Retain FRITZ DECT equipment while mapping its capabilities. Compare bridge-native Hue against direct Zigbee by required scenes/buttons/updates. Inspect mains-powered Zigbee plugs as potential routing infrastructure through their device definitions, not merely because they are mains powered. Map Shelly's IP network separately. Resolve unidentified small-vendor devices (BLE, proprietary Wi-Fi, legacy Zigbee) before buying radios.

Choose additional protocols when they serve a concrete device or function. A universal-hub purchase does not replace exact compatibility evidence. Use `smart-home-radio` for planning and `smart-home-devices` for model-level tradeoffs.
