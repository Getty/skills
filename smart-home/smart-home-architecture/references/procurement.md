# Evaluate products sold on Amazon and elsewhere

## Resolve the actual variant

Treat the retailer listing as a lead. Record URL, marketplace/country, seller, selected variant, model number, regional socket/radio variant, included hub/accessories, and date. A listing may combine reviews for different hardware generations. An ASIN or product title alone does not establish the model shipped by every seller.

Write a requirement before searching: for example “local switching and power measurement, physical button, restore-off after outage, suitable for this load, exposed through the existing HA path.” Separate mandatory capabilities from convenience features and visual preferences.

Check the [Works with Home Assistant certified product list](https://works-with.home-assistant.io/certified-products/) for exact products and notes. Certification applies to listed variants, not every product from the brand. A generic Alexa/Google label is not a Home Assistant compatibility statement. For Zigbee, inspect the exact [Zigbee2MQTT device entry](https://www.zigbee2mqtt.io/supported-devices/) or ZHA support evidence; check required functions individually.

## Use a capability worksheet

| Dimension | Evidence to record |
|---|---|
| Identity | Retail model, firmware/hardware revision, manufacturer fingerprint, region |
| Functions | Switching, dimming/color, sensing, event types, measurement, calibration, restore behavior |
| Control path | Native local, local bridge, direct Zigbee, Matter, BLE, cloud, community component |
| Initial setup | Account/app/hub/phone requirement, credentials or binding key |
| Offline operation | Tested functions, cloud failure behavior, local schedule and manual control |
| Maintenance | Supported updater, release history, upgrade caveats, configuration export |
| Household use | Physical controls, noise, size, battery, installation constraints |
| Electrical/environmental suitability | Manufacturer rating for the actual load/environment; resistive nameplate rating is not a universal motor/inrush rating |
| User experience | Dated matching-model positive and negative firsthand accounts, later resolution |
| Exit | Re-pairing/reset effort, loss of vendor features, alternate integration, account deletion implications |
| Commercial terms | Current price, delivery, seller and return terms, subscription, accessory costs |

Refresh price/stock/terms immediately before a concrete recommendation. Do not put a timeless “best on Amazon” badge on a changing listing. Avoid speculative discount forecasts.

## Expand by household function

Use `smart-home-devices` family maps for lighting, plugs/relays, heating/AC, meters/EV/solar, covers/locks, environmental and presence sensing, appliances, cleaning and garden devices. Use `smart-home-video-media` for cameras, doorbells, TVs and audio. Include built-in building systems through KNX/Modbus/gateways where relevant; an Amazon catalog is not the boundary of useful automation.

Compare two or three technically distinct paths if needed: preserve a native hub; add a supported direct-radio device; or add a local IP device. Do not force a new mesh for one optional sensor without accounting for its controller and upkeep.

## Buy one, prove it, then expand

For a batch replacement, validate one sample with the required firmware and integration first. Run the actual button/measurement/restore tests. Save exact identity, settings and observations. Confirm later deliveries match that revision before applying the result to the whole batch.

Return one of: supported for the required features; supported with explicit losses/dependencies; plausible but needs a sample test; or unsuitable for the stated requirements. Unknown evidence should not become a positive compatibility claim.
