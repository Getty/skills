# Additional lighting, locks, curtains and covers

Research baseline: 2026-10-22. Use the dedicated Hue, Govee, Paulmann, Zengge and OSRAM/LEDVANCE references for those brands. This map expands the range of devices considered while retaining exact model and protocol checks.

## Lighting and general accessories

| Manufacturer / family | Candidate HA route | Dependency and important exception |
| --- | --- | --- |
| IKEA legacy TRÅDFRI bulbs, outlets, remotes and blinds | Core `tradfri` through the old gateway, or supported exact endpoint directly in ZHA/Z2M | The TRÅDFRI gateway integration is not a DIRIGERA integration. Direct pairing moves the device to the chosen Zigbee network. [HA TRÅDFRI](https://www.home-assistant.io/integrations/tradfri/) |
| IKEA DIRIGERA with Zigbee children | HomeKit Device or Matter bridge route; compare child features | No dedicated core DIRIGERA integration is implied by `tradfri`. A bridge's supported types and firmware determine what crosses the bridge. [HA TRÅDFRI](https://www.home-assistant.io/integrations/tradfri/), [IKEA Matter explanation](https://www.ikea.com/de/de/customer-service/knowledge/articles/99f660cc-544a-4f35-b9b5-7b72556be25b.html) |
| IKEA native Matter/Thread products | Commission/share the individual Matter device to HA with a suitable Thread network | Adding a DIRIGERA Matter bridge does not mean every native Matter device managed by it is automatically shared. See the firsthand record below. |
| Nanoleaf Panels, Canvas, Shapes, Elements and Lines | Core `nanoleaf` local integration for supported families | Essentials and Remote are outside that integration's family list. Older HomeKit Essentials and newer Matter Essentials need their actual protocol route. [HA Nanoleaf](https://www.home-assistant.io/integrations/nanoleaf/) |
| Eve plugs, contact/motion/room sensors, covers and other accessories | Actual Matter device through Matter; older HomeKit hardware through HomeKit Device where supported | Thread is a transport, not proof of Matter firmware. Confirm SKU, generation and migration consequences before a firmware conversion. [HA Eve](https://www.home-assistant.io/integrations/eve/), [HomeKit Device](https://www.home-assistant.io/integrations/homekit_controller/) |
| SwitchBot Bot, Curtain/Blind Tilt, sensors, plugs and selected locks | Core `switchbot` Bluetooth for its supported list; separate actual hub/cloud/Matter routes | Distinguish BLE advertisement sensing from commands requiring an active connection and keys. A hub's Matter exposure can be a subset of native/vendor features. [HA SwitchBot](https://www.home-assistant.io/integrations/switchbot/) |

For lighting, compare color mode, low-end dimming, transitions, startup behavior, group synchronization, remote events and vendor effects. Basic on/off compatibility does not establish equal support for scenes or entertainment features. Separate the radio endpoint from logical rooms, grouped lights and bridge services when counting devices.

## Locks and access devices

| Family | Integration route | Check before choosing |
| --- | --- | --- |
| Nuki with compatible Bridge | Core `nuki` through the Bridge's HTTP API | Bridge presence is a real requirement for this particular integration. Local callbacks require reachable HTTP on HA; do not assume an HTTPS-only URL works. Other generations may expose MQTT, HomeKit or Matter via separate routes. [HA Nuki](https://www.home-assistant.io/integrations/nuki/) |
| Nuki native MQTT/Matter/HomeKit models | Exact model's documented protocol into the corresponding HA integration | Read the manufacturer's generation-specific API and feature list before buying. Compare lock state, unlatch, battery and keypad/activity support rather than assuming equivalence to Bridge. |
| Yale Home devices | Core `yale` account integration | Cloud service, supported region and account mapping matter; inspect its current alert before deployment. [HA Yale](https://www.home-assistant.io/integrations/yale/) |
| Supported Yale/August locks with Bluetooth interface/module | Core `yalexs_ble` | Active BLE connection and offline keys; some hardware has state-update limits. The integration documents a conflict when the same lock is used through HomeKit Device and Yale Access Bluetooth in the same HA instance. [Yale Access Bluetooth](https://www.home-assistant.io/integrations/yalexs_ble/) |
| Supported SwitchBot locks | Core Bluetooth route or model-specific hub/Matter route | Verify encrypted control, state freshness, physical calibration, and which hub exposes which lock features. Do not treat a BLE presence beacon as lock-state evidence. [HA SwitchBot](https://www.home-assistant.io/integrations/switchbot/) |

Pilot a lock while the door is open and manual access remains available. Validate lock, unlock, latch behavior, jammed/unknown state, battery events and recovery separately. An unlocked bolt does not prove an open door; a contact sensor does not prove a locked bolt. Do not automatically issue real unlock commands merely to test discovery. Use the task's established authorization and an explicit test context.

A presence signal alone should not silently become an unlock policy. If the user requests such an automation, define which person/device is authorized, freshness, additional conditions, manual override and an event log. Keep credentials and access codes out of capability reports.

## Covers and motors

| Family | Route | Feature caveat |
| --- | --- | --- |
| Somfy TaHoma/Connexoon and other Overkiz gateways | Core `overkiz`; local API on supported gateways or cloud | RTS can be stateless; position may be estimated. Local mode can lose scenarios or other functions. Verify io-homecontrol versus RTS and the exact hub. [HA Overkiz](https://www.home-assistant.io/integrations/overkiz/) |
| VELUX io-homecontrol via KLF 200 | Core `velux` local gateway | KLF 150 and KIG 300 are not supported by this integration; KIG 300 has a separate HomeKit Device path. Check KLF 200 firmware and credentials; integration features depend on gateway-reported devices. [HA VELUX](https://www.home-assistant.io/integrations/velux/) |
| Shelly roller/cover-capable relays | Core `shelly` using the actual device's cover mode | Not every relay supports interlocked cover operation or position calibration. Verify motor, wiring, power and device mode in its manual. See `shelly.md`. |
| Zigbee curtain/blind motors from Aqara, Tuya, IKEA and others | Exact endpoint definition in ZHA/Z2M, or vendor bridge route | Check full fingerprint, direction, limits, calibration, position feedback and battery behavior. A similar casing is insufficient identification. |
| SwitchBot Curtain / Blind Tilt | Supported Bluetooth or actual hub route | Calibration, angle versus travel, group behavior and active connection coverage must match the installation. [HA SwitchBot](https://www.home-assistant.io/integrations/switchbot/) |

For cover acceptance, test stop first, then direction, travel limits and position. Observe a manual movement and verify how HA learns the result. Mark estimated position explicitly; do not use it as proof that a window or shutter is physically secure. Preserve device-local limits and obstacle behavior.

## Firsthand route-confusion example

In [HA issue 160196](https://github.com/home-assistant/core/issues/160196), opened 2026-01-03 with HA 2025.6.3, an owner saw DIRIGERA's Zigbee children through Matter but not its native Matter/Thread products. The discussion distinguishes bridge exposure from sharing individual Matter devices. A March 2026 participant reported success after host IPv6 repair and individual sharing; the maintainer closed the issue as completed on 2026-06-09. This documents route and commissioning confusion, not an IKEA-wide reliability rating. Use the generated sharing code for the existing device and diagnose IPv6 reachability; do not reset the whole fleet as a first response.
