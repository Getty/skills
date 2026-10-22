# Aqara, Xiaomi and LUMI identities

LUMI United Technology builds Aqara and many Xiaomi Mijia devices. `lumi.*` appears as a Zigbee model ID, a MIoT model string and a gateway ID, so the prefix alone does not tell you the retail product or the transport. Xiaomi, Aqara and older Mi ecosystems overlap, but they do not share one API. LUMI Zigbee devices use manufacturer code `0x115F` and the manufacturer-specific cluster `0xFCC0` (`manuSpecificLumi` in Z2M) for settings and extra reports. [Z2M LUMI definitions](https://github.com/Koenkk/zigbee-herdsman-converters/blob/master/src/devices/lumi.ts).

## Product range

Model codes and IDs below come from Z2M definitions (checked 2026-10) unless another source is linked. Before relying on one, check the exact definition page.

| Line / family | Device classes (examples: model → Zigbee ID) | Radio | HA route | Key caveat |
| --- | --- | --- | --- | --- |
| Xiaomi Mijia/Mi Zigbee (legacy) | T/H `WSDCGQ01LM` → `lumi.sensor_ht`; motion `RTCGQ01LM` → `lumi.sensor_motion`; contact `MCCGQ01LM` → `lumi.sensor_magnet`; button `WXKG01LM`; plug `ZNCZ02LM` → `lumi.plug`; light `GZCGQ01LM` | Zigbee, not fully standard | ZHA with Xiaomi quirk, or Z2M; legacy gateway | Router-incompatibility list below; pairing can take many attempts |
| Aqara first-generation sensors | T/H/pressure `WSDCGQ11LM` → `lumi.weather`; motion `RTCGQ11LM` → `lumi.sensor_motion.aq2`; contact `MCCGQ11LM`; leak `SJCGQ11LM`; vibration `DJT11LM`; cube `MFKZQ01LM`; mini switch `WXKG11LM` | Zigbee, same LUMI behaviour | ZHA quirk or Z2M | `RTCGQ11LM` ignores motion for 60 s after a trigger, so keep the occupancy timeout at 60 s or more |
| Aqara T1 / E1 / P1 / P100 sensors | T1: `WSDCGQ12LM`, `RTCGQ12LM`, `MCCGQ12LM`, `DJT12LM`, `SJCGQ12LM`, `GZCGQ11LM`; E1: `RTCGQ15LM`, `MCCGQ14LM`, `SJCGQ13LM`; P1: `RTCGQ14LM` → `lumi.motion.ac02`, `MCCGQ13LM`; `RTCGQ13LM` high precision; `DWZTCGQ11LM` P100; cube `CTP-R01` | Zigbee (check the spec sheet for the Zigbee version) | Z2M; ZHA only where a quirk matches the exact ID | Sensitivity, intervals and modes travel over `0xFCC0`, so a generic Zigbee route loses them |
| Aqara mmWave presence (Zigbee) | FP1 `RTCZCGQ11LM` → `lumi.motion.ac01`; FP1E → `lumi.sensor_occupy.agl1`; FP300 `PS-S04D`/`PS-S04E` → `lumi.sensor_occupy.agl8`; FP310 → `lumi.sensor_occupy.acn1` | Zigbee; FP300 is Zigbee or Thread | Z2M; ZHA quirk if one exists | FP1 does not work on Zigbee channels 21–24 and needs a minimum adapter firmware ([Z2M FP1](https://www.zigbee2mqtt.io/devices/RTCZCGQ11LM.html)) |
| Buttons, wall switches, relays, plugs | Remotes `WXKG…`; CN wall switches `QBKG…`; H1 EU `WS-EUK01`–`04`; US `WS-USC01`–`04`; H2 EU `WS-K07E`/`WS-K08D`; T1 modules `SSM-U01`/`SSM-U02`; relays `LLKZMK11LM`, T2 `LLKZMK12LM`; plugs `SP-EUC01`, `ZNCZ12LM` | Zigbee | Z2M or ZHA quirk | Neutral or no-neutral, decoupled mode and multi-click events differ by model. Check whether the device routes; do not infer it from mains power |
| Climate | TRV E1 `SRTS-A01` → `lumi.airrtc.agl001`; W600 TRV `WT-A03E`; W500 floor `UT-A01E`; Climate Sensor W100 `TH-S04D` → `lumi.sensor_ht.agl001` | Zigbee; W100 ships with Thread firmware | Z2M; ZHA quirk `thermostat_agl001` for E1 | W100 must be switched to Zigbee in Aqara Home before Z2M pairing ([Z2M W100](https://www.zigbee2mqtt.io/devices/TH-S04D.html)) |
| Covers | Curtain `ZNCLDJ11LM` → `lumi.curtain`; B1 `ZNCLDJ12LM`; C2 `ZNCLDJ14LM`; C3 `ZNCLDJ01LM`; roller T1C `ZNGZDJ16LM`; roller shade driver E1 `ZNJLBL01LM`; curtain driver E1 `ZNCLBL01LM` | Zigbee | Z2M or ZHA quirk | Set calibration and travel limits before automating; confirm the power source (battery or mains) |
| Zigbee locks | `ZNMS11LM`, S2 `ZNMS12LM`, S2 Pro `ZNMS13LM`, Vima `A6121` (Xiaomi) | Zigbee | Z2M definition; verify control and not just state | Mostly CN models; user codes and remote unlock may stay in the vendor app |
| Aqara native Thread / Matter | Door and Window Sensor P2; Motion and Light Sensor P2 `ML-S03D`/`ML-S03E`; Smart Lock U200 `EL-D02D`/`EL-D02E` (Thread, BLE 5.1, NFC); W100 and FP300 in Thread mode | Thread | HA Matter + Thread border router | Not the Zigbee P1 models. Tuning P2 sensitivity and timeout needs an Aqara Thread controller such as M3. The hubs E1, M1S, M2, G2H and G3 cannot add P2 ([press release](https://www.businesswire.com/news/home/20240409809799/en/Aqara-Expands-Thread-Product-Portfolio-with-a-New-Motion-Sensor)) |
| Aqara hubs | Matter bridges: M2, M1S/M1S Gen 2, E1, Camera Hub G3. Matter controllers and bridges: M3 (`HM-G01D`/`HM-G01E`), M100, Camera Hub G5 Pro, Doorbell Camera Hub G410 | Zigbee + Wi-Fi/LAN; M3 also 802.15.4 Thread | HA Matter (bridge) | Only supported Aqara children, mapped to Matter types, are exposed. Advanced bridging needs firmware 4.3.4 and app 5.1.4 or newer; it exposes scenes as virtual plugs or occupancy sensors ([Aqara Matter](https://www.aqara.com/en/explore/everything-matter/), [2025 bridging](https://www.aqara.com/en/news/aqara-enhances-user-experience-with-expanded-matter-device-integration-and-advanced-bridging-capabilities/)) |
| FP2 Wi-Fi presence | Presence Sensor FP2; up to 30 zones; wired USB-C | 2.4 GHz Wi-Fi + BLE | HomeKit Controller | No Matter listed; fall detection needs ceiling mounting ([Aqara FP2](https://eu.aqara.com/en-eu/products/aqara-presence-sensor-fp2)) |
| Xiaomi Zigbee gateways | `lumi.gateway.v3` (`DGNWG02LM`), `lumi.gateway.mieu01` (`ZHWG11LM-763`, `DGNWQ05LM`), `lumi.gateway.aqhm01` (`ZHWG11LM`), `lumi.gateway.mgl03` (`ZNDMWG03LM`) | Zigbee + Wi-Fi | Core `xiaomi_miio`; legacy `xiaomi_aqara` only for v2/v3 LAN protocol | `mieu01` needs cloud credentials to list children; many child types create no entities. `xiaomi_aqara` rejects `aqhm01` ([core `xiaomi_miio`](https://www.home-assistant.io/integrations/xiaomi_miio/), [legacy gateway](https://www.home-assistant.io/integrations/xiaomi_aqara/)) |
| Xiaomi Wi-Fi MIoT appliances | Purifiers, fans, humidifiers, plugs, vacuums: `zhimi.*`, `dmaker.fan.*`, `chuangmi.plug.*`, `deerma.humidifier.*` | Wi-Fi miIO/MIoT | Core `xiaomi_miio` (cloud login fetches token, then local); vendor `xiaomi_home` (HACS) | Both are titled "Xiaomi Home", so tell them apart by domain. Vendor integration uses the cloud by default; its local mode needs a Central Hub Gateway, sold only in mainland China |
| Xiaomi BLE (MiBeacon) | `LYWSD03MMC`, `MHO-C401`, `LYWSDCGQ`, `MJWSD05MMC`, `CGG1`, `CGDK2`, Flower Care `HHCCJCY01`, Yeelight remotes | BLE advertisements | Core [`xiaomi_ble`](https://www.home-assistant.io/integrations/xiaomi_ble/) (bindkey for v4/v5) | No BLE Mesh support; vendor `xiaomi_home` skips Bluetooth devices. See [thermobeacon-and-ble-sensors.md](thermobeacon-and-ble-sensors.md) |

Router compatibility: ZHA documents that Xiaomi/Aqara devices are known not to work with routers from Centralite, GE, Iris, Ledvance/OSRAM, LIGHTIFY/Sylvania, Orvibo, PEQ, Securifi and SmartThings/Samsung. Z2M device notes give a similar list and add Legrand. Treat these lists as a hypothesis to test; they are not proof for a given firmware. [HA ZHA](https://www.home-assistant.io/integrations/zha/), [Z2M WSDCGQ11LM notes](https://www.zigbee2mqtt.io/devices/WSDCGQ11LM.html).

## Identify from label or model ID

- **LUMI SKU prefixes** (consistent across Z2M definitions):
  - `WSDCGQ` temperature/humidity
  - `RTCGQ` motion; `RTCZCGQ` presence
  - `MCCGQ` contact
  - `SJCGQ` leak
  - `DJT` vibration
  - `MFKZQ` cube
  - `WXKG` wireless switch; `QBKG` wall switch
  - `ZNCZ` plug; `QBCZ` wall outlet
  - `ZNCLDJ`, `ZNGZDJ`, `ZNJLBL`, `ZNCLBL` covers
  - `LLKZMK` relay
  - `ZNMS` lock
  - `GZCGQ` light

  `…01LM`/`…02LM` are usually Xiaomi-branded; `…11LM` and up are Aqara.
- **Newer global SKUs** use `XX-YNN` codes with a `D`/`E` suffix, for example `TH-S04D`, `ML-S03D`/`E`, `EL-D02D`/`E`, `SRTS-A01`, `SSM-U01`. For FP300, Aqara lists `PS-S04E` as the online version and `PS-S04D` as the retail version with a mounting kit ([Aqara FP300](https://www.aqara.cn/en/product/presence-multi-sensor-fp300/)).
- **Zigbee IDs**: suffixes `aq1`/`aq2` mark early Aqara devices. `acn…` IDs are typically China-market. `agl`, `aeu` and `aus` appear on global, EU and US variants. These are observed patterns, not rules, so match the full ID.
- **MIoT strings** (`vendor.type.version`, for example `zhimi.*`, `lumi.gateway.mgl03`) name Wi-Fi or gateway devices for `xiaomi_miio`/`xiaomi_home`. They are not Zigbee signatures. MiBeacon BLE devices carry a numeric product ID, for example `0x055B` = `LYWSD03MMC` in the `xiaomi-ble` parser.
- **Multi-protocol devices** (W100, FP300) change route with their mode. Aqara documents that FP300 Zigbee mode needs an Aqara hub and keeps most settings, while Thread mode needs a Matter controller and loses some tuning. Record the mode before you compare evidence.

## Choose the route

- Z2M usually adds new LUMI models first; W100, W600 and FP300 definitions exist there. For ZHA, find the exact model ID among the `zhaquirks/xiaomi/aqara` quirks before promising features ([quirks](https://github.com/zigpy/zha-device-handlers/tree/dev/zhaquirks/xiaomi/aqara)).
- A Matter bridge keeps the Aqara app, automations and hub-only features, at the cost of a reduced capability set. Direct Zigbee gives raw `0xFCC0` settings but drops the vendor app. HA's Matter docs cite Aqara Hub M2 as a bridge example ([HA Matter](https://www.home-assistant.io/integrations/matter/)).
- HomeKit accessories pair with only one controller at a time. Removing an Apple Home pairing to add a device to HA breaks the existing control ([HA HomeKit Device](https://www.home-assistant.io/integrations/homekit_controller/)).
- Region: Xiaomi cloud data is isolated per server region (China, Europe, India, Russia, Singapore, USA). Pick the region the device is bound to ([vendor Xiaomi Home](https://github.com/XiaoMi/ha_xiaomi_home)). Reports describe China-market Aqara hubs that cannot join non-China servers; verify for each model before buying imports.
- For video from G-series cameras, use `smart-home-video-media`.

## Worked examples

**Inspect an existing LUMI device.**
1. Export the device signature.
2. Record whether it is a battery sensor, a mains device or a hub, plus the precise `lumi.*` ID, the selected quirk or converter, and the firmware.
3. Look up that exact model's button events, reporting and documented quirks.
4. Do not assume every mains-powered wall switch routes Zigbee, or that every Aqara sensor behaves the same with its parent router.

**Diagnose a disconnect.**
1. Separate a loss of radio delivery from a stale availability threshold.
2. Inspect coordinator placement, parent/router availability and power cuts to routing lamps.
3. Test a known stable path with one sensor.
4. Do not advise a blanket coordinator migration based on one anecdote, and preserve the network backup before any re-pairing.

A community thread started **2024-07-19** reports Aqara sensors repeatedly dropping off a Zigbee network, with participants offering different router and placement explanations. It does not establish a universal list of incompatible routers. Use it to form a testable parent/radio hypothesis, then compare the actual installed models. [Aqara sensors disconnecting](https://community.home-assistant.io/t/aqara-sensors-keep-disconnecting/751436).

**FP2 zones.** Aqara documents adding FP2 directly to HA through HomeKit Controller. Keep this Wi-Fi product separate from the similarly named Zigbee or Thread presence sensors. Test each required zone, the clear delay, stationary occupancy, and the reset after a room layout change. Map zones as capabilities, not as guaranteed people counting.

**Migration and account cautions.** Keep the region and account binding stable while diagnosing. A device visible in one vendor region may not be returned by another server. Back up maps, calibration and zones where the vendor permits. Removing a HomeKit pairing, changing the Zigbee coordinator or resetting a hub can break existing household control, so each needs an explicit rollback. For a purchase, compare the HA entities you need against that specific route. A Matter logo does not guarantee gesture, scene, energy or camera features. Local sensing, cloud provisioning and cloud analytics are separate dependencies; record each one.
