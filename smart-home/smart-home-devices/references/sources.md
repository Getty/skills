# Primary source index and refresh policy

Research baseline: **2026-10-22**. URLs below were used to identify routes, support boundaries or original user reports. They are entry points to current documentation, not an immutable compatibility database. Read the relevant page again before implementation, updates or purchases. A manufacturer family in this skill is not a claim of exhaustive SKU coverage.

## Contents

- [Evidence hierarchy](#evidence-hierarchy)
- [Date guard and refresh](#date-guard-and-refresh)
- [Identity and protocol boundaries](#identity-and-protocol-boundaries)
- [Philips Hue](#philips-hue)
- [Shelly](#shelly)
- [THIRDREALITY](#thirdreality)
- [Tuya Zigbee](#tuya-zigbee)
- [Tuya cloud and LAN](#tuya-cloud-and-lan)
- [SONOFF and eWeLink](#sonoff-and-ewelink)
- [Zengge](#zengge)
- [ThermoBeacon and BLE sensors](#thermobeacon-and-ble-sensors)
- [Aqara Xiaomi and LUMI](#aqara-xiaomi-and-lumi)
- [OSRAM and LEDVANCE](#osram-and-ledvance)
- [Govee](#govee)
- [Paulmann](#paulmann)
- [Heating and HVAC](#heating-and-hvac)
- [Lighting locks and covers](#lighting-locks-and-covers)
- [Appliances cleaning and garden](#appliances-cleaning-and-garden)
- [Energy EV and solar](#energy-ev-and-solar)
- [Presence air quality and safety](#presence-air-quality-and-safety)
- [Additional firsthand cases](#additional-firsthand-cases)

## Evidence hierarchy

1. Use the exact manufacturer's label/manual for hardware identity, electrical/mechanical limits and intended reset procedure.
2. Use the current HA integration or exact Z2M definition for what the software implements; specialized ZHA behavior requires its own actual quirk/source evidence.
3. Use a custom integration's canonical repository, supported-model definitions and release history for that project's behavior. A HACS listing does not guarantee maintenance, security or every advertised vendor capability.
4. Use original issues and community posts for firsthand experience, retaining model, version, date and outcome. A report is not a failure-rate estimate.
5. Use retailer listings to check the selected purchasable variant and current price; do not substitute marketplace prose for protocol documentation.

## Date guard and refresh

A crawl date is not a release date. At this baseline the accessible HA LEDVANCE page stated introduction in **2026.11**, so this collection excludes that future feature as evidence of released native support. Check an integration's introduction version and current installed release; distinguish an announced capability, merged code and released usable support.

For each live task, refresh only the relevant vendor/route, current alerts, firmware release notes and directly matching issues. Record the review date and exact versions. If a support page has changed, retain historical issue conditions and mark current applicability rather than rewriting old reports as current facts. Do not make a purchase or firmware recommendation from an undated search snippet.

The topical references contain the practical interpretation. The first occurrence of each URL is indexed below; some sources are reused in more than one reference. Issue records are indexed alongside their vendor or in the last section. All links to issues are experience evidence, not specifications.

## Identity and protocol boundaries

See [fingerprint-and-routing.md](fingerprint-and-routing.md) for the model-specific interpretation.

- [Zigbee2MQTT Tuya support](https://www.zigbee2mqtt.io/advanced/support-new-devices/02_support_new_tuya_devices.html)
- [HA HomeKit Device](https://www.home-assistant.io/integrations/homekit_controller/)
- [HA Matter](https://www.home-assistant.io/integrations/matter/)

## Philips Hue

See [philips-hue.md](philips-hue.md) for the model-specific interpretation.

- [HA Hue](https://www.home-assistant.io/integrations/hue/)
- [HA Hue BLE](https://www.home-assistant.io/integrations/hue_ble/)
- [Hue developer onboarding](https://developers.meethue.com/develop/get-started-2/)
- [Core issue 154049](https://github.com/home-assistant/core/issues/154049)

## Shelly

See [shelly.md](shelly.md) for the model-specific interpretation.

- [HA Shelly](https://www.home-assistant.io/integrations/shelly/)
- [Plus Plug S technical reference](https://shelly-api-docs.shelly.cloud/gen2/Devices/Gen2/ShellyPlusPlugS/)
- [Shelly Gen1 API, Flood section](https://shelly-api-docs.shelly.cloud/gen1/#shelly-flood)
- [Core issue 124998](https://github.com/home-assistant/core/issues/124998)

## THIRDREALITY

See [third-reality.md](third-reality.md) for the model-specific interpretation.

- [Exact device definition](https://www.zigbee2mqtt.io/devices/3RSPE01044BZ.html)
- [Manufacturer catalog](https://www.thirdreality.com/)
- [Issue 29573](https://github.com/Koenkk/zigbee2mqtt/issues/29573)
- [Issue 31332](https://github.com/Koenkk/zigbee2mqtt/issues/31332)

## Tuya Zigbee

See [tuya-zigbee.md](tuya-zigbee.md) for the model-specific interpretation.

- [TS0201](https://www.zigbee2mqtt.io/devices/TS0201.html)
- [TS0203](https://www.zigbee2mqtt.io/devices/TS0203.html)
- [Issue 25207](https://github.com/Koenkk/zigbee2mqtt/issues/25207)

## Tuya cloud and LAN

See [tuya-wifi-local-cloud.md](tuya-wifi-local-cloud.md) for the model-specific interpretation.

- [HA Tuya](https://www.home-assistant.io/integrations/tuya/)
- [LocalTuya](https://github.com/rospogrigio/localtuya)
- [tuya-local](https://github.com/make-all/tuya-local)
- [LocalTuya issue 1380](https://github.com/rospogrigio/localtuya/issues/1380)

## SONOFF and eWeLink

See [sonoff-ewelink.md](sonoff-ewelink.md) for the model-specific interpretation.

- [SonoffLAN](https://github.com/AlexxIT/SonoffLAN)
- [SNZB-02P](https://www.zigbee2mqtt.io/devices/SNZB-02P.html)
- [SNZB-01P](https://www.zigbee2mqtt.io/devices/SNZB-01P.html)
- [Motion-sensor report](https://github.com/AlexxIT/XiaomiGateway3/issues/738)
- [SNZB-03 definition](https://www.zigbee2mqtt.io/devices/SNZB-03.html)
- [SONOFF MS01 probe](https://sonoff.tech/en-de/products/sonoff-ms01-smart-soil-moisture-sensor-with-rj9-adapter)
- [Issue 27919](https://github.com/Koenkk/zigbee2mqtt/issues/27919)

## Zengge

See [zengge-lighting.md](zengge-lighting.md) for the model-specific interpretation.

- [HA Magic Home](https://www.home-assistant.io/integrations/flux_led/)
- [HA LED BLE](https://www.home-assistant.io/integrations/led_ble/)
- [LEDnetWF BLE project](https://github.com/8none1/lednetwf_ble)
- [Core issue 124083](https://github.com/home-assistant/core/issues/124083)

## ThermoBeacon and BLE sensors

See [thermobeacon-and-ble-sensors.md](thermobeacon-and-ble-sensors.md) for the model-specific interpretation.

- [HA ThermoBeacon](https://www.home-assistant.io/integrations/thermobeacon/)
- [HA Bluetooth](https://www.home-assistant.io/integrations/bluetooth/)
- [Core issue 139972](https://github.com/home-assistant/core/issues/139972)
- [Airthings BLE](https://www.home-assistant.io/integrations/airthings_ble/)
- [Sensirion BLE](https://www.home-assistant.io/integrations/sensirion_ble/)

## Aqara Xiaomi and LUMI

See [aqara-xiaomi-lumi.md](aqara-xiaomi-lumi.md) for the model-specific interpretation.

- [Legacy gateway](https://www.home-assistant.io/integrations/xiaomi_aqara/)
- [Core Xiaomi Home](https://www.home-assistant.io/integrations/xiaomi_miio/)
- [Vendor Xiaomi Home project](https://github.com/XiaoMi/ha_xiaomi_home)
- [Aqara FP2](https://eu.aqara.com/en-eu/products/aqara-presence-sensor-fp2)
- [Aqara sensors disconnecting](https://community.home-assistant.io/t/aqara-sensors-keep-disconnecting/751436)

## OSRAM and LEDVANCE

See [osram-ledvance.md](osram-ledvance.md) for the model-specific interpretation.

- [OSRAM announcement](https://ams-osram.com/news/press-releases/pr-09-03-2020)
- [LEDVANCE Zigbee FAQ](https://www.ledvance.com/en-asia/home-lighting/services/faq/faq-for-smart-zigbee-products)
- [Observed future-dated page](https://www.home-assistant.io/integrations/ledvance/) — **future introduction at this baseline; excluded as released support**
- [Z2M issue 26686](https://github.com/Koenkk/zigbee2mqtt/issues/26686)

## Govee

See [govee.md](govee.md) for the model-specific interpretation.

- [HA Govee lights local](https://www.home-assistant.io/integrations/govee_light_local/)
- [Manufacturer LAN guide](https://app-h5.govee.com/user-manual/wlan-guide)
- [HA Govee Bluetooth](https://www.home-assistant.io/integrations/govee_ble/)
- [govee2mqtt SKU notes](https://github.com/wez/govee2mqtt/blob/main/docs/SKUS.md)
- [Core issue 140100](https://github.com/home-assistant/core/issues/140100)

## Paulmann

See [paulmann.md](paulmann.md) for the model-specific interpretation.

- [Paulmann compatibility and support](https://de.paulmann.com/smart-home/kompatibilitaet/)
- [Paulmann 929.66](https://www.zigbee2mqtt.io/devices/929.66.html)
- [Z2M issue 26186](https://github.com/Koenkk/zigbee2mqtt/issues/26186)

## Heating and HVAC

See [heating-hvac-ecosystems.md](heating-hvac-ecosystems.md) for the model-specific interpretation.

- [HA Bosch SHC](https://www.home-assistant.io/integrations/bosch_shc/)
- [Bosch SHC community integration](https://github.com/tschamm/boschshc-hass) — separate capability/migration evaluation for thermostat control
- [HA Homematic IP Cloud](https://www.home-assistant.io/integrations/homematicip_cloud/)
- [Project](https://github.com/sukramj/homematicip_local)
- [integration guide](https://sukramj.github.io/aiohomematic/user/homeassistant_integration/)
- [HA tado](https://www.home-assistant.io/integrations/tado/)
- [HA Netatmo](https://www.home-assistant.io/integrations/netatmo/)
- [HA Daikin](https://www.home-assistant.io/integrations/daikin/)
- [HA MELCloud](https://www.home-assistant.io/integrations/melcloud/)
- [HA Overkiz](https://www.home-assistant.io/integrations/overkiz/)
- [meross_lan](https://github.com/krahabb/meross_lan)

## Lighting locks and covers

See [lighting-locks-covers-ecosystems.md](lighting-locks-covers-ecosystems.md) for the model-specific interpretation.

- [HA TRÅDFRI](https://www.home-assistant.io/integrations/tradfri/)
- [IKEA Matter explanation](https://www.ikea.com/de/de/customer-service/knowledge/articles/99f660cc-544a-4f35-b9b5-7b72556be25b.html)
- [HA Nanoleaf](https://www.home-assistant.io/integrations/nanoleaf/)
- [HA Eve](https://www.home-assistant.io/integrations/eve/)
- [HA SwitchBot](https://www.home-assistant.io/integrations/switchbot/)
- [HA Nuki](https://www.home-assistant.io/integrations/nuki/)
- [HA Yale](https://www.home-assistant.io/integrations/yale/)
- [Yale Access Bluetooth](https://www.home-assistant.io/integrations/yalexs_ble/)
- [HA VELUX](https://www.home-assistant.io/integrations/velux/)
- [HA issue 160196](https://github.com/home-assistant/core/issues/160196)

## Appliances cleaning and garden

See [plugs-appliances-cleaning-garden.md](plugs-appliances-cleaning-garden.md) for the model-specific interpretation.

- [HA TP-Link](https://www.home-assistant.io/integrations/tplink/)
- [HA Home Connect](https://www.home-assistant.io/integrations/home_connect/)
- [HA LG ThinQ](https://www.home-assistant.io/integrations/lg_thinq/)
- [HA Miele](https://www.home-assistant.io/integrations/miele/)
- [HA SmartThings](https://www.home-assistant.io/integrations/smartthings/)
- [HA Roborock](https://www.home-assistant.io/integrations/roborock/)
- [Project](https://github.com/Tasshack/dreame-vacuum)
- [HA Ecovacs](https://www.home-assistant.io/integrations/ecovacs/)
- [Valetudo supported robots](https://valetudo.cloud/pages/general/supported-robots/)
- [HA GARDENA Bluetooth](https://www.home-assistant.io/integrations/gardena_bluetooth/)
- [HA Hydrawise](https://www.home-assistant.io/integrations/hydrawise/)
- [HA Rachio](https://www.home-assistant.io/integrations/rachio/)
- [HA Automower](https://www.home-assistant.io/integrations/husqvarna_automower/)

## Energy EV and solar

See [energy-ev-solar.md](energy-ev-solar.md) for the model-specific interpretation.

- [HA DSMR](https://www.home-assistant.io/integrations/dsmr/)
- [HA Fronius](https://www.home-assistant.io/integrations/fronius/)
- [HA SMA](https://www.home-assistant.io/integrations/sma/)
- [HA Powerwall](https://www.home-assistant.io/integrations/powerwall/)
- [HA Wallbox](https://www.home-assistant.io/integrations/wallbox/)
- [evcc HA guide](https://docs.evcc.io/en/smarthome/home-assistant/)
- [HA Tibber](https://www.home-assistant.io/integrations/tibber/)
- [HA Energy documentation](https://www.home-assistant.io/docs/energy/)

## Presence air quality and safety

See [presence-air-quality-safety.md](presence-air-quality-safety.md) for the model-specific interpretation.

- [Project](https://github.com/EverythingSmartHome/everything-presence-lite)
- [setup guide](https://docs.everythingsmart.io/s/products/doc/set-up-your-epl-device-in-home-assistant-EcxzrA79Z3)
- [Project](https://github.com/ApolloAutomation/MSR-2)
- [manufacturer wiki](https://wiki.apolloautomation.com/products/msr2/introduction/)

## Additional firsthand cases

See [community-evidence.md](community-evidence.md) for the model-specific interpretation.

Primary sources for this topic are indexed in the preceding vendor sections.
