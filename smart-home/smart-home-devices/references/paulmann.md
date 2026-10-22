# Paulmann

## Keep the product number and system boundary

Paulmann's range includes bulbs, recessed LED modules, strips/controllers, URail components, Plug & Shine outdoor equipment, actuators, remotes, sensors and the smik gateway. Distinguish non-smart electrical components from the smart controller that operates them.

| Family | Candidate path | Required evidence |
| --- | --- | --- |
| Zigbee lamps, Coin modules, LED strips/controllers | Direct ZHA/Z2M or supported existing bridge | Exact article number and Zigbee signature |
| URail smart adapters/controllers | Exact Zigbee device entry | Supply/load compatibility and dimming behavior |
| Plug & Shine | Identify smart controller separately from lamps/power supply | Radio variant, outdoor rating, cable/voltage budget |
| Gent/Basic remotes and wall switches | Exact Zigbee event/binding behavior | A paired remote may control lights directly without HA events |
| In-wall actuators | Exact model/firmware/converter | Neutral/wiring, relay/dimmer mode and installer requirements |
| smik gateway | Manufacturer's documented interfaces | It is not a drop-in Zigbee2MQTT coordinator |
| Bluetooth or future Matter-branded products | Verify actual product documentation | Do not infer support from other Paulmann families |

Paulmann explicitly states that smik uses proprietary software and is not intended for integration through Zigbee2MQTT. Its supported Zigbee child products can be assessed for direct pairing to another coordinator; these are different designs. The same FAQ documents differences in remote and actuator pairing behavior. [Paulmann compatibility and support](https://de.paulmann.com/smart-home/kompatibilitaet/).

As a concrete example, Z2M's **929.66** page exposes dimming, color temperature, color and startup behavior for that LED module. This does not establish the same capabilities for every outdoor controller or URail product. [Paulmann 929.66](https://www.zigbee2mqtt.io/devices/929.66.html).

## Integrating the installed unspecified devices

Capture label/article number and the existing bridge or ZHA/Z2M signature. Decide whether preserving smik scenes, vendor sensor settings and remotes is required. If migrating, move one endpoint and recreate the user-facing functions before deciding to move the rest. Do not open or flash smik to pursue an unverified interface.

Test brightness transitions at low output, on/off restoration, available color modes and remote actions. For outdoor lighting, separate radio dropout from voltage drop, insufficient power supply, wet connectors or an incompatible dimmer; software cannot correct a physical supply mismatch.

## Exact fingerprint matters even for a named brand

A **2025-02-04** issue for **50139** reported a successfully interviewed unit that was still unsupported because its signature contained a `_TZ3210_…` manufacturer variant. The report identified `TS000F`; the issue is closed, but the captured record alone does not establish the release containing a fix. [Z2M issue 26186](https://github.com/Koenkk/zigbee2mqtt/issues/26186).

Operational implication: compare the actual manufacturer string and installed converter. Do not conclude that the user bought a counterfeit solely because the Zigbee identity differs from the retail brand. Do not edit a global converter to match all `TS000F` devices without checking electrical functions and endpoints.

## Feature verification

For a purchasing comparison, require article number, protocol, compatible power supply, HA route and the specific feature needed. “Works with Alexa” may describe a cloud skill or a gateway path rather than direct local HA support. A Zigbee logo is useful transport evidence but not proof of every manufacturer-specific setting.

Keep reset sequences model-specific. Repeated power cycling can reset neighboring lamps or disrupt the network; isolate the test device and retain physical lighting control.
