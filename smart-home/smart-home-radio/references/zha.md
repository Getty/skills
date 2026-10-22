# Operate ZHA

## Establish the supported path

ZHA is HA's integrated Zigbee stack. Confirm the coordinator appears in the current [compatible hardware and configuration documentation](https://www.home-assistant.io/integrations/zha/) and has the required coordinator firmware. Use a persistent serial identity for USB passthrough and prevent other applications from opening it.

Pair one device through the intended network. Keep a sleeping device awake using its documented procedure during interview. If setup completes but functions are missing, capture manufacturer/model, endpoints, input/output clusters, software build and quirk details. Pairing failure and missing manufacturer-specific attributes are different problems.

## Inspect before choosing a workaround

Use the device's ZHA management/diagnostics surfaces and available entity/device triggers. Record actual events from a physical press; do not invent `zha_event` payload fields from a similar remote. Check the exact [zha-device-handlers](https://github.com/zigpy/zha-device-handlers) implementation when a quirk is needed. A repository's development branch is not necessarily the code shipped with HA.

If one feature is absent, compare supported quirk/converter capabilities in the installed versions. Moving every device to Zigbee2MQTT is not the first diagnostic step. If migration is chosen, include paired devices, groups, bindings, automation IDs and rollback work.

## Use direct control carefully

Bindings and Zigbee groups can provide a path independent of HA for supported endpoints. Check both source command generation and target cluster handling. Test the desired short/long press, dimming and state reporting with HA disconnected. Some buttons only send vendor-specific events and do not provide usable standard bindings.

For example, do not assume every SONOFF button can bind directly merely because another SONOFF model can. Route exact SNZB-01P behavior to `smart-home-devices`.

## Maintain without destroying evidence

Before a radio migration, export the network backup through supported ZHA tools and record radio firmware/serial mapping. Use the current [ZHA migration procedure](https://www.home-assistant.io/integrations/zha/#migrating-to-a-new-zigbee-coordinator-adapter-inside-zha) for the exact source/target. Keep the old radio disconnected once its identity is transferred; do not run two live copies of the same coordinator.

For OTA, verify update provider, image identity and model-specific warnings. Device firmware can alter reporting, bindings and battery behavior. Do one sample during an agreed window. A successful transfer is not sufficient; check sensor values/events and reconnect behavior afterward.

## Minimal diagnosis record

Record HA/ZHA version, radio and firmware, full device signature, issue timing, power source, one raw event or failed exchange, last known good version, and changes already attempted. Attach redacted diagnostics to a focused upstream issue only when needed. Do not expose network keys or routinely edit HA's internal storage files.
