# Zengge, Magic Home, Surplife, LEDnet/LEDnetWF and RGB controllers

Zengge (JM Zengge Co., Ltd., publisher of the Magic Home Pro, Surplife and ZENGGE apps; zengge.com now serves **Surplife**, an OEM platform offering controllers, cloud and white-label apps to brand partners) is an OEM ecosystem, not one product line. HA's Magic Home page lists 50+ retail brands on this hardware (Magic Home, Magic Hue, Flux LED, LEDENET, Arilux, SurpLife, Zengge, Daybetter and more). The app name, brand and logo do not determine the protocol. Research baseline 2026-10-22.

## Product range

| Line / family | Device classes | Radio / protocol | HA route(s) | Key caveat |
| --- | --- | --- | --- | --- |
| Magic Home Pro / Surplife Wi-Fi lighting | strip controllers (RGB, RGBW, RGBCW, CCT, dim), bulbs, downlights, ceiling and floor lamps, Christmas lights | Wi-Fi, local TCP 5577 + vendor cloud | core Magic Home (`flux_led`) | Match the model code against HA's tested/unsupported table |
| Addressable (SPI) Wi-Fi controllers | WS2811/WS2812B/SK6812/WS2815/APA102/UCS… pixel strips | Wi-Fi | `flux_led` (Addressable v1–v7) | Zones only on Addressable v3; music mode only on mic models |
| Magic Home switches and sockets | 1-channel switch, socket | Wi-Fi | `flux_led` for 0x93/0x97 | 0x19, 0x94–0x96 confirmed unsupported |
| Other Magic Home appliances | plant grow light, aroma lamp, fill light, digital time lamp | Wi-Fi | none in core | 0x18, 0x1B, 0x1D, 0xD1 confirmed unsupported |
| Classic BLE controllers (some Zengge, Magic Blue, Triones, LEDBlue, Happy Lighting…) | strip controllers, bulbs | BLE GATT | core LED BLE (`led_ble`) | Supports LEDnet, BLE-LED, LEDBLE, Triones, LEDBlue, Dream, QHM, AP names — **except LEDnetWF** |
| LEDnetWF / IOTBT BLE controllers (ZENGGE app) | strip and pixel controllers, ring/corner lamps | BLE (Telink or "segment" protocol) | HACS `lednetwf_ble` (v2.0.0, Jan 2026) | WIP project; wrong LED count/type/colour order breaks effects |
| Hao Deng BLE mesh | bulbs, downlights, flood lights | BLE mesh, optional Wi-Fi bridge + cloud | HACS `hao_deng_cloud` (cloud, needs bridge); `home-assistant-zengge` (BLE, archived 2026-03-31) | A BLE proxy does not translate the mesh; no core route |
| Reflashed controller | any of the above with a supported chip | ESPHome/Tasmota/OpenBeken/WLED | ESPHome, MQTT, WLED | Only after confirming chip and board; stock firmware is lost |

Legacy core `zengge` (`platform: zengge`, bluepy) is removed: the stub only raises an "integration removed" repair pointing to LED BLE, and its doc URL redirects there. Treat old tutorials as a migration clue.

## Identify the line from the label or model ID

- **Wi-Fi discovery**: `flux_led` broadcasts `HF-A11ASSISTHREAD` to UDP 48899; replies read `ip,MAC,AK001-ZJxxxx`. The `AK001-ZJ…` string is the Wi-Fi module, not the light type.
- Module → chip (flux_led hardware table): `AK001-ZJ100`, `-ZJ200`, `-ZJ210`, `-ZJ2101`, `-ZJ2104` = ESP8266/ESP8285; `-ZJ2131`, `-ZJ2134` = S82GESNC; `-ZJ2145` through `-ZJ21412` = BL602 (also BLE); `HF-A11` = HF-LPB100 legacy box controllers.
- **Device type** is the one-byte model code HA shows in diagnostics: e.g. 0x06 RGBW, 0x07 RGBCW, 0x25 multi-mode RGB/W/WW/CW/DIM, 0x33 RGB, 0x35/0x44/0x52/0x21 bulbs, 0x1E/0xE1 ceiling, 0xA1–0xA7 addressable. Mic models: 0x08, 0xA2, 0xA3, 0xA6, 0xA7.
- **BLE**: the advertised name decides the route: `LEDnetWF…`/`IOTB…` → `lednetwf_ble`; `LEDnet`, `BLE-LED`, `LEDBLE`, `Triones`, `LEDBlue`, `Dream`, `QHM`, `AP` → `led_ble`.
- **App** is a hint only: Magic Home Pro (`com.zengge.wifi`) and Surplife (`com.zennge.magichome2`) = Wi-Fi/BLE products; ZENGGE (`com.zengge.blev2`) = BLE; Hao Deng = mesh. HA: "likely works" with `flux_led` if it runs in Magic Home or Surp Life.
- Tasmota labels the classic ESP boards LC01–LC06 (RGB, RGBW, ±IR, screw headers).

## Reflash options

| Chip | Option | Status |
| --- | --- | --- |
| ESP8266/ESP8285 (older ZJ modules) | Tasmota, ESPHome, WLED | Tasmota documents MagicHome LC01–LC06 boards |
| BL602 (ZJ2145+ modules) | OpenBeken (BL602 OTA tutorial "Magic Home devices only") | Tasmota: "cannot be flashed"; ESPHome BL602 request #1049 still open; LibreTiny covers BK72xx/RTL87xx, not BL602 |
| S82GESNC, HF-LPB100 | none verified | keep stock firmware |

Do not flash a working controller only to test; route firmware/MQTT design to `smart-home-esphome-mqtt`.

## Map light capabilities correctly

Record whether the strip is RGB, RGBW, RGB+CCT, tunable white, single-channel or addressable. Voltage, current, pin order, channel order and constant-voltage vs constant-current are separate from HA compatibility; a wrong channel mode gives wrong colours and can be an electrical fault. A 0x25 controller serves RGB, RGBW, RGBWW, CW or DIM strips; its configured mode must match the strip before colour tests mean anything.

Test on/off, dimming, R/G/B, warm/cool white, effects and restoration after power loss. Check whether an effect overrides colour commands. For addressable strips record pixel count/order; one aggregate HA light does not prove per-segment control. HA notes strips that drop off Wi-Fi during effects may need a higher-amperage supply.

## Worked example: BLE controller that pairs but will not control

First establish the hardware works in the vendor app, then close the app (BLE contention). Check proxy range and active-connection support; seeing advertisements does not prove a GATT session. If the name is LEDnetWF, `led_ble` is the wrong route. In `lednetwf_ble`, misdetected Telink vs segment protocol shows as on/off working but colour/effects failing — override in the device's Configure dialog. Keep the 120 s disconnect delay default; 0 holds the link open permanently.

A historical core issue reported the legacy `zengge` platform failing with a `bluepy` dependency on HAOS 2024.8.2, closed stale/not planned. [Core issue 124083](https://github.com/home-assistant/core/issues/124083). Do not install Python packages into HAOS to revive it.

## Changes and alternatives

Before a custom-integration upgrade, back up config and note entity IDs; `lednetwf_ble` may need delete-and-re-add after upgrades, so map entity impact first. If the stock protocol cannot give the required reliability or effects, compare a documented compatible controller (or WLED on supported hardware) rather than repeated software guesses. A replacement must keep manual control, power-supply compatibility and restore behaviour.
