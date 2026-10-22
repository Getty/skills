# Z-Wave, EnOcean and legacy RF

## Z-Wave

Use HA's [Z-Wave integration](https://www.home-assistant.io/integrations/zwave_js/) with the appropriate Z-Wave JS server. Distinguish the integration, server/app and radio. Z-Wave JS UI is an alternative server-management surface; do not start two servers against one serial controller.

Verify controller and device region, firmware, S2/SmartStart support, security keys and recovery method. Region cannot be inferred from a seller's shipping destination. Choose the correct device variant before ordering. Do not assume imported radios can be made compliant by changing a software label.

During inclusion, verify the intended device and security information. For an already paired device, use documented exclusion/re-inclusion rather than arbitrary factory resets. Sleeping nodes require their documented wake procedure for configuration changes. Record values before modifying parameters and verify exact units and range.

For migration, back up controller NVM and server/application state as documented for the specific radio generations. A network-key list does not replace an NVM backup. Keep the old controller disconnected after migration and test a secure device, sleepy node and actuator. Check current [controller support](https://www.home-assistant.io/docs/z-wave/controllers/) for Long Range and regional capabilities instead of assuming every 800-series device supplies every mode.

## EnOcean

The [EnOcean integration](https://www.home-assistant.io/integrations/enocean/) supports selected devices and profiles through a compatible controller. Match the exact equipment profile and region. Energy harvesting can remove a battery requirement, but HA support still depends on decoding the telegram and representing its functions.

Capture real button telegrams before writing automations. A press and release are distinct signals; verify repeat behavior, dimming and scene semantics. Do not treat an unknown profile as a network-range problem.

## Proprietary 433 MHz and other sub-GHz devices

The [RFXtrx integration](https://www.home-assistant.io/integrations/rfxtrx/) is a defined hardware/protocol path, not a universal receiver for every device on that frequency. Determine modulation, protocol, transceiver firmware, device ID and whether the original remote uses rolling codes or encryption. Do not infer transmit capability from a receive-only solution.

For a one-way remote, HA's remembered state may differ from physical state after another remote is used. Prefer explicit ON/OFF commands where supported; power toggles cannot establish a known state without feedback. An SDR/decoder approach such as [rtl_433](https://github.com/merbanan/rtl_433) is useful for supported broadcast sensors, but not a blanket solution for locks or rolling-code garage controls.

## Choose whether to add another radio

Count the additional controller, backup procedure, firmware and failure boundary. Add a protocol for a specific feature, building requirement or existing installed equipment. Avoid replacing healthy equipment merely to unify logos. Route wired building buses to `smart-home-architecture`; route DECT ULE/HAN FUN and FRITZ gateway support to `fritzbox-operator`.
