# Dashboards and energy

## Design for household decisions

Start with native cards and views. Make common controls easy to find: current room mode, override, target/actual temperature, light scene, alarm acknowledgment, and unavailable devices. Keep engineering diagnostics in a separate view. Core dashboards support visual construction and custom cards when needed. [Dashboards](https://www.home-assistant.io/dashboards/).

Do not depend on a custom frontend for the only emergency/manual control. Card visibility is presentation, not an authorization boundary. A hidden actuator may still be callable through another surface.

## Good display semantics

Show unknown/unavailable as such. Avoid green “healthy” badges based on missing values defaulting to zero. Show the timestamp/freshness where decisions depend on it. Distinguish desired setpoint, measured room temperature, and observed heating action.

Use HACS references when a native card cannot express the requirement: Mushroom/Bubble for presentation, auto-entities for dynamic lists, ApexCharts for analysis. Keep graph horizons and point counts bounded on wall tablets.

## Energy accounting

Map each meter's physical boundary: whole-home import/export, generation, battery, circuit, or plug. Avoid counting the same energy twice. Record units, device class, state class, reset behavior, and whether a value is a real counter or derived from sampled power.

Current Energy documentation covers both power and energy inputs with their appropriate metadata, and statistics errors can keep entities out of selection lists. Inspect the installed field requirements rather than relying on old blanket claims that every input must be an energy counter. [Energy FAQ](https://www.home-assistant.io/docs/energy/faq/).

For Shelly/Third Reality outlets, confirm exact model metering capabilities and load ratings. A working relay does not imply a reliable energy counter. Lost power samples limit numerical integration; a device's accumulated counter may recover totals differently after downtime. Preserve that distinction in reports.

## Verification

Compare a known appliance cycle with the physical meter or manufacturer UI where possible. Inspect resets, unit conversion, daylight-saving boundaries, and duplicated aggregate totals. Do not call HA telemetry a billing-grade measurement without evidence of the metering system's actual certification and use.

For dashboard issues, compare backend state, a native card, the custom resource version, and browser behavior. Validate actionable controls on the actual touch device; hover-only behavior and tiny targets often fail household use.
