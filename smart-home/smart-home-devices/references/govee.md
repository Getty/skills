# Govee

## Choose by exact H-model and feature

| Family | Candidate route | Missing-feature checks |
| --- | --- | --- |
| Supported Wi-Fi lighting with LAN control | Core Govee lights local | LAN switch, multicast path, supported colors/brightness; effects can differ |
| Supported Bluetooth thermometers and sensors | Core Govee Bluetooth | Exact model; some require active scanning |
| Actual Matter lighting/devices | HA Matter | Required clusters and feature subset |
| Products supported only by a cloud API | A currently maintained integration/bridge using that API | Account/API key, quota, cloud availability and polling |
| BLE-only lights or proprietary control variants | Exact supported BLE project | Core Govee Bluetooth sensor support is not proof of light control |
| Humidifiers, air purifiers, buttons, presence and other appliances | Per-model supported list | Do not inherit lighting support across product categories |

The core LAN integration publishes a long supported-model list and points to Govee's LAN setup instructions. Compare the exact product number instead of copying the full list into a static recommendation. [HA Govee lights local](https://www.home-assistant.io/integrations/govee_light_local/).

Govee's LAN guide specifies enabling LAN control and its UDP/multicast communication. Inspect interface selection and network segmentation if local discovery fails. A working vendor cloud app does not prove that LAN control is enabled. [Manufacturer LAN guide](https://app-h5.govee.com/user-manual/wlan-guide).

The core BLE integration supports specified environmental and other sensor models; H5074/H5075 and other listed models may require active scans. Do not confuse “active scanning” with an established GATT connection. [HA Govee Bluetooth](https://www.home-assistant.io/integrations/govee_ble/).

## Integration assessment

Record which capability matters: simple on/off, full RGB/white control, per-segment control, scene selection, music mode, temperature, leak alarm, device buttons or humidifier settings. Test each one on the candidate route. A cloud bridge such as govee2mqtt can combine multiple APIs, but its documented local support and feature subset still depend on SKU. [govee2mqtt SKU notes](https://github.com/wez/govee2mqtt/blob/main/docs/SKUS.md).

Use one command owner while testing. Running a local integration, another LAN bridge and a cloud automation together can create command competition and socket conflicts. Confirm whether status updates describe the actual hardware state or merely the last commanded state.

## Failure investigation

For discovery: model/LAN-toggle → local address → HA network interface → multicast/UDP return path → duplicate service binding → integration parser. For BLE: advertisement visibility → scan requirement → parser → freshness. For cloud: vendor app/account region → API permission/quota → cloud availability → HA behavior.

A **2025-03-08** firsthand issue on HA **2025.3.1**, previously working on 2025.2.x, reported that Govee Lights Local could not bind port 4002. It later closed stale/not planned; no universal fix is established here. [Core issue 140100](https://github.com/home-assistant/core/issues/140100). Use the concrete error to inspect duplicate listeners and the matching version's bug history, not as evidence of a defective lamp.

## Commissioning and updates

Pilot a single device before changing all room lighting. Observe manual/app changes reflected in HA, a device reboot, HA restart, internet interruption and recovery. Preserve vendor scene configuration where important. If a newer firmware removes or changes a LAN option, retain exact version evidence and check manufacturer guidance before reset or replacement.

Do not claim current Amazon availability, “best” reliability or subscription cost without a fresh listing/API-policy check. The installed Govee count is small but the exact models are unknown; keep their route unresolved until identified.
