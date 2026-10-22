# Reolink cameras, NVRs, doorbells and chimes

## Inventory the topology

For each NVR, record hardware code, firmware, channels, directly attached versus LAN cameras, current recording configuration and HA connection. Record the doorbell's exact variant separately. Treat a number of chimes as an inventory claim, not proof that they all pair with one compatible doorbell.

The official [NVR hardware guide](https://support.reolink.com/articles/900000602543-Comprehensive-Guide-to-Reolink-NVR-Hardware-Versions/) distinguishes multiple revisions with different camera/feature support. Firmware files are not interchangeable merely because the enclosure says RLN8-410. Resolve model and hardware in the [download center](https://reolink.com/download-center/) before planning an update.

## Route product families

| Family | Integration approach to investigate | Explicit unknowns |
|---|---|---|
| Wired PoE / Wi-Fi cameras | Native Reolink directly or via supported NVR | Local API availability, exact model, event/control capabilities |
| Kit cameras and entry models | May require NVR/Home Hub rather than direct native integration | Exact API limitation and channel exposure |
| Battery/solar camera families | Model/firmware-specific direct or hub/NVR path | Sleep/wake, continuous stream limitations, wake-induced battery use |
| Doorbell PoE / Wi-Fi | Native Reolink; direct versus NVR mapping | Visitor events, talkback path, chime revision |
| Battery doorbells, including later generations | Exact generation's current support table | Required hub, compatible chime family and firmware |
| RLN8/RLN16/RLN36/NVS and Wi-Fi NVRs | Add the NVR, then inspect channels | Hardware version, firmware, camera compatibility and storage |
| Home Hub family | Native hub integration where supported | Exact device/firmware support and differences from an NVR |

Use the native [HA Reolink documentation](https://www.home-assistant.io/integrations/reolink/) for supported/tested lists. It requires an administrative device account for full operation. Current support includes more than video: available entities depend on device capabilities. Do not enable every diagnostic/configuration entity by default.

## Identify chime generation before designing quiet hours

Reolink's [PoE/Wi-Fi pairing guide](https://support.reolink.com/articles/32888306699673-How-to-Pair-Reolink-Doorbell-with-Chime-Doorbell-PoE-WiFi/) and [doorbell FAQ](https://support.reolink.com/articles/29213749981209-Reolink-Video-Doorbell-Cameras-FAQ/) describe different V1 and V2/V3 pairings and counts. New battery generations can use a different compatibility matrix. Do not extend a PoE/Wi-Fi table to every battery product.

On supported devices, inspect separate chime controls and test a ringtone. **Deleting a chime device through the Reolink integration also unpairs it from the doorbell**, so use reversible volume/notification settings for quiet hours rather than deletion. Preserve physical ringing if HA is unavailable.

## Diagnose each function independently

Test local login, live view, physical button, visitor/motion/person events, one supported setting, recording playback and chime. For an NVR-mediated camera, compare its channel identity and firmware with the direct camera path if available. Prevent duplicate notification automations while doing this comparison.

For connection failures, inspect enabled services using [Reolink port settings](https://support.reolink.com/articles/900000621783-How-to-Configure-Reolink-Ports-Settings/). Use the configured service ports and exact model; do not enable internet port forwarding as a substitute for LAN reachability.

Reolink ONVIF push events require a locally reachable HTTP callback, whereas the user-facing HA URL can use HTTPS through an appropriate deployment. Verify the callback direction separately from working video. Avoid exposing that local callback publicly. Route detailed networking/stream analysis to `streams-and-events.md`.

## Update without losing the baseline

Export configuration, note paired chimes, capture HA diagnostics and select a maintenance window. Match both NVR and camera firmware. Validate recording, event delivery and physical chime after any update. Use one device first; retain the old configuration and documented recovery route. Do not promise a firmware downgrade unless the vendor supports it.
