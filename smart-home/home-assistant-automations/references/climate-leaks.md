# Climate and protective actions

## Thermostat ownership

Map measured room temperature, TRV's local temperature, setpoint, HVAC mode, observed heating action, valve information if actually exposed, schedule, and battery. A generic climate domain lists possible actions; each integration implements a subset. [Climate](https://www.home-assistant.io/integrations/climate/).

For FRITZ! 301/302, compare the router schedule, device overrides, and HA automation. Choose one active policy or explicitly define override duration. Do not keep writing setpoints to fight a vendor schedule. Sleepy/battery devices and bridges introduce latency; polling faster cannot guarantee immediate valve movement. Exact API capabilities belong in `fritzbox-operator`.

An external room sensor can improve the location of a measurement, but it introduces freshness and failure dependencies. Define maximum acceptable age and fallback. Calibrate one room empirically before applying offsets to every radiator. Do not claim an arbitrary control algorithm reduces energy by a particular percentage.

## Controllers

Generic Thermostat is a sensor-plus-switch controller, not a universal wrapper around any existing climate entity. [Generic Thermostat](https://www.home-assistant.io/integrations/generic_thermostat/). Better Thermostat and Versatile Thermostat offer different higher-level strategies; evaluate the precise actuator adapter and mode through `home-assistant-hacs`. Never run competing wrappers over one TRV.

For windows, use debounce and explicit resume behavior. A lost door-contact report must not indefinitely disable frost protection. Distinguish comfort reduction from disabling all heat. Preserve native equipment protections and minimum cycle timing where applicable.

## Leak detection

Treat detection, local alarm, message delivery, and shutoff as separate paths. A Shelly Flood or other battery sensor can sleep between reports; last-seen age alone is not an alarm. Check the device's wake/report behavior and physical test method.

Design a latch: wet detection raises a persistent incident, notifies through the required channel, optionally performs an explicitly authorized validated shutoff, and waits for a deliberate recovery procedure. Do not automatically reopen a water valve merely because a sensor dries or HA restarts. Verify valve position feedback if available, and report its absence.

## Validate without inventing hardware tests

First test logic with a helper/test entity. Then perform the manufacturer's safe physical sensor test and observe the real event, notification, and any separately authorized actuator. Test unavailable inputs, battery low, internet loss, HA restart, and manual override. Keep certified/local protective systems independent of HA's best-effort availability; do not promise HA substitutes for them.
