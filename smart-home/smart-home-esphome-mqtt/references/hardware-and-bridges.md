# Hardware, sensors and protocol bridges

## Identify the electronics

Record chip family, board revision, flash size, voltage domains, boot/strapping pins, UART pins, power source and the component datasheet. A device family may change from ESP to a different chip without changing its marketing name. Compare the exact board to the current [ESPHome component catalog](https://esphome.io/components/) and [ESP32 platform](https://esphome.io/components/esp32/) before selecting firmware.

Keep firmware choice separate from electrical compatibility. A UART label does not establish 3.3 V logic, isolation, or a safe reference ground. Work on an isolated low-voltage development setup first. Do not connect a USB serial adapter to an energized mains-referenced appliance. Use a supported commercial interface when opening the appliance is unnecessary.

## Select a bridge by required feedback

| Bridge | Verify before implementation | Acceptance evidence |
|---|---|---|
| I²C/SPI environmental sensor | Exact IC, supported component, address/pins, voltage and sampling | Plausible values against a reference; disconnected sensor produces an explicit fault |
| UART/RS-485/Modbus | Electrical transceiver, baud/parity, address, protocol and read/write registers | A known read matches the device UI before any write |
| IR remote | Protocol, carrier, repeat behavior and complete state payload | Command works; independent physical feedback is identified or optimistic state is labeled |
| BLE advertisement/proxy | Passive versus active operations, HA integration, coverage and connection slots | Device remains usable across proxy reconnect and competing connections |
| GPIO relay/cover | Pin map, startup state, interlocks, feedback and physical override | Safe startup/recovery demonstrated on a low-risk bench fixture |

[UART documentation](https://esphome.io/components/uart/) and the device-specific component contract govern configuration; random bytes in a debug log are not sufficient to infer an undocumented actuator protocol. For [IR transmitters](https://esphome.io/components/remote_transmitter/), successful transmission does not confirm the appliance received or applied the command. Prefer explicit state commands over toggles where the appliance supports them.

## Bluetooth proxy versus sensor firmware

A [Bluetooth proxy](https://esphome.io/components/bluetooth_proxy/) forwards supported BLE traffic to HA; it is not a generic Bluetooth Classic audio bridge. Passive advertisements and active connections consume different resources. Platform, Wi-Fi coexistence and memory affect active capacity; inspect the current platform-specific limits instead of repeating a universal maximum.

Begin with a supported reference configuration. Avoid adding heavy display, audio, camera and BLE workloads to the same board before measuring memory and timing. Place proxies by measured radio reach and network reliability. Use `smart-home-radio` for placement, interference and proxy selection, and `smart-home-devices` for the exact ThermoBeacon, Govee or Xiaomi protocol.

## Native integration before reflashing

For Shelly, SONOFF and Tuya, first determine whether native local support, a supported LAN mode, Zigbee, Matter or an existing bridge satisfies the requirement. Reflashing changes recovery, vendor updates, calibration and sometimes certification/warranty considerations; do it only for a concrete capability gap.

Do not infer a working OTA exploit from an old video or a different hardware revision. Preserve the original firmware/configuration where technically supported, establish a recovery path, then evaluate one spare unit. Do not bulk-flash installed leak alarms, locks or heating controls as a discovery technique.
