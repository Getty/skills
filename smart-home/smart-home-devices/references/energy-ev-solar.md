# Energy meters, solar, batteries and EV charging

Research baseline: 2026-10-22. Separate observation, accounting and control. An energy dashboard that looks correct does not prove the meter's direction, scaling or control safety. Identify inverter, gateway, meter and firmware independently.

## Family and route map

| Product family | Candidate HA route | Local/cloud and exact-device limit |
| --- | --- | --- |
| Shelly EM/3EM/Pro energy-meter families and metering relays | Core `shelly` using generation-specific API | Local path; exact channels, CT type, phase mapping and energy counters vary. Plus Plug S is an appliance plug, not a whole-house meter. See `shelly.md`. |
| Compatible DSMR/P1 meters and reader hardware | Core `dsmr` and supported serial/network reader | Local reader and region-specific telegram format. A German optical/SML meter is not automatically a DSMR device. [HA DSMR](https://www.home-assistant.io/integrations/dsmr/) |
| German optical/SML or pulse meters with appropriate reader | Exact reader integration, ESPHome or MQTT | Verify meter interface, optical polarity, protocol, PIN/readout permissions and counter identifiers from actual documentation. Route firmware to `smart-home-esphome-mqtt`. |
| Fronius inverters, Datamanager/Datalogger, meters and storage reported through SolarAPI | Core `fronius` | Local SolarAPI. GEN24 firmware from 1.14.1 needs the SolarAPI setting enabled; verify gateway and API availability. Modbus writes are a separate capability. [HA Fronius](https://www.home-assistant.io/integrations/fronius/) |
| Supported SMA solar, meter and battery devices | Core `sma` | Local device API for documented hardware; credentials and user/installer roles matter. Do not assume every Sunny-branded product uses the same interface. [HA SMA](https://www.home-assistant.io/integrations/sma/) |
| Tesla Powerwall with compatible local gateway | Core `powerwall` | Powerwall 2 is documented; Powerwall 3 has limitations and Powerwall 1 is not supported here. Account or fleet integrations are separate paths. [HA Powerwall](https://www.home-assistant.io/integrations/powerwall/) |
| MyWallbox-compatible EV chargers | Core `wallbox` | Cloud data/control via MyWallbox; exact model and login method matter. A working cloud entity does not establish local load balancing. [HA Wallbox](https://www.home-assistant.io/integrations/wallbox/) |
| Multi-vendor chargers, cars, meters and solar systems supported by evcc | evcc as the charge controller, HA via custom `ha-evcc`, REST or MQTT | Check every hardware template and its dependencies. HA App installation and HA integration are different components. [evcc HA guide](https://docs.evcc.io/en/smarthome/home-assistant/) |
| Tibber prices, account statistics and Pulse data | Core `tibber` | Cloud account/service; separate tariff data from local electricity measurement and charger control. [HA Tibber](https://www.home-assistant.io/integrations/tibber/) |
| Other inverter/charger brands, including OCPP/Modbus/SunSpec candidates | Manufacturer's exact integration or explicitly supported protocol implementation | A protocol logo does not give a register map, authentication, writable limits or a compatible OCPP profile. Read the hardware/firmware manual and current integration support before promising support. |

For broad shopping research, use these as interface families and then enumerate the actual regional models. Do not substitute a neighboring inverter, a different dongle or a gateway from another generation merely because the vendor name matches.

## Define measurements before dashboard configuration

Record each source's physical boundary: whole property, grid connection, inverter AC output, battery, EV circuit or an individual plug. Also record unit, sign, phase mapping, timestamp, refresh interval, counter persistence and whether values are instantaneous or cumulative.

| Quantity | Interpretation to verify | Common category error |
| --- | --- | --- |
| Power in W/kW | Current rate of energy flow | Treating a power value as a kWh counter |
| Energy in Wh/kWh | Accumulated flow over a defined period | Combining a reset-at-midnight value with a lifetime counter without understanding resets |
| Grid import/export | Direction at the grid boundary | Negating the wrong source or counting inverter output twice |
| Battery charge/discharge | Separate flow directions and reference point | Treating state of charge percentage as stored energy without capacity/model assumptions |
| EV delivered energy | Charger session/lifetime boundary | Equating charger-side energy with energy retained in the traction battery |
| Cost/price | Currency, interval, taxes/fees and chosen tariff source | Multiplying the wrong time interval or presenting a forecast as a bill |

The [HA Energy documentation](https://www.home-assistant.io/docs/energy/) distinguishes energy from instantaneous power and links the integration method for deriving energy from power. Prefer a trustworthy device energy counter when available. If integrating sampled power, document sample gaps and the integration method. Inspect entity metadata and statistics warnings before treating the chart as evidence.

## Acceptance procedure

1. Use read-only access first. Record the source's own display/web UI at the same time as HA; compare the same boundary and interval.
2. Observe a known change under normal operating conditions: an appliance switching on, solar rising or EV charging. Check direction and scale rather than requiring a perfect theoretical value from a variable load.
3. Check all phases/channels and counter persistence across an ordinary device restart. Do not reset billing or historical counters to make a chart appear clean.
4. Inspect missing data and unavailable states. A repeated last value is not a fresh measurement; do not use it for rapid control without age checks.
5. Reconcile a longer interval with the physical meter using matching timestamps. State any measurement or aggregation differences.
6. Add the source to HA Energy with its correct role. Avoid double-counting subcircuits as additional grid import.

## Control ownership and evcc

The evcc project documents a custom `ha-evcc` integration, manual REST/MQTT alternatives and the ability to consume HA entities. Choose one clear controller for charging policy. HA can provide a requested mode, schedule or presence input while evcc manages charging, or another arrangement can be chosen deliberately. Avoid two loops alternately writing charger current or battery modes. [evcc HA guide](https://docs.evcc.io/en/smarthome/home-assistant/)

Before enabling writes, record the hardware's limits, existing local load balancing, response to stale measurements and loss-of-controller behavior. A successful API call does not verify the installation's electrical capacity. Keep device-local protections intact. Use the current manufacturer's documentation for writable settings and qualified electrical work when the task involves wiring or installation changes.

For tariff optimization, account for departure deadline, required charge, battery state uncertainty and service outages. Do not present speculative cost savings as measured results. Log requested settings and observed device behavior so conflicting controllers can be diagnosed.

## Troubleshooting order

For no entities: exact model/API support, enabled interface, credentials, network. For wrong values: units/scaling, phase/channel, sign, source boundary, timestamps. For gaps: polling limits, cloud outages, gateway sleep/restart, recorder/statistics. For rejected commands: user role, vendor operating mode, conflicting controller and writable capability. Only then consider a firmware change, after preserving settings and checking the exact release notes.
