# Aqara, Xiaomi and LUMI identities

## Separate ecosystems and generations

`LUMI` / `lumi.*` can be protocol identities, not a sufficient retail product classification. Xiaomi, Aqara and older Mi ecosystems overlap historically but do not expose one universal API.

| Product family | Candidate route | Critical boundary |
| --- | --- | --- |
| Aqara/Mijia Zigbee contacts, motion, temperature, vibration, buttons/cubes | Direct ZHA/Z2M by exact signature; or compatible vendor hub | Legacy and newer devices differ; check endpoint events and router behavior |
| Zigbee relays, wall switches, plugs, curtains and thermostats | Exact device definition or bridge | Neutral/no-neutral, router/end-device, calibration and vendor-only features |
| Aqara Matter-over-Thread sensors/devices | HA Matter + Thread border router | Not interchangeable with Zigbee models or HomeKit-over-Thread |
| Aqara FP2 Wi-Fi presence | HomeKit Device path, with vendor setup where required | Zones and setup need exact model/firmware handling |
| Aqara hubs/camera hubs | Supported HomeKit/Matter bridging or documented API | Bridging exposes only supported child capabilities, not the whole vendor app |
| Xiaomi Wi-Fi appliances/robots | Core `xiaomi_miio` or vendor `XiaoMi/ha_xiaomi_home` as appropriate | These are different integration implementations, accounts and local/cloud paths |
| Older Xiaomi gateway LAN protocol | Legacy `xiaomi_aqara` only for its actual supported hardware | Do not apply old gateway-key tutorials to modern Aqara hubs |

The legacy gateway integration documents particular older hubs, whereas core `xiaomi_miio` has a detailed model list. The vendor-maintained Xiaomi Home project has separate MIoT/account behavior; its documented full local mode depends on suitable central-gateway hardware/firmware and region, while generic LAN-control support is narrower. [Legacy gateway](https://www.home-assistant.io/integrations/xiaomi_aqara/), [Core Xiaomi Home](https://www.home-assistant.io/integrations/xiaomi_miio/), [Vendor Xiaomi Home project](https://github.com/XiaoMi/ha_xiaomi_home).

## Inspect an existing LUMI device

Export the device signature. Record whether it is a battery sensor, mains device or hub, the precise `lumi.*` identifier, selected quirk/converter and firmware. Look up the exact model's button events, reporting and documented quirks. Do not assume that every mains-powered wall switch routes Zigbee or that every Aqara sensor has identical parent behavior.

If it disconnects, distinguish loss of radio delivery from a stale availability threshold. Inspect coordinator placement, parent/router availability and power cuts to routing lamps. Test a known stable path with one sensor. Avoid advising a blanket coordinator migration from a single anecdote. Preserve the existing network backup before any re-pairing.

## Presence and zones

Aqara's FP2 product documentation describes direct Home Assistant use through HomeKit Controller/Device. Identify this Wi-Fi product separately from similarly named Zigbee or Thread presence sensors. Test each required zone, clear delay, stationary occupancy and reset after a room layout change. Map zones as capabilities, not as guaranteed people counting. [Aqara FP2](https://eu.aqara.com/en-eu/products/aqara-presence-sensor-fp2).

## Field evidence

A community thread started **2024-07-19** reports Aqara sensors repeatedly dropping from a Zigbee network and includes different participants' router/placement explanations. It does not establish a universal incompatible-router list. Use it to form a testable parent/radio hypothesis, then compare the actual installed models. [Aqara sensors disconnecting](https://community.home-assistant.io/t/aqara-sensors-keep-disconnecting/751436).

## Migration and account cautions

Keep region and account binding stable while diagnosing. A device visible in one vendor region may not be returned by another server. Back up maps/calibration/zones where the vendor permits. Removing a HomeKit pairing, changing Zigbee coordinator or resetting a hub can break existing household control and must have an explicit rollback.

For a new purchase, compare the actual HA entities required against its specific route. A Matter logo can simplify integration but does not guarantee vendor gesture, scene, energy or camera features. Local sensing, cloud provisioning and cloud analytics are separate dependencies; record each.
