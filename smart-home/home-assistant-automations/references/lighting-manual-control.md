# Lighting and manual control

## Assign ownership

For each room, name the normal controller: Hue Bridge scene/routine, HA motion logic, Adaptive Lighting, or a physical dimmer. Define when another controller takes over, which attributes it owns, and how automatic behavior resumes. Brightness, color temperature, color, and power state can have different owners.

A retained Hue Bridge keeps its own routines and accessories; direct Zigbee migration changes that ownership and pairing. Do not remove a working bridge just to reduce device count. Use `smart-home-devices` for the exact Hue route.

## Respect people

Use an explicit automatic-mode helper or a bounded manual-override deadline. Explain it with a visible control. Do not infer every context-less state change was human: firmware reports, bridge routines, and integrations may not carry the same context chain. Test the physical button, vendor app, HA dashboard, and voice separately.

For motion lighting, distinguish occupied, recently occupied, unknown sensor, manual-on, and automatic-on. A light left on intentionally should not necessarily follow the same off timer as an automated session. A motion sensor is not continuous proof that nobody remains seated.

## Control efficiently

Use room/group-level commands where they preserve required behavior and reduce traffic, but verify whether groups are native protocol groups or HA fan-out. Keep transitions modest for the target hardware. Avoid repeated per-second brightness writes when a device supports its own transition. Read state feedback before treating retries as safe.

Adaptive Lighting supports manual-control handling and distinguishes relevant brightness/color behavior in current versions. Its change-detection options can alter polling and ownership; read the installed version's documentation. [Adaptive Lighting](https://github.com/basnijholt/adaptive-lighting).

## Concrete mixed-vendor procedure

Start with one Hue light and one non-Hue controller. Test on/off, dimming, color/white modes, transitions, and state feedback. Select a common scene that both actually support; do not send an unsupported RGB/temperature mode because a generic light entity exists. Add a physical manual override before scaling to all rooms.

For Zengge/Govee/Paulmann products, require exact protocol/model mapping; brand or app name does not guarantee equal scene/effect support. Keep effects that only exist in vendor cloud separate from locally controllable brightness/color.

## Acceptance

Test manual changes during an active routine, power loss, unavailable sensor, repeated button events, an HA restart, and bridge-only operation. Use a native dashboard card as a control case when tap/hold behavior appears wrong. Preserve a simple accessible scene even if a custom dashboard fails.
