# Product families, radio roles, and expansion

## Family catalogue and capability boundaries

Use this as a research index, not an exhaustive SKU catalogue. Refresh the official product listing and the precise article number when making a purchase recommendation.

| Family | Relevant examples | Integration question |
| --- | --- | --- |
| Radiator controls | Legacy DECT 300/301; Thermo 302; announced Thermo 303 | Valve fit, firmware, schedule/group behavior, supported climate attributes |
| Plugs | DECT/Smart Energy 200, 210; announced Energy 201 | Country plug, permitted load/use location, metering, switch behavior after outage |
| Optical electricity reader | Smart Energy 250 | Exact meter model/protocol, enabled optical output, available import/export registers |
| Buttons and contacts | DECT 400, Control 440, Control 350 | Native action vs polled measurement vs actual HA event support |
| Lighting | DECT 500; supported third-party Zigbee/HAN FUN lamps | Brightness/color capabilities and exported functions differ |
| Smart-home base/bridge | Smart Gateway; selected FRITZ!Box models with integrated Zigbee/Matter roles | Actual radios, firmware, pairing location, exported endpoints |
| Home networking | DSL, Cable, Fiber, mobile, and Ethernet-WAN FRITZ!Boxes; Repeaters; Powerline | WAN medium, switch/AP topology, TR-064 exposure, mesh role |
| Telephony | FRITZ!Fon, compatible handsets, DECT Repeater 100 | Telephone DECT role is separate from ULE smart-home compatibility |

The current [smart-home catalogue](https://fritz.com/collections/smart-home) covers plugs, metering, heating, contact/button controls, and gateways. The [September 2026 manufacturer announcement](https://about.fritz.com/en/press/press-releases/2026/09/fritz-makes-the-digital-home-future-proof-new-fritzbox-genera-tion-and-more-power-for-fiber-optics-5g-mesh-wi-fi-and-the-smart-home) discusses Energy 201, Thermo 303, new router names, and FRITZ!OS 8.50. An announcement, planned launch, API schema entry, and an available regional retail SKU are different evidence. Check shipping status and support at purchase time.

For Energy 250, use the manufacturer's [meter setup and compatibility resource](https://fritz.com/pages/stromsensor). Do not infer compatibility merely because a meter is digital or has a visible LED. Confirm whether a PIN or output activation is necessary for the desired registers. An HA energy dashboard needs cumulative energy with appropriate units and statistics metadata; a current-power reading alone is insufficient.

## Keep the radio systems separate

| Layer | What it means | What it does not establish |
| --- | --- | --- |
| DECT telephony | Handset-to-telephone-base communication | ULE repeatability, Zigbee, or HA event support |
| DECT ULE / HAN FUN | Smart-home radio plus supported application functions | Universal interoperability with every DECT-branded device |
| Zigbee | A separate coordinator and device network | Automatic pairing to any FRITZ!Box merely because it is a FRITZ!Box |
| FRITZ Wi-Fi Mesh | Coordinated AP/repeater Wi-Fi functions | A common mesh for DECT, Zigbee, Thread, and Wi-Fi |
| Matter bridge | Exports supported non-Matter device functions into a Matter fabric | A universal Matter controller, Thread border router, or complete vendor API |

The [Smart Gateway technical specification](https://fritz.com/en/products/fritz-smart-gateway-20003012) identifies Zigbee 3.0 and DECT ULE/HAN FUN, a Wi-Fi or Ethernet uplink, and a Matter bridge. Its Wi-Fi is an uplink, not a Wi-Fi extender or client AP; its DECT radio does not register telephone handsets. Its listed prerequisite is a DECT-capable FRITZ!Box with FRITZ!OS 7.50 or newer. Check more specific firmware requirements for individual later functions.

Do not assume a DECT Repeater 100 extends every thermostat, contact, or button. Verify the exact device's repeater compatibility in its manual/knowledge base. If the device is not supported through a repeater, investigate base placement or a supported additional smart-home base instead. The [manufacturer's thermostat/repeater resource](https://fritz.com/apps/knowledge-base/FRITZ-Smart-Thermo-302/1362_fritz-heizkorperregler-mit-dect-repeater-einsetzen) is model-scoped; if its body fails to load, record that retrieval limitation rather than inventing its contents.

## Zigbee and third-party interoperability

Use the [FRITZ Zigbee compatibility list](https://fritz.com/pages/zigbee) to check model and firmware. A Hue, Paulmann, or OSRAM/Ledvance name in a catalogue does not cover the entire brand, and a successful pairing does not prove all features reach HA. For HAN FUN or third-party DECT, check the actual function units and HA mapping; Comet DECT and RolloTron DECT are examples in HA's tested list, not a blanket approval of every related model.

For an existing Zigbee device, compare three concrete routes:

1. Its existing vendor bridge and native HA integration.
2. An HA-owned ZHA or Zigbee2MQTT network, with the exact device fingerprint supported.
3. A compatible FRITZ Zigbee base, followed by native FRITZ API or verified Matter export.

A Zigbee endpoint normally belongs to one coordinator network. Moving it may require reset/re-pairing and may change entity identities, group membership, scenes, firmware-update paths, and button events. Document those consequences before moving a working device just to reduce hub count. See `smart-home-radio` for network migration.

## Matter with FRITZ and HA

The current [official Matter overview](https://fritz.com/pages/matter-mit-fritz) names both the FRITZ!Box 5690 Pro and Smart Gateway as Matter bridges. An older statement that only the Gateway can bridge is stale. Conversely, this does not establish Matter bridging on an older cable model such as the 6591 or on every new FRITZ!Box.

Verify the deployed bridge firmware, commissioning UI, HA Matter controller, network reachability, and exported endpoint/cluster list. Compare the desired features: a temperature setpoint, relay, metering register, contact state, and physical button event are distinct capabilities. Do not infer Control 440 button support from the manufacturer's general interoperability wording. Prefer the route that exposes the required function with an operable recovery plan. Avoid duplicate automation triggers when the same physical device appears through native FRITZ and Matter paths.

## Procurement and maintenance workflow

Record exact article number, region, radio, firmware baseline, base/bridge, HA integration and release, required entities/events, offline behavior, replacement path, and dated primary evidence. Add firsthand user reports as contextual evidence, including unsuccessful experiences and any commercial relationship. Check an Amazon listing's model/variant against the manufacturer record; seller keywords and review aggregation do not prove device identity or HA support.

For a new or unlisted model, perform a read-only capability check before recommending migration of the installed fleet. Preserve the proven 301/302 heating path while evaluating a different thermostat in one room. Revisit the decision after firmware changes or relevant integration releases, rather than treating a one-time shopping list as a permanent compatibility database.
