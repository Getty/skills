# Heating, thermostats, ventilation and air conditioning

Research baseline: 2026-10-22. These are candidate family routes, not blanket support promises. Match the exact thermostat, radio, gateway and regional heating interface. For FRITZ!DECT 301/302 and Control 440 use `fritzbox-operator`; for cross-vendor room control use `home-assistant-automations`.

## Family and integration map

| Manufacturer / family | Route into HA | Local or cloud dependency | Model-level decision and limitation |
| --- | --- | --- | --- |
| Bosch Smart Home radiator/room thermostats, contacts, plugs, shutters, Twinguard | Core `bosch_shc`, through Bosch Smart Home Controller | Local controller registration and client certificate | Check controller generation and exposed entities; a Bosch heating boiler is not automatically a Bosch Smart Home endpoint. Registration needs the controller system password and physical pairing action. [HA Bosch SHC](https://www.home-assistant.io/integrations/bosch_shc/) |
| Homematic IP Access Point devices | Core `homematicip_cloud` | Vendor cloud | Check current integration alert, service availability and exact device support. The Access Point path is distinct from CCU/OpenCCU; switching routes can require device migration. [HA Homematic IP Cloud](https://www.home-assistant.io/integrations/homematicip_cloud/) |
| Homematic / Homematic IP with CCU/OpenCCU | Custom `homematicip_local` / Homematic(IP) Local for OpenCCU | Local central unit and suitable radio hardware | Read project-supported central-unit versions, interfaces, callback networking and device definitions. It is a custom integration, not the similarly named cloud integration. [Project](https://github.com/sukramj/homematicip_local), [integration guide](https://sukramj.github.io/aiohomematic/user/homeassistant_integration/) |
| tado legacy thermostat/TRV/AC families | Core `tado` | Unofficial vendor cloud API and authentication | Verify model, region, account authorization and current API restrictions. **tado X is not supported by this integration**; evaluate the actual X device through Matter instead. [HA tado](https://www.home-assistant.io/integrations/tado/) |
| Netatmo thermostats/TRVs, weather and indoor sensors | Core `netatmo` | Cloud account and vendor service | Distinguish heating from weather and security products; account ownership, module presence and features differ. Related Legrand devices are not all the same transport. [HA Netatmo](https://www.home-assistant.io/integrations/netatmo/) |
| Daikin AC with supported network adapter | Core `daikin` | Local controller for the documented adapters | Verify the adapter label as well as indoor-unit name. BRP069A/B and selected regional BRP072, BRP084, AirBase/SKYFi families have specific conditions; a ONECTA app alone does not prove local support. [HA Daikin](https://www.home-assistant.io/integrations/daikin/) |
| Mitsubishi Electric AC / heat-pump families | Core `melcloud` | MELCloud account/service | Check exact air-to-air/air-to-water features and regions; energy-recovery ventilators are not supported here. Mitsubishi Heavy Industries is a different product lineage; do not transfer support by the shared word Mitsubishi. [HA MELCloud](https://www.home-assistant.io/integrations/melcloud/) |
| Atlantic, Thermor, Hitachi and other Overkiz-backed heating products | Core `overkiz` with the exact supported service/gateway | Cloud, or local API on selected gateways | Local mode can omit climate entities, sensors and scenarios that cloud exposes. Verify the real feature list before trading cloud access for local operation. [HA Overkiz](https://www.home-assistant.io/integrations/overkiz/) |
| Aqara/Tuya/SONOFF temperature sensors and compatible TRVs | Direct Zigbee, actual Matter model, or vendor hub route | Varies by exact hardware | A temperature sensor does not itself provide a heating actuator. Use vendor references for fingerprint, data-point and calibration requirements. |
| Meross heating controllers / hub child thermostats | Custom `meross_lan` where supported; actual HomeKit/Matter SKU alternatives | LAN HTTP, local MQTT, or vendor MQTT depending on configuration | Confirm the controller's electrical role and exact profile; app schedules and every preset need not appear in HA. [meross_lan](https://github.com/krahabb/meross_lan) |
| Existing wired boiler/heat-pump control | The manufacturer's documented interface or a specifically supported gateway | Local bus or cloud depending on system | Identify dry contact, bus interface and control ownership. Route KNX, Modbus, OpenTherm or ESPHome work to the appropriate architecture/firmware skill after identifying the equipment. |

The maps identify integration candidates; they do not establish mechanical or electrical compatibility. A TRV must match the valve body and travel; a relay does not emulate a modulating boiler bus. Keep those checks separate from HA entity support.

**Bosch heating boundary:** at this research baseline, the native `bosch_shc` functionality list exposes thermostat measurements, diagnostic valve position and selected settings; it does not document a climate platform for setting room targets. Do not turn “thermostat supported” into a promise of heating control. If target-temperature control is required, evaluate the separate [boschshc-hass community project](https://github.com/tschamm/boschshc-hass) against its current device/controller/version matrix and migration instructions. Avoid simultaneous competing integrations without checking how they register and share controller access.

## Specify the control contract

For a room, write down the actuator, physical temperature measurement, intended setpoint, schedule owner, occupancy input, window input and fallback behavior. An example contract is: a radiator TRV retains its local schedule; HA can request a temporary room setpoint; a contact can request a bounded setback; manual changes remain usable. Choose the actual behavior with the user rather than assuming all households want central scheduling.

Check these capabilities independently:

| Capability | Evidence to collect |
| --- | --- |
| Setpoint write | Device physically accepts the target; observed target matches; unit and rounding are understood |
| Current temperature | Sensor location and update age; internal valve sensor versus a room sensor |
| Heating state | Reported demand versus inferred demand; valve percentage is not heat delivered |
| Modes and presets | Actual supported values, vendor schedule resume behavior and duration semantics |
| External sensor input | A real device/API facility or HA control logic; do not label a dashboard helper as native external sensing |
| Window handling | Local device behavior, gateway behavior and HA automation do not fight each other |
| Outage behavior | Manual knob/control, stale sensor handling, internet loss, HA restart and battery depletion |
| Recovery | No repeated override loop, retained intended schedule and clear source of last command |

## Pilot commissioning

1. Record one room's baseline: existing schedule, valve adapters, current state, room sensor placement and entity IDs. Take a configuration backup before removing a central unit or re-pairing devices.
2. Add the integration without replacing the entire schedule. Verify readings, availability and one reversible target change.
3. Observe a complete heating or cooling cycle appropriate to the equipment. A fast UI change does not establish room response, sensor accuracy or energy savings.
4. Test manual override and schedule resume. Avoid having vendor schedules, HA automations and another hub repeatedly restore different values.
5. Test stale data and recovery before introducing occupancy setbacks. Define a bounded fallback using the existing controller's capabilities.
6. Roll out to other rooms only after the pilot passes. Preserve different rooms' valve types, window behavior and occupants' settings.

## Diagnose without guessing

For a missing climate entity, inspect integration support and gateway-reported capabilities before changing radio channels. For a target that reverts, inspect schedules and command traces. For a room that never reaches target, distinguish valve installation, actual heat supply, sensor placement and control logic. For loss of all cloud devices at once, check authentication and the integration alert before resetting endpoints. For only one battery endpoint, check wake/report timing and battery contact before replacing the gateway.

Do not promise savings from a brand or protocol. A product-family match and an online anecdote cannot quantify this home's thermal behavior. Compare comfort, override frequency, outages and measured energy under comparable conditions if the user wants an evaluation.
