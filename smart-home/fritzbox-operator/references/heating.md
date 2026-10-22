# Heating with FRITZ thermostats and external sensors

## Scope the room before the device

Map every 301/302 thermostat to its room, radiator and native FRITZ group, and each Control 440 to the rooms it references. Record the valve adapter, calibration result, battery condition, target/actual readings, schedule, manual override, and selected temperature reference. The number of thermostats alone cannot determine whether each radiator should be its own controller or part of a room group.

The [Thermo 302 product specification](https://fritz.com/en/products/fritz-smart-thermo-302-20003120) describes native schedules, group operation, offset, window detection, and local controls. The [Control 440 specification](https://fritz.com/en/products/fritz-smart-control-440-20003121) supports its use as a room temperature reference for FRITZ radiator control. Verify firmware and actual exposed capabilities for an older DECT-branded device instead of assuming all new product-page features appear identically.

## Choose one authority for the target

| Policy | Suitable behavior | Failure behavior to define |
| --- | --- | --- |
| FRITZ schedule owns daily heating; HA supplies occasional overrides | Simple baseline; local operation remains useful | Define override end and next scheduled transition |
| HA owns room setpoints; FRITZ acts as actuator | Cross-vendor occupancy/window/energy logic | Persist or reconstruct intended state after restart; ensure safe local fallback |
| FRITZ native group owns a multi-radiator room | Shared local room control | Verify a member command's propagation before addressing members separately |
| Human/manual override owns temporarily | Respect a person's immediate choice | Explicit expiration and visible ownership indicator |

Avoid several periodic automations that continuously restore competing target values. Diagnose apparent “random changes” by collecting a timeline of HA trace, native schedule boundary, manual input, group command, holiday/summer state, and external sensor update.

## Treat HA modes precisely

The inspected [HA climate implementation at 2026.10.2](https://github.com/home-assistant/core/blob/2026.10.2/homeassistant/components/fritzbox/climate.py) offers heat/off and eco/comfort/boost presets, handles special on/off setpoints, and rejects ordinary changes during holiday/summer modes or API lock. Its nominal temperature range is 8–28 °C with half-degree precision. Verify the current entity attributes before calling it; do not invent `auto` mode or a schedule-management action.

An eco or comfort preset is not proof that HA has taken permanent schedule ownership. A new setpoint may later be superseded by native behavior. “Boost” and “off” also have device-specific meanings; do not use special encoded API numbers as Celsius temperatures in HA.

## Engineer reliable logic

Use bounded target temperatures and a clearly defined fallback. Treat an unavailable thermometer as missing input, not 0 °C. Do not issue a heating change on every small sensor fluctuation. Apply hysteresis, minimum dwell time, and a meaningful control interval appropriate to room thermal inertia and battery radio communication.

An external room thermometer is not automatically a FRITZ external sensor. A third-party HA sensor can inform an HA control loop, but that is a different architecture from native Control 440 compensation. Check native sensor compatibility before suggesting that arbitrary values can be written into the thermostat's internal measurement.

Account for curtains, radiator proximity, sunlight, sensor height, and thermal lag when diagnosing disagreement. A single static offset may not correct a measurement location whose bias changes with radiator output. Compare readings over a stable interval before editing offsets.

For window handling, define open-state confirmation, maximum suspension duration, stale-contact behavior, and close/resume behavior. Preserve frost protection and a manual means of restoring heat. Do not treat a polling-only sensor as a guaranteed immediate safety signal.

## Validation sequence

1. Validate manual operation and valve calibration locally.
2. Verify one modest target change in the FRITZ UI and on the physical device after normal radio delay.
3. Verify the same change through the chosen HA route.
4. Observe a native schedule boundary and a manual override.
5. Simulate missing occupancy/temperature input without changing physical safety limits.
6. Restart HA during a noncritical period and verify ownership/fallback recovery.

Record observed response delays rather than promising an exact universal number. A 30-second HA poll is not the thermostat's radio wake interval or the time required for a room to warm.

Use the [FRITZ schedule guide](https://fritz.com/en-fr/apps/knowledge-base/FRITZ-DECT-301/4354_Configuring-a-schedule-for-FRITZ-radiator-controls) and [temperature-adjustment guide](https://fritz.com/apps/knowledge-base/FRITZ-DECT-301/3422_am-fritz-heizkorperregler-gemessene-temperatur-anpassen) for the exact current UI procedure. If the site loads only a shell, report that retrieval limit and use the device UI/manual rather than inventing menu steps.
