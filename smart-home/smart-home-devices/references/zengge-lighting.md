# Zengge, LEDnet, LEDnetWF and RGB controllers

## Identify the protocol of each controller

The Zengge label and app name cover multiple protocols. Capture model label, app, whether the unit joins Wi-Fi, BLE advertisement name, chipset only if documented, controller firmware and LED strip type. Do not send an alternate LED driver configuration during discovery.

| Observation | Candidate path | Limit |
| --- | --- | --- |
| Wi-Fi controller using a supported Magic Home/Surp Life protocol | Core Magic Home (`flux_led`) | Compare the precise supported/unsupported model list |
| BLE advertisement such as LEDnet, BLE-LED, LEDBLE, Triones or listed aliases | Core LED BLE | The core page explicitly excludes LEDnetWF from the LEDnet family |
| LEDnetWF / supported Zengge BLE variant | Community `8none1/lednetwf_ble` | Check supported protocol and release; custom software is not equivalent to core support |
| Proprietary BLE mesh / other protocol | Verify a dedicated project and exact model | A BLE proxy does not automatically translate a proprietary mesh protocol |
| Controller intentionally running WLED | HA WLED | Stock Zengge firmware is not WLED; flashing requires verified hardware |

Magic Home offers local control for supported Wi-Fi devices. Core LED BLE supports several advertisement families sold under many brands, including some Zengge devices. Neither establishes brand-wide compatibility. [HA Magic Home](https://www.home-assistant.io/integrations/flux_led/), [HA LED BLE](https://www.home-assistant.io/integrations/led_ble/).

The LEDnetWF project documents supported Zengge-derived variants and protocol-specific behavior. Use it only after identifying a matching family; preserve its exact repository URL and release. [LEDnetWF BLE project](https://github.com/8none1/lednetwf_ble).

## Map light capabilities correctly

Record whether the strip is RGB, RGBW, RGB+CCT, tunable white, single-channel, or addressable. Voltage, current capacity, pin order, channel order and constant-voltage versus constant-current control are separate from HA compatibility. A wrong channel mode can make white/color control incorrect and can create a physical electrical problem; follow the actual strip/controller specification.

For each controller test on/off, dimming, red/green/blue, warm/cool white where supported, effects and restoration after power loss. Check whether changing an effect overrides normal color commands. For addressable strips record segment count/order; a single aggregate HA light does not prove per-segment capability.

## Diagnostics and changes

First use the existing vendor app to establish that the hardware works. Close active app control while testing BLE connection contention. Check receiver/proxy range and whether active connections are supported; advertisement reception alone does not prove a control session can be established. Test one controller rather than pairing all six to an unverified integration.

A historical core issue reported the legacy `zengge` YAML platform failing with a `bluepy` dependency on HAOS 2024.8.2, and closed as stale/not planned. Treat old `platform: zengge` tutorials as a migration clue, not a supported setup recipe. Do not install arbitrary Python packages into HAOS to revive that path. [Core issue 124083](https://github.com/home-assistant/core/issues/124083).

Before a custom integration upgrade, back up its config and note stable entity IDs. If the upstream guide calls for re-adding to discover metadata, map the entity impact first; deletion is not a harmless diagnostic. Preserve a working firmware/controller type and do not write protocol-driver settings merely to see what happens.

## Alternative design

If the exact stock protocol cannot provide required reliability or effects, compare a documented compatible controller rather than repeatedly changing software guesses. WLED is a separate local option for supported hardware; selection must match the strip's electrical and addressing requirements. Route firmware and MQTT design to `smart-home-esphome-mqtt`. A replacement proposal must include retained manual control, power supply compatibility and restoration behavior.
