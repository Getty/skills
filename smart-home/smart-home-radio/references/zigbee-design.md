# Design a Zigbee network

## Identify roles and boundaries

| Role | Operational implication |
|---|---|
| Coordinator | Creates/manages the network; one stack owns its serial or network endpoint |
| Router | Forwards packets; normally continuously powered, but verify the exact product's role |
| Sleepy end device | Conserves battery and communicates through a parent; cannot be treated like an always-awake relay |
| Application group/binding | May allow local interaction when supported by both endpoints; verify behavior with HA stopped |
| Separate network | Hue bridge, ZHA and Zigbee2MQTT meshes remain separate even inside one house |

The official [ZHA introduction](https://www.home-assistant.io/integrations/zha/) describes its coordinator/device model. Use exact [Zigbee2MQTT device definitions](https://www.zigbee2mqtt.io/supported-devices/) to determine supported behavior and quirks.

Inventory direct-paired plugs and bulbs separately from bulbs behind a Hue bridge. Only devices on the same mesh can assist that mesh. Do not count router network host records as a Zigbee device total.

## Plan placement before firmware

Put a USB radio away from the host, USB 3 storage, HDMI and strong nearby transmitters using a suitable extension. Prefer a documented supported coordinator. For a remote coordinator, a wired Ethernet path avoids Wi-Fi jitter in serial-over-TCP transport. These are documented considerations in [network stability](https://www.zigbee2mqtt.io/advanced/zigbee/02_improve_network_range_and_stability.html) and [supported adapters](https://www.zigbee2mqtt.io/guide/adapters/); they do not prove the cause of every dropout.

Place stable routers to bridge difficult rooms and floors. Do not depend on a bulb residents routinely disconnect at the wall as the sole router for an important sensor. Verify both directions of communication: increasing coordinator transmit power cannot make a weak battery device transmit more strongly.

Choose channels after recording nearby 2.4 GHz Wi-Fi, existing Zigbee networks and Thread. Evaluate interference, device/channel support and migration cost; do not prescribe one universally best channel. Avoid changing Wi-Fi and Zigbee channels simultaneously because the experiment becomes uninterpretable.

## Measure the useful signals

| Signal | What it can tell you | What it cannot establish alone |
|---|---|---|
| Last-seen/report age | Recent observed communication | Whether a sleeping sensor should have reported sooner |
| LQI/RSSI | Quality of an observed link at that moment | Whole-path quality, physical distance or a universal pass threshold |
| Failed interviews | Pairing/application-exchange problem | Whether reset, more routers or a converter is the correct fix |
| Route/topology map | Observed neighborhood and routing clues | A continuously accurate physical topology |
| Latency/lost test events | User-visible reliability for a defined experiment | Long-term failure probability from a small test |

Keep a dated map of coordinator, routers, power sources and problematic areas. If only one manufacturer's sleepy sensors fail, inspect parent compatibility/reporting before replacing the entire coordinator.

## Capacity and maintenance

Do not promise a device limit from the radio chipset name. Effective capacity depends on firmware, child/routing tables, traffic, reporting frequency and application stack. Remove needless rapid polling and repeated writes before adding hardware.

Capture firmware, network backup, coordinator identity and recovery instructions. Schedule migrations separately from routine troubleshooting. A forced re-pair can hide a problem temporarily while destroying useful diagnostic evidence.
