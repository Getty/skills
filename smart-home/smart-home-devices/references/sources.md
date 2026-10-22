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
- [HA Hue config_flow 2026.10.2](https://github.com/home-assistant/core/blob/2026.10.2/homeassistant/components/hue/config_flow.py) — BSB002/BSB003 model IDs, automatic v2→Bridge Pro entry migration, TLS verification disabled for BSB003
- [HA Hue binary_sensor 2026.10.2](https://github.com/home-assistant/core/blob/2026.10.2/homeassistant/components/hue/v2/binary_sensor.py) — MotionAware, contact, tamper, camera motion, entertainment-active entities
- [Hue End of Support policy](https://www.philips-hue.com/en-us/support/legal/end-of-support-policy) — Bridge v1 updates and online services ended 2020-04-30
- [Hue Bridge Pro product page](https://www.philips-hue.com/en-us/p/hue-bridge-pro/046677582111) — Ethernet/Wi-Fi, 150 lights/50 accessories, 12NC 929003582615
- [Signify 2025-09-04 Bridge Pro/Essential](https://www.signify.com/en-us/our-company/news/press-releases/2025/20250904-far-more-than-intelligent-lighting-philips-hue-reimagines-smart-home) — Bridge Pro specs, Essential range, OmniGlow, Festavia
- [Signify 2025-09-04 ambiance release](https://www.signify.com/global/our-company/news/press-releases/2025/20250904-ambiance-reimagined-how-philips-hue-unlocks-a-new-level-of-smart-lighting) — new-generation bulbs incl. Essential support Matter over Thread; regional Essential SKUs
- [Signify 2025-09-04 Hue Secure](https://www.signify.com/global/our-company/news/press-releases/2025/20250904-hue-secure-expands-portfolio-with-wired-video-doorbell-2k-cameras-and-motionaware-for-smarter-home-monitoring) — doorbell, chime, 2K cameras (Wi-Fi), MotionAware Bridge-Pro-exclusive
- [Signify 2023-08-31 Hue Secure launch](https://www.signify.com/en-us/our-company/news/press-releases/2023/20230831-philips-hue-integrates-smart-lighting-sensors-and-cameras-to-help-secure-your-home) — wired, battery, floodlight cameras and contact sensor
- [Signify 2026-09-03 IFA release](https://www.signify.com/global/our-company/news/press-releases/2026/20260903-philips-hue-expands-on-smart-lighting-with-ai-immersive-entertainment-and-design) — Sync Box 4K, Play Screen Sync, BLE bridgeless sync, Nanoleaf Wall Light Module, Backup/Restore, AI behaviors
- [Hue MotionAware support](https://www.philips-hue.com/en-us/support/article/motionawaretm--transform-your-hue-lights-into-motion-sensors/000011) — 3–4 lights per area, 4 areas, indoor only, subscription for alerts
- [Hue and Matter guide](https://www.philips-hue.com/en-us/support/article/philips-hue-and-matter-complete-setup-and-support-guide/000012) — Matter box/QR/11-digit marks, remove from bridge before direct Matter, bridge-vs-direct feature table
- [Hue Matter overview](https://www.philips-hue.com/en-us/explore-hue/works-with/matter) — Sync Box and Tap dial rotary not via Matter; BLE-connected products not Matter
- [Silicon Labs/Signify 2026-06-23](https://news.silabs.com/2026-06-23-Signify-Enhances-Philips-Hue-Matter-Support-Through-Collaboration-with-Silicon-Labs) — Zigbee-or-Thread at commissioning today; concurrent Zigbee + Thread update later in 2026
- [Z2M philips.ts](https://github.com/Koenkk/zigbee-herdsman-converters/blob/master/src/devices/philips.ts) — modelID ↔ product/12NC/EAN map, Hue Tap Green Power fingerprint, floodlight-camera light
- [Z2M Hue device page](https://www.zigbee2mqtt.io/devices/9290012573A.html) — Touchlink reset by serial, community power-cycle reset
- [ZHA quirks philips](https://github.com/zigpy/zha-device-handlers/blob/dev/zhaquirks/philips/__init__.py) — manufacturer strings `Philips` / `Signify Netherlands B.V.`
- [huesyncbox (HACS)](https://github.com/mvdwetering/huesyncbox) — sync box/Screen Sync support, HA ≥ 2026.8
- Report: [matter-smarthome.de CTO interview](https://matter-smarthome.de/en/products/philips-hue-details-on-the-next-generation-with-thread/) — Thread disabled while on a bridge; Bridge Pro won't be a border router; no Thread for battery accessories

## Shelly

See [shelly.md](shelly.md) for the model-specific interpretation.

- [HA Shelly](https://www.home-assistant.io/integrations/shelly/)
- [Plus Plug S technical reference](https://shelly-api-docs.shelly.cloud/gen2/Devices/Gen2/ShellyPlusPlugS/)
- [Shelly Gen1 API, Flood section](https://shelly-api-docs.shelly.cloud/gen1/#shelly-flood)
- [Core issue 124998](https://github.com/home-assistant/core/issues/124998)
- [Shelly Gen2+ Firmware Update Policy](https://shelly-api-docs.shelly.cloud/gen2/General/FirmwareUpdatePolicy) — Gen3/Gen4 get all updates; list of Gen2 devices feature-frozen at 1.7.x
- [Shelly component / GET /shelly](https://shelly-api-docs.shelly.cloud/gen2/ComponentsAndServices/Shelly) — Gen2+ device-info fields gen/model/app/id for identification
- [Shelly Gen1 API](https://shelly-api-docs.shelly.cloud/gen1/) — Gen1 type codes (SHSW-1, SHPLG-S, SHWT-1 …), CoIoT, changelog up to v1.14.0
- [Shelly Zigbee component](https://shelly-api-docs.shelly.cloud/gen2/ComponentsAndServices/Zigbee) — Zigbee enable/state RPC on Gen4
- [Shelly 1 Gen4 API](https://shelly-api-docs.shelly.cloud/gen2/Devices/Gen4/Shelly1G4) — Gen4 components; BTHome unavailable in Zigbee mode
- [Shelly Dimmer Gen4 API](https://shelly-api-docs.shelly.cloud/gen2/Devices/Gen4/ShellyDimmerG4) — no-neutral wiring; calibration not via Zigbee
- [Shelly BLU docs](https://shelly-api-docs.shelly.cloud/docs-ble/) — BLU = BTHome, ~30 m range; per-device short names (SBBT/SBDW/SBMO/SBHT/SBTR…)
- [Shelly BLU encryption](https://shelly-api-docs.shelly.cloud/docs-ble/encryption) — AES-CCM key, passkey, reset-only decryption
- [Shelly BLU TRV API](https://shelly-api-docs.shelly.cloud/docs-ble/Devices/BLU_ZB/trv) — TRV Zigbee thermostat clusters and gateway features
- [Shelly KB device lists](https://kb.shelly.cloud/knowledge-base/shelly-gen4-devices) — current per-line lists (also -gen1-, -plus-, -pro-, -gen3-, -ble-, -wave-devices, shelly-control-panels)
- [Shelly KB: Shelly 1 Gen4](https://kb.shelly.cloud/knowledge-base/shelly-1-gen4) — device identification block format; Matter default ↔ Zigbee profile button sequence
- [Shelly KB: Flood Gen4](https://kb.shelly.cloud/knowledge-base/shelly-flood-gen4) — S4SN-0071A; Wi-Fi/BLE/Zigbee/Matter; wake/sleep/inclusion presses
- [Shelly KB: BLU TRV](https://kb.shelly.cloud/knowledge-base/shelly-blu-trv) — simultaneous BLE + Zigbee 3.0; BLU Gateway Gen3 for Shelly control
- [Shelly KB: Wave 1 EU LR](https://kb.shelly.cloud/knowledge-base/shelly-wave-1-eu-lr) — QL* LR SKUs; mesh vs Long Range choice at inclusion; manufacturer 0x0460
- [Shelly KB: Plus Plug S V2](https://kb.shelly.cloud/knowledge-base/shelly-plus-plug-s-v2) — V2 model SNPL-10112EU
- [Shelly KB: enable Matter on Gen3+](https://kb.shelly.cloud/knowledge-base/setting-up-gen3-devices-via-matter) — Matter enabled per device via web UI after firmware update
- [Z2M Shelly converters](https://github.com/Koenkk/zigbee-herdsman-converters/blob/master/src/devices/shelly.ts) — Zigbee model IDs → SKUs for Gen4 and BLU ZB devices
- [HA forum: Shelly Gen4 Zigbee mode](https://community.home-assistant.io/t/shelly-gen4-zigbee-mode/888242) — REPORT: Wi-Fi alongside Zigbee only with BT off; flaky pairing (fw 1.7.1)

## THIRDREALITY

See [third-reality.md](third-reality.md) for the model-specific interpretation.

- [Exact device definition](https://www.zigbee2mqtt.io/devices/3RSPE01044BZ.html)
- [Manufacturer catalog](https://www.thirdreality.com/)
- [Issue 29573](https://github.com/Koenkk/zigbee2mqtt/issues/29573)
- [Issue 31332](https://github.com/Koenkk/zigbee2mqtt/issues/31332)
- [THIRDREALITY store catalog (JSON)](https://www.3reality.com/products.json) — current US range, protocols, retail SKUs (2026-10)
- [Z2M Third Reality converter](https://github.com/Koenkk/zigbee-herdsman-converters/blob/master/src/devices/third_reality.ts) — 3R model IDs, white-label names, private clusters
- [ZHA Third Reality quirks](https://github.com/zigpy/zha-device-handlers/tree/dev/zhaquirks/thirdreality) — manufacturer string `Third Reality, Inc`; plug Gen2/Gen3 quirks incl. 3RSPE01044BZ
- [HA Third Reality brand page](https://www.home-assistant.io/integrations/third_reality/) — Works with HA partner for Zigbee and Matter; certified model list
- [Works with HA certified products](https://works-with.home-assistant.io/certified-products/) — certified IDs (contains data errors)
- [Z2M 3RSP02064Z (Gen3)](https://www.zigbee2mqtt.io/devices/3RSP02064Z.html) — default W reporting lag; rise/drop thresholds

## Tuya Zigbee

See [tuya-zigbee.md](tuya-zigbee.md) for the model-specific interpretation.

- [TS0201](https://www.zigbee2mqtt.io/devices/TS0201.html)
- [TS0203](https://www.zigbee2mqtt.io/devices/TS0203.html)
- [Issue 25207](https://github.com/Koenkk/zigbee2mqtt/issues/25207)
- [zigbee-herdsman-converters tuya.ts](https://github.com/Koenkk/zigbee-herdsman-converters/blob/master/src/devices/tuya.ts) — Z2M Tuya definitions: model IDs, device classes, manufacturer-name fingerprints, magic packet/DP extends
- [zigbee-herdsman cluster definitions](https://github.com/Koenkk/zigbee-herdsman/blob/master/src/zspec/zcl/definition/cluster.ts) — `manuSpecificTuya` = cluster 0xEF00
- [ZHA quirks: zhaquirks/tuya](https://github.com/zigpy/zha-device-handlers/tree/dev/zhaquirks/tuya) — per-model ZHA quirk files; quirks v2 `TuyaQuirkBuilder`, `tuya_enchantment`
- [zhaquirks/tuya/__init__.py](https://github.com/zigpy/zha-device-handlers/blob/dev/zhaquirks/tuya/__init__.py) — Tuya cluster IDs 0xEF00, 0xE000, 0xE001, 0x1888, 0xED00
- [Tuya: Zigbee sub-device custom DPs](https://support.tuya.com/en/help/_detail/Kdah1urvujsay) — private cluster 0xEF00; DP 1–100 standard, 101–255 custom; DP types
- [Z2M device options](https://www.zigbee2mqtt.io/guide/configuration/devices-groups.html) — `throttle`/`debounce`, names TS0601 air-quality sensors
- [Z2M TS011F_plug_1](https://www.zigbee2mqtt.io/devices/TS011F_plug_1.html) — reporting disabled from firmware 1.0.5, polling option, unreliable metering variant
- [CSA: Tuya Smart Wired Gateway Pro](https://csa-iot.org/csa_product/smart-wired-gateway-pro-3/) — Tuya Matter gateway, device type 0x000E, Zigbee + Thread downlink

## Tuya cloud and LAN

See [tuya-wifi-local-cloud.md](tuya-wifi-local-cloud.md) for the model-specific interpretation.

- [HA Tuya](https://www.home-assistant.io/integrations/tuya/)
- [LocalTuya](https://github.com/rospogrigio/localtuya)
- [tuya-local](https://github.com/make-all/tuya-local)
- [LocalTuya issue 1380](https://github.com/rospogrigio/localtuya/issues/1380)
- [HA Tuya manifest](https://github.com/home-assistant/core/blob/dev/homeassistant/components/tuya/manifest.json) — cloud_push, tuya-device-sharing-sdk + tuya-device-handlers, DHCP MAC prefixes
- [tuya-device-handlers docs](https://tuya-device-handlers.readthedocs.io/) — core Tuya quirks by product_id; custom quirks in `<config>/tuya_quirks/`
- [xZetsubou/hass-localtuya](https://github.com/xZetsubou/hass-localtuya) — active LocalTuya fork; sub-devices, IR remotes; protocols 3.1–3.5
- [tuya-local DEVICE_DETAILS.md](https://github.com/make-all/tuya-local/blob/main/DEVICE_DETAILS.md) — key retrieval; only Tuya Smart/Smart Life apps are visible to the portal
- [tinytuya](https://github.com/jasonacox/tinytuya) — protocols 3.1–3.5, ports, wizard and IoT Core one-month trial, 3.5 needs GCM
- [PlusPlus-ua/ha_tuya_ble](https://github.com/PlusPlus-ua/ha_tuya_ble) — direct Tuya BLE; needs cloud device ID/key; no push since 2024-07
- [tuya-cloudcutter](https://github.com/tuya-cloudcutter/tuya-cloudcutter) — supported chips/modules, SDK patched Feb 2022, loses Tuya app
- [OpenBeken (OpenBK7231T_App)](https://github.com/openshwprojects/OpenBK7231T_App) — supported chips; T1/T2/T3/T7 chip mapping
- [LibreTiny supported chips](https://docs.libretiny.eu/docs/status/supported/) — BK72xx, RTL8710B, RTL8720C, LN882H; Tuya module boards
- [ESPHome LibreTiny](https://esphome.io/components/libretiny/) — ESPHome support for BK7231T/N, BK7238, RTL8710BN/BX, LN882H
- [tuya-convert](https://github.com/ct-Open-Source/tuya-convert) — ESP OTA flashing blocked by Tuya's Jan 2019 patch

## SONOFF and eWeLink

See [sonoff-ewelink.md](sonoff-ewelink.md) for the model-specific interpretation.

- [SonoffLAN](https://github.com/AlexxIT/SonoffLAN)
- [SNZB-02P](https://www.zigbee2mqtt.io/devices/SNZB-02P.html)
- [SNZB-01P](https://www.zigbee2mqtt.io/devices/SNZB-01P.html)
- [Motion-sensor report](https://github.com/AlexxIT/XiaomiGateway3/issues/738)
- [SNZB-03 definition](https://www.zigbee2mqtt.io/devices/SNZB-03.html)
- [SONOFF MS01 probe](https://sonoff.tech/en-de/products/sonoff-ms01-smart-soil-moisture-sensor-with-rj9-adapter)
- [Issue 27919](https://github.com/Koenkk/zigbee2mqtt/issues/27919)
- [SONOFF store catalog (JSON)](https://sonoff.tech/products.json) — current product range, model codes, radio per product (2026-10)
- [Z2M SONOFF converter](https://github.com/Koenkk/zigbee-herdsman-converters/blob/master/src/devices/sonoff.ts) — Zigbee model IDs, white-labels, OTA flags, manufacturer strings
- [ZHA SONOFF quirks](https://github.com/zigpy/zha-device-handlers/tree/dev/zhaquirks/sonoff) — which SONOFF models have ZHA quirks
- [Z2M ZBMINIL2](https://www.zigbee2mqtt.io/devices/ZBMINIL2.html) — no-neutral relay is an end device, not a router
- [Z2M ZBM5](https://www.zigbee2mqtt.io/devices/ZBM5-1C-80_86.html) — router/end-device firmware by neutral; 1.0.6 OTA issue; binding requirements
- [Z2M issue 33185](https://github.com/Koenkk/zigbee2mqtt/issues/33185) — ZBM5 1.0.6 captures OTA discovery (open, 2026-09-22)
- [Z2M SNZB-06P](https://www.zigbee2mqtt.io/devices/SNZB-06P.html) — firmware 1.0.3 misbehaves; upgrade to ≥1.0.5
- [Z2M SNZT-04P](https://www.zigbee2mqtt.io/devices/SNZT-04P.html) — Gen3 dual-protocol sensor, Zigbee mode exposes
- [SonoffLAN DEVICES.md](https://github.com/AlexxIT/SonoffLAN/blob/master/DEVICES.md) — eWeLink model/UIID to local-protocol support
- [eWeLink Smart Home add-on](https://github.com/iHost-Open-Source-Project/hassio-ihost-addon/tree/master/hassio-ihost-ewelink-smart-home) — official replacement add-on, MQTT, no HA→eWeLink sync
- [Legacy CoolKit add-on (archived)](https://github.com/CoolKit-Technologies/ha-addon) — archived, unmaintained
- [eWeLink-Remote Gateway add-on](https://github.com/iHost-Open-Source-Project/hassio-ihost-addon/tree/master/hassio-ihost-ewelink-remote) — BLE R5/S-Mate into HA; needs Bluetooth passive scanning
- [iHost HAOS port](https://github.com/iHost-Open-Source-Project/ha-operating-system) — SONOFF-maintained HA OS for iHost
- [SONOFF DIY mode tools/protocol](https://github.com/itead/Sonoff_Devices_DIY_Tools) — DIY LAN API, documented for BASICR3/RFR3/MINI
- [SONOFF: How SONOFF works with HA](https://sonoff.tech/en-us/blogs/news/how-sonoff-works-with-home-assistant) — vendor guide (still references the archived add-on)
- [Tasmota template: BASICR4](https://templates.blakadder.com/sonoff_BASICR4.html) — community template; ESP32-C3

## Zengge

See [zengge-lighting.md](zengge-lighting.md) for the model-specific interpretation.

- [HA Magic Home](https://www.home-assistant.io/integrations/flux_led/)
- [HA LED BLE](https://www.home-assistant.io/integrations/led_ble/)
- [LEDnetWF BLE project](https://github.com/8none1/lednetwf_ble)
- [Core issue 124083](https://github.com/home-assistant/core/issues/124083)
- [flux_led models_db.py](https://github.com/lightinglibs/flux_led/blob/master/flux_led/models_db.py) — AK001-ZJxxxx module → chip (ESP8266/S82GESNC/BL602/HF-LPB100), model-code colour modes
- [flux_led scanner.py](https://github.com/lightinglibs/flux_led/blob/master/flux_led/scanner.py) — UDP 48899 HF-A11ASSISTHREAD discovery and reply format
- [HA core zengge stub](https://github.com/home-assistant/core/tree/dev/homeassistant/components/zengge) — legacy integration removed; repair points to LED BLE
- [Surplife](https://www.surplife.net/) — Zengge's OEM platform (controllers, cloud, white-label apps)
- [Magic Home Pro (Google Play)](https://play.google.com/store/apps/details?id=com.zengge.wifi) — app package/publisher
- [ZENGGE app (App Store)](https://apps.apple.com/us/app/zengge/id1568677696) — BLE app, publisher JM Zengge Co., Ltd.
- [Tasmota MagicHome page](https://tasmota.github.io/docs/devices/MagicHome-LED-strip-controller/) — ESP boards LC01–LC06; BL602 cannot be flashed
- [OpenBeken README](https://github.com/openshwprojects/OpenBK7231T_App) — BL602 support, OTA tutorial for Magic Home devices
- [ESPHome feature request #1049](https://github.com/esphome/feature-requests/issues/1049) — BL602 MagicHome support still open
- [hao_deng_cloud (HACS)](https://github.com/Pharylon/hao_deng_cloud) — Hao Deng mesh via cloud, needs Wi-Fi bridge
- [home-assistant-zengge (archived)](https://github.com/SleepyNinja0o/home-assistant-zengge) — Zengge BLE mesh, archived 2026-03-31

## ThermoBeacon and BLE sensors

See [thermobeacon-and-ble-sensors.md](thermobeacon-and-ble-sensors.md) for the model-specific interpretation.

- [HA ThermoBeacon](https://www.home-assistant.io/integrations/thermobeacon/)
- [HA Bluetooth](https://www.home-assistant.io/integrations/bluetooth/)
- [Core issue 139972](https://github.com/home-assistant/core/issues/139972)
- [Airthings BLE](https://www.home-assistant.io/integrations/airthings_ble/)
- [Sensirion BLE](https://www.home-assistant.io/integrations/sensirion_ble/)
- [thermobeacon-ble parser](https://github.com/Bluetooth-Devices/thermobeacon-ble) — UUID 0xFFF0, manufacturer IDs, 20-byte measurement frames
- [Core issue 139917](https://github.com/home-assistant/core/issues/139917) — root issue of the 2025.3.0 ThermoBeacon regression
- [Core PR 139919](https://github.com/home-assistant/core/pull/139919) — thermobeacon-ble 0.8.1 fix, shipped in 2025.3.1
- [pvvx ATC_MiThermometer](https://github.com/pvvx/ATC_MiThermometer) — supported models, four advertising formats, B1.5/B1.6 warning
- [ESPHome atc_mithermometer](https://esphome.io/components/sensor/atc_mithermometer/) — parses ATC1441 format only
- [BTHome](https://bthome.io/) — v2 current, v1 deprecated Nov 2022, Shelly BLU devices
- [HA BTHome](https://www.home-assistant.io/integrations/bthome/) — 32-hex bindkey
- [Shelly BLU H&T](https://kb.shelly.cloud/knowledge-base/shelly-blu-h-t) — AES-CCM, range, battery
- [HA Shelly](https://www.home-assistant.io/integrations/shelly/) — BLU sensors go to BTHome; Gen2+ proxies without GATT
- [HA Govee BLE](https://www.home-assistant.io/integrations/govee_ble/) — model list, active-scan models
- [HA INKBIRD](https://www.home-assistant.io/integrations/inkbird/) — model list, active scans
- [HA SwitchBot](https://www.home-assistant.io/integrations/switchbot/) — Meter family, discovery in passive mode
- [HA Qingping](https://www.home-assistant.io/integrations/qingping/) — CG* model list, passive
- [HA Ruuvi BLE](https://www.home-assistant.io/integrations/ruuvitag_ble/) — RuuviTag/Pro/Air
- [HA SensorPush](https://www.home-assistant.io/integrations/sensorpush/) — app activation required
- [HA BlueMaestro](https://www.home-assistant.io/integrations/bluemaestro/) — Tempo Disc models

## Aqara Xiaomi and LUMI

See [aqara-xiaomi-lumi.md](aqara-xiaomi-lumi.md) for the model-specific interpretation.

- [Legacy gateway](https://www.home-assistant.io/integrations/xiaomi_aqara/)
- [Core Xiaomi Home](https://www.home-assistant.io/integrations/xiaomi_miio/)
- [Vendor Xiaomi Home project](https://github.com/XiaoMi/ha_xiaomi_home)
- [Aqara FP2](https://eu.aqara.com/en-eu/products/aqara-presence-sensor-fp2)
- [Aqara sensors disconnecting](https://community.home-assistant.io/t/aqara-sensors-keep-disconnecting/751436)
- [Z2M LUMI definitions](https://github.com/Koenkk/zigbee-herdsman-converters/blob/master/src/devices/lumi.ts) — SKU ↔ lumi.* IDs, manufacturer code 0x115F, cluster 0xFCC0
- [Z2M WSDCGQ11LM notes](https://www.zigbee2mqtt.io/devices/WSDCGQ11LM.html) — Xiaomi non-compliance, router-incompatibility list
- [Z2M FP1 RTCZCGQ11LM](https://www.zigbee2mqtt.io/devices/RTCZCGQ11LM.html) — fails on channels 21–24, minimum adapter firmware
- [Z2M W100 TH-S04D](https://www.zigbee2mqtt.io/devices/TH-S04D.html) — ships with Thread firmware; switch to Zigbee in Aqara Home
- [ZHA Xiaomi/Aqara quirks](https://github.com/zigpy/zha-device-handlers/tree/dev/zhaquirks/xiaomi/aqara) — which LUMI IDs have ZHA quirks
- [HA ZHA](https://www.home-assistant.io/integrations/zha/) — incompatible router brands, long pairing for Xiaomi/Aqara
- [HA Matter](https://www.home-assistant.io/integrations/matter/) — Aqara Hub M2 named as a Matter bridge; HA is controller only
- [HA HomeKit Device](https://www.home-assistant.io/integrations/homekit_controller/) — one controller per accessory; BLE/Thread pairing
- [HA Xiaomi BLE](https://www.home-assistant.io/integrations/xiaomi_ble/) — MiBeacon key lengths, cloud bindkey, no BLE Mesh, pvvx flasher models
- [Aqara Everything Matter](https://www.aqara.com/en/explore/everything-matter/) — which hubs are Matter bridges vs controllers
- [Aqara advanced Matter bridging (2025-04-09)](https://www.aqara.com/en/news/aqara-enhances-user-experience-with-expanded-matter-device-integration-and-advanced-bridging-capabilities/) — firmware 4.3.4 / app 5.1.4, scenes as virtual devices
- [Aqara Motion and Light Sensor P2 release](https://www.businesswire.com/news/home/20240409809799/en/Aqara-Expands-Thread-Product-Portfolio-with-a-New-Motion-Sensor) — tuning needs an Aqara Thread controller
- [Aqara FP300](https://www.aqara.cn/en/product/presence-multi-sensor-fp300/) — Zigbee/Thread modes, feature split, PS-S04E/PS-S04D

## OSRAM and LEDVANCE

See [osram-ledvance.md](osram-ledvance.md) for the model-specific interpretation.

- [OSRAM announcement](https://ams-osram.com/news/press-releases/pr-09-03-2020)
- [LEDVANCE Zigbee FAQ](https://www.ledvance.com/en-asia/home-lighting/services/faq/faq-for-smart-zigbee-products)
- [Observed future-dated page](https://www.home-assistant.io/integrations/ledvance/) — **future introduction at this baseline; excluded as released support**
- [Z2M issue 26686](https://github.com/Koenkk/zigbee2mqtt/issues/26686)
- [HA blog: LEDVANCE joins Works with HA (2026-10-13)](https://www.home-assistant.io/blog/2026/10/13/ledvance-joins-works-with-home-assistant/) — 116 certified devices, all Matter over Wi-Fi on the `matter` integration; OSRAM brand licensed
- [LEDVANCE SMART+ Matter FAQ](https://www.ledvance.com/en-int/home-lighting/services/faq/faq-for-smart-app_matter-products) — current Matter products are Wi-Fi; reset steps; 5 fabrics; no Matter OTA; Amazon-only variants
- [LEDVANCE add Matter devices](https://www.ledvance.com/en-int/home-lighting/services/faq/faq-for-new-smart-app/add-devices/matter) — no hub for Wi-Fi Matter; app-compatibility badges
- [LEDVANCE SMART+ app](https://www.ledvance.com/en-int/home-lighting/services/control-options/smart-app) — one app for Wi-Fi/Matter and Bluetooth mesh, no Zigbee
- [LEDVANCE smart home catalogue](https://www.ledvance.com/en-int/professional-lighting/products/smart-home-c6248) — protocol split (Wi-Fi, Matter-over-Wi-Fi, Zigbee), named SKUs
- [SUN@HOME product story](https://www.ledvance.com/en-uk/professional-lighting/lighting-insights/product-stories/sun-at-home) — Wi-Fi, LEDVANCE SMART+ WiFi app, SunLike 2200–5000 K
- [HA OSRAM Infrared](https://www.home-assistant.io/integrations/osram_infrared/) — 2026.10, IR emitter required, assumed state, no brightness
- [HA Osramlightify](https://www.home-assistant.io/integrations/osramlightify/) — legacy YAML gateway integration, local polling
- [Z2M ledvance.ts](https://github.com/Koenkk/zigbee-herdsman-converters/blob/master/src/devices/ledvance.ts), [osram.ts](https://github.com/Koenkk/zigbee-herdsman-converters/blob/master/src/devices/osram.ts), [sylvania.ts](https://github.com/Koenkk/zigbee-herdsman-converters/blob/master/src/devices/sylvania.ts) — modelID suffixes (Z3, T, Value), EAN/article codes, energy-meter plug, US line
- [ZHA quirks osram](https://github.com/zigpy/zha-device-handlers/tree/dev/zhaquirks/osram) — manufacturer strings `OSRAM` / `LEDVANCE`
- [tuya-local](https://github.com/make-all/tuya-local) — LEDVANCE Planon, camera and ceiling-fan Tuya DP configs
- Report: [HA forum: LEDVANCE Wi-Fi is Tuya-based](https://community.home-assistant.io/t/local-integration-to-ledvance-smart-wifi/406475)

## Govee

See [govee.md](govee.md) for the model-specific interpretation.

- [HA Govee lights local](https://www.home-assistant.io/integrations/govee_light_local/)
- [Manufacturer LAN guide](https://app-h5.govee.com/user-manual/wlan-guide)
- [HA Govee Bluetooth](https://www.home-assistant.io/integrations/govee_ble/)
- [govee2mqtt SKU notes](https://github.com/wez/govee2mqtt/blob/main/docs/SKUS.md)
- [Core issue 140100](https://github.com/home-assistant/core/issues/140100)
- [Govee developer API: Get your devices](https://developer.govee.com/reference/get-you-devices) — OpenAPI base URL, Govee-API-Key header, device types, capability model, rate limits
- [Govee Matter FAQ](https://us.govee.com/pages/matter-faq) — Matter over Wi-Fi only, IPv6 and 15-min commissioning, feature subset, network change disables Matter, older products not upgradable
- [CSA: Govee Ceiling Light Pro](https://csa-iot.org/csa_product/govee-ceiling-light-pro/) — Matter 1.3 certificate, Wi-Fi+BLE, Product ID 0x60A6
- [Govee TV lights comparison](https://us.govee.com/blogs/tv-lighting/govee-tv-lights-review-comparison) — AI Sync Box 2 = H6604
- [govee2mqtt README](https://github.com/wez/govee2mqtt) — LAN, AWS IoT (account login, undocumented) and Platform API (key); add-on/Docker
- [goveelife (HACS)](https://github.com/disforw/goveelife) — OpenAPI v2 cloud polling, appliances and RGBIC segments
- [hacs-govee (LaggAt)](https://github.com/LaggAt/hacs-govee) — author discontinued development
- [govee_ble_lights (HACS)](https://github.com/Beshelmek/govee_ble_lights) — BLE light control, per-model protocols
- [rtl_433 Govee decoder](https://github.com/merbanan/rtl_433/blob/master/src/devices/govee.c) — H5054 leak / B5023 contact over 433 MHz; README lists H5059, H5310, H5112 decoders

## Paulmann

See [paulmann.md](paulmann.md) for the model-specific interpretation.

- [Paulmann compatibility and support](https://de.paulmann.com/smart-home/kompatibilitaet/)
- [Paulmann 929.66](https://www.zigbee2mqtt.io/devices/929.66.html)
- [Z2M issue 26186](https://github.com/Koenkk/zigbee2mqtt/issues/26186)
- [Paulmann Bluetooth FAQ](https://de.paulmann.com/smart-home/produkte/bluetooth/faqs-bluetooth/) — Bluetooth line closed, Paulmann app only, no smart speakers
- [Plug & Shine smart control](https://de.paulmann.com/aussenleuchten/plug-shine-gartenbeleuchtungssystem/smarte-steuerung/) — 24 V system, Zigbee controller, Smart Plug Outdoor, Hue/Echo compatibility
- [URail smart home](https://de.paulmann.com/innenleuchten/schienensysteme/urail-230v-schienensystem/smart-home/) — Zigbee feed-ins, spot and section adapters, "bereit für Philips Hue"
- [URail adapter 95524](https://de.paulmann.com/p/urail-schienenadapter-smart-home-zigbee-3.0-on-off-dimm-166x50mm-schwarz-matt/95524) — 50 W max, continuously dimmable lamps only, compatible systems list
- [Z2M Paulmann converters](https://github.com/Koenkk/zigbee-herdsman-converters/blob/master/src/devices/paulmann.ts) — model IDs, manufacturer strings, softwareBuildID splits, 501.39 = TS000F
- [Z2M Paulmann 501.39](https://www.zigbee2mqtt.io/devices/501.39.html) — universal switch device page
- [ZHA Paulmann quirk](https://github.com/zigpy/zha-device-handlers/tree/dev/zhaquirks/paulmann) — 501.34 four-button remote; manufacturer strings

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
