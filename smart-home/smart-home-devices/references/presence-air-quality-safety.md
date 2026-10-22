# Presence, air quality, environmental and safety sensors

Research baseline: 2026-10-22. Identify what the sensor physically measures, how it reports and what the automation needs. Motion, room occupancy, personal presence, air quality and a safety alarm are different signals.

## Product families and routes

| Family / examples | Candidate HA path | Model and capability caveat |
| --- | --- | --- |
| Hue, Aqara, SONOFF and Tuya PIR sensors | Native bridge or exact Zigbee endpoint via ZHA/Z2M | Motion hold time, cooldown, sensitivity and light level are model-specific. A sleeping battery device may not answer a read immediately. Use its dedicated vendor reference. |
| Aqara FP2 presence zones | HomeKit Device for supported local functionality | Wi-Fi device; not the same route as Zigbee FP1 or actual Matter/Thread generations. Vendor setup/calibration and HA zone exposure are separate. [Aqara FP2](https://eu.aqara.com/en-eu/products/aqara-presence-sensor-fp2), [HomeKit Device](https://www.home-assistant.io/integrations/homekit_controller/) |
| Everything Presence Lite | ESPHome native API with the project's hardware/firmware | mmWave and light sensing; use the exact firmware/configuration and installation guide, not a generic radar YAML. [Project](https://github.com/EverythingSmartHome/everything-presence-lite), [setup guide](https://docs.everythingsmart.io/s/products/doc/set-up-your-epl-device-in-home-assistant-EcxzrA79Z3) |
| Apollo MSR-2 and related supported products | ESPHome native API | Check the actual sensor options; optional CO₂ hardware is not present in every unit. [Project](https://github.com/ApolloAutomation/MSR-2), [manufacturer wiki](https://wiki.apolloautomation.com/products/msr2/introduction/) |
| Other mmWave products sold as Tuya/SONOFF/Aqara-compatible | Exact Zigbee fingerprint, actual Matter model, Wi-Fi local/cloud or ESPHome | The same retail shape can hide different radars, data points and protocols. Require the exact definition before promising zones or target coordinates. |
| ThermoBeacon/SensorBlue and Govee BLE thermometers | Core `thermobeacon` or `govee_ble` for listed models | Advertisement visibility, active scanning and model parser differ. Humidity and temperature support does not prove a Govee light is BLE-controllable. See vendor references. |
| Airthings supported Wave families | Core `airthings_ble` or the separate applicable cloud route | Confirm Bluetooth versus SmartLink mode and proxy active-connection support. Exact gas/particle measurements differ by model. [HA Airthings BLE](https://www.home-assistant.io/integrations/airthings_ble/) |
| Sensirion MyCO2 and supported development sensor families | Core `sensirion_ble` | Read the supported and untested model distinctions; do not infer all Sensirion-based third-party products share the protocol. [HA Sensirion BLE](https://www.home-assistant.io/integrations/sensirion_ble/) |
| Netatmo weather / indoor air modules | Core `netatmo` | Cloud account, station/module pairing and measurement types. [HA Netatmo](https://www.home-assistant.io/integrations/netatmo/) |
| Shelly Flood / BLU, Aqara/Tuya/THIRDREALITY water sensors | Generation-specific Shelly or exact Zigbee/BLE route | Test real wet and dry state transitions, not battery availability alone. Original Shelly Flood sleep and event delivery require special attention. |
| Bosch smoke/Twinguard, compatible Zigbee/Z-Wave smoke/CO alarms | Bosch SHC or exact supported radio device | Alarm, test, battery, tamper and hush capabilities must be verified separately. HA notifications supplement the actual certified alarm functions; do not infer certification from an HA entity. [HA Bosch SHC](https://www.home-assistant.io/integrations/bosch_shc/) |

## Match sensor to the decision

PIR primarily reacts to motion; a stationary occupant can be missed by a motion-based timeout. Radar can detect small movements but may respond to fans, curtains or activity beyond the intended zone. A phone's network or BLE presence can lag departure or be absent while its owner remains home. Treat each as a signal with its own failure mode rather than universal occupancy truth.

Define a precise automation statement, such as “keep this light on while someone is in the seating area, but turn it off after confirmed absence.” Then record entry latency, stationary-person behavior, exit delay, false detections, range and unavailable-state handling. The correct test is room-specific; a manufacturer's detection range does not validate a zone in this home.

For ventilation, distinguish measured CO₂ from an estimated equivalent value, and VOC indices from a calibrated concentration. Record units, calibration method, placement and age. Do not diagnose health or indoor hazards from an unspecified consumer sensor. For safety-related decisions, use the actual alarm device and applicable manufacturer instructions, with HA providing additional observation.

## Presence commissioning

1. Capture the installed location, orientation, power supply, room boundaries and nearest interfering moving objects without including private household identities in reports.
2. Observe raw entities before applying delays or templates. Verify target/zone support in the selected integration, not only in a vendor app.
3. Test entry from each ordinary route, still occupancy, movement near a wall, a running fan and departure. Test normal pets if relevant to the user's task.
4. Set zones/sensitivity only from observed errors. Change one parameter at a time and preserve the prior setting.
5. Apply bounded delays and record the reason. Avoid masking persistent ghost presence with a long fixed reset or making inactivity mean absence automatically.
6. Test unavailable/stale values and restart recovery. A retained occupied flag should not indefinitely force an action without an explicit fallback.

## Environmental sensor acceptance

Place comparable sensors together long enough to stabilize before discussing offsets. Record reference instrument uncertainty and the time interval; do not “calibrate” one device to another unknown device simply because their numbers differ. Check a realistic stimulus such as a room temperature change, open/closed contact or manufacturer-prescribed alarm test. Verify the whole path from device to HA, including return to normal.

For BLE, distinguish packets received by a scanner from a successful active GATT connection. Verify proxy placement, firmware and connection capacity for the exact protocol. A nearby phone receiving a beacon does not prove the HA host/proxy hears it reliably. For Zigbee battery sensors, inspect last-seen/report timestamps and the model's wake behavior before repeated re-pairing.

## Notifications and failure detection

Build explicit stale-data detection for critical observations. Record which component can still warn when HA is unavailable: device buzzer, local hub, independent notification or none. An HA automation must not suppress a physical smoke/CO alarm or replace device-required maintenance. Use the automation skill for notification retries, escalation and acknowledgement only after the sensor path has been physically validated.
