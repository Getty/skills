# Lighting, schedules, and climate wrappers

## One policy owner

Draw the existing chain: physical control → bridge/device routine → HA entity → optional wrapper → automation. Identify which layer owns on/off, brightness, color, temperature, or scheduling. Avoid adding another controller before explaining how the current one yields.

## Adaptive Lighting

Use for supported lights needing time-dependent brightness/color behavior. Inspect the installed version's manual-control settings and the distinction between HA-originated commands and external changes. Detection settings can cause additional entity updates; do not enable every option by default. Test Hue dimmer, Hue app, HA scene, and manual switch separately. [Adaptive Lighting](https://github.com/basnijholt/adaptive-lighting).

For mixed-vendor groups, use capabilities common to the members or split the group. A device with only RGB is not guaranteed to behave like a tunable-white lamp. Preserve an explicit manual override and understandable resume action.

## Scheduler

Scheduler Card is the UI for Scheduler Component's backend entities. Installing the card alone does not create scheduling behavior. Compare native helpers/automations when the schedule is simple. Check how schedules interact with restart, disabled targets, and device-side weekly programs. [Card](https://github.com/nielsfaber/scheduler-card), [component](https://github.com/nielsfaber/scheduler-component).

## Thermostat wrappers

Better Thermostat combines room measurement and other inputs with supported TRV behavior, including calibration approaches. Verify the exact integration adapter and firmware; “climate entity exists” is insufficient. [Better Thermostat](https://github.com/KartoffelToby/better_thermostat).

Versatile Thermostat provides several actuator/control strategies. Select the correct mode and its requirements; an over-switch setup and over-climate setup have different control responsibility. Do not apply a valve-control strategy where the integration does not expose a real valve action. [Versatile Thermostat](https://github.com/jmcollin78/versatile_thermostat).

For FRITZ! 301/302, begin with one room, identify native schedule override semantics and update latency, and compare against existing local behavior. Keep the Control 440's actual exposed features separate from assumptions about button events. Route API/model facts to `fritzbox-operator`.

## Acceptance before scaling

Test steady state, manual intervention, window opened/closed, stale temperature, unavailable TRV, restart, bridge outage, and native schedule transition. Define safe fallback and one owner for restoring normal control. Report comfort/behavior observations; do not invent energy-saving percentages from installation alone.
