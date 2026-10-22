# Paulmann

Paulmann Licht GmbH sells mostly non-smart lighting; its smart range is a **Zigbee 3.0 (Lightlink)** line plus a separate legacy Bluetooth line. **smik** is the Zigbee gateway and app (50135), not a luminaire system; **Plug & Shine** (24 V outdoor) and **URail** (230 V track) are electrical systems that gain Zigbee through specific controllers or lamps. Separate the smart controller from power supplies, rails and passive lamps. Research baseline 2026-10-22.

## Product range

| Line / family | Device classes (article examples) | Radio | HA route(s) | Key caveat |
| --- | --- | --- | --- | --- |
| Smart Home Zigbee lamps and luminaires | E27/E14/GU10 bulbs (4137, 291.45, 291.46, 291.48, 50394 filament), Coin modules (929.60, 929.63, 929.66, 924.70), panels/pendants (Amaris, Puric pane, Aptare 500.45), house-number light | Zigbee 3.0 router | ZHA, Z2M, Hue Bridge, smik | Many share generic model IDs (`RGBW`, `CCT`, `RGBWW`); Z2M separates them by `softwareBuildID` |
| Zigbee LED stripe controllers | MaxLED RGBW 500.47 / tunable white 500.46, YourLED RGB 500.49 and dim/switch 500.48, SimpLED 150257, Cephei switch controller 50043, dimmer/stripe 50044/50045 | Zigbee 3.0 router | ZHA, Z2M, Hue | Controller output must match strip voltage/channels |
| Plug & Shine 24 V outdoor | Plug & Shine Zigbee controller 93999, RGBW LED strip 94191, spot Shira 94849, Smart Plug Outdoor 50138 | Zigbee 3.0 | ZHA, Z2M, Hue, smik | 50138 switches a whole non-smart run on/off and cannot use Touchlink — needs a gateway/coordinator |
| URail 230 V track | rail/spot adapters On/Off/Dimm (96893, 95524, 95676, 95677; Z2M 968.93), Zigbee mid/cable feed-in, Dimm/Switch section adapter, URail power supply 500.44 | Zigbee 3.0 | ZHA, Z2M, Hue, smik | Adapter max 50 W, only for continuously dimmable lamps; with a Zigbee bulb use the non-Zigbee feed |
| Actuators and plugs | Smart Plug 50131 (on/off, stays off after power loss), Unterputzaktor / universal switch 50139, relay controller 500.43 | Zigbee 3.0 | ZHA, Z2M | 50139 is a Tuya `TS000F` OEM module; wiring per manual A1 |
| Remotes, switches, sensors | Gent 50067, Gent 2 50140, Basic Remote 50141, Smart Switch 50134/50137, motion indoor 50133/50150, outdoor 50136, outdoor motion detector 94842, twilight/motion sensor 18012, Skyla CCT-I with sensor | Zigbee 3.0 end devices | Z2M (all listed above incl. 50140/50141/50134); ZHA quirk for 501.34 | Touchlinked remotes control lamps directly; HA may see no events. 18012 is Touchlink-only by design |
| smik gateway | 50135 + smik app; cloud for remote, Alexa/Google | Zigbee 3.0 Lightlink, channel 11; LAN | none direct — proprietary | Paulmann: not for Zigbee2MQTT; one gateway per app; cloud limit 30 000 accesses/week |
| Smart Friends Box (legacy) | 50066 | Zigbee + others | none | No further Paulmann support |
| Paulmann Bluetooth line | lamps, controllers, Boss remote | Bluetooth, app-local | none verified | Paulmann app only, no smart speakers, no third-party control; app reported withdrawn from stores — verify |
| Matter | — | — | — | Paulmann FAQ: Matter is being evaluated, none offered |

Compatibility claims: Paulmann states its Zigbee products are "Zigbee certified und bereit für Philips Hue" and work with Hue Bridge 2 and Pro (excluding Hue Entertainment), Amazon Echo with Zigbee, smik and MagentaZuhause. That is a compatibility claim, not a Hue certification; Hue does not expose these third-party devices to HomeKit.

