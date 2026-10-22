# Plugs, appliances, cleaning robots and garden equipment

Research baseline: 2026-10-22. A marketplace category is only a starting point. Confirm the exact product model, app, firmware, account region and intended control capabilities before choosing a route. Use dedicated Shelly, THIRDREALITY, SONOFF and Tuya references for the installed plugs and sensors.

## Plugs and mains-powered accessories

| Manufacturer / family | HA path | Dependency / exception |
| --- | --- | --- |
| TP-Link Kasa and Tapo plugs, strips, bulbs, switches and supported hubs | Core `tplink` | Local control for documented models; authentication and firmware may require the vendor app's Third-party Compatibility setting. Cross-subnet discovery may need a manual IP. Supported cameras/vacuums/hub children are separate model lists. [HA TP-Link](https://www.home-assistant.io/integrations/tplink/) |
| Tapo hub buttons and sensors | Same native family where supported | Do not infer action-event support from successful discovery: the integration documents missing press alerts for S200B/S200D. Read the actual hub child capabilities. [HA TP-Link](https://www.home-assistant.io/integrations/tplink/) |
| Meross plugs, strips, lights, garage controllers, thermostats and sensors | Custom `meross_lan`; actual Matter/HomeKit models can use those routes | `meross_lan` can use LAN HTTP, private MQTT or Meross cloud MQTT; the name alone does not prove no cloud dependency. Key recovery and time services can matter. [Project](https://github.com/krahabb/meross_lan) |
| Eve/IKEA/Nanoleaf Matter outlets and other actual Matter SKUs | Core Matter with the device's transport | Verify metering, multi-outlet endpoints and power-restore options in HA, not only on/off certification. See `lighting-locks-covers-ecosystems.md`. |

A plug's current rating does not establish suitability for every motor, heater or continuous load. Use the actual manual, physical installation and intended load. A smart plug cannot safely turn every appliance into a remote-start appliance. Preserve device-local controls and verify behavior after power loss before unattended use.

## Household appliances

| Ecosystem / family | HA route | Capability limits to check |
| --- | --- | --- |
| Bosch, Siemens, Neff, Gaggenau and other BSH Home Connect appliances | Core `home_connect`, official API | Cloud account and appliance support. Status, program options and remote start differ by model; local arming/door state and vendor safety prerequisites remain relevant. [HA Home Connect](https://www.home-assistant.io/integrations/home_connect/) |
| LG ThinQ washers, dryers, refrigeration, AC and other supported appliances | Core `lg_thinq` | Cloud API/account token and exact supported product classes. LG TVs use the video/media skill, not appliance assumptions. [HA LG ThinQ](https://www.home-assistant.io/integrations/lg_thinq/) |
| Miele connected appliances | Core `miele` | Official third-party cloud API and Miele account; exact connectivity can be built-in Wi-Fi or supported gateway hardware. Features vary with appliance type. [HA Miele](https://www.home-assistant.io/integrations/miele/) |
| Samsung SmartThings appliances and hub-connected devices | Core `smartthings` | Cloud integration and device capabilities. A SmartThings logo does not imply a direct local HA API for the appliance. [HA SmartThings](https://www.home-assistant.io/integrations/smartthings/) |

For a dishwasher or washer, distinguish program selection, start permission, current cycle, remaining time, completion and error status. Test a harmless read-only status first. Do not bypass a physical remote-start requirement with a repeated button or power-cycle workaround. A notification based on measured plug power is an inference; label its thresholds and failure cases.

## Cleaning robots

| Manufacturer / family | Candidate route | Exact-model caution |
| --- | --- | --- |
| Roborock robots in the Roborock app | Core `roborock` | Despite local polling, the documentation explicitly requires cloud connectivity. Mi Home account devices are a different setup path. Maps, segments and commands vary by model. [HA Roborock](https://www.home-assistant.io/integrations/roborock/) |
| Xiaomi/Mi Home robot families | Core `xiaomi_miio` or vendor Xiaomi Home project, only where the model is supported | Device token, account region and transport differ from Roborock app integration. Do not migrate apps without checking map/room preservation. [HA Xiaomi Miio](https://www.home-assistant.io/integrations/xiaomi_miio/), [Xiaomi Home](https://github.com/XiaoMi/ha_xiaomi_home) |
| Dreame and supported related OEM robots | Custom `dreame-vacuum` | Check project branch/release, exact model and account path; brand-wide map or cloud-free support is not implied. [Project](https://github.com/Tasshack/dreame-vacuum) |
| Ecovacs Deebot robots and supported GOAT mower families | Core `ecovacs` | Vendor cloud account, region and model-specific features. Do not infer every Ecovacs appliance is supported. [HA Ecovacs](https://www.home-assistant.io/integrations/ecovacs/) |
| Specifically listed robots with Valetudo | Local firmware ecosystem and MQTT after supported installation | Verify the exact supported hardware and installation path. Rooting and a vendor firmware upgrade can have lasting effects; it is a separate project from adding an integration. [Valetudo supported robots](https://valetudo.cloud/pages/general/supported-robots/) |

Robot acceptance should include start, pause, return, charge state, error state and one selected room. Capture room/segment identifiers after map changes; friendly room names and numerical segment IDs are not interchangeable. Test whether map data or authentication needs the internet even if basic commands use LAN. Avoid multiple integrations concurrently sending incompatible cleaning jobs.

Keep vendor maps and schedules until the replacement route passes. A cloud outage should not trigger endless retries or repeatedly start a mission after recovery. Use an explicit timeout and inspect the robot's actual state before retrying.

## Garden, watering and mowing

| Family | HA route | Operational caveat |
| --- | --- | --- |
| GARDENA supported Bluetooth watering devices, pumps and pressure tanks | Core `gardena_bluetooth` | Exact BLE model list and pairing/active connection range. Bluetooth lawn mowers are explicitly unsupported; the listed 9 V irrigation valve is documented as untested. This does not cover every GARDENA smart gateway product. [HA GARDENA Bluetooth](https://www.home-assistant.io/integrations/gardena_bluetooth/) |
| Hunter Hydrawise controllers | Core `hydrawise` | Vendor cloud and API/account dependencies; separate controller schedules from HA overrides. [HA Hydrawise](https://www.home-assistant.io/integrations/hydrawise/) |
| Rachio controllers and supported hose timers | Core `rachio` | Controller event callbacks can require an externally reachable HA endpoint; hose timers use a different polling behavior. Check exact documentation before changing networking. [HA Rachio](https://www.home-assistant.io/integrations/rachio/) |
| Husqvarna Automower Connect products | Core `husqvarna_automower` | Requires compatible Automower Connect/module and cloud authorization; Bluetooth-only branding is not sufficient. [HA Automower](https://www.home-assistant.io/integrations/husqvarna_automower/) |
| Ecovacs supported GOAT mowers | Core `ecovacs` | Exact mower, region and available controls; lawn mapping is not a Deebot room map. [HA Ecovacs](https://www.home-assistant.io/integrations/ecovacs/) |
| SONOFF MS01 soil probe with compatible TH controller | Controller-specific eWeLink/local route | The wired probe is not a standalone Zigbee moisture sensor. Verify connector/adapter and controller; see `sonoff-ewelink.md`. |
| Zigbee/BLE moisture, rain, leak and valve products | Exact device definition or compatible gateway | A soil reading, leak alarm and water-flow meter measure different things. Do not infer sensor support from a valve brand. |

Define a maximum run time and an independent way to close a valve. Check what happens if HA, the network or a sensor fails mid-cycle. Use stale-data detection and record the difference between a commanded valve state and measured water flow. Preserve mower-local boundary/obstacle and manufacturer safety functions. Never assume a software integration replaces them.

## Purchase and migration decision

Compare the route's supported functions with the task, its account/service dependencies and the maintenance burden. Pilot one appliance or controller; use current primary support lists and same-model experience reports. Marketplaces can mix protocol, socket and region variants in one listing, so record the selected variant and physical label after delivery. Use `procurement-and-community-research.md` before a recommendation that commits money or significant setup time.
