# OSRAM, LIGHTIFY and LEDVANCE SMART+

## Identify the protocol and product generation

Treat OSRAM/LIGHTIFY and LEDVANCE SMART+ as product histories with multiple transports. The same lighting brand can appear on Zigbee, Wi-Fi, Bluetooth, HomeKit or Matter packaging.

| Family | Candidate path | Verify |
| --- | --- | --- |
| Older LIGHTIFY / SMART+ Zigbee bulbs, plugs and luminaires | Direct ZHA/Z2M or an already compatible bridge | Exact Zigbee model, firmware, dimming/color behavior and reset instructions |
| SMART+ Wi-Fi products | Actual vendor/app/API or confirmed local integration | Do not assume all are ordinary Tuya LAN devices |
| SMART+ Bluetooth/HomeKit generations | Exact HomeKit Device or supported BLE path | Firmware generation, pairing code and active connection support |
| Actual Matter products | HA Matter | Specific model/certification, firmware and exposed clusters |
| Legacy LIGHTIFY gateway | Existing documented local route only if still supportable | Ended vendor cloud/service is a lifecycle constraint |

OSRAM announced shutdown of the LIGHTIFY gateway cloud for **2021-08-31**. That does not erase the Zigbee radio in every lamp, but it changes gateway setup, service and maintenance assumptions. [OSRAM announcement](https://ams-osram.com/news/press-releases/pr-09-03-2020). LEDVANCE's own Zigbee FAQ documents protocol-specific reset and compatibility details; use the procedure matching the actual product rather than a universal on/off count. [LEDVANCE Zigbee FAQ](https://www.ledvance.com/en-asia/home-lighting/services/faq/faq-for-smart-zigbee-products).

## Integrate existing devices

Read labels and existing device signatures first. A functioning Zigbee lamp can remain on its current bridge when the required HA controls work. Before moving it, inventory every remote or group binding and plan to restore those functions. If the old gateway is the failing component, verify direct support for each child rather than discarding working lamps.

For lamp testing, check minimum dimming, startup brightness, color temperature range, transition behavior and state after power restoration. A lamp used as a Zigbee router must not be casually cut off by a wall switch if battery devices depend on that path. For plugs, inspect the physical load rating rather than deriving it from an integration capability.

## Source date guard

At the research baseline **2026-10-22**, the live HA LEDVANCE brand page was already marked **introduced in 2026.11**. Do not use that page's future release or certification count as evidence of currently released functionality. Check an installed-release tag and the actual Matter/Zigbee support instead. [Observed future-dated page](https://www.home-assistant.io/integrations/ledvance/).

This distinction matters when browsing a continuously updated documentation site: an accessible page can describe an upcoming release. A brand landing page also does not imply that every historical product is certified.

## Recovery and replacement decision

Capture the existing bridge/controller backup and exact models. Pilot one lamp at a time; use the manufacturer reset sequence only when migration is intended. Keep a physical lighting fallback. Compare a replacement's lumen/color quality and control behavior as well as its protocol; successful pairing alone does not preserve the household experience.

When user reports mention flashing, dropout or poor mesh routing, verify that the report matches the model and firmware. Do not carry an older LIGHTIFY issue into a blanket conclusion about current LEDVANCE Matter devices. Use dated first-person logs where available; label unresolved support for unspecified installed models rather than fabricate experience for them.

## Firsthand pairing example

[Z2M issue 26686](https://github.com/Koenkk/zigbee2mqtt/issues/26686), opened 2025-03-10, concerned an OSRAM strip linked to 4058075036185, Z2M 2.1.1/2.1.3 and Dongle-E firmware 7.4.5. The reporter described incomplete pairing and eventual success after another restart/reconfigure. It was closed as duplicate of a delivery-failure issue; the maintainer suspected broader interference, which the reporter disputed. This does not establish a universal OSRAM defect or a general restart remedy. Distinguish identity matching, interview completion and network delivery before changing a whole mesh.