## Identify the line from the label or model ID

- **Article number**: 5 digits on box/label (50131, 94849, 96893); Z2M often writes it dotted (`501.31`, `968.93`). Some Zigbee items report 9-digit IDs (`371000001`, `371232040`).
- **Zigbee manufacturer strings**: `Paulmann Licht GmbH`, `Paulmann Licht`, `Paulmann lamp` (some with trailing space), `Paulmann LichtGmbH` (ZHA quirk). A Paulmann product can also report an OEM identity: 50139 reports `TS000F` / `_TZ3210_hjxqqofs` plus a NUL byte.
- **Zigbee model IDs** take several forms: article number (`50131`, `501.37`, `94842`), OEM module code (`H036-0001` P&S controller, `H036-0005/-0006/-0007` Coin modules, `H036-0500` URail adapter) or a generic type (`RGBW`, `CCT`, `Dimmablelight`, `RGBW Controller`). Generic IDs need manufacturer string and build ID before choosing a converter.
- **Chip generation**: after reset, newer Telink-based products light cold white, older NXP-based ones warm white (Paulmann FAQ) — useful when two units of one article behave differently.

## Routes

| Route | Use | Limits |
| --- | --- | --- |
| Z2M | Broadest exact definitions (lamps, controllers, URail, P&S, remotes, 50139) | Compare raw fingerprint with the converter |
| ZHA | Lamps/controllers as standard Zigbee lights; quirk for 501.34 four-button switch | Remote events beyond 501.34 may need checking |
| Hue Bridge | Lamps and controllers as third-party lights | No Paulmann sensor/switch configuration; no Entertainment |
| smik gateway + app | Paulmann scenes, routines, HCL cycle, configuration of 50134/50136 | No local API to HA; accessories are programmed specifically for smik |
| Touchlink remote only | Gateway-free control | Invisible to HA unless the remote is also joined |

## Commissioning and reset

Lamps and controllers stay in pairing mode for 3 min after power-on. Reset: power-cycle 5× (2–3 s off, 1–2 s on); the light pulses ~10 s then comes up 100 % white. Plug & Shine spot 94849: 5× with 5 s off / 2 s on, ends warm white 2000 K. Plug 50131: hold button 5 s. Basic Remote 50141: On/Off + "+" 3×. Smart Switch 50134: both lower keys 3×. smik 50135 button 5× within 10 s deletes all paired devices. Lamps recall brightness/colour after power loss but always come back **on**; Paulmann says this cannot be changed, yet Z2M exposes a startup setting on some models (929.66) — test before relying on either. Repeated power cycling can reset neighbouring lamps on the same circuit — isolate the test device.

## Worked examples

**Coin module 929.66**: Z2M exposes dimming, colour temperature, colour and startup behaviour. This does not establish the same capabilities for any outdoor controller or URail product. [Paulmann 929.66](https://www.zigbee2mqtt.io/devices/929.66.html).

**Universal switch 50139**: a **2025-02-04** issue reported a fully interviewed unit still unsupported because its signature was `TS000F` with `_TZ3210_hjxqqofs…`. [Z2M issue 26186](https://github.com/Koenkk/zigbee2mqtt/issues/26186). The current converter source maps that fingerprint to `501.39`; confirm the installed Z2M release contains it. A Tuya identity under a Paulmann label is OEM sourcing, not proof of a counterfeit; do not widen a converter to all `TS000F` devices without checking endpoints and electrical function.

## Migration and buying checks

Capture article number, existing bridge and raw Zigbee signature. Decide whether smik scenes, sensor settings and Touchlink remotes must be kept. Move one endpoint, recreate its user-facing functions, then decide on the rest. Do not open or flash smik for an unverified interface. For outdoor faults, separate radio dropout from voltage drop, undersized supply, wet connectors or an incompatible dimmer.

For purchases require article number, protocol (Zigbee vs Bluetooth), compatible supply, HA route and the needed feature. "Works with Alexa" may mean the smik cloud skill rather than direct Zigbee; a Zigbee logo is transport evidence, not proof of every setting.
