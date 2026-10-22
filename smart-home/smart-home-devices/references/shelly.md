# Shelly: generations, APIs and the installed plug/leak devices

## Identify the actual generation

| Family | Interface to investigate | Practical boundary |
| --- | --- | --- |
| Original Gen1 relays, Plug/Plug S, Flood, H&T and related devices | HTTP Gen1 API, CoIoT/CoAP, model-dependent MQTT | Gen1 instructions are not Plus RPC instructions |
| Plus / many Pro devices, including Plus Plug S | Gen2 RPC over HTTP/WebSocket, components, scripts, MQTT | Components and firmware support differ by device |
| Gen3 / Gen4 devices | Current model API and enabled protocol mode | Do not assume every product offers every radio or Matter feature |
| BLU sensors/remotes | Bluetooth protocol with suitable receiver/proxy | Native Shelly Wi-Fi entity support does not establish BLU coverage |
| Wave products | Z-Wave controller/integration | A Shelly brand name does not make these Wi-Fi devices |
| Pro meters, cover controllers, dimmers, safety devices | Exact model and installation manual | Meter channels, neutral requirements, dry contacts and load limits differ |

For Gen1 HA communication, CoIoT must be enabled. A unicast peer targeting HA on UDP 5683 is required for battery devices; routed networks must pass this traffic. Gen2+ uses a different connection model; diagnose it using the matching section rather than opening CoAP as a universal fix. [HA Shelly](https://www.home-assistant.io/integrations/shelly/).

## Plus Plug S

The exact Plus Plug S exposes `switch:0`, power measurement, LED configuration, MQTT, outbound WebSocket and scripting components in the vendor API. The current device page marks firmware 1.7.x as a feature-freeze boundary with critical fixes continuing; recheck policy before making a lifecycle recommendation. [Plus Plug S technical reference](https://shelly-api-docs.shelly.cloud/gen2/Devices/Gen2/ShellyPlusPlugS/).

Read-only discovery examples, replacing the explicit host with an authorized local address:

```text
GET http://DEVICE_IP/rpc/Shelly.GetDeviceInfo
GET http://DEVICE_IP/rpc/Shelly.GetStatus
GET http://DEVICE_IP/rpc/Switch.GetStatus?id=0
```

Confirm these methods against the installed firmware. Do not dump complete configuration responses containing Wi-Fi, MQTT or webhook credentials into a shared diagnostic. For normal HA use select the native integration unless a specific MQTT requirement justifies another path; avoid both paths issuing commands concurrently.

Pilot one plug with a known steady load and compare device UI, HA power and a reference meter. Distinguish W from cumulative Wh/kWh. Check restored state after an authorized power interruption, overload behavior specified by its manual, and whether an automation accidentally switches the HA host/router itself. Test the reporting load of the whole set of plugs before shortening every interval.

## Flood sensors

Confirm the label: original Shelly Flood and later generations require different procedures. Original Flood is a battery Wi-Fi sensor that sleeps between reports/events. Its local interface is available during a limited setup wake window. Rain mode changes local alarm behavior. [Shelly Gen1 API, Flood section](https://shelly-api-docs.shelly.cloud/gen1/#shelly-flood).

A sleeping HTTP endpoint is not automatically a broken sensor. Wake one unit, verify network and CoIoT settings, then perform the manual's safe wet/dry contact test. Observe local alarm, HA wet event, notification, dry recovery and next health report separately. Test each installed location; radio behavior near plumbing is not established by a desk test.

A 2024-08-31 report on firmware 1.14.0 and HA 2024.8.3 described local water detection and audible alarm without the HA event. The record was closed, with no universal fix established here. [Core issue 124998](https://github.com/home-assistant/core/issues/124998). Operational implication: a plausible battery value or visible device is insufficient acceptance for leak protection.

## Troubleshooting order

Capture exact firmware/generation → inspect local state → verify HA's correct source interface and return path → confirm authentication → inspect event delivery → evaluate recorder load. Use per-device logging for a bounded period. Change a single parameter and retain its original value. Preserve local protective behavior even if HA is offline.
