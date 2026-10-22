# Radio evidence and source ledger

Checked **2026-10-22**. Each report below concerns a specific setup. Counts of reports are not failure-rate estimates.

| Firsthand record | Date/setup | Observation and outcome | Use and limitation |
|---|---|---|---|
| [ZHA and Z2M sharing one LAN coordinator](https://community.home-assistant.io/t/zha-and-zigbee2mqtt-on-the-same-lan-zigbee-coordinator/731862) | 2024-05-22; existing ZHA network with 100+ devices, second Z2M client | Reporter saw two sockets but Z2M crashed when both ran | A connected TCP socket is not proof of safe shared coordinator ownership; no general reliability measurement |
| [HA core #161398](https://github.com/home-assistant/core/issues/161398) | 2026-01-21, HA Container 2026.1.0; later reports through 2026.9.4 | IPv6-only host hit Zeroconf source-address error; later dual-stack comparison initialized | Open in the inspected record; recheck installed release. Does not negate Thread's IPv6 requirement |
| [ESPHome #18614](https://github.com/esphome/esphome/issues/18614) | 2026-08-22; ESP32-WROOM, 2026.8.0 versus 2026.7.2 | Active BLE failed while API/Wi-Fi worked; same-hardware rollback restored behavior; closed via #18609 on Aug 23 | Firmware-specific regression evidence; identify a released fix, do not prescribe permanent old firmware |

## Primary technical sources

- [ZHA](https://www.home-assistant.io/integrations/zha/) and [device handlers](https://github.com/zigpy/zha-device-handlers): exact support and quirks.
- [Z2M adapters](https://www.zigbee2mqtt.io/guide/adapters/), [adapter settings](https://www.zigbee2mqtt.io/guide/configuration/adapter-settings.html), [network stability](https://www.zigbee2mqtt.io/advanced/zigbee/02_improve_network_range_and_stability.html): radio transport and placement.
- [Z2M HA discovery](https://www.zigbee2mqtt.io/guide/usage/integrations/home_assistant.html), [MQTT API](https://www.zigbee2mqtt.io/guide/usage/mqtt_topics_and_messages.html), [FAQ](https://www.zigbee2mqtt.io/guide/faq/), [OTA](https://www.zigbee2mqtt.io/guide/usage/ota_updates.html): service and migration behavior.
- [Matter](https://www.home-assistant.io/integrations/matter/), [Thread](https://www.home-assistant.io/integrations/thread/), [Matter server host requirements](https://github.com/home-assistant-libs/python-matter-server/blob/main/docs/os_requirements.md): commissioning and IPv6.
- [HA Bluetooth](https://www.home-assistant.io/integrations/bluetooth/), [ESPHome proxy](https://esphome.io/components/bluetooth_proxy/): BLE transport and connection capacity.
- [Z-Wave](https://www.home-assistant.io/integrations/zwave_js/), [controllers](https://www.home-assistant.io/docs/z-wave/controllers/), [EnOcean](https://www.home-assistant.io/integrations/enocean/), [RFXtrx](https://www.home-assistant.io/integrations/rfxtrx/), [rtl_433](https://github.com/merbanan/rtl_433): alternative radios.

Refresh exact-model sources in `smart-home-devices` before issuing OTA or migration instructions. Preserve the distinction between a supported procedure, a proposed workaround and a locally reproduced fix.
