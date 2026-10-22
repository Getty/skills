# Device bridges and local alternatives

## Select by transport and feature

Classify the product as direct Zigbee, direct Matter, BLE advertisement/control, native local Wi-Fi API, vendor cloud, or bridge-mediated. This comes before choosing HACS. A brand's app support does not identify its hardware protocol.

## Tuya

Keep three routes separate: native Tuya cloud integration, LocalTuya, and Tuya Local. Local alternatives depend on supported device protocols, keys, and data-point behavior; compare the exact project/fork and its current compatibility. [LocalTuya](https://github.com/rospogrigio/localtuya), [Tuya Local](https://github.com/make-all/tuya-local).

Do not treat Tuya's `TS0601`, `TS0201`, or `_TZ…` strings as complete identities. Direct Zigbee devices need a matching ZHA quirk or Zigbee2MQTT definition, not a Tuya Wi-Fi local key. Ask for manufacturer fingerprint, endpoints, clusters, firmware, and current route before writing custom DP mappings. Use `smart-home-devices` and `smart-home-radio`.

For local Wi-Fi migration, test command/status/availability separately, preserve the original configuration, and check whether competing local clients affect the device. Re-pairing or cloud changes can alter credentials; do not assume a once-retrieved key is permanent.

## Sonoff/eWeLink

SonoffLAN supports selected stock-firmware devices through LAN and/or cloud routes; support is model-specific. [SonoffLAN](https://github.com/AlexxIT/SonoffLAN). A directly paired SNZB Zigbee sensor does not need this integration simply because Sonoff sold it. Distinguish Sonoff bridge support from native ZHA/Z2M pairing, and do not flash firmware to solve an unexamined pairing problem.

## Govee

Check the native Govee lights local integration and its exact model list/LAN-control prerequisites before a custom bridge. [Native Govee local](https://www.home-assistant.io/integrations/govee_light_local/). Govee2MQTT can provide another feature path but is an external service with broker, credentials, and actual cloud/local dependencies. It is not interchangeable with a backend HACS integration. [Govee2MQTT](https://github.com/wez/govee2mqtt).

## Decision record

Record each route's required account, runtime network, offline behavior, exposed features, latency, restart recovery, update burden, and rollback. “Local” can describe command traffic while setup, credential retrieval, effects, or firmware still involve a cloud. Prove the specific feature works with internet unavailable before promising offline operation.
