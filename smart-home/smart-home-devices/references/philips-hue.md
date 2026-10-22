# Philips Hue / Signify

## Product families and integration routes

| Family | Candidate path | Check before choosing |
| --- | --- | --- |
| White, White Ambiance, White and Color Ambiance bulbs; spots, strips, indoor/outdoor luminaires | Native Hue bridge integration; direct Zigbee for an exact supported model | Color modes, dimming range, power-on behavior, effects and OTA route |
| Hue dimmers, buttons, wall switch modules and motion sensors | Existing bridge via Hue; or direct Zigbee | Every press/release/hold event; sensor temperature/lux; battery reporting |
| Rooms, zones and scenes | Native Hue | Logical groups are not extra physical devices; avoid individual-command fan-out |
| Bluetooth-capable lamps | Hue BLE for supported models; bridge or Zigbee alternatives | Exact model and Bluetooth pairing mode |
| New bridge generations, motion-sensing features, cameras and entertainment products | Verify each feature separately | Do not inherit support from older square bridges or from basic lamp control |

HA's Hue integration handles bridge-connected lights and sensors, exposes remotes as automation triggers, and offers grouped-light entities for rooms/zones that may be disabled initially. Bridge generations have different update behavior. Read the current documentation before relying on new bridge features. [HA Hue](https://www.home-assistant.io/integrations/hue/).

Hue BLE is a separate integration for Bluetooth lamps; the documented voice-assistant discoverability flow can allow HA pairing while retaining the app. It does not turn a BLE lamp into a Zigbee router or recreate bridge scenes. [HA Hue BLE](https://www.home-assistant.io/integrations/hue_ble/).

## Preferred assessment for an existing mixed Hue installation

For a mixed list of lamps, remotes, sensors and rooms, first count physical devices separately from logical groups. Retain the bridge when existing scenes, updates, remotes and household use already work. Compare direct Zigbee only against a concrete need: bridge removal, additional vendor mix, or capabilities the native integration does not expose. Check the actual direct Zigbee device definition before moving anything.

For each room, identify the authoritative scene owner. If Hue scenes, HA Adaptive Lighting, wall-switch behavior and presence automations all adjust the same lamps, define priority and a manual-override period. A failed transition can originate from competing commands, power being cut at the wall, a bridge connection issue, or the lamp's radio path; these are distinct faults.

Use grouped controls where suitable and test whether the group state represents “any on” or the behavior required by the automation. Do not use a group aggregate as proof that every lamp reached the command.

## API and diagnostic workflow

Use the manufacturer's developer documentation to distinguish legacy v1 resources from v2 CLIP resources and the event stream. Discover and authorize against the real bridge; avoid embedding application keys in logs or shell history. Prefer the HA integration for ordinary operation rather than adding a second poller. For a read-only API investigation, record bridge software and API generation, inspect resource types, then compare one lamp's resource with its HA entity. [Hue developer onboarding](https://developers.meethue.com/develop/get-started-2/).

Diagnose in layers: physical power and vendor app → bridge reachability → HA integration log/update stream → entity → automation trace. Compare “unavailable” with “off”; an automation must not interpret temporary unavailability as a request to toggle.

## Firsthand evidence and test implications

A 2025-10-09 report using HA 2025.10.1 and a Hue Bridge Pro described temporary unavailability and lights switching; moving the bridge's network connection did not establish a solution. The issue later closed as stale/not planned. Treat it as a reason to correlate device history, power behavior and logs, not evidence that Hue bridges generally fail. [Core issue 154049](https://github.com/home-assistant/core/issues/154049).

Acceptance: each remote event, motion/lux/temperature, a room scene, power restoration, HA restart, bridge restart, and manual override. Record any vendor-specific feature lost under Matter or direct Zigbee before changing the route.
